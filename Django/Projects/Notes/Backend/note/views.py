from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets, response, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.pagination import PageNumberPagination

from note.serializer import NoteSerializer
from note.models import Note

def home_note(self,request):
    return render(request, 'base.html')

class NotePagination(PageNumberPagination):
    page_size = 4
    page_query_param = 'pagenum'
    page_size_query_param = 'pagelen'
    max_page_size = 50

    def get_paginated_response(self, data):
        msg = getattr(self,"pagination_message", "Success")
        return response.Response(data={
            "data":data,
            "meta":{
                "count": self.page.paginator.count,
                "next": self.get_next_link(),
                "prev": self.get_previous_link()
            },
            "message": msg
        },status=status.HTTP_200_OK)

# Create your views here.
class NoteViewSet(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Note.objects.filter(is_active=True).order_by('-id')
    serializer_class = NoteSerializer
    pagination_class = NotePagination

    def get_queryset(self):
        if self.request.user.is_superuser:
            return self.queryset
        return self.queryset.filter(author=self.request.user)
    
    def perform_update(self, serializer):
        serializer.save(is_active=False)
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def create_note(self,request):
        # if request.user:
        req_data = request.data
        # req_data["created_date"] = datetime.now()
        # create_query = self.get_queryset()
        # if create_query.filter(title__icontains = req_data.get('title')).exists():
        #     return response.Response(data={
        #         "data":[],
        #         "message":"Already similar title post exists"}, status=status.HTTP_400_BAD_REQUEST)
        post_serialize = self.get_serializer(data=req_data)
        if post_serialize.is_valid():
            self.perform_create(post_serialize)
            # post_serialize.save(author=request.user)
            return response.Response(data={
                "data": post_serialize.data,
                "message": "Note Created"
                },
                status=status.HTTP_201_CREATED
            )
        return response.Response(
            {
                "data": post_serialize.errors,
                "message": "Not Created"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        # return HttpResponse("Create note")


    def list_note(self,request):
        title = request.GET.get("title")
        note_id = int(request.GET.get("note_id", 0))
        is_completed = request.query_params.get("is_completed")
        compelted = False
        if is_completed:
            compelted = is_completed.lower() == "true"
        # compelted = request.GET.get("is_completed", False) in {"true", True}
        queryset = self.get_queryset()
        if note_id:
            queryset = queryset.filter(id=note_id)
        if title:
            queryset = queryset.filter(title__icontains=title)
        if compelted:
            queryset = queryset.filter(is_completed=compelted)
        page_data = self.paginate_queryset(queryset=queryset)
        req_data = self.get_serializer(page_data, many=True)
        self.paginator.pagination_message = "Note list Fetched"
        return self.get_paginated_response(req_data.data)


    def delete_note(self,request, pk=None):
        note_data = self.get_object()
        if note_data:
            # self.perform_update(note_data)
            note_data.is_active = False
            note_data.save(update_fields=['is_active'])
            return response.Response({
                "data": [],
                "message": "Deleted Success"
            }, status=status.HTTP_200_OK)
        return response.Response({
            "data": [],
            "message": "No Note Found!!"
        }, status=status.HTTP_400_BAD_REQUEST)


    def edit_note(self,request, pk=None):
        note_data = self.get_object()
        if note_data:
            # note_data.update(**data)
            req_data = self.get_serializer(note_data, data=request.data, partial=True)
            if req_data.is_valid():
                req_data.save()
                return response.Response({
                    "data": req_data.data,
                    "message": "Data is updated"
                }, status=status.HTTP_200_OK)
        return response.Response({
            "data": [],
            "message": "No Note Found!"
        }, status=status.HTTP_400_BAD_REQUEST)