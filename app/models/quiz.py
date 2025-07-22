from tortoise import fields, models
from app.models.user import User
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.question import Question
    from app.models.question import Attempt


class Quiz(models.Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(100)
    owner = fields.ForeignKeyField("models.User", related_name="quizzes")
    is_published = fields.BooleanField(default=False)

    questions: fields.ReverseRelation["Question"]
    attempts: fields.ReverseRelation["Attempt"]
