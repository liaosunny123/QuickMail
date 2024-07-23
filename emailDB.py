from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean, Enum, MetaData, Table
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.sql import text
from datetime import datetime
from sqlalchemy import inspect
from mail_api import Email
# class Email:
#     def __init__(self, sender: str, receiver: str, title: str, body: str, timestamp: datetime.time, obj_id,
#                  is_read: bool = False, is_deleted: bool = False, folder: str = 'inbox', offset_id: int=0):
#         self.sender = sender
#         self.receiver = receiver
#         self.title = title
#         self.body = body
#         self.timestamp = timestamp
#         self.is_read = is_read
#         self.is_deleted = is_deleted
#         self.folder = folder
#         self.offset_id = offset_id
#         self.obj_id = obj_id

#     def __repr__(self):
#         return f"<Email(title={self.title}, sender={self.sender}, receiver={self.receiver}, folder={self.folder})>"
    
Base = declarative_base()

class EmailModel(Base):
    __tablename__ = 'emails'
    
    obj_id = Column(Integer, primary_key=True)
    sender = Column(String(255), nullable=False)
    receiver = Column(String(255), nullable=False)
    title = Column(String(255), nullable=False)
    body = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    is_read = Column(Boolean, default=False)
    is_deleted = Column(Boolean, default=False)
    folder = Column(Enum('inbox', 'drafts', 'sent', name='email_folders'), nullable=False)

    def to_email(self):
        email = Email(
            obj_id=self.obj_id,
            sender=self.sender,
            receiver=self.receiver,
            title=self.title,
            body=self.body,
            timestamp=self.timestamp,
            is_read=self.is_read,
            is_deleted=self.is_deleted,
            folder=self.folder
        )
        # email.obj_id = self.obj_id
        return email

    @classmethod
    def from_email(cls, email):
        return cls(
            obj_id=email.obj_id,
            sender=email.sender,
            receiver=email.receiver,
            title=email.title,
            body=email.body,
            timestamp=email.timestamp,
            is_read=email.is_read,
            is_deleted=email.is_deleted,
            folder=email.folder
        )

