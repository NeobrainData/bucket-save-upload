import os, shutil
import json
from aiohttp.client_exceptions import ClientResponseError

class Utils():
    def clean_directory(self,folder : str) -> None:
        """ This function clean the given directory """
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))

    def save_json_file(self,json_data:dict,filename:str,folder:str) -> None:
        """
        This function save a json as a file from files folder
        """
        path = folder + filename

        with open(path, 'w') as f:
            json.dump(json_data, f)


    def delete_file(self,filename:str,files_path) -> None:
        """
        This function deletes a json as a file from files folder
        """
        os.remove(files_path + '/{}'.format(filename))

    def load_json_file(self,filename:str) -> dict:
        """Load a json file given a path"""
        with open(filename) as f:
            return json.load(f)

    def save_files_to_folder(self,json_data:dict, filename : str, folder : str, comparison_field : str) -> None:
        """
        This function saves the documents into files folder.
        It first checks if the files is already in the folder and if it is instead of replacing it it adds the new esco id's.
        """
        #Check if the file is already inside the folder if not just save it otherwise check if esco id's are the same and merge them if not
        path = folder + filename

        files = os.listdir(folder)
        if not filename in files:
            self.save_json_file(json_data,filename,folder)
        else:
            doc = self.load_json_file(path)
            if json_data[comparison_field] != doc[comparison_field]:
                doc[comparison_field] = list(set(doc[comparison_field]+ json_data[comparison_field]))
                self.save_json_file(doc,filename,folder)

    def parse_response(self,response: list, filename_field : str) -> list:
        """
        Receives a list of responses from GCS and returns a list of dictionaries with the information of each file.
        """        
        downloaded_jobs_dict = {}
        for file in response[0]:
            try:
                if isinstance(file,ClientResponseError):
                    continue
                else:
                    tmp_f = json.loads(file)
                    downloaded_jobs_dict.update({tmp_f[filename_field]:tmp_f})
            except Exception as e:
                print(e)
        return downloaded_jobs_dict