from selenium import webdriver
from models.black_lists import BlackLists
from models.job_histories import JobHistories
from models.job_histories import db

class AnalyzeService: 
    @staticmethod
    def get_list_group_history():
        # Get list group history by job_index and show number of records by status 
        list_group_history = db.session.query(JobHistories.job_index, JobHistories.status, db.func.count(JobHistories.status)).group_by(JobHistories.job_index, JobHistories.status).order_by(JobHistories.job_index.desc()).all()
        # Initialize a dictionary to hold the results for each job_index
        results = {}
        # Populate the results dictionary with counts from the query
        for row in list_group_history:
            job_index = row[0]
            status = row[1]
            count = row[2]
            if job_index not in results:
                results[job_index] = {
                    "total_index": 0,
                    "job_index": job_index,
                    "count_status_0": 0,
                    "count_status_1": 0,
                    "count_status_2": 0,
                    "count_status_3": 0
                }
            results[job_index][f"count_status_{status}"] = count
            results[job_index]["total_index"] += count
        # Convert the results dictionary to a list

        result_list = list(results.values())
        
        return result_list

