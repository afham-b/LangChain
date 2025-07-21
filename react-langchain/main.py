from dotenv import load_dotenv
from langchain.agents.format_scratchpad import format_log_to_str
from langchain_core.tools import Tool

load_dotenv()
import os 

from langchain.agents import tool 
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from typing import Tuple, List
from langchain.tools.render import render_text_description
from langchain.agents.output_parsers import ReActSingleInputOutputParser
from langchain.agents import create_react_agent, AgentExecutor
from langchain.schema import AgentAction, AgentFinish
from typing import Union

from callbacks import AgentCallbackHandler

@tool
def get_text_length(text:str) -> int:
    """
        Returns the length of a text my characters.
    """
    print(f"get_text_length enter with {text}")
    text = text.strip("'\n").strip(
        '"'
    ) # stripping away non-alphabetic characters from text
    return len(text)


def find_tool_by_name(tools: List[Tool],tool_name:str)-> Tool:
    for tool in tools:
        if tool.name == tool_name:
            return tool
    raise ValueError("No such tool")


if __name__ == "__main__":
    print("hello React LangChain")
    #print(get_text_length.invoke(input={"text":"Dog"}))

    tools = [get_text_length]

    template = """
    Rules:
    - At each step, you must only provide either an Action/Action Input or a Final Answer, not both.
    - Only provide Final Answer after seeing an Observation for your last action.

    Answer the following questions as best you can. You have access to the following tools:

    {tools}

    Use the following format:

    Question: the input question you must answer
    Thought: you should always think about what to do
    Action: the action to take, should be one of [{tool_names}]
    Action Input: the input to the action
    Observation: the result of the action
    ... (this Thought/Action/Action Input/Observation can repeat N times)
    Thought: I now know the final answer
    Final Answer: the final answer to the original input question
    
    Instruction: 
    1. Either respons with Final Answer or with [Action, Action Input]
    2. Dont include both Final Answer and [Action, Action Input]
    3. If you have an action input do the following before replying:
        3.1 In Action Input dont mention the parameter name.
        3.2 For Example: instead of Action Input: "DOG" use Action Input: DOG

    Begin!

    Question: {input}
    Thought:{agent_scratchpad}
    """

    prompt = PromptTemplate.from_template(template=template).partial(
        tools=render_text_description(tools), tool_names = ", ".join([t.name for t in tools])
        ) 
    
    llm = ChatOpenAI(temperature=0, model_name="gpt-4o-mini", stop = ["Observation"], callbacks=[AgentCallbackHandler()])

    intermediate_steps = []

    agent_executor = AgentExecutor(
        agent=(
                {
                    "input": lambda x: x["input"],
                    "agent_scratchpad": lambda x: format_log_to_str(x["agent_scratchpad"]),
                }
                | prompt
                | llm
                | ReActSingleInputOutputParser()
        ),
        tools=tools,
        verbose=True,
        handle_parsing_errors=True
    )

    agent_step = []

    agent_step : Union[AgentAction, AgentFinish] = agent_executor.invoke({
        "input": "What is the length of 'DOG' in characters?",
        "agent_scratchpad": intermediate_steps,
    },
    handle_parsing_errors = True,
    )

    print(agent_step)

    if isinstance(agent_step,AgentAction):
        tool_name = agent_step.tool
        tool_to_use = find_tool_by_name(tools, tool_name)
        tool_input = agent_step.tool_input

        observation = tool_to_use.func(str(tool_input))
        print(observation)
        intermediate_steps.append((agent_step, str(observation)))

        if isinstance(agent_step, AgentFinish):
            print(agent_step)


    print(f"Final Answer: {agent_step}")