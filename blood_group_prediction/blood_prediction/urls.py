# blood_prediction/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_fingerprint, name='upload_fingerprint'),
    path('predict/', views.predict_fingerprint, name='predict_fingerprint'),  # Ensure this line is here
]
