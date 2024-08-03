from drf_yasg import openapi


SIGN_UP_EXAMPLE = {
    201: openapi.Response(
        description="User created successfully",
        examples={
            "application/json": {
                "message": "success",
                "data": {
                    "username": "HugoCon",
                    "email": "hugo_con@gmail.com"
                },
                "errors": None
            }
        },
    ),
    400: openapi.Response(
        description="Bad Request",
        examples={
            "application/json": {
                "username": ["This field is required."],
                "email": ["This field must be a valid email address."],
                "password": ["This field is required."],
            }
        },
    ),
}


LOGIN_EXAMPLE = {
    200: openapi.Response(
        description="User login successfully",
        examples={
            "application/json": {
                "message": "success",
                "data": {
                    "token": {
                        "refresh": "refresh token example ...",
                        "access": "access token example ..."
                    }
                },
                "errors": None
            }
        },
    ),
    400: openapi.Response(
        description="User login successfully",
        examples={
            "application/json": {
                "message": "success",
                "data": {
                    "non_field_errors": [
                        "Invalid login credentials."
                    ]
                },
                "errors": None
            }
        },
    ),
}