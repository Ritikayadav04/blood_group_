from django.shortcuts import render
from django.http import HttpResponse
import os
import cv2
import numpy as np
import tensorflow as tf
from rest_framework.response import Response
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Fingerprint
from .serializers import FingerprintSerializer
import sys

# Load the trained model
model = tf.keras.models.load_model("blood_group_model.h5")

# Define blood group labels
blood_groups = ["A", "B", "AB", "O"]

@api_view(["POST"])
@parser_classes([MultiPartParser, FormParser])
def upload_fingerprint(request):
    """Handles fingerprint image upload and saves it."""
    print("FILES RECEIVED:", request.FILES, file=sys.stderr)  

    if "image" not in request.FILES:
        return Response({"error": "No image uploaded"}, status=400)

    serializer = FingerprintSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    
    return Response(serializer.errors, status=400)

@api_view(["POST"])
@parser_classes([MultiPartParser, FormParser])
def predict_fingerprint(request):
    """Handles fingerprint image upload and predicts blood group."""
    print(f"Request path: {request.path}")  # Log the path to confirm it's hitting the correct view

    if "image" not in request.FILES:
        return Response({"error": "No image uploaded"}, status=400)

    image_file = request.FILES["image"]
    image_path = f"temp/{image_file.name}"
    os.makedirs("temp", exist_ok=True)

    with open(image_path, "wb") as f:
        for chunk in image_file.chunks():
            f.write(chunk)

    # Load and preprocess the image
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        return Response({"error": "Invalid image format"}, status=400)

    image = cv2.resize(image, (128, 128))
    image = image / 255.0
    image = np.expand_dims(image, axis=[0, -1])

    # Make prediction
    prediction = model.predict(image)
    predicted_class = np.argmax(prediction)

    # Clean up temp file
    os.remove(image_path)

    return Response({"blood_group": blood_groups[predicted_class]})




def home(request):
    return HttpResponse("Welcome to the Fingerprint Blood Group Prediction API!")
