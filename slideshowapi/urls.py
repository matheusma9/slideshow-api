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
    path('doc/', schema_view),
    path('login/', LoginView.as_view(), name='login'),
]
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)