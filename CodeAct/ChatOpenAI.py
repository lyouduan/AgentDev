import os
from typing import Any, Dict, List, Optional
from openai import OpenAI

SYSTEM_PROMPT = """
You will be given a task to perform. You should output either
- a Python code snippet that provides the solution to the task, or a step towards the solution. 
Any output you want to extract from the code should be printed to the console. Code should be output in a fenced code block.
- text to be shown directly to the user, if you want to ask for more information or provide the final answer.

In addition to the Python Standard Library, you can use the following functions:
""".strip()

# 封装openai
class ChatOpenAICompat:
    def __init__(self):
        # ollama初始化本地模型
        # ollama OpenAI compatibility >> https://docs.ollama.com/api/openai-compatibility
        self.client = OpenAI(
            base_url="http://localhost:11434/v1/",
            api_key="ollama"  # required but ignored
        )
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
        response = self.client.responses.create(
            model=self.model,
            instructions=self.instructions,
            input=query,
            tool_choice="auto",
            previous_response_id=previous_response_id,
        )
        return response
    