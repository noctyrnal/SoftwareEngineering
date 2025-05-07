from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path
from staffscheduling import views

urlpatterns = [
    path("", views.staff_scheduling, {"name": "Guest"}, name="staff_scheduling_default"),
    path("<str:name>/", views.staff_scheduling, name="staff_scheduling"),
]

urlpatterns += staticfiles_urlpatterns()