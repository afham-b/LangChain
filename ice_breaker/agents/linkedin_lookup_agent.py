import os 
from dotenv import load_dotenv

load_dotenv()

from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

from langchain_core.tools import Tool
from langchain.agents import(
    create_react_agent,
    AgentExecutor
)
from langchain import hub

#make sure that this .py script can access its parent directory
import sys
# Add project root (parent of agents/) to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from tools.tools import get_profile_url_tavily


def lookup(name: str) -> str:

    llm = ChatOpenAI(
        temperature=0,
        model_name= "gpt-4o-mini",
    )

    template = """
        given the full name {name_of_person} I want you to give me link to their Linkedin Profile Page.
        Your answer should only contain only a URL
    """

    prompt_template = PromptTemplate(
        template=template, input_variables=["name_of_person"]
    )
    
    tools_for_agent = [
        Tool(
            name="Crawl Google for Linkedin profile page",
            func=get_profile_url_tavily,
            description="useful for when you need to get the Linkedin Page URL",
        )
    ]

    react_prompt = hub.pull("hwchase17/react")

    #we set the llm, tools above 
    agent = create_react_agent(llm=llm, tools=tools_for_agent, prompt=react_prompt)
    #specify how we want the agent to run, essentially this what brings everything together. 
    agent_executor = AgentExecutor(agent=agent, tools=tools_for_agent, verbose=False, handle_parsing_errors=True)

    result = agent_executor.invoke(
        input= {"input": prompt_template.format_prompt(name_of_person = name)}
    )

    linkedin_profile_url = result["output"]
    return linkedin_profile_url

if __name__ == "__main__":
    #linkedin_url = lookup(name='Afham Bashir ')
    print('hi')