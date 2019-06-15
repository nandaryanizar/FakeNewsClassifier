from django.urls import path
import classifier.classifier_api as api

urlpatterns = [
    path('predict/', api.ClassifierList.as_view()),
    path('predict/<int:pk>/', api.ClassifierDetail.as_view()),
]