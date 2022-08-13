from functools import partial
from http import server
from wsgiref.util import request_uri
from xmlrpc.client import ResponseError
from django.shortcuts import render
from rest_framework.views import APIView
# Create your views here.
from rest_framework.permissions import IsAuthenticated, AllowAny
from note.models import MyNotes
from note.serializers import NoteSerializer, RegisterSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from django.contrib.auth.models import User
from django.db.models import F

class RegisterView(APIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer
    def post(self, request, *args, **kwargs):
        request_data = request.data.copy()
        request_data['username'] = request.data.get('email')
        serializer = self.serializer_class(data= request_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)


class NoteView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = NoteSerializer
    def post(self, request):
        request_data = request.data.copy()
        request_data["user"] = request.user.id
        serializer = self.serializer_class(data=request_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        
    def get(self, request):
        qs = MyNotes.objects.all().filter(user=request.user)
        if qs:
            serializer = self.serializer_class(qs, many=True)
            return Response(serializer.data, status = status.HTTP_200_OK)
        else:    
            return Response({"result":"data not found"}, status = status.HTTP_404_NOT_FOUND)

class NoteDetailsView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = NoteSerializer
    def get(self, request, pk):
        obj = MyNotes.objects.filter(user=request.user,pk=pk).first()
        if obj:
            serializer = self.serializer_class(obj)
            return Response(serializer.data, status = status.HTTP_200_OK)
        else:    
            return Response({"result":"data not found"}, status = status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, pk):
        obj = MyNotes.objects.filter(user=request.user,pk=pk).first()
        if obj:
            obj.delete()
            return Response({"result":"data deleted"}, status = status.HTTP_204_NO_CONTENT)
        else:    
            return Response({"result":"data not found"}, status = status.HTTP_404_NOT_FOUND)
    
    def put(self, request, pk):
        obj = MyNotes.objects.filter(user=request.user,pk=pk).first()
        if obj:
            serializer = self.serializer_class(obj, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status = status.HTTP_205_RESET_CONTENT)
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        else:    
            return Response({"result":"data not found"}, status = status.HTTP_404_NOT_FOUND)

        