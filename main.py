from sanic import Sanic, response
from config.settings import TORTOISE_ORM, init_redis 
from tortoise.contrib.sanic import register_tortoise
from app.routes import auth, quiz, attempt

from dotenv import load_dotenv
load_dotenv()

app = Sanic("QuizApp")

@app.get("/")
async def home(request):
    return response.text("Sanic Quiz App is running")

@app.before_server_start
async def setup_redis(app, _):
    app.ctx.redis = await init_redis()
    print("redis connected")

app.blueprint(auth.bp)
app.blueprint(quiz.bp)
app.blueprint(attempt.bp)

register_tortoise(
    app,
    config=TORTOISE_ORM,
    generate_schemas=True,
)

if __name__ == "__main__":
    app.run(host="localhost", port=8000, debug=True)
