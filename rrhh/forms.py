from django import forms
from .models import Empleado, Departamento


class EmpleadoForm(forms.ModelForm):
    class Meta:
        model = Empleado
        fields = [
            'nombre', 'apellido', 'cedula', 'fecha_nacimiento', 'genero', 'direccion',
            'cargo', 'departamento', 'fecha_ingreso', 'tipo_contrato', 'salario',
            'estado', 'motivo_salida',
        ]
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'fecha_ingreso': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'direccion': forms.Textarea(attrs={'rows': 2}),
            'motivo_salida': forms.Textarea(attrs={'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
        self.fields['departamento'].widget.attrs['class'] = 'form-select'
        self.fields['genero'].widget.attrs['class'] = 'form-select'
        self.fields['tipo_contrato'].widget.attrs['class'] = 'form-select'
        self.fields['estado'].widget.attrs['class'] = 'form-select'

    def clean_cedula(self):
        cedula = self.cleaned_data.get('cedula', '').strip()
        if not cedula:
            raise forms.ValidationError("La cédula es obligatoria.")
        qs = Empleado.objects.filter(cedula=cedula)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("Ya existe un empleado con esta cédula.")
        return cedula

    def clean_salario(self):
        salario = self.cleaned_data.get('salario')
        if salario is not None and salario < 0:
            raise forms.ValidationError("El salario no puede ser negativo.")
        return salario
