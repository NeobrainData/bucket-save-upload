import json
import asyncio
from .utils_file import Utils
import os
from .async_bucket import AsyncBucket
from aiohttp.client_exceptions import ClientResponseError

class Bucket():
    """
    This class deals with the GCP bucket.
    """
    def __init__(self,bucket_name : str ) -> None:
        #Initialize bucket
        self.async_bucket = AsyncBucket()
        self.bucket_name = bucket_name
        self.utils = Utils()

    def save_files_to_folder(self,json_data:dict,filename:str,folder:str) -> None:
        """
        This function saves the documents into files folder.
        It first checks if the files is already in the folder and if it is instead of replacing it it adds the new esco id's.
        """
        #Check if the file is already inside the folder if not just save it otherwise check if esco id's are the same and merge them if not
        path = folder + filename

        files = os.listdir(folder)
        if not filename in files:
            self.utils.save_json_file(json_data,filename,folder)
        else:
            doc = self.utils.load_json_file(path)
            if json_data["esco_alt_job_ids"] != doc["esco_alt_job_ids"]:
                doc["esco_alt_job_ids"] = list(set(doc["esco_alt_job_ids"]+ json_data["esco_alt_job_ids"]))
                self.utils.save_json_file(doc,filename,folder)

    def retrieve_files_from_gcs(self,files_list : list,folder : str) -> dict:
        """
        This function receives the list of files_list which are the files contained in files folder (new jobs).
        It tries to download each one of them from bucket. 
        If it succeeds it means that we already have the job.
        This helps to avoid duplicates.
        """
        files_list = [folder+"/"+name for name in files_list]
        response = asyncio.run(self.async_bucket.download(self.bucket_name, files_list))
        fls = {}
        fails = 0
        for file in response[0]:
            try:
                if isinstance(file,ClientResponseError):
                    fails += 1
                    continue
                else:
                    tmp_f = json.loads(file)
                    fls.update({tmp_f["id"]:tmp_f})
            except Exception as e:
                print(e)
        print("Total Files: ", len(files_list))
        print("Sucessful downloaded files from GCS: {}. Fails (Files not in GCS): {}".format(len(fls),fails))
        return fls

    def up_jsons_to_gcp(self,files_path : str, gcs_bucket_folder : str) -> dict:
        """
        This function receives the list of files_list which are the files contained in files folder (new jobs).
        It tries to download each one of them from bucket. 
        If it succeeds it means that we already have the job.
        This helps to avoid duplicates.
        """
        files_list = list(os.listdir(files_path))

        files = []
        for file in files_list:
            with open(files_path+"/"+file, mode="r") as f:
                files.append(f.read())
        response = asyncio.run(self.async_bucket.upload(self.bucket_name, gcs_bucket_folder, files_list,files ))
        return response


    def compare_jobkeys(self, gcs_bucket_folder : str, files_path : str) -> None:
        """
        This function tries to download each file contained inside files folder. 
        If it downloads it means that we already have this offer in the bucket and in this case we only update the key.
        """

        files_list = list(os.listdir(files_path))

        #Returns a dictionary with files that are already in the bucket and share the same jobkey as the files in files folder
        downloaded_jobs_dict = self.retrieve_files_from_gcs(files_list,folder=gcs_bucket_folder) 


        for filename in files_list:
            new_job = self.utils.load_json_file(files_path + "/{}".format(filename)) #Scraped job offer
            
            #If this code fails it means that we don't have the job in the bucket, nothing needs to be done, we just upload it.
            try:
                downloaded_job = downloaded_jobs_dict[new_job["id"]] #Job offer from bucket

                #Iterate over the scraped offer esco id's and check if they are already inside of the one in the bucket
                #If not add and replace the file in the bucket with the updated esco id's
                new_esco_id = False
                for esco_id in new_job["esco_alt_job_ids"]:
                    if esco_id not in downloaded_job["esco_alt_job_ids"]:
                        downloaded_job["esco_alt_job_ids"].append(esco_id) #Append current id to the existing job
                        new_esco_id = True
                if new_esco_id:
                    self.utils.save_json_file(downloaded_job,filename,files_path+"/") #Save the job with the new id
                else:
                    self.utils.delete_file(filename,files_path) #Delete the file if we already have the offer

            except Exception as e:
                pass




    def gsutil_upload_files(self, gcs_bucket_folder : str, files_path : str, bucket : str = "test_indeed_bucket_neobrain") -> int:
        """This function compares the scraped jobs with the jobs that are already in the bucket and uploads the new ones / updates the old ones."""
        
        self.compare_jobkeys(gcs_bucket_folder=gcs_bucket_folder,files_path=files_path) #Check if we already have those offers on bucket and update/delete them if we do
        #up_cmd = "gsutil -m cp {}/* gs://{}/{}".format(files_path,bucket,gcs_bucket_folder) #GSUtil command #Not used anymore (replaced by the function below)
        #os.system(up_cmd) #Upload remaining files in files folder to bucket #Not used anymore (replaced by the function below)
        response = self.up_jsons_to_gcp(files_path=files_path,gcs_bucket_folder=gcs_bucket_folder) #Upload remaining files in files folder to bucket

        counter = 0
        for d in response[0]:
            try:
                if d["kind"] == "storage#object":
                    counter += 1
            except Exception as e:
                pass

        return counter

    def insert(self,doc_list : list,files_path : str = "temp/files",bucket_folder : str = "indeed") -> None:
        """
        This function inserts a list of dictionaries into the bucket.
        """
        print("Step 4: Inserting into bucket")
        #If the folder doesn't exist create it
        if not os.path.exists(files_path):
            os.makedirs(files_path)


        ids = [doc_list[i]["id"] +".json" for i in range(len(doc_list))] #Generator with Id's
        paths = [files_path+"/" for _ in ids] #Generator with paths

        self.utils.clean_directory(files_path) 

        list(map(self.save_files_to_folder,doc_list,ids,paths)) #Save jsons into files
        files_inserted = self.gsutil_upload_files(
            gcs_bucket_folder=bucket_folder,
            bucket=self.bucket_name,
            files_path=files_path) #Save files in files folder into the bucket
        
        print("Files inserted/updated: {}".format(files_inserted))

        self.utils.clean_directory(files_path)