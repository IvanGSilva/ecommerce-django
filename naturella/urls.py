from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('store.urls'))
]

#configurando a url das imagens dos produtos
#a imagem é randerizada e depois é aberta no bloco de produtos
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)