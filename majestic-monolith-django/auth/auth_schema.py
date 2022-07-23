from drf_spectacular.extensions import OpenApiAuthenticationExtension


class MMDJWTAuthenticationScheme(OpenApiAuthenticationExtension):
    target_class = "core.authentication.MMDJWTAuthentication"
    name = "MMDJWTAuthentication"

    def get_security_definition(self, auto_schema):
        return {
            "type": "http",
            "in": "header",
            "scheme": "bearer",
            "name": "Authorization",
            "description": "JWT authentication with format: `Bearer <token>`",
        }
