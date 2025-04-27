from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("images/", views.ImagesList.as_view(), name="List-of-images"),
    path("image/<int:pk>", views.ImagesRD.as_view(), name = "Retrieve/Delete image"),
    path("labels/", views.LabelsList.as_view(), name="List-of-labels"),
    path("label/<int:pk>", views.LabelsRD.as_view(), name = "Retrieve/Delete label"),
    path("classify/", views.ImageClassificationView.as_view(), name="classify-image"),
    path("classify/results/", views.ResultsView.as_view(), name="classify-results"),
    path("user/login/", views.LoginUser.as_view(), name="user-login"),
    path("user/register/",views.RegisterView.as_view(), name="user_register"),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]