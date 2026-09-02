from app import create_app
from app.extensions import db
from app.models.user import User, UserRole  # Adjust 'UserRole' if your model uses strings or Enums

# Paste your actual Supabase DB string here directly
SUPABASE_DB_URL = "postgresql+psycopg://postgres.ztlytiuiupqytwvzgwxj:a1b2c3d4e5f67890a1b2c3d4e5f67kjhfdkjh8998745iuhrek@aws-1-eu-west-1.pooler.supabase.com:6543/postgres"

app = create_app()
app.config["SQLALCHEMY_DATABASE_URI"] = SUPABASE_DB_URL

with app.app_context():
    # Check if user exists
    existing = db.session.scalar(db.select(User).where(User.email == "gisyncmust@gmail.com"))
    if existing:
        print("User gisyncmust@gmail.com already exists in Supabase!")
    else:
        # Create user
        user = User(email="gisyncmust@gmail.com", role=UserRole.ADMIN, is_active=True)
        user.setPassword("admin@gisyc#hello")  # Hashes password using your model's method
        
        db.session.add(user)
        db.session.commit()
        print("✅ User gisyncmust@gmail.com successfully created in Supabase!")