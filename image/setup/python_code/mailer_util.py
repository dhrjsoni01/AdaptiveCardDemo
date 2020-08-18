import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jinja2 import Template
from python_code.config import Config


class MailerUtil:

    @staticmethod
    def send_mails(payload_df):
        from_mail = Config.get_config()['mail']
        password = Config.get_config()['password']
        smtp_server = MailerUtil.__connect_mail(mail=from_mail, password=password)
        for i, row in payload_df.iterrows():
            to_mail = row['to']
            is_sent = MailerUtil.__send_mail_util(
                to_mail=to_mail,
                payload_dump=row['card_payload'],
                subject=row['subject'],
                smtp_server=smtp_server,
                from_mail=from_mail)
        smtp_server.quit()

    @staticmethod
    def __attach_payload_in_html(payload):
        content_template = Template("""<html>
                                           <head>
                                           <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
                                           <script type = "application/adaptivecard+json" > {{card}} </script>
                                           </head><body><center>
                                            For more details check out FAQ's
                                            <a href="https://google.com">here</a>
                                            </center></body>
                                           </html>""")
        data_msg = content_template.render(card=payload)
        return data_msg

    @staticmethod
    def __connect_mail(mail, password):
        print("Authenticating account")
        host_server = ('smtp.office365.com')
        smtp_server = smtplib.SMTP(host_server)
        smtp_server.connect(host_server, 587)
        smtp_server.starttls()
        smtp_server.ehlo()
        smtp_server.login(mail, password)
        print("Authenticating complete")
        return smtp_server

    @staticmethod
    def __send_mail_util(to_mail: str, subject: str, payload_dump: str,
                         smtp_server, from_mail) -> bool:
        print("sending mails")
        try:
            msg = MIMEMultipart()
            msg['Subject'] = subject
            msg['From'] = from_mail
            msg['To'] = to_mail
            content_html = MIMEText(MailerUtil.__attach_payload_in_html(payload_dump), 'html')
            msg.attach(content_html)
            smtp_server.send_message(msg)
            return True
        except smtplib.SMTPException as ex:
            print("mail send Failed, with ex {}".format(ex))
            return False
