from poll.models import Question, Choice

from django.contrib.auth import authenticate

from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import exceptions



class ChoiceSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Choice
        fields = ["id", "question", "text",]
        read_only_fields = ('question',)


class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True)
    class Meta:
        model = Question
        fields = ["id", "title", "status", "created_by", "choices" ]

    def create(self, validated_data):
        choices = validated_data.pop("choices")
        question = Question.objects.create(**validated_data)
        for choice in choices:
            Choice.objects.create(**choice, question=question)
        return question

    def update(self, instance, validated_data):
        choices = validated_data.pop("choices")
        instance.title = validated_data.get("title", instance.title)
        instance.save()
        existing_id = [c.id for c in instance.choices]
        keep_choice = []
        for choice in choices:
            if "id" in choice.keys():
                if Choice.objects.filter(id=choice["id"]).exists():
                    c = Choice.objects.get(id=choice["id"])
                    c.text = choice.get("text", c.text)
                    c.save()
                    keep_choice.append(c.id)
                else:
                    continue
            else:
                c = Choice.objects.create(**choice, question=instance)
                keep_choice.append(c.id)
        for choice in instance.choices:
            if choice.id not in keep_choice:
                choice.delete()
        return instance


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username = data.get("username", "")
        password = data.get("password", "")
        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    data["user"] = user
                else:
                    msg = "user is deactivated"
                    raise exceptions.ValidationError(msg)
            else:
                msg = "unable to proceed with the given credentials"
                raise exceptions.ValidationError(msg)
        
        else:
            msg = "please provide both username and password"
            raise exceptions.ValidationError(msg)

        return data