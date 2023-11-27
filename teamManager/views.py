import base64
import io

import matplotlib.pyplot as plt
import openpyxl
from django.shortcuts import render, redirect

from teamManager.dtos import TeamDTO, TaskDTO, EmployeeDTO, ProjectDTO
from teamManager.forms import TeamForm, TaskForm, EmployeeForm, ProjectForm
from teamManager.models import Team, Task, Employee, Project


# Create your views here.


# Return all teams data

def task_base(request):
    return render(request, "base.html")


def task_list(request):
    teams = list()
    for team in Task.objects():
        teams.append(TaskDTO(team.id.__str__(), team.name, team.assignee, team.description).__dict__)
    return render(request, "task-list.html", {'teams': teams})


def task_create(request, project_id):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            form_data = form.data
            task = Task()
            task.project_id = project_id
            task.name = form_data.get("name")
            task.assignee = form_data.get("assignee")
            task.description = form_data.get("description")
            task.save()
            return redirect('/project-task-list/' + project_id)
    else:
        form = TaskForm()
    return render(request, 'task-create.html', {'form': form, 'project_id': project_id})


def task_update(request, project_id):
    task = Task.objects.get(id=project_id)

    custom_choices = [(obj.id.__str__(), obj.name) for obj in Employee.objects(project_id=task.project_id)]
    #form = TaskForm(name=task.name, custom_choices=custom_choices, description=task.description)
    form = TaskForm(initial={'name': task.name, 'assignee': task.assignee, 'description': task.description})
    #form.fields['assignee'].choices = custom_choices#[(obj.id.__str__(), obj.name) for obj in Employee.objects(project_id=task.project_id)]

    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            form_data = form.data
            task.name = form_data.get("name")
            task.assignee = form_data.get('assignee')
            task.description = form_data.get("description")
            task.save()
            return redirect('/project-task-list/' + task.project_id)
    return render(request, 'task-update.html', {'form': form, 'project_id': task.project_id})


def task_delete(request, team_id):
    team = Task.objects.get(id=team_id)
    key = team.project_id
    team.delete()

    return redirect('/project-task-list/' + key)


SALARY_BORDERS = [1500, 4000]
TENURE_BORDERS = [2, 5]


def project_employee_list(request):
    projects = list()
    for project in Project.objects():
        projects.append(ProjectDTO(project.id.__str__(), project.name).__dict__)
    return render(request, "project-list-employee.html", {'projects': projects})


def project_task_list(request):
    projects = list()
    for project in Project.objects():
        projects.append(ProjectDTO(project.id.__str__(), project.name).__dict__)
    return render(request, "projects-list-task.html", {'projects': projects})


def project_task_view(request, project_id):
    project = Project.objects.get(id=project_id)

    tasks = list()
    for task in Task.objects(project_id=project_id):
        tasks.append(TaskDTO(
            task.id.__str__(),
            task.name,
            task.assignee,
            task.description,
        ).__dict__)

    return render(request, "project-task-view.html",
                  {
                      'tasks': tasks,
                      'project_id': project_id,
                      'team_name': project.name
                  })


def employee_task_view(request, project_id):
    employee = Employee.objects.get(id=project_id)
    project = Project.objects.get(id=employee.project_id)

    tasks = list()
    for task in Task.objects(project_id=employee.project_id):
        if task.assignee == employee.name:
            tasks.append(TaskDTO(
                task.id.__str__(),
                task.name,
                task.assignee,
                task.description,
            ).__dict__)

    return render(request, "employee-task-view.html",
                  {
                      'tasks': tasks,
                      'project_id': project_id,
                      'employee_name': employee.name,
                      'team_name': project.name
                  })


def project_create(request):
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            form_data = form.data
            project = Project()
            project.name = form_data.get("name")
            project.save()
            return redirect('project-list-task')
    else:
        form = ProjectForm()
    return render(request, 'project-create.html', {'form': form})


def project_delete(request, project_id):
    Project.objects.get(id=project_id).delete()
    return redirect('project-list-task')


