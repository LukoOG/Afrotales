from django.db import models
from azure.storage.blob import BlobServiceClient
AZURE_STORAGE_ACCOUNT_NAME = 'afrotales'
AZURE_STORAGE_CONTAINER_NAME = 'afrotales-images'
from PIL import Image

class UploadedImage(models.Model):
    image = models.ImageField(upload_to='images/')
    url = models.CharField(max_length = 255)
    def upload_to_azure(self):
        if self.image:
            with self.image.open() as image_file:
                print(image_file)
                image = Image.open(image_file)
                # image_format = image.format.lower()
                # image_name = f'{self.pk}.{image_format}'
                # blob_service_client = BlobServiceClient(account_url=f"https://{AZURE_STORAGE_ACCOUNT_NAME}.blob.core.windows.net/", credential=AZURE_STORAGE_ACCOUNT_KEY)
                # blob_client = blob_service_client.get_blob_client(container=AZURE_STORAGE_CONTAINER_NAME, blob=image_name)
                # blob_client.upload_blob(data=image_file)

                # # default_storage.save(f'images/{image_name}', image_file)
                # self.image.name = f'images/{image_name}'
                # self.save()