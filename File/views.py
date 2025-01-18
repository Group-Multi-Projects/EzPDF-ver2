from django.shortcuts import render, redirect, get_object_or_404
from .forms import UploadFileForm
import os
import requests
from .models import FileModel
import logging
from rest_framework.decorators import api_view,permission_classes,action
from rest_framework import status, viewsets
from rest_framework.response import Response
from. serializers import FileSerializer, UploadFileSerializer
from rest_framework.permissions import IsAuthenticated
from Account.models import AccountModel
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import JsonResponse
from conversion.utils import pdf_to_word, pdf_to_html, html_to_pdf
from bs4 import BeautifulSoup
from datetime import datetime
from drf_spectacular.utils import extend_schema, OpenApiParameter

logger = logging.getLogger(__name__)

def get_jwt_token(username, password):
    url = '/auth/api/token/'
    data = {
        'username': username,
        'password': password
    }
    response = requests.post(url, data=data)
    
    if response.status_code == 200:
        tokens = response.json()
        return tokens['access'], tokens['refresh']
    else:
        print(f"Error: {response.status_code}")
        return None, None
    
@api_view(['POST'])
def upload_file(request):
    print("zoo")
    now = datetime.now()

    unique_id = now.strftime("%Y%m%d%H%M%S")

    serializer = UploadFileSerializer(data=request.data, context={'request': request})
    
    try:
      account = AccountModel.objects.get(username = request.user.username)
      account_id = account.id
    except:
      account_id = "client"
    if serializer.is_valid():
        validated_data = serializer.validated_data  
        serializer.save()
        
        if validated_data.get('request_type') == "editfile":
            file_url = serializer.data['file']
            base_url = file_url.split('/media')[0] + '/media/'
            file_path = file_url.replace(base_url, settings.MEDIA_ROOT)
            output_file_url =  (os.path.join(settings.MEDIA_ROOT,'files','converted_files',f'output-{account_id}-{unique_id}.html')).replace("\\", "/")
            pdf_to_html(file_path,output_file_url)
            with open(output_file_url, 'r') as f:
                    html_content = f.read()
            soup = BeautifulSoup(html_content, 'html.parser')
            style = soup.head.style.string if soup.head and soup.head.style else ''
            body = soup.body.decode_contents() if soup.body else ''
            dict_serializer_data = dict(serializer._data)
            dict_serializer_data['style'] = style
            dict_serializer_data['body'] = body
            dict_serializer_data['ouput_file_url'] = f'{base_url}files/converted_files/output-{account_id}-{unique_id}.html'
            return Response(dict_serializer_data, status=status.HTTP_201_CREATED)
        
        elif validated_data.get('request_type') == "pdf2word":
            file_url = serializer.data['file']
            base_url = file_url.split('/media')[0] + '/media/'
            file_path = file_url.replace(base_url, settings.MEDIA_ROOT)
            output_file_url =  (os.path.join(settings.MEDIA_ROOT,'files','converted_files',f'output-{account_id}-{unique_id}.docx')).replace("\\", "/")
            pdf_to_word(file_path,output_file_url)
            dict_serializer_data = dict(serializer._data)
            dict_serializer_data['ouput_file_url'] = f'{base_url}files/converted_files/output-{account_id}-{unique_id}.docx'
            return Response(dict_serializer_data, status=status.HTTP_201_CREATED)
        
        elif validated_data.get('request_type') == "pdf2html":
            file_url = serializer.data['file']
            base_url = file_url.split('/media')[0] + '/media/'
            file_path = file_url.replace(base_url, settings.MEDIA_ROOT)
            output_file_url =  (os.path.join(settings.MEDIA_ROOT,'files','converted_files',f'output-{account_id}-{unique_id}.html')).replace("\\", "/")
            pdf_to_html(file_path,output_file_url)
            dict_serializer_data = dict(serializer._data)
            dict_serializer_data['ouput_file_url'] = f'{base_url}files/converted_files/output-{account_id}-{unique_id}.html'
            return Response(dict_serializer_data, status=status.HTTP_201_CREATED)
        elif validated_data.get('request_type') == "html2pdf":
            file_url = serializer.data['file']
            base_url = file_url.split('/media')[0] + '/media/'
            file_path = file_url.replace(base_url, settings.MEDIA_ROOT)
            output_file_url =  (os.path.join(settings.MEDIA_ROOT,'files','converted_files',f'output-{account_id}-{unique_id}.pdf')).replace("\\", "/")
            html_to_pdf(file_path,output_file_url)
            dict_serializer_data = dict(serializer._data)
            dict_serializer_data['ouput_file_url'] = f'{base_url}files/converted_files/output-{account_id}-{unique_id}.pdf'
            return Response(dict_serializer_data, status=status.HTTP_201_CREATED)
        else:
            return JsonResponse({'status':'None'})
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
def edit_file(request, file_id):
    try:
        file = get_object_or_404(FileModel, id=file_id)
        logger.info(f"File with ID {file_id} found for user {request.user.username}")
        file_path = file.get_file_path()
        num_pages = file.get_num_pages()
        account = AccountModel.objects.get(username=request.user.username)
        refresh = RefreshToken.for_user(account)
        context = {
            "file": file,
            "file_path": file_path,
            "num_pages": num_pages,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

        logger.info(f"Successfully retrieved file data for user {request.user.username}")

        return JsonResponse(context)
    
    except FileModel.DoesNotExist:
        logger.error(f"File with ID {file_id} does not exist for user {request.user.username}")
        return JsonResponse({"error": "File not found."}, status=404)
    
    except AccountModel.DoesNotExist:
        logger.error(f"Account for user {request.user.username} does not exist.")
        return JsonResponse({"error": "User account not found."}, status=404)

    except Exception as e:
        logger.error(f"Error occurred while retrieving file data for user {request.user.username}: {str(e)}")
        return JsonResponse({"error": "An error occurred while retrieving the file data."}, status=500)


class FileViewSet(viewsets.ModelViewSet):
    queryset = FileModel.objects.all()
    serializer_class = FileSerializer

    @action(detail=False, methods=['get'])
    def files(self, request):
        try:
            files = FileModel.objects.filter(trash=0)
            serializer = FileSerializer(files, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'])
    def trashs(self, request):
        try:
            trashs = FileModel.objects.filter(trash=1)
            serializer = FileSerializer(trashs, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['post'])
    def add_to_trash(self, request, pk=None):
        try:
            file = self.get_object()  # Lấy đối tượng dựa vào pk
            if file.trash == 1:
                return Response({"error": "File đã ở trong thùng rác"}, status=status.HTTP_400_BAD_REQUEST)
            
            file.trash = 1
            file.save()
            serializer = FileSerializer(file)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except FileModel.DoesNotExist:
            return Response({"error": "Không tìm thấy file"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    