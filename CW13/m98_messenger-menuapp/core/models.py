from base import BaseModel
from dataclasses import dataclass

@dataclass
class User(BaseModel):
    TABLE_NAME = 'users'
    COLUMNS = {
        'name': ('name', 'VARCHAR(20)', 'NOT NULL'),
        'username': ('username', 'VARCHAR(20)', 'UNIQUE'),
        'password': ('password', 'VARCHAR(100)', 'NOT NULL'),
    }

    name: str
    username: str
    password: str


@dataclass
class Message(BaseModel):
    TABLE_NAME = 'messages'
    COLUMNS = {
        'from_user': ('from_user', 'INT', 'NOT NULL'),
        'to_user': ('to_user', 'INT', 'NOT NULL'),
        'content': ('content', 'TEXT', 'NOT NULL'),
        'subject': ('subject', 'VARCHAR(100)', 'NOT NULL'),
        'create_timestamp': ('create_timestamp', 'TIMESTAMP', 'DEFAULT CURRENT_TIMESTAMP'),
    }

    from_user: int
    to_user: int
    content: str
    subject: str
    create_timestamp: str
