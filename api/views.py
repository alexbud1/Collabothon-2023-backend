from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import action, parser_classes
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework import viewsets, permissions, status, views, mixins
from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView
from django_filters.rest_framework import DjangoFilterBackend
from django.db import transaction
from rest_framework.decorators import action, parser_classes
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import re 
from .utils import(
    serializer_create,
)
from .models import (
    User,
    Participant,
    Survey, 
    Mood
)
from .serializers import (
    UserSerializer,
    ParticipantWriteSerializer,
    ParentSerializer,
    ChildSerializer,
    ParticipantSerializer,
    SurveySerializer,
    SurveyWriteSerializer,
    MoodSerializer,
    MoodWriteSerializer
)
from .ChatbotWithMemory import ChatbotWithHistory
from .vecdb import Embedder
from .mongo import get_history, add_answer, add_prompt


class SignUpViewSet(viewsets.ViewSet):
    """
    ViewSet which is responsible for a sign up process using credentials
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        request_body=UserSerializer,  # Use your UserSerializer as the request body
        responses={status.HTTP_201_CREATED: UserSerializer()},
        operation_description="Create a new user",
    )
    def create(self, request):
        """
        Sign-up route by email and password. 
        User is created as the result.
        """
        if "email" in request.data and "password" in request.data:
            user_data = {
                'email' : request.data['email'],
                'password': request.data['password'],
                'is_active': False
            }
            if len(user_data['password']) < 8 and (not re.match("^[a-zA-Z]+[0-9]+$",user_data['password'])):
                return Response('Password should contain at least 8 characters with letters and digits', status=status.HTTP_400_BAD_REQUEST)
            
            try:


                user = serializer_create(UserSerializer, data = user_data)
                request.data['user'] = user['id']
                
            except Exception as e:
                return Response(str(e),  status = status.HTTP_400_BAD_REQUEST)
            
            return Response(data = user,  status = status.HTTP_201_CREATED)
        else:
            return Response("email and password are required fields",status = status.HTTP_400_BAD_REQUEST)


class PersonalInfoViewSet(viewsets.ViewSet):
    """
    ViewSet which is responsible for a personal info of a user. 

    You can use it for creating, updating and retrieving personal info of a user.
    """
    queryset = Participant.objects.all()
    serializer_class = ParticipantWriteSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'post', 'patch']

    @swagger_auto_schema(
        request_body=ParticipantWriteSerializer,  # Use your UserSerializer as the request body
        responses={status.HTTP_201_CREATED: ParticipantWriteSerializer()},
        operation_description="Create a new personal info",
    )
    def create(self, request):
        """
        Create a new personal info.
        """
        if "first_name" in request.data and "last_name" in request.data and "age" in request.data and "role" in request.data:
            request.data['user'] = request.user.id
            participant = serializer_create(ParticipantWriteSerializer, data = request.data)
            if request.data['role'] == 'parent':
                parent = serializer_create(ParentSerializer, data = request.data)
            elif request.data['role'] == 'child':
                child = serializer_create(ChildSerializer, data = request.data)
            return Response(data = participant,  status = status.HTTP_201_CREATED)
        else:
            return Response("first_name, last_name, role and age are required fields",status = status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        responses={status.HTTP_200_OK: ParticipantSerializer()},
        operation_description="Get personal info for the authenticated user.",
    )
    def list(self, request):
        """
        Get personal info for the authenticated user.
        """
        try:
            participant = Participant.objects.get(user=request.user)
            serializer = ParticipantSerializer(participant)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except Participant.DoesNotExist:
            return Response("Personal info not found", status=status.HTTP_404_NOT_FOUND)

class SurveyViewSet(viewsets.ViewSet):
    """
    ViewSet which is responsible for a survey of a user. 

    You can use it for creating survey of a user just after registration.
    """
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['post']

    @swagger_auto_schema(
        request_body=SurveySerializer,  # Use your UserSerializer as the request body
        responses={status.HTTP_201_CREATED: SurveyWriteSerializer()},
        operation_description="Create a new survey",
    )
    def create(self, request):
        """
        Create a new survey.
        """
        participant_id = Participant.objects.get(user=request.user.id).id
        print(participant_id)
        request.data['participant'] = participant_id
        survey = serializer_create(SurveyWriteSerializer, data = request.data)
        return Response(data = survey,  status = status.HTTP_201_CREATED)
    
class MessageViewSet(viewsets.ViewSet):
    """
    ViewSet which is responsible for a message of a user. 

    You can use it for creating message from a user and get response from a bot as a response.
    """
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['post']

    @swagger_auto_schema(
        responses={status.HTTP_200_OK: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'message': openapi.Schema(type=openapi.TYPE_STRING, description='Message from a bot'),
            },
        )},
        operation_description="Send message to a bot and get response from it.",
    )
    def create(self, request):
        if "message" not in request.data:
            return Response("message is a required field",status = status.HTTP_400_BAD_REQUEST)
        
        # TO DO -> call ml_model.py here
        chatbot = ChatbotWithHistory()
        embedder = Embedder()
        participant_id = Participant.objects.get(user=request.user.id).id
        dict_to_send = {
            "new_prompt" : {
                "prompt" : request.data['message'],
                "vectorized_prompt" : embedder.get_embedding(request.data['message'])
            },
            "history" : get_history(participant_id)
        }
        print(dict_to_send)
        answer = chatbot.get_response(dict_to_send)
        answer = answer['text']
        print(f"Answer: {answer}")
        answer_id = add_answer(participant_id, answer)
        print(f"Answer id: {answer_id}")
        add_prompt(participant_id, request.data['message'], embedder.get_embedding(request.data['message']), answer_id)
        return Response(data={'message': answer}, status=status.HTTP_200_OK)

class MoodViewSet(viewsets.ViewSet):
    """
    ViewSet which is responsible for a mood of a user. 

    You can use it for creating mood of a user.
    """
    queryset = Mood.objects.all()
    serializer_class = MoodSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['post']

    @swagger_auto_schema(
        request_body=MoodWriteSerializer,  # Use your UserSerializer as the request body
        responses={status.HTTP_201_CREATED: MoodSerializer()},
        operation_description="Create a new mood",
    )
    def create(self, request):
        """
        Create a new mood.
        """
        participant_id = Participant.objects.get(user=request.user.id).id
        request.data['participant'] = participant_id
        mood = serializer_create(MoodSerializer, data = request.data)
        return Response(data = mood,  status = status.HTTP_201_CREATED)