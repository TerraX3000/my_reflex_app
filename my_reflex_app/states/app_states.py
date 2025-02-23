import reflex as rx
from my_reflex_app.models.users import User
import bcrypt

class UserState(rx.State):
    username: str = ""
    password: str = ""
    is_logged_in: bool = False
    invalid_credentials: bool = False

    @rx.event 
    def login(self):
        self.is_logged_in = True

    
    @rx.event
    def logout(self):
        self.is_logged_in = False
        return rx.redirect("/")

    @rx.event
    def validate_user_credentials(self):
        with rx.session() as session:
            user = session.exec(User.select().where(User.username == self.username)).first()
            print("submitted password", self.password)
            print("enrypted password", user.password)
            if user:
                # is_valid_password = bcrypt.checkpw(self.password.encode('utf-8'), user.password)
                is_valid_password = bcrypt.checkpw(self.password.encode('utf-8'), user.password.encode('utf-8'))
                self.is_logged_in = is_valid_password
                self.invalid_credentials = not is_valid_password
                return rx.redirect("/")
            else:
                self.invalid_credentials = True
                self.is_logged_in = False

    @rx.event
    def create_default_user(self):
        # Check if any users exist
        with rx.session() as session:
            users = session.exec(User.select()).all()
            if users:
                return
            else:
                hashed_password = bcrypt.hashpw("password123".encode('utf-8'), bcrypt.gensalt())
                default_user = User(username="admin", password=hashed_password)
                session.add(default_user)
                session.commit()