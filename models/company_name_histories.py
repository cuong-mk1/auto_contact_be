from .databaseConfig import db
class CompanyNameHistories(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String, nullable=False)
    company_url = db.Column(db.String, nullable=True)
    status = db.Column(db.Integer, nullable=True, default=0) # 0: Queued, 1: Running, 2: Thành công, 3: Thất bại
    created_at = db.Column(db.DateTime, nullable=True)
    job_index = db.Column(db.Integer, nullable=True)
    error_message = db.Column(db.String, nullable=True)

    def __repr__(self):
        return f'<company_name_histories {self.company_url}>'
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    @classmethod
    def bulk_create_data_company_name_histories(cls, data):
        company_name_histories = [cls(company_name=d) for d in data]
        # add index  = max index + 1
        max_index = cls.query.order_by(cls.job_index.desc()).first()
        job_index = 0
        if max_index and max_index.job_index is not None:
            job_index = max_index.job_index + 1
        else:
            job_index = 1
        company_name_histories = [cls(company_name=d, job_index=job_index) for d in data]
        db.session.bulk_save_objects(company_name_histories)
        db.session.commit()
        data = cls.query.order_by(cls.id.desc()).limit(len(company_name_histories)).all()
        return data
    @classmethod
    def update_status(cls, id, status, error_message=None):
        company_name_history = cls.query.get(id)
        company_name_history.status = status
        company_name_history.error_message = error_message
        db.session.commit()
        return company_name_history
    @classmethod
    def update_contact_url(cls, id, contact_url):
        company_name_history = cls.query.get(id)
        company_name_history.company_url = contact_url
        company_name_history.status = 2
        db.session.commit()
        return company_name_history