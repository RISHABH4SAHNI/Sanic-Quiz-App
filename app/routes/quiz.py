from sanic import Blueprint, Request, response
from app.models.quiz import Quiz
from app.models.user import User
from app.models.question import Question, Option
from app.utils.quiz_formatter import display_quiz

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

@bp.get("/display")
async def display_quizzes(request: Request):
    user_id = request.args.get("user_id")

    if not user_id:
        return response.json({"error": "Missing user_id in query params"}, status=400)

    try:
        user_id = int(user_id)
    except ValueError:
        return response.json({"error": "Invalid user_id"}, status=400)

    quizzes = await Quiz.filter(owner_id=user_id).all()

    return response.json([
        {
            "id": quiz.id,
            "title": quiz.title,
            "is_published": quiz.is_published
        }
        for quiz in quizzes
    ])

@bp.get("/user")
async def user_quiz(request: Request):
    user_id = int(request.args.get("user_id"))
    quizzes = await Quiz.filter(owner_id=user_id).prefetch_related("questions")

    result = [
        {
            "id": quiz.id,
            "title": quiz.title,
        }
        for quiz in quizzes
    ]
    return response.json({"quizzes": result})

@bp.get("/user/<quiz_id:int>")
async def user_quiz_details(request: Request, quiz_id: int):
    user_id = int(request.args.get("user_id"))
    quiz = await Quiz.get_or_none(id=quiz_id, owner_id=user_id).prefetch_related(
        "questions__options", "owner"
    )

    if not quiz:
        return response.json({"error": "Quiz not found"}, status=404)

    return response.json(display_quiz(quiz))
