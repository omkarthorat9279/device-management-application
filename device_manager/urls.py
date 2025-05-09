from django.urls import path
from . import views

urlpatterns = [
    path('', views.DeviceListView.as_view(), name='device-list'),
    path('create/', views.DeviceCreateView.as_view(), name='device-create'),
    path('update/<int:pk>/', views.DeviceUpdateView.as_view(), name='device-update'),
    path('delete/<int:pk>/', views.DeviceDeleteView.as_view(), name='device-delete'),
    path('ping/<int:pk>/', views.ping_device, name='device-ping'),
    path('dashboard/stats/', views.dashboard_stats, name='dashboard-stats'),
    path('fetch-data/', views.fetch_device_data, name='fetch-device-data'),
] 