from tools import Calculator
from Agent import Agent

def main():
    tools = [Calculator()]
    agent = Agent(tools)

    query = "(48÷6+7)×(15−9)−5×(3+2)"#15*6-25
    agent.query(query)

if __name__ == "__main__":
    main()
