from django import forms
from .models import RegistroPlanilla
from .calculadora import SMV


class PlanillaForm(forms.ModelForm):
    class Meta:
        model = RegistroPlanilla
        fields = ['empleado', 'periodo', 'sueldo_basico', 'tiene_asignacion_familiar', 'tipo_pension']
        widgets = {
            'periodo': forms.DateInput(attrs={'type': 'month'}, format='%Y-%m'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-check-input'
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs['class'] = 'form-select'
            else:
                field.widget.attrs['class'] = 'form-control'

    def clean_sueldo_basico(self):
        sueldo = self.cleaned_data.get('sueldo_basico')
        if sueldo is None:
            raise forms.ValidationError("El sueldo es obligatorio.")
        if sueldo < SMV:
            raise forms.ValidationError(
                f"El sueldo básico no puede ser menor al Sueldo Mínimo Vital legal (S/ {SMV})."
            )
        return sueldo

    def clean_periodo(self):
        from datetime import date
        periodo = self.cleaned_data.get('periodo')
        if periodo:
            return periodo.replace(day=1)
        return periodo


class CalculadoraRapidaForm(forms.Form):
    sueldo_basico = forms.DecimalField(
        max_digits=10, decimal_places=2,
        min_value=SMV,
        initial='1250.00',
        label='Sueldo Básico (S/)',
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': '1250.00'}),
    )
    tiene_asignacion_familiar = forms.BooleanField(
        required=False,
        label='Tiene Asignación Familiar',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
    )
    tipo_pension = forms.ChoiceField(
        choices=[('ONP', 'ONP (13%)'), ('AFP', 'AFP (~12.82%)')],
        label='Sistema de Pensiones',
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
