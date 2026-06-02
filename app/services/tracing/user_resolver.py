from sqlalchemy.orm import Session

from app.db.models.user import User


class UserResolver:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_or_create_user(self, email: str) -> User:
        existing_user = self.db.query(User).filter(User.email == email).one_or_none()

        if existing_user is not None:
            return existing_user

        user = User(email=email, role="user")
        self.db.add(user)
        self.db.flush()

        return user
