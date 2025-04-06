from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views
from django.contrib import admin
from .swagger import schema_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('users.urls')),  # Include the users app URLs
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include('savings_group.urls')),  # Your app URLs
    path('api/', include('wallet.urls')),
   #  path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]

