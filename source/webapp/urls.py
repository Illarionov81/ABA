from django.urls import path, include
from webapp.views import ChildDetailView
app_name = 'webapp'


urlpatterns = [

    path('child/', include([
        path('<int:pk>/', include([
            path('', ChildDetailView.as_view(), name='child_view'),

        ]))
    ])),
]