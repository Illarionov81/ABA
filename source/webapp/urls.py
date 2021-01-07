from django.urls import path, include

from webapp.views import DoneSelf, DoneWithHint, SessionCloseView, SessionAddGoalView, SessionDataCollectionView
from webapp.views.child import IndexView, ChildDetailView
from webapp.views.child_test import TestResultView, TestsView, ChildTestUpdateView, ChildMakeTestView
from webapp.views.program import ProgramDetailView, ProgramCreateView, UpdateProgram, ProgrmDelete, DeleteGoalView, \
    DeleteCreteriaView, DeleteAddCreteriaView
from webapp.views.session import SessionListView, SessionCreateView, SessionSkillCreateView
from webapp.views.session import SessionListView, SessionCreateView, SessionSkillCreateView, SessionAddSkill, \
    SessionDeleteSkill

app_name = 'webapp'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('test_result/<int:pk>/', TestResultView.as_view(), name='test_result'),
    path('update_test/<int:pk>/', ChildTestUpdateView.as_view(), name='child_update_test'),
    path('program/<int:pk>/', ProgramDetailView.as_view(), name='program_detail'),
    path('program/<int:pk>/delete/', ProgrmDelete.as_view(), name='program_delete'),
    path('delete/goal/<int:pk>/', DeleteGoalView.as_view(), name='delete_goal'),
    path('delete/<int:pk>/critaria', DeleteCreteriaView.as_view(), name='delete_creteria'),
    path('delete/<int:pk>/add_critaria', DeleteAddCreteriaView.as_view(), name='delete_add_creteria'),
    path('program/<int:pk>/update/', UpdateProgram.as_view(), name='update_program'),
    path('program/<int:pk>/add-goal/to-level/<int:level>/', SessionAddGoalView.as_view(), name='session_add_goal'),
    path('program/<int:pk>/data-collection/', SessionDataCollectionView.as_view(), name='session_data_collection'),
    path('session', include([
        path('done_self/<int:pk>/', DoneSelf.as_view(), name='done_self'),
        path('done_with_hint/<int:pk>/', DoneWithHint.as_view(), name='done_with_hint'),
        path('<int:pk>/', include([
            path('', SessionListView.as_view(), name='session_list'),
            path('close', SessionCloseView.as_view(), name='session_close'),
            path('create', SessionCreateView.as_view(), name='session_create'),
            path('create/skill', SessionSkillCreateView.as_view(), name='session_prepear'),
            path('create/skill/add', SessionAddSkill.as_view(), name='add_skill'),
            path('create/skill/delete', SessionDeleteSkill.as_view(), name='delete_skill'),
        ]))
    ])),
    path('child/', include([
        path('<int:pk>/', include([
            path('', ChildDetailView.as_view(), name='child_view'),
            path('tests/', TestsView.as_view(), name='child_tests'),
            path('program/create/', ProgramCreateView.as_view(), name='program_create'),
            path('create_test/', ChildMakeTestView.as_view(), name='child_create_test'),
        ])),
    ])),
]
