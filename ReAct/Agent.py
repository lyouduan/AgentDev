from ChatOpenAI import ChatOpenAICompat
from tools import Tool
from typing import Any, Dict, List
import json

# 初始化Agent，实现ReAct逻辑
class Agent:
    def __init__(self, tools:List[Tool]):
        self.tools = tools
        self.llm = ChatOpenAICompat(self.__get_tools_definition())

    def query(self, query:str):
        # 询问模型
        response = self.llm.chat(query)
        while True:
            function_calls = []
            # 解析输出
            for item in response.output:
                output_type = item.type
                if output_type == "reasoning":
                    if item.summary:
                        for s in item.summary:
                            print("Thought:", s.text)

                elif output_type == "message":
                    for c in item.content:
                        if c.type == "output_text":
                            print("Answer:", c.text)

                elif output_type == "function_call":
                    function_calls.append(item)

            # 没有工具调用
            if not function_calls:
                return

            # 执行工具调用
            tool_outputs = []

            for function in function_calls:
                tool_name = function.name
                tool_args = json.loads(function.arguments)

                print(f"Acting: {tool_name} -> {function.arguments}")

                #调用对应工具
                tool_obj = next((t for t in self.tools if t.name == tool_name), None)
                if tool_obj is None:
                    tool_result = f"Tool {tool_name} not found"
                else:
                    tool_result = tool_obj.execute(tool_args)

                print(f"Observation: {tool_result}")

                tool_outputs.append({
                    "type": "function_call_output",
                    "call_id": function.call_id,
                    "output": tool_result,
                })
                print("--------------------------------")

            # 把工具执行结果接回上一轮，继续推理
            response = self.llm.chat(
                query=tool_outputs,
                previous_response_id=response.id,
            )

    # 模型的工具定义格式
    # https://developers.openai.com/api/docs/guides/function-calling
    def __get_tools_definition(self) -> List[Dict[str, Any]]:
        return [
            {
                "type": "function",
                "name": tool.name,
                "description": tool.description,
                "parameters": tool.parameters,
            }
            for tool in self.tools
        ]

