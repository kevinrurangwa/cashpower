from django.http import Http404
from .models import User, Request, Upload, Dispense
from .serializers import UserSerializer, RequestSerializer, UploadSerializer, DispenseSerializer
from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import authenticate, logout
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import make_password
from rest_framework.views import APIView
from django.http import FileResponse, Http404
from django.http import FileResponse, HttpResponse
from django.conf import settings
import os
import requests




@api_view(['GET'])
def test_token(request):
    try:
        Token.objects.get(key=request.data.get('Token'))
        return  Response("Passed!")
    except Token.DoesNotExist:
        return Response("Failed!")

# AdmClientin login
# -----------
@api_view(['POST'])
def login_view(request: Request):
    username = request.data.get('email')
    password = request.data.get('password')
    
    if not username or not password:
        return Response({'detail': 'Username and password are required.'}, status=status.HTTP_400_BAD_REQUEST)
    
    user = authenticate(username=username, password=password)
    
    if user:
        token, created = Token.objects.get_or_create(user=user)
        serializer = UserSerializer(user)
        user_info = {
            "id": serializer.data['id'],
            "username": serializer.data['username'],
            "email": serializer.data['email'],
        }
        return Response({
            "success": "Authenticated successfully",
            "token": token.key,
            "user": user_info,
        }, status=status.HTTP_200_OK)
    
    return Response({"detail": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)


# Admin login
# -----------
@api_view(['POST'])
def admin_login(request):
    username = request.data.get('email')
    password = request.data.get('password')
    
    if not username or not password:
        return Response({'detail': 'Username and password are required.'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Check if the user with given email and user_type exists
    user = User.objects.filter(email=username, user_type="ADM").first()
    if not user:
        return Response({"detail": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)
    
    # Authenticate user
    authenticated_user = authenticate(username=username, password=password)
    if not authenticated_user:
        return Response({"detail": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)
    
    # Generate token
    token, created = Token.objects.get_or_create(user=authenticated_user)
    
    # Serialize user info
    user_info = {
        "id": user.id,
        "username": user.username,
        "email": user.email,
    }
    
    return Response({
        "success": "Authenticated successfully",
        "token": token.key,
        "user": user_info,
    }, status=status.HTTP_200_OK)


# Logout
# ------
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    try:
        request.user.auth_token.delete()
    except (AttributeError, ObjectDoesNotExist):
        return Response({
            "detail": "User does not have an active session."
        }, status=status.HTTP_400_BAD_REQUEST)
    
    request.session.flush()    
    logout(request)
    
    return Response({
        "success": "Logged out successfully",
    }, status=status.HTTP_200_OK)
    

# Get and post all users
# -------------
class GetAllUsers(generics.ListCreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    

# Get specific user
# -----------------
class GetUser(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    lookup_field = 'id'
    
    def get_queryset(self):
        user_id = self.kwargs.get('id')
        if user_id is not None:
            try:
                return User.objects.filter(pk=user_id)
            except User.DoesNotExist:
                raise Http404("User does not exist")
        else:
            return User.objects.none()
        

class ChangePassword(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        old_password = request.data.get('current_password')
        new_password = request.data.get('new_password')

        if not old_password or not new_password:
            return Response({'detail': 'Current password and new password are required'}, status=status.HTTP_400_BAD_REQUEST)

        if not user.check_password(old_password):
            return Response({'detail': 'Invalid current password'}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()
        return Response({'detail': 'Password updated successfully'}, status=status.HTTP_200_OK)


class Dispenses(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DispenseSerializer
    queryset = Dispense.objects.all()

class UserDispenses(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DispenseSerializer

    def get_queryset(self):
        user = self.kwargs['user']

        try:
            queryset = Dispense.objects.filter(user=user)
            return queryset
        except ValueError:
            return Dispense.objects.none()

    
# Get and post Requests
# ---------------------
class RequestsView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RequestSerializer

    def get_queryset(self, *args, **kwargs):
        queryset = Request.objects.all()
        return queryset
    
class NewRequestsView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RequestSerializer

    def get_queryset(self, *args, **kwargs):
        queryset = Request.objects.filter(requested_service='Gusaba cashpower nshya')
        return queryset
    
class ReplaceRequestsView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RequestSerializer

    def get_queryset(self, *args, **kwargs):
        queryset = Request.objects.filter(requested_service='Gusimbuza cashpower')
        return queryset
    
class RepairRequestsView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RequestSerializer

    def get_queryset(self, *args, **kwargs):
        queryset = Request.objects.filter(requested_service='Gusana cashpower')
        return queryset
    
class DisplaceRequestsView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RequestSerializer

    def get_queryset(self, *args, **kwargs):
        queryset = Request.objects.filter(requested_service='Kwimura cashpower')
        return queryset
    
    
class UserRequestsView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RequestSerializer

    def get_queryset(self):
        user = self.kwargs['user']

        try:
            queryset = Request.objects.filter(client=user).order_by('-requested_on')
            return queryset
        except ValueError:
            return Request.objects.none
    
    
# Get, update, and delete single Request
# ------------------
class RequestView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RequestSerializer

    def get_queryset(self):
        req = self.kwargs.get('req')
        
        if req is not None:
            try:
                queryset = Request.objects.filter(pk=req)
                return queryset
            except ValueError:
                return Request.objects.none()
        else:
            return Request.objects.none()

    def get_object(self):
        queryset = self.get_queryset()
        obj = generics.get_object_or_404(queryset)
        return obj
        

class UpdateRequest(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RequestSerializer

    def put(self, request, *args, **kwargs):
        req_id = self.kwargs.get('req')
        decision = request.data.get('decision')
        note = request.data.get('note')

        try:
            request_obj = Request.objects.get(pk=req_id)
        except Request.DoesNotExist:
            return Response({'detail': 'Request not found'}, status=404)

        request_obj.decision = decision 
        request_obj.note = note
        request_obj.save()

        return Response({'detail': 'Request updated successfully'})
    

# Get and post uploads
# --------------------
class UploadsView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UploadSerializer
    
    def get_queryset(self):
        queryset = Upload.objects.all()
        return queryset
    

# Get uploads for a request
# -------------------------
class UploadsByRequestView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UploadSerializer
    
    def get_queryset(self):
        req = self.kwargs.get('req')
        queryset = Upload.objects.filter(request=req)
        
        return queryset

# Get and post dispenses
# ----------------------
class DispensesView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DispenseSerializer
    queryset = Dispense.objects.all()
    

# Get, update, and delete single dispense
# ----------------------------------------
class DispenseView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DispenseSerializer
    
    def get_queryset(self):
        id = self.kwargs.get('id')
        
        if id is not None:
            queryset = Dispense.objects.get(pk=id)
        
        return queryset
    
    
class StatusChange(APIView):
    serializer_class = [IsAuthenticated]
    serializer_class = RequestSerializer

    def put(self, request, *args, **kwargs):
        request_id = kwargs.get('id')
        status = request.data.get('status')

        try:
            request_obj = Request.objects.get(pk=request_id)
        except Request.DoesNotExist:
            return Response({'detail': 'Request not found'}, status=404)

        request_obj.status = status 
        request_obj.save()

        return Response({'detail': 'Request updated successfully'})


    

def download_file(request, file_url):
    try:
        response = requests.get(file_url)
        if response.status_code == 200:
            filename = file_url.split("/")[-1] 
            return HttpResponse(response.content, content_type=response.headers['Content-Type'])
        else:
            return HttpResponse("Failed to download file", status=response.status_code)
    except Exception as e:
        return HttpResponse(str(e), status=500)
    