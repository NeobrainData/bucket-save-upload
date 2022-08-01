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
        self.__async_bucket = AsyncBucket()
        self.__bucket_name = bucket_name
        self.__utils = Utils()


    def retrieve_files(self,files_names : list,folder : str) -> dict:
        """
        This function receives the list of files_list which are the files contained in files folder (new jobs).
        It tries to download each one of them from bucket. 
        If it succeeds it means that we already have the job.
        This helps to avoid duplicates.
        """
        files_names = [folder+"/"+name for name in files_names]
        response = asyncio.run(self.__async_bucket.download(self.__bucket_name, files_names))
        fails = 0
        downloaded = 0
        for file in response[0]:
            try:
                if isinstance(file,ClientResponseError):
                    fails += 1
                else:
                    downloaded += 1
            except Exception as e:
                print(e)
                
        return {"response":response,"downloaded":downloaded,"fails":fails}



    def __compare_jobkeys(self, gcs_bucket_folder : str, comparison_field : str, files_path : str, filename_field : str) -> None:
        """
        This function tries to download each file contained inside files folder. 
        If it downloads it means that we already have this offer in the bucket and in this case we only update the key.
        """

        files_names = list(os.listdir(files_path))

        #Generate dictionary with files that are already in the bucket and share the same jobkey as the files in files folder
        rs = self.retrieve_files(files_names,folder=gcs_bucket_folder)
        response = rs["response"]
        downloaded_jobs_dict = self.__utils.parse_response(response,filename_field)


        #Iterate over files in files folder and update the key if we already have it in the bucket
        for filename in files_names:
            new_job = self.__utils.load_json_file(files_path + "/{}".format(filename)) #Scraped job offer
            
            #If this code fails it means that we don't have the job in the bucket, nothing needs to be done, we just upload it.
            try:
                downloaded_job = downloaded_jobs_dict[new_job[filename_field]] #Job offer from bucket

                #Iterate over the scraped offer esco id's and check if they are already inside of the one in the bucket
                #If not add and replace the file in the bucket with the updated esco id's
                new_esco_id = False
                for esco_id in new_job[comparison_field]:
                    if esco_id not in downloaded_job[comparison_field]:
                        downloaded_job[comparison_field].append(esco_id) #Append current id to the existing job
                        new_esco_id = True
                if new_esco_id:
                    self.__utils.save_json_file(downloaded_job,filename,files_path+"/") #Save the job with the new id
                else:
                    self.__utils.delete_file(filename,files_path) #Delete the file if we already have the offer

            except Exception as e:
                pass




    def upload_files(self,files : list, files_names : list, gcs_bucket_folder : str) -> int:
        """
        This function uploads the files contained in files_path folder to GCS bucket.
        It returns the number of files uploaded.
        """
        files = [json.dumps(file) if isinstance(file,dict) else file for file in files]

        if len(files) != len(files_names):
            raise Exception("Files and files_names must have the same length")

        response = asyncio.run(self.__async_bucket.upload(self.__bucket_name, gcs_bucket_folder, files_names,files ))

        counter = 0
        for d in response[0]:
            try:
                if d["kind"] == "storage#object":
                    counter += 1
            except Exception as e:
                pass

        return counter

    def insert_replacing(self,doc_list : list,filename_field : str, bucket_folder : str,comparison_field : str, files_path : str = "temp/files") -> None:
        """
        This function compare each document from doc_list with the docs that are already in the bucket and uploads the new ones / updates the old ones.
        """

        #If the folder doesn't exist create it
        if not os.path.exists(files_path):
            os.makedirs(files_path)


        ids = [doc_list[i][filename_field] +".json" for i in range(len(doc_list))] #Generator with Id's
        paths = [files_path+"/" for _ in ids] #Generator with paths

        self.__utils.clean_directory(files_path) 

        list(map(self.__utils.save_files_to_folder,doc_list,ids,paths,comparison_field)) #Save jsons into files

        self.__compare_jobkeys(
            gcs_bucket_folder=bucket_folder,
            comparison_field=comparison_field,
            files_path=files_path,
            filename_field=filename_field
            ) #Check if we already have those offers on bucket and update/delete them if we do

        files_names = list(os.listdir(files_path))

        files = []
        for file in files_names:
            with open(files_path+"/"+file, mode="r") as f:
                files.append(f.read())

        files_inserted = self.upload_files(
            files=files,
            files_names=files_names,
            gcs_bucket_folder=bucket_folder,
            ) #Save files in files folder into the bucket
        
        print("Files inserted/updated: {}".format(files_inserted))

        self.__utils.clean_directory(files_path)