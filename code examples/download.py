from bucket_save.gcp_bucket import Bucket
import json

bucket = Bucket("test_indeed_bucket_neobrain")

files_names = ["123.json","456.json"] #List with files names to download

rs = bucket.retrieve_files(files_names=files_names,folder="testing")

#rs["downloaded"] is the number of downloaded files
#rs["fails"] is the number of files that failed to download
#rs["response"][0] is the list of downloaded files

print(json.loads(rs["response"][0][0])) #This is the first file downloaded