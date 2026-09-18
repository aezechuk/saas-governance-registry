import os
from app import create_app, db

app = create_app()

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    # Default changed from 5000 to 5001 — macOS's built-in AirPlay
    # Receiver service commonly occupies port 5000, causing
    # "Address already in use" errors. Override with the PORT env
    # var if 5001 is ever unavailable too.
    port = int(os.environ.get("PORT", 5001))
    app.run(debug=True, host="0.0.0.0", port=port)