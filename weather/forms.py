from django import forms

from weather.models import Weather


class WeatherForm(forms.ModelForm):
    """
    Форма для добавления новой погоды.
    """

    class Meta:
        model = Weather
        fields = ('location',)
        widgets = {
            'location': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Введите наименование населенного пункта',
                    'input_type': 'search',
                })}
        labels = {
            'location': ''
        }
