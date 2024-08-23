from rest_framework import serializers
from apps.book.models import Author


class AuthorSerializer(serializers.ModelSerializer): 
    # TODO: Specify the model that this serializer will link to 
    # TODO: Specify which fields dhould be considered in the model 

    # Force django REST to recognize the method
    name = serializers.CharField(read_only=True) # by the default read-only
    # Create a serialized method
    username = serializers.SerializerMethodField()

    # Serialized method's implemetation
    def get_username(self,obj): # get <serializer_method_field>
        return '_'.join([obj.first_name, obj.last_name])

    def validate_first_name(self, value):
        """Field-Level Validation"""
        if '-' in value:
            # TODO: Always raise a validation exception when condition fials
            raise serializers.ValidationError('first name should not contain hyphen (-)')
        # TODO: Always raise a validation exception when condition fials
        return value
    
    def validate(self, attrs): # validate
        """Object-Level Validation"""
        if attrs.get('first_name') == attrs.get('last_name'):
            raise serializers.ValidationError('first name and last name should not be the same')
        
        return attrs
        

    class Meta:
        model = Author
        fields = '__all__' # ('id', 'first_name', 'last_name')
        read_only_fields = ('id',)