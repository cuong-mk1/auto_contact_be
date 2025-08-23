from models.job_histories import db
# import model setting
from models.setting import Setting

class SettingService: 
    @staticmethod
    def save_setting_data(data_setting):
        # Get setting by id
        setting_id = data_setting["id"]
        if setting_id:
            setting = Setting.query.filter_by(id=setting_id).first()
            if setting is None:
                setting = Setting()
        else:
            setting = Setting()
        setting.name_of_setting = data_setting['name_of_setting']
        setting.company_name = data_setting['company_name']
        setting.department = data_setting.get('department')
        setting.lastname = data_setting['lastname']
        setting.firstname = data_setting['firstname']
        setting.lastname_kana = data_setting.get('lastname_kana')
        setting.firstname_kana = data_setting.get('firstname_kana')
        setting.fax = data_setting.get('fax')
        setting.email = data_setting['email']
        setting.company_url = data_setting.get('company_url')
        setting.number_of_employees = data_setting.get('number_of_employees')
        setting.phone = data_setting.get('phone')
        setting.zip = data_setting.get('zip')
        setting.zip1 = data_setting.get('zip1')
        setting.zip2 = data_setting.get('zip2')
        setting.province = data_setting.get('province')
        setting.city = data_setting.get('city')
        setting.address = data_setting.get('address')
        setting.title_question = data_setting.get('title_question')
        setting.content_question = data_setting.get('content_question')
        setting.created_at = data_setting.get('created_at')
        setting.updated_at = data_setting.get('updated_at')
        db.session.add(setting)
        db.session.commit()
        return setting.to_dict()
    #create api get setting data
    @staticmethod
    def get_all_setting_data():
        setting = Setting.query.all()
        return [setting.to_dict() for setting in setting]
    #create api get setting data by id
    @staticmethod
    def get_setting_data_by_id(id):
        setting = Setting.query.filter_by(id=id).first()
        return setting.to_dict() if setting else None
    


