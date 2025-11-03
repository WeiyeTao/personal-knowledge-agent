from langchain.agents import initialize_agent, AgentType, load_tools
from langchain.llms import Ollama
from langchain.memory import ConversationBufferMemory

llm = Ollama(model="llama3")
memory = ConversationBufferMemory(memory_key="chat_history")

# 加载一个简单的内置工具
tools = load_tools(["python_repl"], llm=llm)

# 初始化 Agent
agent = initialize_agent(tools, llm, agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION, memory=memory, verbose=True)

if __name__ == "__main__":
    while True:
        query = input("\n🧠 输入任务或问题 (exit退出): ")
        if query.lower() in ["exit", "quit"]:
            break
        ans = agent.run(query)
        print("\n🤖:", ans)
