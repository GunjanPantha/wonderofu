from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
import views

urlpatterns = [
    path('', views.index, name='index'),
    path('process-input/', views.process_input, name='process_input'),
]

# Serve static files during development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
