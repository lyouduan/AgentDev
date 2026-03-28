import io
import traceback
import contextlib

class Sandbox:
    def __init__(self):
        self.tools = {}
        self.context = {}

        self.safe_builtins = {
            "print": print,
            "len": len,
            "range": range,
            "str": str,
            "int": int,
            "float": float,
            "sum": sum,
            "min": min,
            "max": max,
            "abs": abs,
            "sorted": sorted,
            "list": list,
            "dict": dict,
            "set": set,
            "tuple": tuple,
        }

    def register_tool(self, name, func):
        self.tools[name] = func

    def execute(self, code: str):
        stdout_buffer = io.StringIO()

        locals_dict = {
            **self.tools,
            **self.context,
        }
        globals_dict = {
            "__builtins__": self.safe_builtins
        }

        try:
            with contextlib.redirect_stdout(stdout_buffer):
                exec(code, globals_dict, locals_dict)

            new_context = {
                k: v for k, v in locals_dict.items()
                if k not in self.tools
            }
            self.context = new_context

            output = stdout_buffer.getvalue().strip() or "(no output)"
            return output, self.context

        except Exception:
            return "Execution error:\n" + traceback.format_exc(), self.context