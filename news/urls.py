from django.urls import path
import news.news_api as api

urlpatterns = [
    path('news/', api.NewsList.as_view()),
    path('news/<int:pk>/', api.NewsDetail.as_view()),
    path('feedback/', api.NewsPredictionFeedbackList.as_view()),
    path('feedback/<int:pk>/', api.NewsPredictionFeedbackDetail.as_view()),
]