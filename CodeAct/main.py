from Agent import Agent
from Sandbox import Sandbox
from tools import calculator


def main():
    sandbox = Sandbox()
    sandbox.register_tool("calculator", calculator)

    agent = Agent(sandbox)
    agent.query("(48÷6+7)×(15−9)−5×(3+2)")


if __name__ == "__main__":
    main()