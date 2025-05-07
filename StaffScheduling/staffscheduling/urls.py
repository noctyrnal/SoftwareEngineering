from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path
from staffscheduling import views

urlpatterns = [
    path("", views.staff_scheduling, {"name": "Guest"}, name="scheduling_page"),
    path("time-off/", views.time_off_page, name="time_off_page"),
    path("request-changes/", views.request_changes_page, name="request_changes_page"),
    path("schedule-management/", views.schedule_management_page, name="schedule_management_page"),
]

urlpatterns += staticfiles_urlpatterns()