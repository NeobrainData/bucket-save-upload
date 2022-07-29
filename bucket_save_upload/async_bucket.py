import asyncio
from gcloud.aio.auth import Token
from gcloud.aio.storage import Storage 
from .storage_backoff import StorageWithBackoff 
from aiohttp.client_exceptions import ClientConnectorError,ClientResponseError
class AsyncBucket():
    def __init__(self) -> None:
        # Used a token from a service account for authentication
        self.scopes = ["https://www.googleapis.com/auth/devstorage.full_control"]

    async def download(self,bucket : str, obj_names : list) -> list:
        """
        This function downloads a list of json objects from a bucket in a parallel fashion.
        """
        sa_token = Token(scopes=self.scopes)
        response = []
        async with Storage(token=sa_token) as client:
            tasks = (client.download(bucket, file) for file in obj_names) # Used the gcloud library download method, with required args
            try:
                response.append(await asyncio.gather(*tasks,return_exceptions=True))
            except ClientConnectorError as e:
                raise("Exception: ClientConnectorError.Please check GCS bucket name and credentials.")  
            except Exception as e:
                print(e)

        await sa_token.close()
        return response

    async def upload(self,bucket : str,gcs_bucket_folder : str, file_names : list, jsons : list) -> list:
        """
        This function uploads a list of objects to a bucket in a parallel fashion.
        """
        file_names = [gcs_bucket_folder+"/"+i for i in file_names]
        sa_token = Token(scopes=self.scopes)
        response = []
        async with StorageWithBackoff(token=sa_token) as client:
            tasks = [client.upload(*arg) for arg in zip([bucket for _ in range(len(file_names))],file_names,jsons)] # Used the gcloud library upload method, with required args
            try:
                response.append(await asyncio.gather(*tasks,return_exceptions=True))
            except ClientResponseError as e:
                raise Exception("Exception: ClientResponseError.Maybe due to a connection error.")

            except ClientConnectorError as e:
                raise Exception("Exception: ClientConnectorError.Please check GCS bucket name and credentials.")

            except Exception as e:
                if e == ClientConnectorError:
                    raise("Exception: ClientConnectorError.Please check GCS bucket name and credentials.")    
                else:
                    print(e)

        await sa_token.close()
        return response

