from models.job_histories import JobHistories
from models.company_name_histories import CompanyNameHistories
from models.upload_histories import UploadHistories
import time
import requests

class JobService: 
    @staticmethod
    def get_list_job_histories(limit, page):
        offset = (page - 1) * limit
        total_count = JobHistories.query.count()
        dataJson = JobHistories.query.order_by(JobHistories.id.desc()).limit(limit).offset(offset).all()
        return {
            "total_count": total_count,
            "job_histories": [job_history.to_dict() for job_history in dataJson]
        }
    @staticmethod
    def get_list_company_name_histories(limit, page):
        offset = (page - 1) * limit
        total_count = CompanyNameHistories.query.count()
        dataJson = CompanyNameHistories.query.order_by(CompanyNameHistories.id.desc()).limit(limit).offset(offset).all()
        return {
            "total_count": total_count,
            "job_company_histories": [job_history.to_dict() for job_history in dataJson]
        }
    @staticmethod
    def get_list_upload_histories(limit, page):
        offset = (page - 1) * limit
        total_count = UploadHistories.query.count()
        dataJson = UploadHistories.query.order_by(UploadHistories.id.desc()).limit(limit).offset(offset).all()
        return {
            "total_count": total_count,
            "upload_histories": [upload_history.to_dict() for upload_history in dataJson]
        }
