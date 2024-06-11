from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(host="https://surprising-warmth-production.up.railway.app/")
