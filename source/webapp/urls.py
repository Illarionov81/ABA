from django.urls import path, include

from webapp.views.child_test import TestResultView, TestsView
from webapp.views.child import IndexView, ChildDetailView
from webapp.views.program import ProgramDetailView

app_name = 'webapp'


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('test_result/<int:pk>/', TestResultView.as_view(), name='test_result'),
    path('child/', include([
        path('<int:pk>/', include([
            path('', ChildDetailView.as_view(), name='child_view'),
            path('tests/', TestsView.as_view(), name='child_tests'),
            path('program/', ProgramDetailView.as_view(), name='program_detail'),
        ])),
    ])),
]
