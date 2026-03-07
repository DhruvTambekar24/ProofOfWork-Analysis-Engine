from pydantic import BaseModel

class Student(BaseModel):

    name: str
    github_username: str