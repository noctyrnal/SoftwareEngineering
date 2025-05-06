from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # Login/logout/password URLs
    path('accounts/', include('django.contrib.auth.urls')),
    
    # Point-of-Sale app URLs (this makes /order/ work)
    path('', include('pos.urls')),
]
