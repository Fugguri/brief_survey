from pydantic import BaseModel, Field


class InfoButtons(BaseModel):
    finish_text:str = Field(default="Завершить",)
    multi_select_confirm:str = Field(default="Подтвердить выбор")
    start_again:str = Field(default="Начать сначала")
    class Config:
        from_attributes=True
