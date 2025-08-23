from .databaseConfig import db
from datetime import datetime
class UploadHistories(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String, nullable=False)
    file_path = db.Column(db.String, nullable=True)
    number_of_records = db.Column(db.Integer, nullable=True)
    status = db.Column(db.Integer, nullable=True, default=0) # 0: Queued, 1: Running, 2: Thành công, 3: Thất bại
    created = db.Column(db.DateTime, nullable=True)
    file_path_result = db.Column(db.String, nullable=True)

    def __repr__(self):
        return f'<upload_histories {self.file_name}>'
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    @classmethod
    def update_status(cls, id, status):
        upload_histories = cls.query.get(id)
        upload_histories.status = status
        db.session.commit()
        return upload_histories
    @classmethod
    def create_data_upload_histories(cls, data):
        upload_histories = cls(file_name=data['file_name'], file_path=data['file_path'], number_of_records=data['number_of_records'], status=0, created=datetime.now(), file_path_result=data['file_path_result'])
        db.session.add(upload_histories)
        db.session.commit()
        return upload_histories
    @classmethod
    def check_exist_file_name(cls, file_name):
        return cls.query.filter_by(file_name=file_name).first()

