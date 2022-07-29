## This library save/download files in Google Cloud Storage in a parallel fashion

To install the library use: `pip install -U  git+https://github.com/NeobrainData/bucket-save/`


### This library has 3 methods: 

* retrieve_files: Download files from GCP as JSON objects.
* upload: Upload files to GCS
* insert_replacing: Compares each document from doc_list with the docs that are already in the bucket and uploads the new ones / updates the old ones.

The code examples folder contains a python file with an example for each method. 

PS: This library doesn't support Jupyter Notebooks because it relies on asyncio library to parallelize the code.


#### Retrieve Files (Download)

parameters:
    * files_names (list of strings) : Name of the files in GCS
    * folder (string) : The folder on GCS where the files are located

returns (dict):
{
    response (list): A list with the results
    "downloaded" (int): The number of downloaded fiels
    "fails" (int): The number of failed downloads
}

#### Upload

parameters:
    * files (list): The list of JSON/Dictionarie documents,
    * files_names (list): A list of strings with the names that each file should have when the code saves it to GCS
    * gcs_bucket_folder (string): The folder on GCS where the files are going to be save

returns an int with the number of successful updates.



#### Insert Replacing

This function is specifically done to solve Neobrain's problem. I don't recomend the use of it in other cases.

parameters:
    * doc_list (list): list with dictionaries/jsons to update/upload
    * filename_field (string):  Name of the field in each JSON/DICT that holds the name of the files ("id" in most of the cases. This field holds the name of the files.)
    * bucket_folder (string): The folder on GCS where the files are going to be save/update.
    * comparison_field (string): The field to update in case the file is already in GCP ( "esco_alt_job_ids")
    * files_path (string - default="temp/files"): Local folder path to save files. It will create the folder if it doesn't exist and clean it after finish running.

**Steps:**

**For each document:**

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