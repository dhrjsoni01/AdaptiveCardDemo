import json


class Config:
    @staticmethod
    def get_config():
        file_path = 'config/config.json'
        f = open(file_path)
        data = json.load(f)
        return data
