
from drf_yasg.utils import swagger_auto_schema
from Authentication.docs import schema_example
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from Task.docs import schema_example
from django.contrib.auth import get_user_model


from .models import Task

from .serializers import TaskSerializer, CreateTaskSerializer, UpdateTaskSerializer

from Helpers.response import Response
from Helpers.validators import validate_date




class TaskViewSet(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Create Task",
        operation_summary="Create Task",
        tags=["Task"],
        request_body=CreateTaskSerializer,
        responses=schema_example.TASKS_EXAMPLE,
    )
    def post(self, request):
        serializer = CreateTaskSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        assigned_to_id = serializer.validated_data.get("assigned_to_id")
        assigned_to = None

        if assigned_to_id:
            User = get_user_model()
            assigned_to = User.objects.filter(id=assigned_to).first()
            if not assigned_to:
                return Response(
                    errors={
                        "message": "assigned to user does not exist"
                    },
                    status=status.HTTP_404_NOT_FOUND
                )
        
        serializer.validated_data['created_by'] = request.user
        serializer.validated_data['assigned_to'] = assigned_to
    
        task = Task.objects.create(
            **serializer.validated_data
        )
        return Response(
            data = TaskSerializer(task).data,
            status=status.HTTP_201_CREATED
        )
    
    @swagger_auto_schema(
        operation_description="List Tasks",
        operation_summary="List Tasks",
        tags=["Task"],
        responses=schema_example.TASKS_EXAMPLE,
        manual_parameters=[schema_example.status_param, schema_example.due_date_param, schema_example.search_param],
    )
    def get(self, request):
        task_status = request.GET.get("status")
        due_date_str = request.GET.get("due_date")
        search_value = request.GET.get("search")

        tasks = Task.objects.all().order_by('-created_at')

        if task_status is not None:
            tasks = tasks.filter(status=task_status)

        if due_date_str is not None:
            try:
                due_date = validate_date(due_date_str)
                tasks = tasks.filter(due_date=due_date)
            except ValidationError as e:
                return Response(
                        errors = dict(due_date = str(e)), 
                        status=status.HTTP_400_BAD_REQUEST)
        
        if search_value is not None:
            tasks = tasks.filter(name__icontains=search_value)

        return Response(
            data =dict(tasks = TaskSerializer(tasks, many=True).data),
            status=status.HTTP_200_OK
        )
    


class TaskDetailAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Retrieve a task by ID",
        operation_summary="Get task by ID",
        tags=["Task"],
        responses=schema_example.TASK_EXAMPLE
    )
    def get(self, request, pk):
        try:
            task = Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            return Response(errors={"message":"Task does not exist"},status=status.HTTP_404_NOT_FOUND)
        serializer = TaskSerializer(task)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Update a task by ID",
        operation_summary="Update task by ID",
        tags=["Task"],
        request_body=TaskSerializer,
        responses={200: TaskSerializer}
    )
    def put(self, request, pk):
        try:
            task = Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = UpdateTaskSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Delete a task by ID",
        operation_summary="Delete task by ID",
        tags=["Task"],
        responses={204: 'No Content'}
    )
    def delete(self, request, pk):
        try:
            task = Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            return Response(data={"task": "task does not exist"}, status=status.HTTP_404_NOT_FOUND)
        task.delete()
        return Response(data={
            "task": "task deleted successfully"
        },status=status.HTTP_204_NO_CONTENT)
