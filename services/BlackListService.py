from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from models.black_lists import BlackLists
from models.bl_groups import BlGroups
from models.databaseConfig import db


class BlackListService: 
    @staticmethod
    def get_black_list(bl_group_id):
        # get back_list by group_id
        black_list = BlackLists.query.filter_by(bl_group_id=bl_group_id).all()
        black_list = [item.url for item in black_list]
        return black_list
    def update_black_list(data,data_bl_group):
        bl_group_id = data_bl_group.get('id')
        if bl_group_id is None:
            #create new bl_group
            bl_group = BlGroups.create_blacklist_group(data_bl_group)
            bl_group_id = bl_group.id
        else:
            # update name 
            bl_group = BlGroups.get_blacklist_group(bl_group_id)
            bl_group.name = data_bl_group.get('name')
            bl_group.description = data_bl_group.get('description')
            db.session.commit()
        try:
            BlackLists.bulk_create_data_black_lists(data,bl_group_id)
            return True
        except Exception as e:
            print(e)
            return False
    @staticmethod
    def get_all_bl_groups():
        bl_groups = BlGroups.get_all_blacklist_groups()
        bl_groups = [item.to_dict() for item in bl_groups]
        return bl_groups
    # create function get

