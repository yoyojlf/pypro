from django.http import HttpResponse
from django.http import response
from django.shortcuts import render
from photos.models import Photo, PUBLIC
from photos.forms import PhotoForm
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.generic import View, ListView
from django.utils.decorators import method_decorator
from django.db.models import Q

# Create your views here.
class PhotosQueryset(object):

    def get_photos_queryset(self,request):
        if not request.user.is_authenticated:
            photos = Photo.objects.filter(visibility=PUBLIC)
        elif request.user.is_superuser:
            photos = Photo.objects.all()
        else:
            photos = Photo.objects.filter(Q(owner=request.user) | Q(visibility=PUBLIC))
        return photos

class HomeView(View):
    def get(self, request):
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

class DetailView(View, PhotosQueryset):
    def get(self,request,pk):
        """
        Carga la página de detalle de una foto
        :param request:
        :param pk:
        :return: HttpResponse
        """
#        possible_photos = Photo.objects.filter(pk=pk).select_related('owner')
        possible_photos = self.get_photos_queryset(request).filter(pk=pk).select_related('owner')
        photo = possible_photos[0] if len(possible_photos) == 1 else None
        if photo is not None:
            #cargamos el detalle
            context = {
                'photo': photo
            }
            return render(request, 'photos/detail.html',context)
        else:
            return response.HttpResponseNotFound('No existe la foto')#error 404

class CreateView(View):

    @method_decorator(login_required())
    def get(self,request):
        """
        esto cmuestra un formulario para crear una foto
        :param request:
        :return:
        """
        form = PhotoForm()
        context = {
            'form': form,
            'success_message': ''
        }
        return render(request, 'photos/new_photo.html', context)

    @method_decorator(login_required())
    def post(self,request):
        """
        esto cmuestra un formulario para crear una foto y la crea
        :param request:
        :return:
        """

        success_message = ''

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

class PhotoListView(View, PhotosQueryset):
    def get(self,request):
        """
        Devuelve:
        - Las fotos publicas si el usuario no está autenticado
        - Las fotos del usuario autenticado o las publicas de otros
        - Si el usuario es superuser, todas la fotos
        :param request:
        :return: HttpResponse
        """
        """
        if not request.user.is_authenticated:
            photos = Photo.objects.filter(visibility=PUBLIC)
        elif request.user.is_superuser:
            photos = Photo.objects.all()
        else:
            photos = Photo.objects.filter(Q(owner=request.user) | Q(visibility=PUBLIC))
        """
        context = {
            'photos': self.get_photos_queryset(request)
        }
        return render(request, 'photos/photos_list.html', context)

class UserPhotosView(ListView):
    model = Photo
    template_name = 'photos/user_photos.html'

    def get_queryset(self):

        queryset = super(UserPhotosView, self).get_queryset()
        return queryset.filter(owner=self.request.user)
