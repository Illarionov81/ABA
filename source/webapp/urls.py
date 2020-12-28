from django.urls import path, include

from webapp.views.child_test import TestResultView, TestsView, ChildTestUpdateView, ChildMakeTestView
from webapp.views.child import IndexView, ChildDetailView
from webapp.views.program import ProgramDetailView, ProgramCreateView,UpdateProgram, ProgrmDelete
from webapp.views.session import SessionListView, SessionCreateView, SessionSkillCreateView

app_name = 'webapp'


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('test_result/<int:pk>/', TestResultView.as_view(), name='test_result'),
    path('program/<int:pk>/', ProgramDetailView.as_view(), name='program_detail'),
    path('program/<int:pk>/delete/', ProgrmDelete.as_view(), name='program_delete'),
    path('program/<int:pk>/update/', UpdateProgram.as_view(), name='update_program'),
    path('update_test/<int:pk>/', ChildTestUpdateView.as_view(), name='child_update_test'),
    path('session/<int:pk>/', SessionListView.as_view(), name='session_list'),
    path('session/<int:pk>/create', SessionCreateView.as_view(), name='session_create'),
    path('session/<int:pk>/create/skill', SessionSkillCreateView.as_view(), name='session_prepear'),
    path('child/', include([
        path('<int:pk>/', include([
            path('', ChildDetailView.as_view(), name='child_view'),
            path('tests/', TestsView.as_view(), name='child_tests'),
            path('program/create/', ProgramCreateView.as_view(), name='program_create'),
            path('create_test/', ChildMakeTestView.as_view(), name='child_create_test'),
        ])),
    ])),
]
