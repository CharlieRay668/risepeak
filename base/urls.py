from django.urls import path
from . import views

urlpatterns = [
    path("", views.alone, name="alone"),
    path("home/", views.base, name="home"),
    path("staff/", views.staff_only, name="staff_only"),
    path("student/<str:student_name>/", views.student, name="student"),
    path("staff/<str:staff_pass>/", views.staff, name="staff")
]


