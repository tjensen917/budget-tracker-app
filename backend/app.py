from backend import create_app

import os
print("Current Working Directory:", os.getcwd())  # Debugging

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
