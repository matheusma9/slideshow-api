"""slideshowapi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
import content.viewsets as content_viewsets
import tv.viewsets as tv_viewsets
import accounts.viewsets as accounts_viewsets
from django.conf.urls.static import static
from django.conf import settings
import tv.views as tv_views
from rest_framework_swagger.views import get_swagger_view
from accounts.views import LoginView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

schema_view = get_swagger_view(title='SlideShow API')


router = routers.DefaultRouter()
router.register(r'groups', content_viewsets.GroupViewset)
router.register(r'contents', content_viewsets.ContentViewset)
router.register(r'medias', content_viewsets.MediaViewset)
router.register(r'tvs', tv_viewsets.TVViewset)
router.register(r'accounts', accounts_viewsets.UserViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('test/<int:tv>/', tv_views.test, name='test'),
    #path('accounts/', include('accounts.urls')),
    path('doc/', schema_view),
    path('login/', LoginView.as_view(), name='login'),
]
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)