#LLM
from asyncio import tools
import subprocess
from langchain_ollama import ChatOllama
from langchain_core.tools import tool
from langchain.agents import create_agent as create_react_agent

# this is coming from Ollama (ollama connect)
llm = ChatOllama(
    model="qwen3-coder:30b",
    temperature=0,
    num_ctx=8192,      # avoid truncation large kubectl/docker outputs
)

#Tools
def list_containers() -> str:
    """List all Docker containers (running and stopped)."""
    result = subprocess.run(["docker", "ps", "-a"], capture_output=True, text=True)
    return result.stdout or result.stderr

#Agent
#LLM + Toools

agent = create_agent(
    model=llm, #brain
    tools=[get_pods,get_docker_containers], #actions
    system_prompt=(
        "You are a helpful assistant that can provide information about Kubernetes pods and Docker containers. "
        "You have access to the following tools:\n"
        "- get_pods: Use this tool to retrieve information about Kubernetes pods.\n"
        "- get_docker_containers: Use this tool to retrieve information about Docker containers.\n"
        "Please use the appropriate tool based on the user's request."
    )
)

question = input("Ask a question about Kubernetes pods or Docker containers: ")
# Get the agent's response to the question

response = agent.invoke({"message": [("user", question)]})

print(response["message"][-1].content)