class EmailDatabase:
    def __init__(self, user, password, host, database):
        self.engine = create_engine(f'mysql+mysqldb://{user}:{password}@{host}/{database}')
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.username = None

    def _create_users_table(self):
        with self.engine.connect() as conn:
            conn.execute(text(f"""
                CREATE TABLE IF NOT EXISTS users (
                    mail_type VARCHAR(255) NOT NULL,
                    username VARCHAR(255) PRIMARY KEY,
                    password VARCHAR(255) NOT NULL
                )
            """))

    def _sanitize_table_name(self, username):
        return username.replace('@', '_').replace('.', '_')
    
    def login(self, mail_type, username, password):
        self._create_users_table()

        self.username = self._sanitize_table_name(username)

        session = self.Session()

        user = session.execute(text(f"SELECT * FROM users WHERE username = :username"), {'username': username}).fetchone()
        if not user:
            session.execute(text(f"""
                INSERT INTO users (mail_type, username, password)
                VALUES (:mail_type, :username, :password)
            """), {
                'mail_type': mail_type,
                'username': username,
                'password': password
            })
            session.commit()

        if not self._user_tables_exist(username):
            self._create_user_tables(self.username)

        session.close()

    def _user_tables_exist(self, username):
        inspector = inspect(self.engine)
        return f"{username}_emails" in inspector.get_table_names()



    def _create_user_tables(self, username):
        with self.engine.connect() as conn:
            conn.execute(text(f"""
                CREATE TABLE {username}_emails (
                    obj_id VARCHAR(255) PRIMARY KEY,
                    sender VARCHAR(255) NOT NULL,
                    receiver VARCHAR(255) NOT NULL,
                    title VARCHAR(255) NOT NULL,
                    body TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    is_read BOOLEAN DEFAULT FALSE,
                    is_deleted BOOLEAN DEFAULT FALSE,
                    folder ENUM('inbox', 'drafts', 'sent') NOT NULL
                )
            """))

    def add_email(self, email):
        session = self.Session()
        table_name = f"{self.username}_emails"
        
        # 插入数据并获取新插入记录的obj_id
        result = session.execute(text(f"""
            INSERT INTO {table_name} (obj_id,sender, receiver, title, body, timestamp, is_read, is_deleted, folder)
            VALUES (:obj_id,:sender, :receiver, :title, :body, :timestamp, :is_read, :is_deleted, :folder)
        """), {
            'obj_id':email.obj_id,
            'sender': email.sender,
            'receiver': email.receiver,
            'title': email.title,
            'body': email.body,
            'timestamp': email.timestamp,
            'is_read': email.is_read,
            'is_deleted': email.is_deleted,
            'folder': email.folder
        })
        # 提交事务并刷新会话以获取新obj_id
        session.commit()
        # email_obj_id = result.lastrowobj_id
        # email.obj_id = email_obj_id
        session.close()
        return email
    
    def get_email_by_obj_id(self, email_obj_id):
        session = self.Session()
        table_name = f"{self.username}_emails"
        result = session.execute(text(f"""
            SELECT * FROM {table_name} WHERE obj_id = :obj_id
        """), {'obj_id': email_obj_id}).mappings().fetchone()
        session.close()

        if result:
            email = Email(
                obj_id=result['obj_id'],
                sender=result['sender'],
                receiver=result['receiver'],
                title=result['title'],
                body=result['body'],
                timestamp=result['timestamp'],
                is_read=result['is_read'],
                is_deleted=result['is_deleted'],
                folder=result['folder']
            )
            # email.obj_id = result['obj_id']
            return email
        return None


    def get_all_emails(self):   
        session = self.Session()
        table_name = f"{self.username}_emails"
        results = session.execute(text(f"""
            SELECT * FROM {table_name} WHERE is_deleted = FALSE
        """)).mappings().fetchall()
        session.close()
        emails=[]
        for result in results:
            email=Email(
            obj_id=result['obj_id'],
            sender=result['sender'],
            receiver=result['receiver'],
            title=result['title'],
            body=result['body'],
            timestamp=result['timestamp'],
            is_read=result['is_read'],
            is_deleted=result['is_deleted'],
            folder=result['folder']
            )
            # email.obj_id=result['obj_id']
            emails.append(email)
        return emails

    def get_inbox(self):
        return self.get_folder_emails('inbox')

    def get_sent_emails(self):
        return self.get_folder_emails('sent')

    def get_draft_emails(self):
        return self.get_folder_emails('drafts')

    def delete_email(self, email_obj_id):
        session = self.Session()
        table_name = f"{self.username}_emails"
        session.execute(text(f"""
            UPDATE {table_name} SET is_deleted = TRUE WHERE obj_id = :obj_id
        """), {'obj_id': email_obj_id})
        session.commit()
        session.close()

    def mark_as_read(self, email_obj_id):
        session = self.Session()
        table_name = f"{self.username}_emails"
        session.execute(text(f"""
            UPDATE {table_name} SET is_read = TRUE WHERE obj_id = :obj_id
        """), {'obj_id': email_obj_id})
        session.commit()
        session.close()

    def update_email(self, email):
        session = self.Session()
        table_name = f"{self.username}_emails"
        session.execute(text(f"""
            UPDATE {table_name}
            SET sender = :sender, receiver = :receiver, title = :title, body = :body, is_read = :is_read, is_deleted = :is_deleted, folder = :folder
            WHERE obj_id = :obj_id
        """), {
            'sender': email.sender,
            'receiver': email.receiver,
            'title': email.title,
            'body': email.body,
            'is_read': email.is_read,
            'is_deleted': email.is_deleted,
            'folder': email.folder,
            'obj_id': email.obj_id
        })
        session.commit()
        session.close()

    def get_folder_emails(self, folder):
        session = self.Session()
        table_name = f"{self.username}_emails"
        results = session.execute(text(f"""
            SELECT * FROM {table_name} WHERE folder = :folder AND is_deleted = FALSE
        """), {'folder': folder}).mappings().fetchall()
        session.close()
        emails=[]
        for result in results:
            email=Email(
            obj_id=result['obj_id'],
            sender=result['sender'],
            receiver=result['receiver'],
            title=result['title'],
            body=result['body'],
            timestamp=result['timestamp'],
            is_read=result['is_read'],
            is_deleted=result['is_deleted'],
            folder=result['folder']
            )
            # email.obj_id=result['obj_id']
            emails.append(email)
        return emails


