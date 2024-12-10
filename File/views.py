from django.shortcuts import render, redirect, get_object_or_404
from .forms import UploadFileForm
import os
import requests
from .models import FileModel
import logging
from rest_framework.decorators import api_view,permission_classes
from rest_framework import status
from rest_framework.response import Response
from. serializers import FileSerializer, UploadFileSerializer
from rest_framework.permissions import IsAuthenticated
from Account.models import AccountModel
from django.contrib.auth.decorators import login_required
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from tools.models import TextModel,DrawModel
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
logger = logging.getLogger(__name__)
# Create your views here.

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
    serializer = UploadFileSerializer(data=request.data, context={'request': request})
    
    if serializer.is_valid():
        serializer.save()  # Save the file data
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
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
    


@api_view(["GET", "PUT", "DELETE"])
# @permission_classes([IsAuthenticated])
def get_put_delete_file_api(request, id):
    model = get_object_or_404(FileModel, id=id)

    if request.method == "GET":
        serializer = FileSerializer(model)
        return Response(serializer.data)

    elif request.method == "PUT":
        serializer = FileSerializer(model, data=request.data)
        print("geellsadlasd")
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == "DELETE":
        model.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    


@api_view(["GET", "POST"])
# @permission_classes([IsAuthenticated])
def get_list_files(request,page_type):
    if request.method == "GET":
        try:
            account = AccountModel.objects.get(username=request.user.username)
            if page_type == "files":
                files = FileModel.objects.filter(
                    account=account,
                    trash = 0
                    )
            elif page_type == "trash":
                files = FileModel.objects.filter(
                    account=account,
                    trash = 1
                    )
            serializers = FileSerializer(files, many=True)
            return Response({"list_files": serializers.data}, status=status.HTTP_200_OK)
        except AccountModel.DoesNotExist:
            return Response({"error": "Account not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    elif request.method == "POST":
        # Xử lý dữ liệu POST ở đây nếu cần
        return Response({"message": "POST method is not implemented"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

@csrf_exempt  
def add_to_trash(request, id):
    if request.method == "POST":
        file = get_object_or_404(FileModel, id=id)
        file.trash = 1
        file.save()
        return JsonResponse({"status": "true"})
    return JsonResponse({"status": "false", "message": "Invalid request method."}, status=400)