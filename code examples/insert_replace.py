from bucket_save_upload import Bucket

bucket = Bucket("test_indeed_bucket_neobrain")

#List with documents to upload
doc_list=[{
    "id": "a1b2c3d4e5f6g7h8i9j0", #Unique field to identify each document
    "title": "title",
    "company": "company",
    "location": "location",
    "url": "url",
    "date": "date",
    "job_type": "job_type",
    "esco_alt_job_ids": ["45678"],
}
]

bucket.insert_replacing(doc_list=doc_list,
filename_field="id", #Every document must have a unique field to identify it and this is the name of this field
files_path="temp/files", #local path to save temp files
bucket_folder="testing", #Folder inside bucket to save those documents
comparison_field="esco_alt_job_ids" #Folder in bucket to save files (If it doesn't exist it will create)
)