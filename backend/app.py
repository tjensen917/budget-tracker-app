from backend import create_app, db
from flask_migrate import Migrate

# Initialize the app using the factory function
app = create_app()

# Initialize migration support
migrate = Migrate(app, db)

if __name__ == "__main__":
    app.run(debug=True)
