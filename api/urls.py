from django.conf.urls import url, include
from django.conf import settings

from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter, SimpleRouter

from . import views

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register(r'reviewer', views.ReviewerViewSet, base_name='reviewer')
router.register(r'review', views.ReviewViewSet, base_name='review')
router.register(r'company', views.CompanyViewSet, base_name='company')

urlpatterns = [
    url(r'^docs/', include_docs_urls(title='api',
                                     authentication_classes=[],
                                     permission_classes=[])),
    url(r'^', include(router.urls)),
    url(r'^auth/', include('djoser.urls')),
    url(r'^auth/', include('djoser.urls.jwt')),
]
