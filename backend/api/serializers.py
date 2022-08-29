from rest_framework import routers, serializers, viewsets
from .models import *

class ContentSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = Content
    fields = ['id', 'image', 'created_at']

class StyleSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = Style
    fields = ['id', 'image', 'created_at']

class GeneratedSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = Generated
    fields = ['id', 'image', 'created_at']