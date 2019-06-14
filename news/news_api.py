from rest_framework import serializers
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from django.http import Http404
from .models import News, NewsPredictionFeedback
from oauth2_provider.models import Application

class NewsPredictionFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsPredictionFeedback
        fields = ('__all__')

class NewsSerializer(serializers.ModelSerializer):
    prediction_feedbacks = NewsPredictionFeedbackSerializer(many=True, read_only=True)
    class Meta:
        model = News
        fields = ('__all__')

class ApplicationSerializer(serializers.ModelSerializer):
    prediction_feedbacks = NewsPredictionFeedbackSerializer(many=True, read_only=True)
    class Meta:
        model = Application
        fields = ('__all__')

class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer

class NewsPredictionFeedbackViewSet(viewsets.ModelViewSet):
    queryset = NewsPredictionFeedback.objects.all()
    serializer_class = NewsPredictionFeedbackSerializer

class NewsList(APIView):
    permission_classes = (permissions.AllowAny,)
    def get(self, request, format=None):
        news = News.objects.all()
        serializer = NewsSerializer(news, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = NewsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class NewsDetail(APIView):
    permission_classes = (permissions.AllowAny,)
    def get_object(self, pk):
        try:
            return News.objects.get(pk=pk)
        except News.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        news = self.get_object(pk)
        serializer = NewsSerializer(news)
        return Response(serializer.data)

    def patch(self, request, pk, format=None):
        news = self.get_object(pk)
        serializer = NewsSerializer(news, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        news = self.get_object(pk)
        news.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class NewsPredictionFeedbackList(APIView):
    permission_classes = (permissions.AllowAny,)
    def get(self, request, format=None):
        news_prediction_feedback = NewsPredictionFeedback.objects.all()
        serializer = NewsPredictionFeedbackSerializer(news_prediction_feedback, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = NewsPredictionFeedbackSerializer(data=request.data)
        if serializer.is_valid():
            news = News.objects.get(pk=request.data['news'])
            if request.data['is_fake_news']:
                news.total_is_fake_feedback += 1
            else:
                news.total_is_not_fake_feedback += 1

            if news.total_is_fake_feedback < news.total_is_not_fake_feedback:
                news.is_fake_news = False
            elif news.total_is_fake_feedback > news.total_is_not_fake_feedback:
                news.is_fake_news = True
            
            news.save()
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class NewsPredictionFeedbackDetail(APIView):
    permission_classes = (permissions.AllowAny,)
    def get_object(self, pk):
        try:
            return NewsPredictionFeedback.objects.get(pk=pk)
        except NewsPredictionFeedback.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        news_prediction_feedbacks = self.get_object(pk)
        serializer = NewsPredictionFeedbackSerializer(news_prediction_feedbacks)
        return Response(serializer.data)

    def patch(self, request, pk, format=None):
        news_prediction_feedbacks = self.get_object(pk)
        serializer = NewsPredictionFeedbackSerializer(news_prediction_feedbacks, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        news_prediction_feedbacks = self.get_object(pk)
        news_prediction_feedbacks.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)