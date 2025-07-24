from sanic import Blueprint, Request, response
from app.models.question import Answer, Attempt
from app.models.quiz import Quiz
from app.utils.auth import protected

bp = Blueprint("attempt", url_prefix="/attempt")

@bp.post("/<quiz_id:int>")
@protected
async def attempt_quiz(request: Request, quiz_id: int):
    data = request.json
    user_id = data["user_id"]
    quiz = await Quiz.get(id=quiz_id).prefetch_related("questions__options")
    attempt = await Attempt.create(user_id=user_id, quiz_id=quiz_id)
    score = 0

    for q in quiz.questions:
        ans = data["answers"].get(str(q.id), [])
        correct_ids = [o.id for o in q.options if o.is_correct]
        if set(ans) == set(correct_ids):
            score += 1
        await Answer.create(attempt=attempt, question=q, selected_option_ids=ans)

    attempt.score = score
    await attempt.save()
    return response.json({"score": score})

@bp.get("/my/<user_id:int>")
@protected
async def my_scores(request: Request, user_id: int):
    attempts = await Attempt.filter(user_id=user_id).prefetch_related("quiz")
    return response.json([
        {"quiz": a.quiz.title, "score": a.score} for a in attempts
    ])

@bp.get("/quiz/<quiz_id:int>")
@protected
async def others_scores(request: Request, quiz_id: int):
    attempts = await Attempt.filter(quiz_id=quiz_id).prefetch_related("user")
    return response.json([
        {"user": a.user.username, "score": a.score} for a in attempts
    ])
