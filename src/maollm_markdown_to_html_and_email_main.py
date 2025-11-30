import smtplib
from email.header import Header
from email.mime.text import MIMEText
from email.utils import formataddr

import mistune
from mistune.plugins import _plugins

from maollm import MaoLLM

class MaoAgent():
    def __init__(self):
        self.llm_module = MaoLLM()

    def send_email_report(self, html):
        # -------------------------- 配置信息（需替换为你的信息）--------------------------
        sender = "xxx@126.com"  # 发件人邮箱（126.com）
        sender_auth_code = "xxx"  # 发件人邮箱授权码（不是登录密码）
        receivers = ["xxx@126.com", "zzz@126.com"]  # 收件人邮箱（126.com，可多个用列表：["a@126.com", "b@126.com"]）
        smtp_server = "smtp.126.com"  # 126 邮箱 SMTP 服务器地址
        smtp_port = 25  # 126 SMTP 端口（非 SSL 端口，SSL 端口为 465，下文有说明）

        # -------------------------- 构造邮件内容 --------------------------
        # 邮件正文（plain 表示纯文本，html 表示HTML格式）
        mail_content = html
        message = MIMEText(mail_content, "plain", "utf-8")  # 第三个参数指定编码（避免中文乱码）


        # 构造收件人（formataddr 自动处理中文编码）
        # 用 formataddr 逐个处理每个收件人的「名称+邮箱」，再用逗号拼接成字符串
        to_addrs = []
        for email in receivers:
            # 每个收件人按「名称 <邮箱>」格式处理，自动编码中文
            to_addrs.append(formataddr(("", email), charset='utf-8'))
        # 用逗号分隔多个收件人（邮件协议要求）
        message["To"] = ", ".join(to_addrs)

        # 构造发件人（同步使用标准方法）
        message["From"] = formataddr(("大毛智能体", sender), charset='utf-8')

        # 邮件主题仍用 Header 处理（主题需特殊编码）
        message["Subject"] = Header("智能体消息发布", "utf-8")

        # -------------------------- 连接 SMTP 服务器并发送 --------------------------
        try:
            # 1. 连接 SMTP 服务器（非 SSL 方式）
            smtp_obj = smtplib.SMTP(smtp_server, smtp_port)

            # （可选）开启调试模式，打印与服务器的交互日志（排查问题用）
            # smtp_obj.set_debuglevel(1)

            # 2. 登录邮箱（用授权码而非密码）
            smtp_obj.login(sender, sender_auth_code)

            # 3. 发送邮件（收件人可传列表，支持多收件人）
            # 注意：sendmail 的第一个参数是发件人，第二个是收件人列表，第三个是邮件字符串
            smtp_obj.sendmail(sender, receivers, message.as_string())
            print("邮件发送成功！")
            # print(message.as_string())

        except smtplib.SMTPException as e:
            print("邮件发送失败！错误信息：", e)

        finally:
            # 关闭 SMTP 连接
            if smtp_obj:
                smtp_obj.quit()

    def main(self):
        # self.send_email_report("qingdao radar")
        # return

        self.llm_module.update_endpoint(
            "https://open.bigmodel.cn/api/paas/v4",
            "xxx")
        self.llm_module.update_llm_model("glm-4.5-flash")
        response = self.llm_module.inference([{"role":"user","content":"输出markdown格式的内容，以下是用户请求：北京海淀"}])
        result = self.llm_module.parse_inference_stream(response)
        with open("qingdao.md", mode="w", encoding="utf-8") as f:
            f.write(result[1])

        with open("qingdao.html", mode="w", encoding="utf-8") as f:
            md = mistune.create_markdown(
                escape=True,  # 转义特殊字符（防止XSS）
                hard_wrap=True,  # 换行符转为 <br>
                plugins=[k for k in _plugins]
            )
            html = md(result[1])
            f.write(html)

        self.send_email_report(html)
        print(result)

if __name__ == "__main__":
    agent = MaoAgent()
    agent.main()
