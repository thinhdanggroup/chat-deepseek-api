from pydantic import BaseModel
from typing import List, Optional


class Delta(BaseModel):
    content: str = ""
    type: str = ""
    role: Optional[str] = None


class Choice(BaseModel):
    index: int = 0
    delta: Delta = Delta()
    finish_reason: Optional[str] = None


class MessageData(BaseModel):
    choices: List[Choice] = []
    model: str = ""
    prompt_token_usage: Optional[int] = None
    chunk_token_usage: Optional[int] = None
    created: int = 0
    message_id: int = 0
    parent_id: int = 0

    def has_content(self) -> bool:
        if not self.choices:
            return False
        return bool(self.choices[0].delta.content)

    def get_message_id(self) -> Optional[int]:
        return self.message_id