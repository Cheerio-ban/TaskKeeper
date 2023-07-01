from app import app


@app.route('/')
def home():
    return 'Task Keeper'