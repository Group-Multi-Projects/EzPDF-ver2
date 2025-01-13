from django.shortcuts import render, redirect
from pdf2docx import Converter as WordConverter
import os
from django.conf import settings
from .forms import ConversionForm
from .models import ConversionModel
import requests 
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from .utils import pdf_to_word, pdf_to_html, html_to_pdf
def upload_to_convert(request):
    pass
def convert_file_after_login(request, type):
    form = ConversionForm()
    file = ""
    if type == "pdf2word":
        docx_file = os.path.join(settings.MEDIA_ROOT,'files', 'converted_files', 'output.docx')
        docx_file = docx_file.replace("/", "\\")
        if request.method == "POST":
            form = ConversionForm(request.POST,request.FILES)
            if form.is_valid():
                input_file_path = form.save(request)
                # input_file_path = input_file_path.replace("/", "\\")
                pdf_to_word(input_file_path, docx_file)
                print("Input file:",input_file_path)
                print("Basename:",os.path.basename(docx_file))
                file = 'output.docx'
                return redirect("conversion:converted",filename = file)
    elif type == "pdf2html":
        html_file = os.path.join(settings.MEDIA_ROOT,'files', 'converted_files', 'output.html')
        html_file = html_file.replace("/", "\\")

        if request.method == "POST":
            form = ConversionForm(request.POST,request.FILES)
            if form.is_valid():
                input_file_path = form.save(request)
                input_file_path = input_file_path.replace("/", "\\")
                pdf_to_html(input_file_path, html_file)
                print("Input file:",input_file_path)
                print("Basename:",os.path.basename(html_file))
                file = 'output.html'
                return redirect("conversion:converted", filename = file)
    context = {
        "form":form,
        "type": type,
        "file": file,
        "link":f"conversion:convert_file_after_login"
    }
    return render(request, "File/upload_file.html", context)

def convert_file_before_login(request, type):
    if type == "pdf2word":
        docx_file = os.path.join(settings.MEDIA_ROOT,'files', 'converted_files', 'output.docx')
        docx_file = docx_file.replace("/", "\\")
        if request.method == "POST":
            uploaded_file = request.FILES["original_file"]
            file_name = uploaded_file.name
            file_path = os.path.join('files', 'original_files', file_name)
            saved_path = default_storage.save(file_path, ContentFile(uploaded_file.read()))
            full_file_path = os.path.join(settings.MEDIA_ROOT, saved_path)
            print(saved_path,full_file_path)
            pdf_to_word(full_file_path, docx_file)

            file = 'output.docx'
            return redirect("conversion:converted",filename = file)
    elif type == "pdf2html":
        docx_file = os.path.join(settings.MEDIA_ROOT,'files', 'converted_files', 'output.html')
        docx_file = docx_file.replace("/", "\\")
        if request.method == "POST":
            uploaded_file = request.FILES["original_file"]
            file_name = uploaded_file.name
            file_path = os.path.join('files', 'original_files', file_name)
            saved_path = default_storage.save(file_path, ContentFile(uploaded_file.read()))
            full_file_path = os.path.join(settings.MEDIA_ROOT, saved_path)
            print(saved_path,full_file_path)
            pdf_to_html(full_file_path, docx_file)

            file = 'output.html'
            return redirect("conversion:converted",filename = file)
    context = {
        "type": type,
        "link":f"conversion:convert_file_before_login"

    }
    return render(request, "File/upload_file.html", context)

def converted(request, filename):
    print(filename)
    file_path = filename.replace("\\", "/")
    
    context = {
        "file_name": filename,
        "file_path": file_path,

    }
    return render(request, "conversion/converted.html", context)

