from tutorial.celery import app


@app.task(queue="lyrics")
def get_lyrics(request_id):
    print(f"Getting lyrics for request ID: {request_id}")
