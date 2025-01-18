# run.py
from flask import Flask
from app.routes import register_routes

app = Flask(__name__)

# Registre as rotas
register_routes(app)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
