from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import ShortURL
from .serializers import ShortURLSerializer
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse

def home(request):
    return JsonResponse({
        "message": "Welcome to the URL Shortener API!",
        "endpoints": {
            "POST /shorten": "Create short URL",
            "GET /shorten/<shortcode>": "Retrieve original URL",
            "PUT /shorten/<shortcode>/update": "Update original URL",
            "DELETE /shorten/<shortcode>/delete": "Delete shortened URL"
        }
    })

# Create your views here.

class CreateShortURL(APIView):
    def post(self, request):
        serializer = ShortURLSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RetrieveOriginalURL(APIView):
    def get(self, request, shortcode):
        url = get_object_or_404(ShortURL, shortcode=shortcode)
        url.access_count += 1
        url.save()
        serializer = ShortURLSerializer(url)
        return Response(serializer.data)

class UpdateShortURL(APIView):
    def put(self, request, shortcode):
        url = get_object_or_404(ShortURL, shortcode=shortcode)
        serializer = ShortURLSerializer(url, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def redirect_view(request, shortcode):
    url = get_object_or_404(ShortURL, shortcode=shortcode)
    url.access_count += 1
    url.save()
    return HttpResponseRedirect(url.url)
