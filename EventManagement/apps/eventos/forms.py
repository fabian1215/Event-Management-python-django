from django import forms
from bootstrap_datepicker_plus import DateTimePickerInput
from apps.eventos.models import *
from django.core.exceptions import ValidationError
import datetime

class EventoForm(forms.ModelForm):
    fecha_hora = forms.DateTimeField(
        widget=DateTimePickerInput(format='%d-%m-%Y %H:%M'),
        input_formats = ['%d-%m-%Y %H:%M']
    )
    class Meta:
        model = Evento
        fields = ('nombre_evento', 'lugar_realizacion', 'fecha_hora', 'activo', 'imagen', 'tipo_evento')

    def __init__(self, *args, **kwargs):
        super(EventoForm, self).__init__(*args, **kwargs)
        self.fields['imagen'].required = False

    def clean_fecha_hora(self):
        data = self.cleaned_data.get('fecha_hora', '')
        fecha_aux_str = self.data['fecha_hora']
        fecha_aux = datetime.datetime.strptime(fecha_aux_str, '%d-%m-%Y %H:%M')
        if not fecha_aux > datetime.datetime.now():
            raise ValidationError("La fecha del evento debe ser mayor a la fecha actual")
        return data

class CategoriaTipoEventoForm(forms.ModelForm):
    id_aux = forms.IntegerField(
        widget=forms.HiddenInput(),
        required = False
    )
    class Meta:
        model = CategoriaTipoEvento
        fields = ('nombre', 'sillas_disponibles')

class TipoEventoForm(forms.ModelForm):
    class Meta:
        model = TipoEvento
        fields = ('nombre',)

class CategoriaEventoForm(forms.ModelForm):
    id_aux = forms.IntegerField(
        widget=forms.HiddenInput(),
        required = False
    )
    class Meta:
        model = EventoCategoria
        fields = ('precio', )