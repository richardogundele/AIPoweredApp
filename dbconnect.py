from sqlalchemy import Column, Integer, MetaData, String, Table, Text, create_engine
from sqlalchemy.orm import Session

engine = create_engine('postgres://chat_history_user:FWR5uxEvl0did82wpeH0qky7APeDBMdP@dpg-ck9c6uf0vg2c73a3s2rg-a/chat_history')
session = Session(engine)

metadata_obj = MetaData()
users = Table(
    "chats",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("email", String(30), nullable=True),
    Column("prompt", Text ),
    Column("completion", Text, nullable=True),
)
user_emails = Table(
    "emails",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("email", String(30), nullable=True),
    )
metadata_obj.create_all(engine)

def getSession():
    return session
