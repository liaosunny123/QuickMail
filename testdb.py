from emailDB import *

def test_email_database():
    # 配置数据库连接信息
    user = 'root'
    password = 'tyxqc'
    host = 'localhost'
    database = 'email'
    
    # 创建 EmailDatabase 实例
    email_db = EmailDatabase(user=user, password=password, host=host,  database=database)
    
    # 用户登录
    email_db.login(mail_type='Gmail', username='test_user', password='test_password')

    # 创建一些测试邮件
    email1 = Email(sender='test_user@gmail.com', receiver='receiver1@gmail.com', title='Test Email 1', body='This is a test email 1.', timestamp=datetime.now(), offset_id=0,folder='inbox',obj_id="first")
    email2 = Email(sender='test_user@gmail.com', receiver='receiver2@gmail.com', title='Test Email 2', body='This is a test email 2.', timestamp=datetime.now(), folder='sent')
    email3 = Email(sender='test_user@gmail.com', receiver='receiver3@gmail.com', title='Test Email 3', body='This is a test email 3.', timestamp=datetime.now(), folder='drafts')

    # 添加邮件到数据库
    email1 = email_db.add_email(email1)
    email2 = email_db.add_email(email2)
    email3 = email_db.add_email(email3)

    print(f"Added Email 1: {email1}")
    print(f"Added Email 2: {email2}")
    print(f"Added Email 3: {email3}")

    # 获取所有未删除的邮件
    all_emails = email_db.get_all_emails()
    print("All Emails:")
    for email in all_emails:
        print(f"{email}\n")

    # 获取收件箱邮件
    inbox_emails = email_db.get_inbox()
    print("Inbox Emails:")
    for email in inbox_emails:
        print(f"{email}\n")

    # 获取已发送邮件
    sent_emails = email_db.get_sent_emails()
    print("Sent Emails:")
    for email in sent_emails:
        print(f"{email}\n")

    # 获取草稿邮件
    draft_emails = email_db.get_draft_emails()
    print("Draft Emails:")
    for email in draft_emails:
        print(f"{email}\n")

    email_db.mark_as_read('first','inbox')



    # 更新邮件
    email3.title = "Updated Test Email 3"
    email_db.update_email(email3)
    # print(f"Updated Email 3: {updated_email3}")

        # 删除邮件
    email_db.delete_email(email2.obj_id,email2.folder)
    all_emails = email_db.get_all_emails()
    print("All Emails:")
    for email in all_emails:
        print(f"{email}\n")

if __name__ == "__main__":
    test_email_database()