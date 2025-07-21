import os
from dotenv import load_dotenv
load_dotenv()

from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser

from third_parties.linkedin import scrape_linkedin_profile


from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent 

from output_parsers import summary_parser
from output_parsers import Summary

from typing import Tuple

from langsmith import traceable
from langsmith.wrappers import wrap_openai

@traceable(name="Ice Break with person name", run_type="chain")
def ice_break_with(name:str) -> Tuple[Summary, str]:
    linkedin_username = linkedin_lookup_agent(name=name)
    linkedin_data = scrape_linkedin_profile(linkedin_profile_url=linkedin_username)

    summary_template = (
        ""
        "given the Linkedin information {information} about a person from I want you to create:"
        "1. a short summary"
        "2. two intersting facts about them" \
        "{format_instructions}" \
        ""
    )

    summary_prompt_template = PromptTemplate(
        input_variables=["information"], 
        template=summary_template,
        partial_variables= {"format_instructions":summary_parser.get_format_instructions()}
    )

    # temperature decides how create the model will be, 0 will no creativety.
    llm = ChatOpenAI(temperature=0, model_name="gpt-4o-mini")

    #llm= wrap_openai(ChatOpenAI(temperature=0, model_name="gpt-4o-mini"))


    #llama3 model 
    #llm = ChatOllama(model="llama3")

    #mistral model 
    #llm = ChatOllama(model='mistral')

    # here lets make a chain using our LangChain operator |
    #chain = summary_prompt_template | llm | StrOutputParser() 
    chain = summary_prompt_template | llm | summary_parser

    # lets run the chain
    res:Summary = chain.invoke(input={"information": linkedin_data})

    return res, linkedin_data.get('photoUrl')

    print(res)

if __name__ == "__main__":
    print("Ice Breaker")
    #ice_break_with('Afham Bashir Columbia')