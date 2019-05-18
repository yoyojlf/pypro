# -*- coding: utf-8 -*-
from django import forms
from photos.models import Photo
from photos.settings import BADWORDS
from django.core.exceptions import ValidationError

class PhotoForm(forms.ModelForm):
    """
    formulario para el modelo photo
    """
    class Meta:
        model = Photo
        exclude = ['owner']

    def clean(self):
        """
        Valida si en la descripcion se han puesto malas palabras definidas en settings.BADWORDS
        :return:
        """
        cleaned_data = super(PhotoForm, self).clean()

        description = cleaned_data.get('description', '').lower()

        for badword in BADWORDS:
            if badword.lower() in description:
                raise ValidationError('La palabra {0} no está permitida'.format(badword))

        #si todo va bien devuelvo los datos limpios o normalizados
