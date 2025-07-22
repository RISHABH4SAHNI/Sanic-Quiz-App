from sanic import Blueprint, Request, response
from app.models.quiz import Quiz
from app.models.user import User
from app.models.question import Question, Option

bp = Blueprint("quiz", url_prefix="/quiz")

@bp.post("/create")
async def create_quiz(request: Request):
    data = request.json
    user_id = int(data["user_id"])
    quiz = await Quiz.create(title=data["title"], owner_id=user_id)
    return response.json({"quiz_id": quiz.id})

@bp.post("/<quiz_id:int>/add_question")
async def add_question(request: Request, quiz_id: int):
    data = request.json
    q = await Question.create(
        quiz_id=quiz_id,
        text=data["text"],
        is_multiple=data.get("is_multiple", False)
    )
    for opt in data["options"]:
        await Option.create(
            question=q, text=opt["text"], is_correct=opt["is_correct"]
        )
    return response.json({"msg": "question added"})

@bp.post("/<quiz_id:int>/publish")
async def publish_quiz(request: Request, quiz_id: int):
    quiz = await Quiz.get(id=quiz_id)
    quiz.is_published = True
    await quiz.save()
    return response.json({"msg": "published"})

@bp.delete("/<quiz_id:int>")
async def delete_quiz(request: Request, quiz_id: int):
    await Quiz.filter(id=quiz_id).delete()
    return response.json({"msg": "deleted"})
