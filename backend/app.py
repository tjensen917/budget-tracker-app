from backend import create_app, db  # Correct import

# Initialize the app using the factory function
app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
