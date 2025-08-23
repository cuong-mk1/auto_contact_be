from .databaseConfig import db
from datetime import datetime

class Setting(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    #add name_of_setting
    name_of_setting = db.Column(db.String(255), nullable=True)
    company_name = db.Column(db.String(255), nullable=False)
    department = db.Column(db.String(255), nullable=True)
    lastname = db.Column(db.String(100), nullable=False)
    firstname = db.Column(db.String(100), nullable=False)
    lastname_kana = db.Column(db.String(100), nullable=True)
    firstname_kana = db.Column(db.String(100), nullable=True)
    fax = db.Column(db.String(50), nullable=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    company_url = db.Column(db.String(255), nullable=True)
    number_of_employees = db.Column(db.Integer, nullable=True)
    phone = db.Column(db.String(50), nullable=True)
    zip = db.Column(db.String(20), nullable=True)
    zip1 = db.Column(db.String(10), nullable=True)
    zip2 = db.Column(db.String(10), nullable=True)
    province = db.Column(db.String(100), nullable=True)
    city = db.Column(db.String(100), nullable=True)
    address = db.Column(db.Text, nullable=True)
    title_question = db.Column(db.String(255), nullable=True)
    content_question = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f'<Setting {self.company_name}>'

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
