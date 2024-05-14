
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.parsers import MultiPartParser, JSONParser, FileUploadParser, FormParser


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

def schema_for_update(serializer_class=None, **kwargs):
    """
    A decorator for viewset methods that adds swagger_auto_schema with JWT security for update operations.

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
            operation_description=f"Update an existing {model_name} object.",
            request_body=serializer_class,
            responses={
                200: openapi.Response(
                    description="Object updated successfully.",
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
                    description="You are not authorized to update this object.",
                    schema=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            "detail": openapi.Schema(type=openapi.TYPE_STRING)
                        }
                    )
                ),
                404: openapi.Response(
                    description="Object not found.",
                    schema=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            "detail": openapi.Schema(type=openapi.TYPE_STRING)
                        }
                    )
                )
            },
            security=[{"Bearer": []}],  # JWT authentication security scheme
            
        )
        def _wrapper(self, request, *args, **kwargs):
            return func(self, request, *args, **kwargs)

        return _wrapper

    return decorator


    
def schema_for_retrieve(serializer_class=None, **kwargs):
    """
    A decorator for viewset methods that adds swagger_auto_schema with JWT security for retrieval operations.

    Args:
        serializer_class (Optional[Serializer]): The serializer class to use for response schema.
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
            operation_description=f"Retrieve a single {model_name} object.",     
            responses={
                200: openapi.Response(
                    description="Object retrieved successfully.",
                    schema=serializer_class
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
                    description="You are not authorized to view this object.",
                    schema=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            "detail": openapi.Schema(type=openapi.TYPE_STRING)
                        }
                    )
                ),
                404: openapi.Response(
                    description="Object not found.",
                    schema=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            "detail": openapi.Schema(type=openapi.TYPE_STRING)
                        }
                    )
                )
            },
            security=[{"Bearer": []}],  # JWT authentication security scheme
       
        )
        def _wrapper(self, request, *args, **kwargs):
            return func(self, request, *args, **kwargs)

        return _wrapper

    return decorator

def schema_for_destroy(serializer_class=None, **kwargs):
    """
    A decorator for viewset methods that adds swagger_auto_schema with JWT security for destroy operations.

    Args:
        serializer_class (Optional[Serializer]): The serializer class to use (usually not needed for destroy).
        **kwargs (dict): Additional arguments to be passed to swagger_auto_schema.

    Returns:
        callable: The decorated viewset method.
    """

    def decorator(func):
        @swagger_auto_schema(
            operation_description=f"Delete an existing object.",
            responses={
                204: openapi.Response(description="Object deleted successfully."),
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
                    description="You are not authorized to delete this object.",
                    schema=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            "detail": openapi.Schema(type=openapi.TYPE_STRING)
                        }
                    )
                ),
                404: openapi.Response(
                    description="Object not found.",
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
