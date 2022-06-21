from pydantic import BaseModel


class BaseSchema(BaseModel):

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
