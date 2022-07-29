from bucket_save import Bucket

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
    "esco_alt_job_ids": ["45678"],
}
]

#append the extension to the filename
files_names = [d["id"] + ".json" for d in doc_list]

#Upload files to bucket
bucket.upload_files(files=doc_list, #List with documents to upload
files_names=files_names, #List with files names
gcs_bucket_folder="testing_upload" #Folder inside bucket to save those documents
)