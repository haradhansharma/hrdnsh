
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema



def schema_for_create(serializer_class=None, **kwargs):
    """
    A decorator for viewset methods that adds swagger_auto_schema with JWT security.

    Args:
        serializer_class (Optional[Serializer]): The serializer class to use for request 
                                                 body validation and response schema.
        **kwargs (dict): Additional arguments to be passed to swagger_auto_schema.

    Returns:
        callable: The decorated viewset method.
    """
    
    def decorator(func):
        if serializer_class is not None:
            model_name = serializer_class().Meta.model._meta.verbose_name
        else:
            model_name = ''
        @swagger_auto_schema(
            # operation_summary="Create Site",
            operation_description=f"Create a new {model_name} object.",
            request_body=serializer_class,
            responses={
                201: openapi.Response(
                    description="Site created successfully.",
                    schema=serializer_class
                ),
                400: openapi.Response(
                    description="Bad request. Please check the provided data.",
                    schema=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            "detail": openapi.Schema(type=openapi.TYPE_STRING)
                        }
                    )
                ),
                401: openapi.Response(
                    description="Authentication credentials were not provided or are invalid.",
                    schema=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            "detail": openapi.Schema(type=openapi.TYPE_STRING)
                        }
                    )
                ),
                403: openapi.Response(
                    description="You are not authorized to create sites.",
                    schema=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            "detail": openapi.Schema(type=openapi.TYPE_STRING)
                        }
                    )
                )
            },
            security=[{"Bearer": []}]  # JWT authentication security scheme
            
        )
        def _wrapper(self, request, *args, **kwargs):
            return func(self, request, *args, **kwargs)

        return _wrapper

    return decorator

    
