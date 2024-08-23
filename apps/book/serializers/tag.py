import re

from rest_framework import serializers
from apps.book.models import Tag


class TagSerializer(serializers.ModelSerializer): 
    # TODO: Specify the model that this serializer will link to 
    # TODO: Specify which fields dhould be considered in the model 


    name = serializers.SerializerMethodField()


    def get_name(self, obj):
        return obj.name.capitalize()
    
    def validate_special_characters(self, value): # validate
        """Object-Level Validation"""
        if re.search(r'[%!@#$%^&+*]', value):
            raise serializers.ValidationError("The tag name shouldn't contain special chracters like %!@#$%^&+*")
        return value

    class Meta:
        model = Tag
        fields = '__all__' # ('id', 'name')
        # exclude = ('id') one of the fields you want to exclude. Note: you only can have fields or exlude cannot be both in your Meta class
        read_only_fields = ('id',)
