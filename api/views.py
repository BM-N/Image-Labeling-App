from datetime import timedelta

from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from ml.inference import predict

from .forms import ClassifyImageForm, LoginForm
from .models import Images, Labels
from .serializers import ImagesSerializer, LabelsSerializer, UserSerializer


class RegisterView(CreateView):
    model = User
    template_name = "registration/register.html"
    form_class = UserCreationForm
    success_url = reverse_lazy("user-login")
    
    
class ResultsView(APIView):
    permission_classes = [IsAuthenticated]
    template_name = "api/results.html"
    
    def get(self, request):
        classification_result = request.session.pop('classification_result', None)
        context = {
            'classification_result': classification_result,
            }
        return render(request, context=context, template_name=self.template_name)


class CreateUser(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class LoginUser(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        form = LoginForm()
        context = {"form": form}
        return render(request, "registration/user_login.html", context)

    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token
            redirect_url = reverse("classify-image")
            response = HttpResponseRedirect(redirect_url)
            # Dynamically set secure flag
            is_secure = request.is_secure() 
            response.set_cookie(
                "access_token",
                str(access_token),
                max_age=timedelta(minutes=30).seconds,
                httponly=True,
                samesite='Lax',
                path='/',
                secure=is_secure 
            )
            response.set_cookie(
                "refresh_token",
                str(refresh),
                max_age=timedelta(days=1).seconds,
                httponly=True,
                samesite='Lax',
                path='/',
                secure=is_secure,
            )
            return response
        return Response(
            data={"message": "Invalid credentials, please try again"},
            status=status.HTTP_401_UNAUTHORIZED,
        )


class ImagesList(generics.ListAPIView):
    queryset = Images.objects.all()
    serializer_class = ImagesSerializer
    permission_classes = [AllowAny]


class ImagesRD(generics.RetrieveDestroyAPIView):
    serializer_class = ImagesSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Images.objects.filter(uploaded_by=self.request.user)


class LabelsList(generics.ListAPIView):
    queryset = Labels.objects.all()
    serializer_class = LabelsSerializer
    permission_classes = [AllowAny]
    

class LabelsRD(generics.RetrieveDestroyAPIView):
    queryset = Labels.objects.all()
    serializer_class = LabelsSerializer
    permission_classes = [IsAuthenticated]


class ImageClassificationView(APIView):
    serializer_class = ImagesSerializer
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        form = ClassifyImageForm()
        return render(request, "api/classify_image.html", {"form": form})

    def post(self, request, *args, **kwargs):
        # Getting image from request
        image_file = request.FILES
        form = ClassifyImageForm({}, image_file)

        # form validation
        try:
            if form.is_valid():
                image_field = form.cleaned_data["image"]
        except Exception as e:
            print(f"Error: {e}")

        # image validation
        try:
            image_serializer = ImagesSerializer(
                data={"image": image_field}
            )
            if image_serializer.is_valid(raise_exception=True):
                image_instance = image_serializer.save(uploaded_by=request.user)
            image_path = image_instance.image.path
        except Exception as e:
            raise Exception(f"Error: {e}")    

        # Getting label info
        try:
            predictions = predict(image_path)[0]
            label_serializer = LabelsSerializer(
                data={
                    "label": predictions["label"],
                    "image_id": image_instance.id,
                    "image": image_instance.image.name,
                    "confidence": round(predictions["confidence"], 4),
                }
            )
            label_serializer.is_valid()
            label_serializer.save()
        except Exception:
            return Response(label_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        request.session['classification_result']={
                "image": image_serializer.data,
                "label": label_serializer.data,
            }
        request.session.modified = True
        
        return HttpResponseRedirect(reverse("classify-results"), status=status.HTTP_302_FOUND)
        