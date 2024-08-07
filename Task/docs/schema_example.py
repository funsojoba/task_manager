from drf_yasg import openapi


status_param = openapi.Parameter(
    'status',
    openapi.IN_QUERY,
    description="Filter tasks by status",
    type=openapi.TYPE_STRING
)

due_date_param = openapi.Parameter(
    'due_date',
    openapi.IN_QUERY,
    description="Filter tasks by due date (YYYY-MM-DD)",
    type=openapi.TYPE_STRING
)

search_param = openapi.Parameter(
    'search',
    openapi.IN_QUERY,
    description="Search tasks by name",
    type=openapi.TYPE_STRING
)

TASKS_EXAMPLE = {
    200: openapi.Response(
        description="Tasks retrieved successfully",
        examples={
        "application/json": {
            "message": "success",
                "data": {
                    "tasks": [
                        {
                            "id": 5,
                            "created_by": {
                                "id": 1,
                                "username": "James"
                            },
                            "name": "this",
                            "description": "That description",
                            "due_date": "2024-08-03T15:30:00Z",
                            "status": "pending",
                            "created_at": "2024-08-03T18:46:59.043313Z",
                            "updated_at": "2024-08-03T18:46:59.043331Z",
                            "assigned_to": None
                        },
                        {
                            "id": 2,
                            "created_by": {
                                "id": 1,
                                "username": "James"
                            },
                            "name": "this",
                            "description": "That description",
                            "due_date": "2024-08-03T15:30:00Z",
                            "status": "pending",
                            "created_at": "2024-08-03T18:36:30.211556Z",
                            "updated_at": "2024-08-03T18:36:30.211567Z",
                            "assigned_to": None
                        }
                    ]
                },
                "errors": None
        }
    },
    )
}

TASK_EXAMPLE = {
    200: openapi.Response(
        description="Task retrieved successfully",
        examples={
        "application/json": {
            "message": "success",
            "data": {
                "id": 5,
                "created_by": {
                    "id": 1,
                    "username": "James"
                },
                "name": "this",
                "description": "That description",
                "due_date": "2024-08-03T15:30:00Z",
                "status": "pending",
                "created_at": "2024-08-03T18:46:59.043313Z",
                "updated_at": "2024-08-03T18:46:59.043331Z",
                "assigned_to": None
            },
            "errors": None
        }
    },
    )
}