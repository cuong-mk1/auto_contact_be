from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from models.black_lists import BlackLists

class BlackListService: 
    @staticmethod
    def get_black_list():
        black_list = BlackLists.query.all()
        black_list = [item.url for item in black_list]
        return black_list
    def update_black_list(data):
        try:
            BlackLists.bulk_create_data_black_lists(data)
            return True
        except Exception as e:
            print(e)
            return False

