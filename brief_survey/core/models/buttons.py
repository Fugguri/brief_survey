from pydantic import BaseModel, Field


class InfoButtons(BaseModel):
    finish_text:str = Field(default="Завершить",)
    class Config:
        from_attributes=True
