from tortoise import fields, models
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.quiz import Quiz
    from app.models.question import Attempt


class User(models.Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(50, unique=True)
    password_hash = fields.CharField(100)

    quizzes: fields.ReverseRelation["Quiz"]
    attempts: fields.ReverseRelation["Attempt"]
