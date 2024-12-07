from django.shortcuts import render, redirect
from .forms import SignUpForm
from .models import AccountModel
from django.contrib.auth import login,authenticate,logout
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from django.contrib import messages
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import HttpResponse, JsonResponse
import logging, json
from rest_framework.permissions import IsAuthenticated
from .serializers import AccountSerializer
from django.views.decorators.csrf import csrf_exempt

logger = logging.getLogger('custom_logger')
@csrf_exempt
def signup(request):
    """
    Handle user signup requests and return JSON response.
    """
    if request.method == "GET":
        logger.debug("Signup page accessed with GET method.")
        return JsonResponse({"success": False, "message": "GET method not allowed for signup."}, status=405)

    if request.method != "POST":
        return JsonResponse({"success": False, "message": "Method not allowed."}, status=405)
    
    try:
        # Lấy dữ liệu JSON từ request
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"success": False, "message": "Invalid JSON input."}, status=400)

        # Khởi tạo form đăng ký với dữ liệu
        form = SignUpForm(data)

        if form.is_valid():
            form.save()  # Lưu thông tin người dùng
            logger.info("User signed up successfully.")
            return JsonResponse({"success": True, "message": "Sign up successful! Redirecting to home page."}, status=201)
        else:
            logger.warning("Sign up failed due to invalid form data.")
            return JsonResponse({"success": False, "message": "Invalid form data.", "errors": form.errors}, status=400)
    except Exception as e:
        logger.error(f"An error occurred during signup: {e}", exc_info=True)
        return JsonResponse({"success": False, "message": "An error occurred during sign up."}, status=500)
@csrf_exempt  
def signin(request):
    """
    Handle user login request via JSON input and return a JSON response with status and JWT tokens.
    """
    if request.method != 'POST':
        return JsonResponse({"success": False, "message": "Method not allowed."}, status=405)
    try:
        # Parse JSON data from request body
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"success": False, "message": "Invalid JSON input."}, status=400)

        email_login = data.get("email_login")
        password_login = data.get("password_login")
        next_page = data.get("next", "")
        # Validate input
        if not email_login or not password_login:
            return JsonResponse({"success": False, "message": "Email and password are required."}, status=400)
        logger.info(f"User attempting login: {email_login}")
        user = authenticate(request, username=email_login, password=password_login)

        if user:
            login(request, user)
            logger.info(f"Login successful for user: {email_login}")
            refresh = RefreshToken.for_user(user)

            return JsonResponse({
                "success": True,
                "next_page": next_page,
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }, status=200)
        else:
            logger.warning(f"Failed login attempt for email: {email_login}")
            return JsonResponse({"success": False, "message": "Email hoặc mật khẩu không đúng!"}, status=400)
    except Exception as e:
        logger.error(f"An error occurred during login: {e}", exc_info=True)
        return JsonResponse({"success": False, "message": "Đã xảy ra lỗi."}, status=500)
@csrf_exempt
def signout(request):
    logout(request)
    return redirect("")

@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def get_user_info_serializers(request):
    if request.method == "GET":
        try:
            account = AccountModel.objects.get(username=request.user.username)
            serializers = AccountSerializer(account)
            return Response({"data": serializers.data}, status=status.HTTP_200_OK)
        except AccountModel.DoesNotExist:
            return Response({"error": "Account not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    elif request.method == "POST":
        # Xử lý dữ liệu POST ở đây nếu cần
        return Response({"message": "POST method is not implemented"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
