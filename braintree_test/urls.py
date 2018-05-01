from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from merchant.views import MerchantViewSet

router = DefaultRouter()

router.register('merchant', MerchantViewSet, base_name='merchant')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('admin/', admin.site.urls),
]
