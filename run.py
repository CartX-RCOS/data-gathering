from app import create_app

app, mysql = create_app()

if __name__ == "__main__":
    app.run(debug=True, port=3000)