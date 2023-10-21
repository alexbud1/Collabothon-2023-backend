from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import User, Participant, Parent, Child, Survey, Mood
import regex as re


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(max_length=68, min_length=6, write_only=True, required=True)

    def validate_password(self, value: str) -> str:
        return make_password(value)

    class Meta:
        model = User
        fields = ["id", "email", "password"]

class ParticipantWriteSerializer(serializers.ModelSerializer):
    age = serializers.IntegerField(min_value=1, max_value=120)
    role = serializers.CharField(max_length=10, required=True)

    class Meta:
        model = Participant
        fields = "__all__"

    def validate(self, data):
        if "role" not in data:
            raise serializers.ValidationError("role is required")
        if data["role"] not in ["parent", "child"]:
            raise serializers.ValidationError("role must be either parent or child")
        if not re.match(r'^[\p{L} -]+$', data['first_name'], re.UNICODE):
            raise serializers.ValidationError("Invalid first name, only letters, spaces and dashes are allowed")
        if not re.match(r'^[\p{L} -]+$', data['last_name'], re.UNICODE):
            raise serializers.ValidationError("Invalid last name, only letters, spaces and dashes are allowed")
        if 'phone' in data:
            if not re.match(r'^\+?[0-9]{9,15}$', data['phone']):
                raise serializers.ValidationError("Invalid phone number, only digits, spaces and dashes are allowed")
        return data

class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = "__all__"

class ParentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parent
        fields = "__all__"

class ChildSerializer(serializers.ModelSerializer):
    class Meta:
        model = Child
        fields = "__all__"

class SurveySerializer(serializers.ModelSerializer):
    class Meta:
        model = Survey
        exclude = ["participant"]

class SurveyWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Survey
        fields = "__all__"

class MoodWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mood
        exclude = ["participant", "date"]

class MoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mood
        fields = "__all__"