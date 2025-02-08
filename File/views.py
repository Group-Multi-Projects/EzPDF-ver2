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
from rest_framework.views import APIView

from django.http import JsonResponse
from conversion.utils import pdf_to_word, pdf_to_html, html_to_pdf
from bs4 import BeautifulSoup
from datetime import datetime
from drf_spectacular.utils import extend_schema, OpenApiParameter
from .pagination import CustomPagination
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiExample
from .docs import file_schema, upload_file_schema
from .html404 import body_response, style_response
logger = logging.getLogger(__name__)

def home_page(request):
    return render(request,"File/home_page.html")
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
class UploadFileView(APIView):
    @upload_file_schema()
    def post(self, request, *args, **kwargs):
        now = datetime.now()
        unique_id = now.strftime("%Y%m%d%H%M%S")

        # 1️⃣ Xử lý lỗi khi tạo serializer
        try:
            serializer = UploadFileSerializer(data=request.data, context={'request': request})
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return Response({'error': f'Serializer error: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

        # 2️⃣ Xử lý lỗi khi lấy `AccountModel`
        try:
            account = AccountModel.objects.get(username=request.user.username)
            account_id = account.id
        except AccountModel.DoesNotExist:
            account = None
            account_id = "client"

        # 3️⃣ Gán giá trị `account` vào serializer
        validated_data = serializer.validated_data
        validated_data['account'] = account

        try:
            serializer.save()
        except Exception as e:
            return Response({'error': f'Failed to save file: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # 4️⃣ Xử lý đường dẫn file
        try:
            file_url = serializer.data.get('file')
            if not file_url:
                raise ValueError("File URL is empty")
            
            base_url = file_url.split('/media')[0] + '/media/'
            file_path = file_url.replace(base_url, settings.MEDIA_ROOT)
            
            output_dir = os.path.join(settings.MEDIA_ROOT, 'files', 'converted_files')
            os.makedirs(output_dir, exist_ok=True)
        except Exception as e:
            return Response({'error': f'File path error: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        request_type = validated_data.get('request_type')
        output_file_url = ""
        is_existed_file = True
        try:
            if request_type == "editfile":
                output_file_path = os.path.join(output_dir, f'output-{account_id}-{unique_id}.html').replace("\\", "/")
                try:
                    
                    pdf_to_html(file_path, output_file_path)
                except Exception as e:
                    print(e)
                try:
                    with open(output_file_path, 'r', encoding='utf-8') as f:
                        html_content = f.read()
                except Exception as e:
                    print(e)
                    is_existed_file = False
                    
                if is_existed_file == False:
                    style = style_response
                    body = body_response
                    output_file_url = f'{base_url}files/converted_files/404.html'
                    
                else:
                    soup = BeautifulSoup(html_content, 'html.parser')
                    style = soup.head.style.string if soup.head and soup.head.style else ''
                    body = soup.body.decode_contents() if soup.body else ''

                    output_file_url = f'{base_url}files/converted_files/output-{account_id}-{unique_id}.html'
                response_data = {
                    **serializer.data,
                    'style': style,
                    'body': body,
                    'output_file_url': output_file_url
                }
                return Response(response_data, status=status.HTTP_201_CREATED)

            elif request_type == "pdf2word":
                output_file_path = os.path.join(output_dir, f'output-{account_id}-{unique_id}.docx').replace("\\", "/")
                pdf_to_word(file_path, output_file_path)
                output_file_url = f'{base_url}files/converted_files/output-{account_id}-{unique_id}.docx'

            elif request_type == "pdf2html":
                output_file_path = os.path.join(output_dir, f'output-{account_id}-{unique_id}.html').replace("\\", "/")
                pdf_to_html(file_path, output_file_path)
                output_file_url = f'{base_url}files/converted_files/output-{account_id}-{unique_id}.html'

            elif request_type == "html2pdf":
                output_file_path = os.path.join(output_dir, f'output-{account_id}-{unique_id}.pdf').replace("\\", "/")
                html_to_pdf(file_path, output_file_path)
                output_file_url = f'{base_url}files/converted_files/output-{account_id}-{unique_id}.pdf'

        except Exception as e:
            return Response({'error': f'File conversion error: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # 5️⃣ Trả về kết quả
        if output_file_url:
            response_data = {**serializer.data, 'output_file_url': output_file_url}
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            return JsonResponse({'status': 'None'}, status=status.HTTP_400_BAD_REQUEST)
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

@file_schema()
class FileViewSet(viewsets.ModelViewSet):
    queryset = FileModel.objects.all()
    serializer_class = FileSerializer
    pagination_class = CustomPagination

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
    