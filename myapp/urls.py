from django.urls import path
from . import views
from .views import export_subscriptions_xls
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.home, name='home'),
    path('<int:sub_id>', views.cv_detail, name='cv_detail'),
    path('subscription/', views.subscription, name='subscription'),
    path('subscription/done/', views.subscription_done, name='subscription_done'),
    path('admin/export-subscriptions/', export_subscriptions_xls, name='export_subscriptions_xls'),
    path('register/', views.register_view, name='register_page'),
    path('success/', views.success_view, name='success_page'),
    path('qr-scanner/', views.qr_scanner_view, name='qr_scanner'),
    path('api/check-reg/<int:registration_id>/', views.check_registration_api, name='check_registration_api'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
