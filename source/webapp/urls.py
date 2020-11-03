from django.urls import path, include
from webapp.views import ChildDetailView, ChildTestsView

app_name = 'webapp'


urlpatterns = [

    path('child/', include([
        path('<int:pk>/', include([
            path('', ChildDetailView.as_view(), name='child_view'),
            path('tests/', ChildTestsView.as_view(), name='child_tests')

        ]))
    ])),
]