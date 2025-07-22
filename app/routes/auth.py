from sanic import Blueprint, Request, HTTPResponse, response
from app.models.user import User
from app.utils.auth import hash_password, verify_password

bp = Blueprint("auth", url_prefix="/auth")

@bp.post("/register")
async def register(request: Request) -> HTTPResponse:
    data = request.json
    user = await User.create(username=data["username"], password_hash=hash_password(data["password"]))
    return response.json({"msg": "registered", "id": user.id})

@bp.post("/login")
async def login(request: Request) -> HTTPResponse:
    data = request.json
    user = await User.get_or_none(username=data["username"])
    if not user or not verify_password(data["password"], user.password_hash):
        return response.json({"msg": "invalid"}, status=401)
    
    await request.app.ctx.redis.set(f"session:{user.id}", "1")
    return response.json({"msg": "logged in", "user_id": user.id})
