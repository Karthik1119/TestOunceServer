from django.shortcuts import render
from rest_framework import generics,mixins

# Create your views here.
from blog.models import Blog
from blog.serializers.blogSerializer import BlogSerializer


class BlogView(generics.ListAPIView,
               generics.CreateAPIView,
               generics.UpdateAPIView,
               generics.DestroyAPIView):

    def get_serializer_class(self):
        return BlogSerializer

    def get_queryset(self,request):
        """
        you can do additional level testing to give refined queryset here
        """

