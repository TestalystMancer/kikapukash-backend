from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Define the schema view for your API documentation
schema_view = get_schema_view(
    openapi.Info(
        title="My API",
        default_version='v1',
        description="My API description",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="Awesome License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,)
)

# JWT Security Definition for Swagger UI (manually define security header)
swagger_security_definition = openapi.Parameter(
    'Authorization',
    openapi.IN_HEADER,
    description='JWT Authorization header using the Bearer scheme. Example: "Bearer <JWT>"',
    type=openapi.TYPE_STRING,
)
