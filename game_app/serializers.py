from rest_framework import serializers
from .models import Game

"""
 Serializers allow complex data such as querysets and model instances
 to be converted to native Python datatypes that can then be easily 
 rendered into JSON, XML or other content types. Serializers also provide
  deserialization, allowing parsed data to be converted back into complex
   types, after first validating the incoming data.

 The serializers in REST framework work very similarly to Django's Form
 and ModelForm classes. We provide a Serializer class which gives you a powerful, 
 generic way to control the output of your responses, as well as a ModelSerializer 
 class which provides a useful shortcut for creating serializers 
 that deal with model instances and querysets.

 https://www.django-rest-framework.org/api-guide/serializers/
 
 the Django rest framework serializer is the normal serializer
  that will be used when building an API with Django. It simply
   parses data from complex types into JSON or XML.

The model serializer is just the same as the above serializer
 in the sense that it does the same job, only that it builds the
 serializer based on the model, making the creation of the serializer easier than building it normally.


"""

#GameListSerialzier is serializing games with specified columns.
class GameListSerializer(serializers.ModelSerializer):
    class Meta:
        #wchich model will be serialize. and must be declared in Meta class.
        model = Game
        #fields describes which column of the game model will be serialize.
        fields = ['id', 'result', 'created_at', 'updated_at']

#this serializer class serializes detail of the Game.
class GameDetailSerializer(serializers.ModelSerializer):
    #this field must be same with the user column of the Game model.
    #if whenever we'll create new Game the user field will pass the current user to the user field.
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    class Meta:
        model = Game
        #__all__ keyword passes all ofthe fields of Game model.
        fields = '__all__'
        #https://stackoverflow.com/questions/34989915/write-only-read-only-fields-in-django-rest-framework
        read_only_fields = ['id', 'user', 'result', 'board', 'created_at', 'updated_at']

#this serializer class serializing data when user sends tile square number from the form.
#this serializer inherits from serializer class not from Model serializer class
#A model serializer builds a serializer based on a model(etc. Game model). 
class TileNumberSerializer(serializers.Serializer):
    #receiving the tile number from the endpoint with formdata.
    number = serializers.IntegerField(required=True)
