from mongoengine import StringField, FloatField, Document, IntField


class Project(Document):
    name = StringField()

class Team(Document):
    name = StringField()
    role = StringField()
    #assignee = StringField()

class Task(Document):
    project_id = StringField()
    name = StringField()
    description = StringField()
    assignee = StringField()


class Employee(Document):
    project_id = StringField()
    name = StringField()
    surname = StringField()
    position = StringField()
    efficiency = StringField()
