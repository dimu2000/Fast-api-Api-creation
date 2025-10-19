from pydantic import BaseModel
from typing import List

class BlogTitles(BaseModel):
    titles: List[str]

class BlogTitlesGeneratorResponse(BaseModel):
    success: bool  # True if it worked, False if failed
    message: str  # Human-readable message
    titles: List[str]  # The actual list of titles


# NEW: Add these models
class BlogTitleWithDescription(BaseModel):
    title: str
    description: str

class BlogTitlesWithDescriptions(BaseModel):
    titles_with_descriptions: List[BlogTitleWithDescription]