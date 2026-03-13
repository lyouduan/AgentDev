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
        while True:
            # 询问模型
            choice = self.llm.chat(query)
            message = choice.message
            
            reasoning = getattr(message, "reasoning", None)
            if reasoning:
                print("Thought:", reasoning)

            if message.content:
                print("Answer:", message.content)

            if choice.finish_reason == "stop":
                return
            
            Observation = ''
            if choice.finish_reason == "tool_calls":
                tool_calls = message.tool_calls
                if not tool_calls:
                    return

                # Action
                for call in tool_calls:
                    tool_name = call.function.name
                    tool_args = json.loads(call.function.arguments)

                    print(f"Acting: {tool_name} -> {call.function.arguments}")

                    #调用对应工具
                    tool_obj = next((t for t in self.tools if t.name == tool_name), None)
                    if tool_obj is None:
                        tool_result = f"Tool {tool_name} not found"
                    else:
                        tool_result = tool_obj.execute(tool_args)

                    print(f"Observation: {tool_result}")
                    Observation += tool_result
                    # 把 Observation 写回消息历史
                    self.llm.append_tool_result(
                        tool_call_id=call.id,
                        result=tool_result,
                    )

                print("--------------------------------")
                query = Observation

    # 模型的工具定义格式
    # https://developers.openai.com/api/docs/guides/function-calling
    def __get_tools_definition(self)-> List[Dict[str, Any]]:
        return [
            {
                "type" : "function",
                "function" :{
                    "name" : tool.name,
                    "description": tool.description,
                    "parameters": tool.parameters,
                },
            }
            for tool in self.tools
        ]

