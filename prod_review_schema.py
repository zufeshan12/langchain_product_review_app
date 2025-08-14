from pydantic import Field,BaseModel
from typing import Literal,Optional

class ProdReview(BaseModel):
    summary: str = Field(description="a brief,clear and concise summary of the product review")
    sentiment: Literal['POSITIVE','NEUTRAL','NEGATIVE'] = Field(description="sentiment of the review")
    tags: list[str] = Field(description="a list of key themes discussed or tags mentioned in the review")
    pros: Optional[list[str]] = Field(default=None,description="list of pros mentioned in the review")
    cons: Optional[list[str]] = Field(default=None,description="list of cons mentioned in the review")