"""
    python_code.py
    ~~~~~~~~~~~~
    Author: dhrjsoni01
"""
import pandas as pd
import json
from python_code.card_template_util import CardTemplateUtil
from python_code.config import Config


class CardBuilder:
    def __init__(self, request_df: pd.DataFrame):
        self.originator_id = Config.get_config()['originator_id']
        self.request_df = request_df

    def get_payload_df(self):
        print("Generating adaptive cards")
        req_to_list = self.request_df['request_to'].unique().tolist()
        rows = []
        for req_to in req_to_list:
            req_df = self.request_df[self.request_df['request_to'] == req_to]
            card_dump = self.__get_card_dump(req_df)
            rows.append([req_to, card_dump])
        req_payload_df = pd.DataFrame(rows, columns=['to', 'card_payload'])
        req_payload_df['subject'] = Config.get_config()['subject']
        return req_payload_df

    def __get_card_dump(self, req_df: pd.DataFrame):
        card = self.__get_card(self.originator_id, req_df=req_df)
        dump_card = json.dumps(card)
        return dump_card

    @staticmethod
    def __get_card(originator_id: str, req_df: pd.DataFrame) -> dict:
        # create Wrapper for adaptive card
        card = CardTemplateUtil.get_card_wrapper(originator_id)
        # add branding header
        card['body'].append(CardTemplateUtil.get_branding_head())
        # add info header
        card['body'].append(CardBuilder.__generate_info(req_df))
        card['body'].append(CardBuilder.__generate_requests(req_df))
        card['body'].append(CardBuilder.__generate_actions(req_df))
        return card

    @staticmethod
    def __generate_info(req_df: pd.DataFrame):
        request_count = req_df.req_id.count()
        info_line = "Hey, You got {} new connection request(s)".format(str(request_count))
        info_head = CardTemplateUtil.get_header_info(info_line=info_line)
        return info_head

    @staticmethod
    def __generate_requests(req_df: pd.DataFrame):
        request_wrapper = CardTemplateUtil.get_request_wrapper()
        # request_wrapper['item']
        for i, request_row in req_df.iterrows():
            request_wrapper['items'].append(CardBuilder.__generate_request_item(request_row))
        return request_wrapper

    @staticmethod
    def __generate_request_item(request_row: pd.Series):
        req_id = str(request_row['req_id'])
        img_url = str(request_row['img_url'])
        message = str(request_row['message'])
        org = str(request_row['org'])
        title = str(request_row['title'])
        name = str(request_row['name'])
        request_item = CardTemplateUtil.get_request_item(req_id=req_id, name=name, img_url=img_url, title=title,
                                                         org=org, message=message)
        return request_item

    @staticmethod
    def __generate_actions(req_df: pd.DataFrame):
        req_id_list = req_df.req_id.tolist()
        approve_url = Config.get_config()['approve_url']
        decline_url = Config.get_config()['decline_url']
        card_action = CardTemplateUtil.get_actions(req_id_list=req_id_list, approve_url=approve_url,
                                                   decline_url=decline_url)
        return card_action
