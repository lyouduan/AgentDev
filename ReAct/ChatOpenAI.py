import os
from typing import Any, Dict, List, Optional
from openai import OpenAI

SYSTEM_PROMPT = """
You run in a loop of Thought, Action, Observation.
At the end of the loop you output an Answer.
- Use Thought to describe your thoughts about the question you have been asked.
- Use Action to run one of the actions available to you.
- Observation will be the result of running those actions.
""".strip()

# 封装openai
class ChatOpenAICompat:
    def __init__(self, tools: List[Dict[str, Any]]):
        # ollama初始化本地模型
        # ollama OpenAI compatibility >> https://docs.ollama.com/api/openai-compatibility
        self.client = OpenAI(
            base_url="http://localhost:11434/v1/",
            api_key="ollama"  # required but ignored
        )
        self.tools = tools
        self.model = os.getenv("OLLAMA_MODEL", "qwen3:8b")
        self.messages:List[Dict[str, Any]] =[
            {
                "role" : "system",
                "content" : SYSTEM_PROMPT,
            }
        ]

        # Responses API 可以直接用 instructions + input
        self.instructions = SYSTEM_PROMPT

    def chat(self, query : str, previous_response_id: Optional[str] = None):
        # 保存聊天记录
        # self.messages.append(
        #     {
        #         "role" : "user",
        #         "content" : query,
        #     }
        # )

        # 调用模型
        # 旧接口 >> https://developers.openai.com/api/reference/resources/chat
        # response = self.client.chat.completions.create(
        #     model=self.model,
        #     messages=self.messages,
        #     tools=self.tools,
        #     tool_choice="auto",
        # )


        #  new API >> https://developers.openai.com/api/docs/guides/migrate-to-responses
        response = self.client.responses.create(
            model=self.model,
            instructions=self.instructions,
            input=query,
            tools=self.tools,
            tool_choice="auto",
            previous_response_id=previous_response_id,
        )


        return response
    
    # Observation
    # def append_tool_result(self, tool_call_id:str, result:str):
    #     self.messages.append(
    #         {
    #             "role" : "tool",
    #             "tool_call_id" : tool_call_id,
    #             "content" : result,
    #         }
    #     )   