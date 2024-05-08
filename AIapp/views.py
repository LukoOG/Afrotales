import os, uuid
from azure.identity import DefaultAzureCredential, ClientSecretCredential

from PIL import Image
import requests



from array import array
import os
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import UploadedImage
from azure.storage.blob import  BlobServiceClient, ContentSettings, BlobClient, ContainerClient

AZURE_STORAGE_ACCOUNT_NAME = 'afrotales'
AZURE_STORAGE_ACCOUNT_KEY = os.environ['ACCOUNT_KEY']
AZURE_STORAGE_CONTAINER_NAME = 'afrotales-images'
from PIL import Image



from PIL import Image
from io import BytesIO
from azure.storage.blob import BlobServiceClient
 
from .ai import *

def redirect_to_upload(request):
    return redirect('/upload_image/')

def upload_image(request):
    if request.method == 'POST':
        image_fi = request.FILES['image']
        image_option = request.POST.get('option')
        if image_fi:
            # Open the image file
            image_name = image_fi.name
           
            # Read the content of the image file
            image_content = BytesIO(image_fi.read())
            if image_name.endswith('.png'):
                content_type = 'image/png'
            elif image_name.endswith('.jpg') or image_name.endswith('.jpeg'):
                content_type = 'image/jpeg'
            elif image_name.endswith('.gif'):
                content_type = 'image/gif'
            
            # Create the BlobServiceClient object
            blob_service_client = BlobServiceClient(account_url=f"https://{AZURE_STORAGE_ACCOUNT_NAME}.blob.core.windows.net", credential=AZURE_STORAGE_ACCOUNT_KEY)
            blob_client = blob_service_client.get_blob_client(container=AZURE_STORAGE_CONTAINER_NAME, blob=image_name)
            
            # Upload the image content
            blob_client.upload_blob(data=image_content, overwrite=True, content_settings=ContentSettings(content_type=content_type))
            blob_url = f'https://{AZURE_STORAGE_ACCOUNT_NAME}.blob.core.windows.net/afrotales-images/{image_name}'
            ocr_text = recognize_text_from_image(blob_url)

            #delete blob
            blob_client.delete_blob()

            filter = filter_text(ocr_text)
            print(filter)
            
            if filter.flagged == True:
                return JsonResponse({'description':"that's not appropriate content", "image":'https://afrotales.blob.core.windows.net/afrotales-images/warning.png'})
            elif filter.flagged == False:
                image_description = fetch_description(ocr_text)
                print(image_description)
                prompt_text = fetch_image_prompt(ocr_text, option=image_option)
                try:
                    image_url  = fetch_image_url(prompt_text)
                except Exception as e:
                    print(e)
                    return JsonResponse({'description':"that's not appropriate content", "image":'https://afrotales.blob.core.windows.net/afrotales-images/warning.png'})
            context = {
                'image':image_url, 
                'text':ocr_text,
                'prompt':prompt_text,
                'description':image_description
                }
            
            #dummy context to test frontend without wasting keys
            # context = {
            #     'image':'https://afrotales.blob.core.windows.net/afrotales-images/warning.png', 
            #     'text':'test',
            #     'prompt':'stuff of a prompt',
            #     'description':'description: This excerpt appears to be from the novel "Arrow of God" by Chinua Achebe. In this scene, Ezeulu, a prominent character in the story, confronts someone who has offended him by implying that he is treating his own people poorly. Ezeulus response reflects his frustration and defiance, as well as his adherence to traditional customs and values. The use of the white clay, a symbol of purity and tradition, adds depth to the dialogue and showcases the cultural'
            # }
            return JsonResponse(context)
    websitename = os.environ['WEBSITE_HOSTNAME']          
    return render(request, 'AIapp/upload_image.html', {'hostname':websitename})