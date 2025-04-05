from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Your API",
        default_version='v1',
        description="Test API documentation",
    ),
    public=True,
    # permission_classes=(permissions.AllowAny,),
    security_definitions={
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header',
            'description': 'JWT token format: Bearer <token>'
        },
    },
)