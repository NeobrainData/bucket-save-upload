import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='bucket_save_upload',
    version='1.0.1',
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
    packages=['bucket_save_upload'],
    install_requires=['requests',"aiohttp","openpyxl","gcloud.aio.storage","backoff","asyncio"],
)


from distutils.core import setup

setup(
    name = 'bucket_save_upload',
    packages = ['bucket_save_upload'],
    version = 'v1.0.1',
    description = "Save and upload to GCS buckets in a parallel fashion.",
    author="Rennan Valadares",
    author_email="rennanvoa2@gmail.com",
    url = 'https://github.com/NeobrainData/bucket-save',
    download_url = 'https://github.com/rennanvoa2/save_spacy/archive/refs/tags/v1.0.1.tar.gz',
    keywords = ['GCS', 'Google Cloud Storage', 'bucket', 'upload'],
    classifiers = [],
)
