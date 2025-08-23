from .databaseConfig import db
from datetime import datetime

class JobHistories(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String, nullable=False)
    contact_url = db.Column(db.String, nullable=True)
    status = db.Column(db.Integer, nullable=True, default=0) # 0: Queued, 1: Running, 2: Thành công, 3: Thất bại
    created = db.Column(db.DateTime, nullable=True)
    job_index = db.Column(db.Integer, nullable=True)
    error_message = db.Column(db.String, nullable=True)
    start_time = db.Column(db.DateTime, nullable=True)
    end_time = db.Column(db.DateTime, nullable=True)
    process_time = db.Column(db.Float, nullable=True)  
    updated_at = db.Column(db.DateTime, nullable=True, onupdate=datetime.utcnow)
    setting_name = db.Column(db.String, nullable=True)  # Name of the setting used for this job

    def __repr__(self):
        return f'<job_histories {self.url}>'
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    @classmethod
    def bulk_create_data_job_histories(cls, data, setting_name=None):
        job_histories = [cls(url=d) for d in data]
        # add index  = max index + 1
        max_index = cls.query.order_by(cls.job_index.desc()).first()
        job_index = 0
        if max_index and max_index.job_index is not None:
            job_index = max_index.job_index + 1
        else:
            job_index = 1
        job_histories = [cls(url=d, job_index=job_index,setting_name=setting_name) for d in data]
        db.session.bulk_save_objects(job_histories)
        db.session.commit()
        data = cls.query.order_by(cls.id.desc()).limit(len(job_histories)).all()
        return data
    @classmethod
    def update_status(cls, id, status, error_message=None):
        job_history = cls.query.get(id)
        job_history.status = status
        job_history.error_message = error_message
        if status == 1: 
            job_history.start_time = datetime.utcnow()
        elif status in [2, 3]: 
            job_history.end_time = datetime.utcnow()
            if job_history.start_time:
                job_history.process_time = (job_history.end_time - job_history.start_time).total_seconds()
        db.session.commit()
        return job_history
    @classmethod
    def update_contact_url(cls, id, contact_url):
        job_history = cls.query.get(id)
        job_history.contact_url = contact_url
        job_history.status = 1
        db.session.commit()
        return job_history