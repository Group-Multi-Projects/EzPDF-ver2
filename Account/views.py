from django.shortcuts import render, redirect
from .forms import SignUpForm
from .models import AccountModel
from django.contrib.auth import login,authenticate,logout
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from django.contrib import messages
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import HttpResponse, JsonResponse
import logging, json
from rest_framework.permissions import IsAuthenticated
from .serializers import AccountSerializer
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_405_METHOD_NOT_ALLOWED
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import AllowAny
import logging, json

logger = logging.getLogger('custom_logger')
class SignupView(APIView):
    permission_classes = [AllowAny]
    @extend_schema(
        request={
            "application/json": {
                "type": "object",
                "properties": {
                    "username": {"type": "string", "example": "testuser"},
                    "email": {"type": "string", "example": "user@gmail.com"},
                    "password1": {"type": "string", "example": "testpassword"},
                    "password2": {"type": "string", "example": "testpassword"},
                },
                "required": ["username", "password1","password2"],
            }
        },
        responses={
            201: {"description": "User created successfully."},
            400: {"description": "Invalid form data."},
            500: {"description": "Internal server error."},
        },
        description="API endpoint for user signup."
    )
    def post(self, request):
        try:
            data = request.data
            form = SignUpForm(data)
            if form.is_valid():
                form.save()
                logger.info("User signed up successfully.")
                return Response({"success": True, "message": "Sign up successful!"}, status=HTTP_201_CREATED)
            else:
                logger.warning("Sign up failed due to invalid form data.")
                return Response({"success": False, "message": "Invalid form data.", "errors": form.errors}, status=HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"An error occurred during signup: {e}", exc_info=True)
            return Response({"success": False, "message": "An error occurred during sign up."}, status=HTTP_500_INTERNAL_SERVER_ERROR)

class SignInAPIView(APIView):
    permission_classes = [AllowAny]  # Cho phép truy cập công khai
    @extend_schema(
        request={
            "application/json": {
                "type": "object",
                "properties": {
                    "email_login": {"type": "string", "example": "testuser"},
                    "password_login": {"type": "string", "example": "testpassword"},
                    "next": {"type": "string", "example": "/dashboard/"}
                },
                "required": ["email_login", "password_login"],
            }
        },
        responses={
            200: {
                "description": "Login successful. Returns JWT tokens.",
                "type": "object",
                "properties": {
                    "refresh": {"type": "string", "example": "refresh_token_example"},
                    "access": {"type": "string", "example": "access_token_example"},
                }
            },
            400: {"description": "Invalid credentials or input."},
            500: {"description": "Internal server error."},
        },
        description="API endpoint for user signin."
    )
    def post(self, request):
        """
        Handle user login request via JSON input and return JWT tokens.
        """
        try:
            # Parse JSON data
            try:
                data = request.data
            except Exception:
                return Response({"success": False, "message": "Invalid JSON input."}, status=400)

            email_login = data.get("email_login")
            password_login = data.get("password_login")
            next_page = data.get("next", "")

            # Validate input
            if not email_login or not password_login:
                return Response({"success": False, "message": "Email and password are required."}, status=400)

            logger.info(f"User attempting login: {email_login}")
            user = authenticate(request, username=email_login, password=password_login)

            if user:
                login(request, user)
                logger.info(f"Login successful for user: {email_login}")
                refresh = RefreshToken.for_user(user)

                return Response({
                    "success": True,
                    "next_page": next_page,
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                }, status=200)
            else:
                logger.warning(f"Failed login attempt for email: {email_login}")
                return Response({"success": False, "message": "Email hoặc mật khẩu không đúng!"}, status=400)
        except Exception as e:
            logger.error(f"An error occurred during login: {e}", exc_info=True)
            return Response({"success": False, "message": "Đã xảy ra lỗi."}, status=500)
@csrf_exempt
def signout(request):
    logout(request)
    return redirect("")

@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def get_user_info_serializers(request):
    if request.method == "GET":
        try:
            user = request.user  
            account = AccountModel.objects.get(username=user.username) 
            serializers = AccountSerializer(account)
            return Response({"data": serializers.data}, status=status.HTTP_200_OK)
        except AccountModel.DoesNotExist:
            return Response({"error": "Account not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    elif request.method == "POST":
        return Response({"message": "POST method is not implemented"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

class AccountViewset(viewsets.ModelViewSet):
    queryset = AccountModel.objects.all()
    serializer_class = AccountSerializer