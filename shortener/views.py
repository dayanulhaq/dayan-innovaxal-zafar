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
        "documentation": {
            "base_url": "http://127.0.0.1:8000",
            "endpoints": [
                {
                    "path": "/",
                    "method": "GET",
                    "description": "API Documentation",
                    "response": "This documentation page"
                },
                {
                    "path": "/shorten",
                    "method": "POST",
                    "description": "Create a new short URL",
                    "request": {
                        "Content-Type": "application/json",
                        "body": {
                            "url": "https://www.example.com/very/long/path"
                        }
                    },
                    "response": {
                        "shortcode": "abc123",
                        "short_url": "http://127.0.0.1:8000/abc123"
                    }
                },
                {
                    "path": "/shorten/<shortcode>",
                    "method": "GET",
                    "description": "Retrieve original URL for a shortcode",
                    "example": "GET /shorten/abc123",
                    "response": "Returns the original URL and usage statistics"
                },
                {
                    "path": "/shorten/<shortcode>/update",
                    "method": "PUT",
                    "description": "Update the original URL for a shortcode",
                    "request": {
                        "Content-Type": "application/json",
                        "body": {
                            "url": "https://www.updated.com"
                        }
                    },
                    "example": "PUT /shorten/abc123/update"
                },
                {
                    "path": "/shorten/<shortcode>/delete",
                    "method": "DELETE",
                    "description": "Delete a short URL",
                    "example": "DELETE /shorten/abc123/delete",
                    "response": "204 No Content on success"
                },
                {
                    "path": "/<shortcode>",
                    "method": "GET",
                    "description": "Redirect to original URL",
                    "example": "GET /abc123",
                    "response": "Redirects to the original URL"
                }
            ],
            "notes": [
                "All endpoints return JSON responses unless specified otherwise",
                "The shortcode is automatically generated if not provided",
                "Shortcodes are case-sensitive",
                "URLs must be properly formatted with http:// or https://"
            ]
        }
    })

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

class DeleteShortURL(APIView):
    def delete(self, request, shortcode):
        url = get_object_or_404(ShortURL, shortcode=shortcode)
        url.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class GetStatistics(APIView):
    def get(self, request, shortcode):
        url = get_object_or_404(ShortURL, shortcode=shortcode)
        serializer = ShortURLSerializer(url)
        return Response(serializer.data)

def redirect_view(request, shortcode):
    url = get_object_or_404(ShortURL, shortcode=shortcode)
    url.access_count += 1
    url.save()
    return HttpResponseRedirect(url.url)
