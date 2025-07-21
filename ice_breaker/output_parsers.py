from typing import List, Dict, Any
from langchain_core.output_parsers import PydanticOutputParser

from pydantic import BaseModel, Field

class Summary(BaseModel):
    summary: str = Field(description="summary")
    facts: List[str] = Field(description="interesting facts about them")

    #transform these into dictionaries 
    def to_dict(self) -> Dict[str,Any]:
        return {"summary": self.summary, "facts": self.facts}
    
#the pydanticoutput parser must always be passed an class object, not a string, here we call the summary class 
summary_parser = PydanticOutputParser(pydantic_object=Summary)
