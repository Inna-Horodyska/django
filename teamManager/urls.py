from django.urls import path

from . import views

urlpatterns = [
    path('', views.task_base, name='base'),
    path('project-list-task', views.project_task_list, name='project-list-task'),
    path('project-list-employee', views.project_employee_list, name='project-list-employee'),

    path('project-create', views.project_create, name='project-create'),
    path('project-delete/<str:project_id>', views.project_delete, name='project-delete'),

    # path('task-list', views.task_list, name='task-list'),
    path('project-task-list/<str:project_id>', views.project_task_view, name='project-task-list'),

    path('project-employee-view/<str:project_id>', views.project_employee_view, name='project-task-list'),

    path('task-create/<str:project_id>', views.task_create, name='task-create'),
    path('task-update/<str:project_id>', views.task_update, name='task-update'),
    path('task-delete/<str:team_id>', views.task_delete, name='task-delete'),

    path('task-view/<str:team_id>', views.task_view, name='task-view'),
    path('employee-create/<str:project_id>', views.employee_create, name='employee-create'),
    path('employee-upload/<str:team_id>', views.employee_upload, name='employee-upload'),
    path('employee-update/<str:employee_id>', views.employee_update, name='employee-update'),
    path('employee-delete/<str:employee_id>', views.employee_delete, name='employee-delete'),

    path('employee-task-view/<project_id>', views.employee_task_view, name='employee-task-view')
]
