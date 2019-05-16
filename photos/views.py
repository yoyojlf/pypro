from django.http import HttpResponse
from django.http import response
from django.shortcuts import render
from photos.models import Photo, PUBLIC

# Create your views here.
def home(request):
    photos = Photo.objects.filter(visibility=PUBLIC).order_by('-created_at')
    """
    html = '<ul>'
    for photo in photos:
        html += '<li>'+photo.name+'</li>'
    html += '</ul>'
    """
    context = {
        "photos_list" : photos[:5]
    }
    return render(request,"photos/home.html", context)

def detail(request,pk):
    """
    Carga la página de detalle de una foto
    :param request:
    :param pk:
    :return: HttpResponse
    """
    possible_photos = Photo.objects.filter(pk=pk)
    photo = possible_photos[0] if len(possible_photos) == 1 else None
    if photo is not None:
        #cargamos el detalle
        context = {
            'photo': photo
        }
        return render(request, 'photos/detail.html',context)
    else:
        return response.HttpResponseNotFound('No existe la foto')#error 404