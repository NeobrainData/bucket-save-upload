## This library is used to save job offers in Neobrain's Google cloud storage in a parallel fashion

To install the library use: `pip install -U  git+https://github.com/NeobrainData/bucket-save/`

### Rules

#### Each dictionary must contain at least:
* id: the jobkey (will save the name of the file as the jobkey)
* esco_alt_job_ids: a list with the ESCO ID's

### Steps to save:
* 1 - 


#### Your machine needs to have the access code in the environment variable before using the library.
#### GCS don’t accept date time objects, you need to convert them to strings.

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