def task_list(request):
    teams = list()
    for team in Task.objects():
        teams.append(TaskDTO(team.id.__str__(), team.name, team.assignee, team.description).__dict__)
    return render(request, "task-list.html", {'teams': teams})


def task_view(request, team_id):
    task = Task.objects.get(id=team_id)

    quality = 1
    cost = 1
    speed = 1

    employees = list()
    for employee in Employee.objects(team_id=team_id):
        employees.append(EmployeeDTO(
            employee.id.__str__(),
            employee.name,
            employee.surname,
            employee.tenure,
            employee.salary,
        ).__dict__)

        employee_cost = 0
        if employee.salary <= SALARY_BORDERS[0]:
            employee_cost = 1
        elif SALARY_BORDERS[0] < employee.salary < SALARY_BORDERS[1]:
            employee_cost = 2
        elif employee.salary >= SALARY_BORDERS[1]:
            employee_cost = 3

        employee_quality = 0
        if employee.tenure <= TENURE_BORDERS[0]:
            employee_quality = 1
        elif TENURE_BORDERS[0] < employee.tenure < TENURE_BORDERS[1]:
            employee_quality = 2
        elif employee.tenure >= TENURE_BORDERS[1]:
            employee_quality = 3

        cost += employee_cost
        quality += employee_quality

    speed += employees.__len__()
    image = io.BytesIO()
    labels = 'Speed', 'Cost', 'Quality'
    sizes = [speed, cost, quality]

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, shadow=True, startangle=90)
    ax1.axis('equal')
    plt.savefig(image, format='png')
    image.seek(0)
    chart_base64 = base64.b64encode(image.read()).decode("utf-8")

    return render(request, "task-view.html",
                  {
                      'employees': employees,
                      'team_id': team_id,
                      'team_name': task.name,
                      'chart_base64': chart_base64
                  })


def project_employee_view(request, project_id):
    project = Project.objects.get(id=project_id)

    employees = list()
    for employee in Employee.objects(project_id=project_id):
        employees.append(EmployeeDTO(
            employee.id.__str__(),
            employee.name,
            employee.surname,
            employee.position,
            employee.efficiency
        ).__dict__)

    return render(request, "project-employee-view.html",
                  {
                      'employees': employees,
                      'project_id': project_id,
                      'team_name': project.name
                  })


def employee_create(request, project_id):
    if request.method == "POST":
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form_data = form.data
            employee = Employee()
            employee.project_id = project_id
            employee.name = form_data.get("name")
            employee.surname = form_data.get("surname")
            employee.position = form_data.get("position")
            employee.efficiency = form_data.get("efficiency")
            employee.save()
            return redirect('/project-employee-view/' + project_id)
    else:
        form = EmployeeForm()
    return render(request, 'employee-create.html', {'form': form, 'project_id': project_id})


def employee_upload(request, team_id):
    if request.method == "POST":
        employee_list = request.FILES.get("employee_list")
        workbook = openpyxl.load_workbook(employee_list)
        worksheet = workbook["Employees"]

        for row in worksheet.iter_rows(min_row=2, values_only=True):
            employee = Employee()
            employee.team_id = team_id
            employee.name = row[0]
            employee.surname = row[1]
            employee.tenure = row[2]
            employee.salary = row[3]
            employee.save()

    return redirect('/project-employee-view/' + team_id)


def employee_update(request, employee_id):
    employee = Employee.objects.get(id=employee_id)
    form = EmployeeForm(initial={'name': employee.name,
                                 'surname': employee.surname,
                                 'position': employee.position,
                                 'efficiency': employee.efficiency})
    if request.method == "POST":
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form_data = form.data
            employee.name = form_data.get("name")
            employee.surname = form_data.get("surname")
            employee.position = form_data.get("position")
            employee.save()
            return redirect('/project-employee-view/' + employee.project_id)
    return render(request, 'employee-update.html', {'form': form, 'project_id': employee.project_id})


def employee_delete(request, employee_id):
    employee = Employee.objects.get(id=employee_id)
    employee.delete()
    return redirect('/task-view/' + employee.team_id)
