from django import forms
from .models import Device

class DeviceForm(forms.ModelForm):
    class Meta:
        model = Device
        fields = ['ip_address', 'hostname', 'serial']
        widgets = {
            'ip_address': forms.TextInput(attrs={'class': 'form-control'}),
            'hostname': forms.TextInput(attrs={'class': 'form-control'}),
            'serial': forms.TextInput(attrs={'class': 'form-control'}),
        }

class DeviceFetchForm(forms.Form):
    ip_address = forms.CharField(
        max_length=15,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    ) 