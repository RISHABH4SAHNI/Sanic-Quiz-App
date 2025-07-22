from tortoise import fields, models
from app.models.quiz import Quiz

class Question(models.Model):
    id = fields.IntField(pk=True)
    quiz = fields.ForeignKeyField("models.Quiz", related_name="questions")
    text = fields.TextField()
    is_multiple = fields.BooleanField(default=False)

    options: fields.ReverseRelation["Option"]

class Option(models.Model):
    id = fields.IntField(pk=True)
    question = fields.ForeignKeyField("models.Question", related_name="options")
    text = fields.CharField(200)
    is_correct = fields.BooleanField(default=False)

class Attempt(models.Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField("models.User", related_name="attempts")
    quiz = fields.ForeignKeyField("models.Quiz", related_name="attempts")
    score = fields.IntField(default=0)
    answers: fields.ReverseRelation["Answer"]

class Answer(models.Model):
    id = fields.IntField(pk=True)
    attempt = fields.ForeignKeyField("models.Attempt", related_name="answers")
    question = fields.ForeignKeyField("models.Question")
    selected_option_ids = fields.JSONField()
