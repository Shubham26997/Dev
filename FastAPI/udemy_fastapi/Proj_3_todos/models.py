from typing import Optional
from sqlmodel import Field, SQLModel


class Users(SQLModel, table=True):
    id: Optional[int] = Field(default = None, primary_key=True, index=True)
    email: str = Field(unique=True)
    username: str = Field(unique=True)
    first_name: str = Field(description="First Name of the user")
    last_name: str = Field(description="Last Name of the user")
    password: str = Field(description="Password Encryted")
    is_active: bool = Field(default=True)
    role: str = Field(description="User Role assigned")

    model_config = {
        "json_schema_extra":{
            "example": {
                "email": "shubhamgoel386@gmail.com",
                "username": "shubham_goel",
                "first_name": "Shubham",
                "last_name": "Goel",
                "password": "test123",
                "role": "admin"
            }
        }
    }

class ToDos(SQLModel, table=True):

    id: Optional[int] = Field(default = None, primary_key=True, index=True)
    title: str = Field(description="Task Title")
    description: str = Field(description="Task Description")
    priority: int = Field(description="Task Priority", index=True)
    completed: bool = Field(default=False)
    owner_id: int = Field(foreign_key="users.id")

    model_config = {
        "json_schema_extra":{
            "example": {
                "title": "A new noob author",
                "description": "This is the description of the noob author book",
                "priority": 5,
                "completed": False,
                "owner_id": "Mention the USER ID"
            }
        }
    }