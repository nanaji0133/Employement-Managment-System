from .models import Question, Choice
from .serializers import QuestionSerializer, LoginSerializer, ChoiceSerializer

from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.contrib.auth import login as app_login, logout as app_logout
from django.http import QueryDict

from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, mixins
from rest_framework.exceptions import ValidationError
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.authtoken.models import Token
from rest_framework import viewsets
from rest_framework.decorators import action


class PollViewSet(viewsets.ModelViewSet):
    serializer_class = QuestionSerializer
    question = Question.objects.all()

    @action(detail=True, methods=["GET"])
    def choices(self,request, id=None):
        question = self.get_object()
        choices = Choice.objects.filter(question=question)
        serializer = ChoiceSerializer(choices, many=True)
        return Response(serializer.data, status=200)

    @action(detail=True, methods=["POST"])
    def choice(self,request, id=None):
        question = self.get_object()
        q_data = request.data
        data = QueryDict('', mutable=True)
        data.update(q_data)
        data["question"] = question.id
        serializer = ChoiceSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

# class PollGeneric(generics.ListAPIView):
#     serializer_class = QuestionSerializer
#     queryset = Question.objects.all()

class PollGenericView(
    generics.GenericAPIView,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
):
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()
    lookup_field = "id"
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]
    # permission_classes_by_action = {'get':[AllowAny],
    #                                 'post':[IsAuthenticated]}

    def get(self, request, id=None):
        if id:
            return self.retrieve(request, id)
        return self.list(request)

    def post(self, request):
        return self.create(request)
        #return super(PollGenericView, self).create(request)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def put(self, request, id):
        return self.update(request, id)

    def perform_update(self, serializer):
        serializer.save(created_by=self.request.user)

    def delete(self, request, id):
        return self.destroy(request, id)

    # def get_permissions(self):
    #     try:
    #         return [permission() for permission in self.permission_classes_by_action[self.action]]
    #     except KeyError:
    #         return [permission() for permission in self.permission_classes]


class PollAPIView(APIView):
    def get(self, request):
        questions = Question.objects.all()
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        if request.method == "POST":
            serializer = QuestionSerializer(data=request.data)
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class PollDetailView(APIView):
    def get_object(self, id):
        return get_object_or_404(Question, pk=id)
        # try:
        #     return Question.objects.get(id=id)
        # except Question.DoesNotExist as e:
        #     return Response({"g;s;kgs;kgs": "sljsl"}, status=404)

    def get(self, request, id=None):
        instance = self.get_object(id)
        serializer = QuestionSerializer(instance)
        return Response(serializer.data, status=200)

    def put(self, request, id):
        data = request.data
        instance = self.get_object(id)
        serializer = QuestionSerializer(instance, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    def delete(self, request, id):
        instance = self.get_object(id)
        instance.delete()
        return HttpResponse(status=204)


@csrf_exempt
def poll(request):
    if request.method == "GET":
        questions = Question.objects.all()
        serializer = QuestionSerializer(questions, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == "POST":
        data = JSONParser().parse(request)
        serializer = QuestionSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def poll_detail(request, id):
    try:
        instance = Question.objects.get(id=id)
    except Question.DoesNotExist as e:
        return JsonResponse({"error": "this is not exis"}, status=404)

    if request.method == "GET":
        serializer = QuestionSerializer(instance)
        return JsonResponse(serializer.data)

    elif request.method == "PUT":
        data = JSONParser().parse(request)
        serializer = QuestionSerializer(instance, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=200)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == "DELETE":
        instance.delete()
        return HttpResponse(status=204)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        app_login(request, user)
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key}, status=200)


class LogoutView(APIView):
    authentication_classes = (TokenAuthentication,)

    def post(self, request):
        app_logout(request)
        return Response(status=204)