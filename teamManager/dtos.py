class TeamDTO(object):

    def __init__(self, team_id, name, role):
        self.team_id = team_id
        self.name = name
        self.role = role

class ProjectDTO(object):

    def __init__(self, project_id, name):
        self.project_id = project_id
        self.name = name

class TaskDTO(object):

    def __init__(self, team_id, name, assignee, description):
        self.team_id = team_id
        self.name = name
        self.assignee = assignee
        self.description = description


class EmployeeDTO(object):

    def __init__(self, employee_id, name, surname, position, efficiency):
        self.employee_id = employee_id
        self.name = name
        self.surname = surname
        self.position = position
        self.efficiency = efficiency
