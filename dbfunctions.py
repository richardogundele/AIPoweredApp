from typing import List
from sqlalchemy import select
from model import Chats, Emails
from dbconnect import getSession
from sqlalchemy.exc import IntegrityError

def saveChat(email:str, prompt:str, completion:str) -> Chats:
    print('here2')
    with getSession() as session: 
        
        chat = Chats()
        chat.email = email
        chat.prompt = prompt
        chat.completion = completion
        
        session.add(chat)
        session.commit()
        print('here1')
        
        return chat

def getChats(email:str) -> List[Chats]:
    with getSession() as session:
       stmt = select(Chats).where(Chats.email==email)
       rs = session.scalars(statement=stmt).all()
       print(f'XXXXXXXXXXXXXXx{rs}')
    
       return rs
   
def check_and_add_email(email:str) -> bool:
    with getSession() as session:
        existing_email = session.query(Emails).filter_by(email=email).first()
        if existing_email:
            return True
        else:
            try:
                new_email = Emails(email=email)
                session.add(new_email)
                session.commit()
                return True
            except IntegrityError:
                session.rollback()
                return False
