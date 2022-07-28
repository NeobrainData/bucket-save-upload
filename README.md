## This library is used to save job offers in Neobrain's Google cloud storage in a parallel fashion

To install the library use: `pip install -U  git+https://github.com/NeobrainData/bucket-save/`

### Rules

#### Each dictionary must contain at least:
* id: This library will save the id as the name of the file
* esco_alt_job_ids: a list with the ESCO ID's

### Steps to save:
#### For each document:

* 1 - Check in GCS if the document is already there
* 2 - If it is, check if the esco_alt_job_ids from the document are inside the one in GCS, if not add them
* 3 - If not add the new document.

### Your machine needs to have the access code in the environment variable before using the library.

If you don't have it, download the key from GCS and set it using this code:
```
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path_to_your_.json_credential_file"
```

### PS: GCS don’t accept date time objects, you need to convert them to strings.

### Code example:

```
import bucket_save

bucket = bucket_save.Bucket("NAME_OF_THE_BUCKET")

#List with documents to upload (any number of dicts)
doc_list=[{
    "id": "a1b2c3d4e5f6g7h8i9j0",
    "title": "title",
    "company": "company",
    "location": "location",
    "url": "url",
    "date": "date",
    "job_type": "job_type",
    "esco_alt_job_ids": ["30061697"],
}]

bucket.insert(doc_list,
files_path="temp/files", #local path to save temp files
bucket_folder="testing" #Folder in bucket to save files (If it doesn't exist it will create)
)
```

