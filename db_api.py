from datetime import datetime
"""
Email 类表示一封邮件
id (int):邮件的唯一标识
sender (str): 发件人的邮箱地址。
receiver (str): 收件人的邮箱地址。
title (str): 邮件的标题。
body (str): 邮件的正文内容。
timestamp (datetime): 邮件发送的时间。
is_read (bool, optional): 是否已读，默认值是 False。
is_deleted (bool, optional): 是否已删除，默认值是 False。
folder (str): 邮件所在的文件夹，可取值为 'inbox'、'drafts' 或 'sent'。
"""
class Email:
    def __init__(self, sender, receiver, title, body, timestamp, is_read=False, is_deleted=False, folder='inbox'):
        self.id = None  # 初始时 id 为空，插入数据库后会自动生成
        self.sender = sender
        self.receiver = receiver
        self.title = title
        self.body = body
        self.timestamp = timestamp
        self.is_read = is_read
        self.is_deleted = is_deleted
        self.folder = folder

    def __repr__(self):
        return f"<Email(id={self.id}, title={self.title}, sender={self.sender}, receiver={self.receiver}, folder={self.folder})>"
#示例
email = Email(
    sender="sender@example.com",
    receiver="receiver@example.com",
    title="Test Email",
    body="This is a test email.",
    timestamp=datetime.now(),
    is_read=False,
    is_deleted=False,
    folder='inbox'
)
#EmailDatabase 类
#用于管理邮件数据的数据库类，包含各种操作邮件数据的方法。
#数据库预计使用mysql
class EmailDatabase:
    def login(self, mail_type: str, username: str, password: str):
        """
        描述: 用户登录。如果用户不存在则创建用户，并创建用户对应的邮件表。
        
        参数:
        mail_type (str): 邮箱类型，可选值为 'Gmail', '163 Mail', 'WHU E-Mail', 'QQ Mail'。
        username (str): 用户名。
        password (str): 密码。
        
        返回: 无。
        """

    def add_email(self, email: Email) -> Email:
        """
        描述: 添加一封新邮件到数据库。
        
        参数:
        email (Email): 要添加的邮件对象。
        
        返回: Email 对象，包含数据库分配的 ID。
        """

    def get_email_by_id(self, email_id: int) -> Optional[Email]:
        """
        描述: 根据邮件 ID 获取邮件。
        
        参数:
        email_id (int): 邮件的 ID。
        
        返回: Email 对象，如果未找到返回 None。
        """

    def get_all_emails(self) -> List[Email]:
        """
        描述: 获取所有未删除的邮件。
        
        参数: 无。
        
        返回: List[Email]，包含所有未删除的邮件列表。
        """

    def get_inbox(self) -> List[Email]:
        """
        描述: 获取当前用户的收件箱邮件。
        
        参数: 无。
        
        返回: List[Email]，包含当前用户的所有收件箱邮件。
        """

    def get_sent_emails(self) -> List[Email]:
        """
        描述: 获取当前用户的已发送邮件。
        
        参数: 无。
        
        返回: List[Email]，包含当前用户的所有已发送邮件。
        """

    def get_draft_emails(self) -> List[Email]:
        """
        描述: 获取当前用户的草稿箱邮件。
        
        参数: 无。
        
        返回: List[Email]，包含当前用户的所有草稿邮件。
        """

    def delete_email(self, email_id: int):
        """
        描述: 标记邮件为已删除。
        
        参数:
        email_id (int): 要删除的邮件 ID。
        
        返回: 无。
        """

    def mark_as_read(self, email_id: int):
        """
        描述: 将收件箱中的邮件标记为已读。
        
        参数:
        email_id (int): 要标记为已读的邮件 ID。
        
        返回: 无。
        """

    def update_email(self, email: Email):
        """
        描述: 更新邮件信息。
        
        参数:
        email (Email): 包含更新信息的邮件对象，必须包含有效的邮件 ID。
        
        返回: 无。
        """


