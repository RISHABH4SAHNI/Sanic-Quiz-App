from passlib.hash import bcrypt
from sanic.response import json

def hash_password(password: str) -> str:
    return bcrypt.hash(password)

def verify_password(password: str, hash_: str) -> bool:
    return bcrypt.verify(password, hash_)

def protected(handler):
    async def wrapper(request, *args, **kwargs):
        session_id = request.headers.get("Authorization")
        if not session_id:
            return json({"error": "Unauthorized"}, status=401)
        user_id = await request.app.ctx.redis.get(f"session:{session_id}")
        if not user_id:
            return json({"error": "Invalid session"}, status=401)
        request.ctx.user_id = int(session_id)
        return await handler(request, *args, **kwargs)
    return wrapper