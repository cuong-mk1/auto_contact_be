from selenium import webdriver
from models.black_lists import BlackLists
from models.job_histories import JobHistories
from models.job_histories import db
from sqlalchemy import func
import csv
import io

class AnalyzeService: 
    @staticmethod
    def get_list_group_history():
        list_group_history = db.session.query(
            JobHistories.job_index,
            JobHistories.status,
            db.func.count(JobHistories.status),
            db.func.min(JobHistories.created),
            db.func.min(JobHistories.setting_name)
        ).group_by(JobHistories.job_index, JobHistories.status).order_by(JobHistories.job_index.desc()).all()
        # Initialize a dictionary to hold the results for each job_index
        results = {}
        # Populate the results dictionary with counts from the query
        for row in list_group_history:
            job_index = row[0]
            status = row[1]
            count = row[2]
            created = row[3]
            template_name = row[4]
            if job_index not in results:
                results[job_index] = {
                    "total_index": 0,
                    "job_index": job_index,
                    "count_status_0": 0,
                    "count_status_1": 0,
                    "count_status_2": 0,
                    "count_status_3": 0,
                    "created": created,
                    "template_name": template_name
                }
            results[job_index][f"count_status_{status}"] = count
            results[job_index]["total_index"] += count
        # Convert the results dictionary to a list

        result_list = list(results.values())
        
        return result_list
    @staticmethod
    def delete_job_by_index(job_index):
        # Delete all job histories with the specified job_index
        db.session.query(JobHistories).filter(JobHistories.job_index == job_index).delete()
        db.session.commit()
        return {"message": "Job and associated blacklists deleted successfully."}
    @staticmethod
    def export_csv_by_job_index(job_index):
        # Query to get all job histories with the specified job_index
        job_histories = db.session.query(JobHistories).filter(JobHistories.job_index == job_index).all()
        
        if not job_histories:
            return "No data found for the specified job index.", "no_data.csv"
        
        # Prepare CSV data

        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["id", "url", "contact_url", "status", "created", "job_index", "error_message", "process_time", "setting_name"])
        for history in job_histories:
            writer.writerow([
            history.id,
            history.url,
            history.contact_url,
            history.status,
            history.created,
            history.job_index,
            history.error_message,
            history.process_time,
            history.setting_name
            ])
        csv_data = output.getvalue()
        output.close()
        filename = f"job_{job_index}_histories.csv"
        # Return as bytes for blob download in FE
        return b'\xef\xbb\xbf' + csv_data.encode('utf-8'), filename

