from pydantic import BaseModel, Field
from typing import List

class Claim(BaseModel):
    claim: str = Field(description="The exact claim extracted from the text.")
    type: str = Field(description="Must be exactly one of: 'metric', 'policy', or 'meeting_decision'.")

class ExtractedClaims(BaseModel):
    claims: List[Claim]