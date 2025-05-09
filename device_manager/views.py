from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.contrib import messages
import json
import subprocess
import requests
from .models import Device
from .forms import DeviceForm, DeviceFetchForm


class DeviceListView(ListView):
    model = Device
    template_name = 'device_manager/device_list.html'
    context_object_name = 'devices'

class DeviceCreateView(CreateView):
    model = Device
    form_class = DeviceForm
    template_name = 'device_manager/device_form.html'
    success_url = reverse_lazy('device-list')

class DeviceUpdateView(UpdateView):
    model = Device
    form_class = DeviceForm
    template_name = 'device_manager/device_form.html'
    success_url = reverse_lazy('device-list')

class DeviceDeleteView(DeleteView):
    model = Device
    template_name = 'device_manager/device_confirm_delete.html'
    success_url = reverse_lazy('device-list')

def ping_device(request, pk):
    device = get_object_or_404(Device, pk=pk)
    try:
        result = subprocess.run(['ping', '-c', '4', '-t', '5', device.ip_address], 
                              capture_output=True, text=True, timeout=10)
        device.ping_output = result.stdout
        device.ping_status = result.returncode == 0
        device.save()
        
        return JsonResponse({
            'status': 'success',
            'ping_status': device.ping_status,
            'ping_output': device.ping_output
        })
    except subprocess.TimeoutExpired:
        device.ping_status = False
        device.ping_output = "Ping timed out"
        device.save()
        return JsonResponse({
            'status': 'error',
            'message': 'Ping timed out'
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        })

def dashboard_stats(request):
    total_devices = Device.objects.count()
    successful_pings = Device.objects.filter(ping_status=True).count()
    failed_pings = Device.objects.filter(ping_status=False).count()
    
    return JsonResponse({
        'total_devices': total_devices,
        'successful_pings': successful_pings,
        'failed_pings': failed_pings
    })

def fetch_device_data(request):
    if request.method == 'POST':
        form = DeviceFetchForm(request.POST)
        if form.is_valid():
            ip_address = form.cleaned_data['ip_address']
            try:
                response = requests.get(f'https://api.incolumitas.com/?q={ip_address}', timeout=10)
                data = response.json()
                
                device, created = Device.objects.get_or_create(ip_address=ip_address)
                
                device.dc_network = data.get('datacenter', {}).get('network')
                device.asn_network = data.get('asn', {}).get('network')
                device.asn_route = data.get('asn', {}).get('route')
                device.location_latitude = data.get('location', {}).get('latitude')
                device.location_longitude = data.get('location', {}).get('longitude')
                device.save()
                
                messages.success(request, 'Device data fetched successfully!')
            except requests.Timeout:
                messages.error(request, 'API request timed out')
            except requests.RequestException as e:
                messages.error(request, f'Error fetching data: {str(e)}')
            except json.JSONDecodeError:
                messages.error(request, 'Invalid response from API')
            except Exception as e:
                messages.error(request, f'Unexpected error: {str(e)}')
        else:
            messages.error(request, 'Invalid IP address')
    
    return redirect('device-list')
