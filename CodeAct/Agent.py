from ChatOpenAI import ChatOpenAICompat

class Agent:
    def __init__(self, sandbox):
        self.llm = ChatOpenAICompat()
        self.sandbox = sandbox

    def _extract_code(self, text: str):
        if "```" not in text:
            return None

        parts = text.split("```")
        if len(parts) < 2:
            return None

        code_block = parts[1].strip()

        lines = code_block.splitlines()
        if lines and lines[0].strip().lower() in {"python", "py"}:
            code_block = "\n".join(lines[1:])

        return code_block.strip()

    def query(self, query:str):
        # 询问模型
        response = self.llm.chat(query)
        while True:
            text = response.output_text
            print("Model Output:\n", text)
            # 解析输出是否有代码块
            code = self._extract_code(text)

            # 没有代码块
            if code is None:
                print("\nFinal Answer:\n", text)
                return
            
            print("\nExecuting code:\n", code)

            observation, context = self.sandbox.execute(code)

            print("\nObservation:\n", observation)
            print("\nContext:\n", context)

            # 回喂给模型
            response = self.llm.chat(
                query=(
                    f"Observation:\n{observation}\n\n"
                    "If the task is solved, give the final answer directly. "
                    "Otherwise, output the next Python code block."
                    )
            )

        

