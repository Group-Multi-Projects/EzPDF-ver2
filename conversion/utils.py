from django.shortcuts import render, redirect
from pdf2docx import Converter as WordConverter
import os
from django.conf import settings
from .forms import ConversionForm
from .models import ConversionModel
import requests, os, subprocess
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
def pdf_to_word(pdf_file_path, word_file_path):
    cv = WordConverter(pdf_file_path)
    cv.convert(word_file_path, start=0, end=None)
    cv.close()
    
# Create your tests here.
def convert_pdf_to_html(pdf_path, html_path):
    # command = f"pdf2htmlEX --optimize-text 1 --no-drm 1 --fit-width 1024 --font-format woff {pdf_path} {html_path}"
    command = f"pdf2htmlEX --optimize-text 1 --process-outline 0 {pdf_path} {html_path}"    
    print('html_path',html_path)
    process = subprocess.Popen(command, shell=True)
    process.communicate()
    if process.returncode != 0:
        return False
    else:
        return True
# if convert_pdf_to_html("input.pdf", "output1.html"):
# print("✅ Chuyển đổi thành công")
def pdf_to_html_payment(pdf_file_path,output_file_path):
    API_KEY = "luutruongan08082003@gmail.com_oPSSSxmvrEfbE9MQmuw5q7XvntJZSUIyDuvlUPe1NEvwr67l6rjd6w42gBzpvG0U"

    BASE_URL = "https://api.pdf.co/v1"

    Pages = ""
    Password = ""
    PlainHtml = False
    ColumnLayout = False
    def convertPdfToHtml(uploadedFileUrl, destinationFile):
        """Converts PDF To Html using PDF.co Web API"""

        parameters = {}
        parameters["name"] = os.path.basename(destinationFile)
        parameters["password"] = Password
        parameters["pages"] = Pages
        parameters["simple"] = PlainHtml
        parameters["columns"] = ColumnLayout
        parameters["url"] = uploadedFileUrl

        url = "{}/pdf/convert/to/html".format(BASE_URL)

        response = requests.post(url, data=parameters, headers={ "x-api-key": API_KEY })
        if (response.status_code == 200):
            json = response.json()

            if json["error"] == False:
                #  Get URL of result file
                resultFileUrl = json["url"]            
                # Download result file
                r = requests.get(resultFileUrl, stream=True)
                if (r.status_code == 200):
                    with open(destinationFile, 'wb') as file:
                        for chunk in r:
                            file.write(chunk)
                    print(f"Result file saved as \"{destinationFile}\" file.")
                else:
                    print(f"Request error: {response.status_code} {response.reason}")
            else:
                print(json["message"])
        else:
            print(f"Request error: {response.status_code} {response.reason}")
        return response


    def uploadFile(fileName):
        """Uploads file to the cloud"""
        

        url = "{}/file/upload/get-presigned-url?contenttype=application/octet-stream&name={}".format(
            BASE_URL, os.path.basename(fileName))
        
        response = requests.get(url, headers={ "x-api-key": API_KEY })
        if (response.status_code == 200):
            json = response.json()
            
            if json["error"] == False:
                uploadUrl = json["presignedUrl"]
                uploadedFileUrl = json["url"]

                with open(fileName, 'rb') as file:
                    requests.put(uploadUrl, data=file, headers={ "x-api-key": API_KEY, "content-type": "application/octet-stream" })

                return uploadedFileUrl
            else:
                print(json["message"])    
        else:
            print(f"Request error: {response.status_code} {response.reason}")

        return None

    uploadedFileUrl = uploadFile(pdf_file_path)
    if (uploadedFileUrl != None):
        convertPdfToHtml(uploadedFileUrl, output_file_path)

def html_to_pdf_payment(html_path, output_pdf_path, api_key=None):
    """
    Converts HTML to PDF using PDF.co Web API.

    Parameters:
        html_path (str): Path to the input HTML file.
        output_pdf_path (str): Path to save the resulting PDF file.
        api_key (str): API key for PDF.co.
    """ 
    if api_key is None:
        api_key = "luutruongan08082003@gmail.com_oPSSSxmvrEfbE9MQmuw5q7XvntJZSUIyDuvlUPe1NEvwr67l6rjd6w42gBzpvG0U"
    with open(html_path, mode='r', encoding='utf-8') as file:
        sample_html = file.read()
 
    parameters = {
        "html": sample_html,
        "name": os.path.basename(output_pdf_path),
        "margins": "5px 5px 5px 5px",
        "paperSize": "A4",
        "orientation": "Portrait",
        "printBackground": "true",
        "async": "false",
        "header": "",
        "footer": ""
    }
 
    base_url = "https://api.pdf.co/v1"
    url = f"{base_url}/pdf/convert/from/html"
 
    response = requests.post(url, data=parameters, headers={"x-api-key": api_key})

    if response.status_code == 200:
        json_response = response.json()

        if not json_response.get("error", True): 
            result_file_url = json_response.get("url")
            r = requests.get(result_file_url, stream=True)
            if r.status_code == 200:
                with open(output_pdf_path, 'wb') as output_file:
                    for chunk in r:
                        output_file.write(chunk)
                print(f"Result file saved as \"{output_pdf_path}\".")
            else:
                print(f"Failed to download the PDF file: {r.status_code} {r.reason}")
        else:
            print(f"API Error: {json_response.get('message')}")
    else:
        print(f"Request Error: {response.status_code} {response.reason}")
