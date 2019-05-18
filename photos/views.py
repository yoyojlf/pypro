from django.http import HttpResponse
from django.http import response
from django.shortcuts import render
from photos.models import Photo, PUBLIC
from photos.forms import PhotoForm
from django.urls import reverse
from django.contrib.auth.decorators import login_required

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
    possible_photos = Photo.objects.filter(pk=pk).select_related('owner')
    photo = possible_photos[0] if len(possible_photos) == 1 else None
    if photo is not None:
        #cargamos el detalle
        context = {
            'photo': photo
        }
        return render(request, 'photos/detail.html',context)
    else:
        return response.HttpResponseNotFound('No existe la foto')#error 404

@login_required()
def create(request):
    """
    esto cmuestra un formulario para crear una foto y la crea si la peticion es post
    :param request:
    :return:
    """

    success_message = ''
    if request.method == 'GET':
        form = PhotoForm()
    else:
        photo_with_owner = Photo()
        photo_with_owner.owner = request.user #asigno como propietario
        form = PhotoForm(request.POST, instance=photo_with_owner)
        if form.is_valid():
            new_photo = form.save()
            #form = PhotoForm()
            success_message = 'Foto guardada con éxito'
            success_message += '<a href="{0}">'.format(reverse('photo_detail', args=[new_photo.pk]))
            success_message += 'Ver foto'
            success_message += '</a>'
    context = {
        'form': form,
        'success_message': success_message
    }
    return render(request, 'photos/new_photo.html', context)

