
from django import forms
from .models import Aprendiz


class AprendizForm(forms.ModelForm):

    class Meta:
        model = Aprendiz

        fields = [
            'nombre',
            'apellido',
            'tipo_documento',
            'documento',
            'telefono',
            'correo',
            'ficha',
            'programa',
            'direccion',
        ]

        widgets = {
            'direccion': forms.TextInput(attrs={
                'placeholder': 'Ejemplo: Calle 13 # 8-25, Soacha',
                'class': 'form-control'
            })
        }
