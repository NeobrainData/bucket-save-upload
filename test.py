from src.database.gcp_bucket import Bucket

bucket = Bucket("test_indeed_bucket_neobrain")

#List with documents to upload
doc_list=[{
    "id": "a1b2c3d4e5f6g7h8i9j0",
    "title": "title",
    "company": "company",
    "location": "location",
    "url": "url",
    "date": "date",
    "job_type": "job_type",
    "esco_alt_job_ids": ["4"],
    "jobkey": "a1b2c3d4e5f6g7h8i9j0",
}]

bucket.insert(doc_list,
files_path="temp/files", #local path to save temp files
bucket_folder="testing" #Folder in bucket to save files (If it doesn't exist it will create)
)