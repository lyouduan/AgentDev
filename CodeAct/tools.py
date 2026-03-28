def calculator(expression: str) -> str:
    expression = (
        expression.replace("×", "*")
        .replace("÷", "/")
        .replace("−", "-")
    )
    try:
        result = eval(expression, {"__builtins__": {}}, {})
        return str(result)
    except Exception as e:
        return f"Calculator error: {e}"