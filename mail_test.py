from mail_api import EmailClient

# 使用示例
if __name__ == "__main__":
    client = EmailClient(
        "smtp-mail.outlook.com",  # SMTP 服务器地址
        587,  # SMTP 端口
        "outlook.office365.com",  # POP 服务器地址
        995,  # POP 端口
        "CarmelaLongerbeam60@outlook.fr",  # 用户名
        "ZUGD3qnDHJ3hAr"  # 密码
    )

    # 发送邮件
    client.send_email(
        "epicmo@whu.edu.cn",
        "Test Subject",
        "<b>This is a test email body.</b>",
        cc_addresses=["1728913755@qq.com"]
    )

    # 获取邮件列表
    email_list = client.get_email_list(offset=1, limit=11)
    print("服务端第1～11封邮件是:", email_list)

    # 获取特定邮件内容
    if email_list:
        email_entity = client.get_email_by_obj_id(email_list[0].obj_id)
        print("偏移量为 ", email_list[0].offset_id, " 的邮件内容是:", email_entity.body)
    # 删除特定邮件
    if email_list:
        delete_response = client.delete_email(email_list[0].obj_id)
        print("已删除邮件，是否成功:", delete_response)