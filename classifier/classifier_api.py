from rest_framework import serializers
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from django.http import Http404, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Classifier
from news.models import News
from news.news_api import NewsSerializer
from classifier.deep_learning.lstm import LSTM

# @csrf_exempt
# def predict(request):
#     if request.method != 'POST':
#         return JsonResponse(request, status=status.HTTP_405_METHOD_NOT_ALLOWED)
#     req_data = JSONParser().parse(request)

#     serializer = NewsSerializer(data=req_data)
#     if serializer.is_valid():
#         news = News.objects.get(content=request.data['content'])
#         if news:
#             return JsonResponse(news, status=status.HTTP_200_OK)
#         serializer.save()
#         return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
#     return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ClassifierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classifier
        fields = ('__all__')

class ClassifierList(APIView):
    permission_classes = (permissions.AllowAny,)
    def get(self, request, format=None):
        classifier = Classifier.objects.all()
        serializer = ClassifierSerializer(classifier, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    def post(self, request, format=None):
        serializer = ClassifierSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ClassifierDetail(APIView):
    permission_classes = (permissions.AllowAny,)
    def get_object(self, pk):
        try:
            return Classifier.objects.get(pk=pk)
        except Classifier.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        classifier = self.get_object(pk)
        serializer = ClassifierSerializer(classifier)
        return Response(serializer.data)    
        
    def post(self, request, format=None):
        news_serializer = NewsSerializer(data=request.data)

        if news_serializer.is_valid():
            news = News.objects.get(content=request.data['content'])
            if news:
                return Response(news, status=status.HTTP_200_OK)
            news_serializer.save()
            train_Y = [request.data['content']]
            train_X = train_Y.copy()
            test_Y = [0]
            test_X = test_Y.copy()
            
            classifier = Classifier.objects.get(pk=1)
            lstm = LSTM(train_X, train_Y, test_X, test_Y, classifier.model_path)
            pred = lstm.predict()
            return Response(pred, status=status.HTTP_201_CREATED)
        return Response(news_serializer.errors, status=status.HTTP_400_BAD_REQUEST)