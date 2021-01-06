from django.urls import path, include

from webapp.views import DoneSelf, DoneWithHint, SessionCloseView, SessionAddGoalView, SessionDataCollectionView
from webapp.views.child import IndexView, ChildDetailView
from webapp.views.child_test import TestResultView, TestsView, ChildTestUpdateView, ChildMakeTestView
from webapp.views.program import ProgramDetailView, ProgramCreateView, UpdateProgram, ProgrmDelete, DeleteGoalView, \
    DeleteCreteriaView, DeleteAddCreteriaView, RemoveProgramView
from webapp.views.session import SessionListView, SessionCreateView, SessionSkillCreateView

app_name = 'webapp'


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('session/done_self/<int:pk>/', DoneSelf.as_view(), name='done_self'),
    path('session/done_with_hint/<int:pk>/', DoneWithHint.as_view(), name='done_with_hint'),
    path('session/<int:pk>/', SessionListView.as_view(), name='session_list'),
    path('session/<int:pk>/close', SessionCloseView.as_view(), name='session_close'),
    path('session/<int:pk>/create', SessionCreateView.as_view(), name='session_create'),
    path('session/<int:pk>/create/skill', SessionSkillCreateView.as_view(), name='session_prepear'),
    path('test_result/<int:pk>/', TestResultView.as_view(), name='test_result'),
    path('update_test/<int:pk>/', ChildTestUpdateView.as_view(), name='child_update_test'),
    path('program/<int:pk>/', ProgramDetailView.as_view(), name='program_detail'),
    path('program/<int:pk>/delete/', ProgrmDelete.as_view(), name='program_delete'),
    path('delete/goal/<int:pk>/', DeleteGoalView.as_view(), name='delete_goal'),
    path('delete/<int:pk>/critaria', DeleteCreteriaView.as_view(), name='delete_creteria'),
    path('delete/<int:pk>/add_critaria', DeleteAddCreteriaView.as_view(), name='delete_add_creteria'),
    path('program/<int:pk>/update/', UpdateProgram.as_view(), name='update_program'),
    path('program/<int:p_pk>/remove/<int:s_pk>/', RemoveProgramView.as_view(), name='update_all_program'),
    path('program/<int:pk>/add-goal/to-level/<int:level>/', SessionAddGoalView.as_view(), name='session_add_goal'),
    path('program/<int:pk>/data-collection/', SessionDataCollectionView.as_view(), name='session_data_collection'),
    path('child/', include([
        path('<int:pk>/', include([
            path('', ChildDetailView.as_view(), name='child_view'),
            path('tests/', TestsView.as_view(), name='child_tests'),
            path('program/create/', ProgramCreateView.as_view(), name='program_create'),
            path('create_test/', ChildMakeTestView.as_view(), name='child_create_test'),
        ])),
    ])),
]
