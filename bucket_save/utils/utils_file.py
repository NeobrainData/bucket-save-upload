import os, shutil
import json

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


