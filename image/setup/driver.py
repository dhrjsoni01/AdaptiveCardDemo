import pandas as pd
from python_code.card_builder import CardBuilder
from python_code.mailer_util import MailerUtil

data = pd.read_csv("data/request_db.csv")

payload_df = CardBuilder(data).get_payload_df()

MailerUtil.send_mails(payload_df)


