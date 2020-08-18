"""
    card_template_util.py
    ~~~~~~~~~~~~
    Author: dhrjsoni01
"""
import json


class CardTemplateUtil:

    @staticmethod
    def load_json_from_template(file_name) -> list or dict:
        file_path = 'template/{}'.format(file_name)
        f = open(file_path)
        data = json.load(f)
        return data

    @staticmethod
    def get_card_wrapper(originator_id) -> dict:
        card_wrapper = CardTemplateUtil.load_json_from_template('card_wrapper.json')
        card_wrapper['originator'] = originator_id
        return card_wrapper

    @staticmethod
    def get_branding_head() -> dict:
        return CardTemplateUtil.load_json_from_template('branding_head.json')

    @staticmethod
    def get_header_info(info_line: str) -> dict:
        card_info = CardTemplateUtil.load_json_from_template('header_info.json')
        card_info['items'][0]['text'] = info_line
        return card_info

    @staticmethod
    def get_request_wrapper() -> dict:
        return CardTemplateUtil.load_json_from_template('request_container.json')

    @staticmethod
    def get_request_item(req_id: str, name: str, img_url: str, title: str, org: str, message: str) -> dict:
        request_item = CardTemplateUtil.load_json_from_template('request_item.json')
        # setting request data
        request_item['columns'][0]['items'][0]['id'] = req_id
        request_item['columns'][1]['items'][0]['url'] = img_url
        request_item['columns'][2]['items'][0]['text'] = name
        request_item['columns'][2]['items'][1]['text'] = title
        request_item['columns'][2]['items'][2]['text'] = org
        request_item['columns'][2]['items'][3]['text'] = "*\"{message}\"*".format(message=message)
        return request_item

    @staticmethod
    def get_actions(req_id_list: list, approve_url: str, decline_url: str) -> dict:
        card_actions = CardTemplateUtil.load_json_from_template('actions.json')
        body = {}
        for req_id in req_id_list:
            body[req_id] = "{{" + str(req_id) + ".value}}"
        body_str = str(body).replace("'", "")
        print("body_str")
        print(body_str)
        card_actions['items'][0]['actions'][0]['url'] = approve_url
        card_actions['items'][0]['actions'][0]['body'] = body_str
        card_actions['items'][0]['actions'][1]['url'] = decline_url
        card_actions['items'][0]['actions'][1]['body'] = body_str
        return card_actions
