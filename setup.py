import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='bucket_save',
    version='1.0',
    author='Rennan Valadares',
    author_email='rennanvoa2@gmail.com',
    description='Save files in a GCS bucket',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/NeobrainData/bucket-save',
    project_urls = {
        "Bug Tracker": "https://github.com/NeobrainData/bucket-save/issues"
    },
    license='None',
    packages=['bucket_save'],
    install_requires=['requests',"aiohttp","openpyxl","gcloud.aio.storage","backoff","asyncio"],
)