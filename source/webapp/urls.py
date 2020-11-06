from django.urls import path, include
from webapp.views import ChildDetailView, ChildTestsView, IndexView

app_name = 'webapp'


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('child/', include([
        path('<int:pk>/', include([
            path('', ChildDetailView.as_view(), name='child_view'),
            path('tests/', ChildTestsView.as_view(), name='child_tests')

        ]))
    ])),
]