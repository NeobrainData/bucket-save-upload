
import backoff
import aiohttp
from gcloud.aio.storage import Storage
import logging

logging.getLogger('backoff').setLevel(logging.ERROR)


class StorageWithBackoff(Storage):
    @backoff.on_exception(backoff.expo, aiohttp.ClientResponseError,
                          max_tries=3, jitter=backoff.full_jitter)
    async def copy(self, *args, **kwargs):
        return await super().copy(*args, **kwargs)

    @backoff.on_exception(backoff.expo, aiohttp.ClientResponseError,
                          max_tries=1, jitter=backoff.full_jitter)
    async def download(self, *args, **kwargs):
        return await super().download(*args, **kwargs)

    @backoff.on_exception(backoff.expo, aiohttp.ClientResponseError,
                          max_tries=3, jitter=backoff.full_jitter)
    async def upload(self, *args, **kwargs):
        return await super().upload(*args, **kwargs)