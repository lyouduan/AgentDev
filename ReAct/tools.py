import json
from abc import ABC, abstractmethod
from typing import Any, Dict, List

#定义工具类
class Tool(ABC):
    name : str
    description : str
    parameters : Dict[str, Any]

    @abstractmethod
    def execute(self, params:Dict[str,Any])->str:
        pass

#算机器
class Calculator(Tool):
    name = "calculator"
    description = "Evaluate a mathematical expression and return the result."
    parameters = {
        "type" : "object",
        "properties":{
            "expression" :{
                "type" : "string",
                "description": "A mathematical expression to evaluate"
            }
        },
        "required":["expression"],
        "additionalProperties": False
    }

    def execute(self, params: Dict[str, Any]) -> str:
        expr = params["expression"]
        expr = expr.replace("×", "*").replace("÷", "/").replace("−", "-")
        try:
            result = eval(expr, {"__builtins__": {}}, {})
            return str(result)
        except Exception as e:
            return f"Calculator error: {e}"
