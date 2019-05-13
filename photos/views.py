from django.http import HttpResponse
from django.shortcuts import render
from photos.models import Photo

# Create your views here.
def home(request):
    photos = Photo.objects.all()
    html = '<ul>'
    for photo in photos:
        html += '<li>'+photo.name+'</li>'
    html += '</ul>'
    return HttpResponse(html)
