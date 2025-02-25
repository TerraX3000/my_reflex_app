import reflex as rx
from my_reflex_app.models.users import User
import bcrypt

class UserState(rx.State):
    username: str = ""
    password: str = ""
    is_logged_in: bool = False
    invalid_credentials: bool = False
    is_default_user_created: bool = False

    @rx.event 
    def login(self):
        self.is_logged_in = True

    
    @rx.event
    def logout(self):
        self.username = ""
        self.password = ""
        self.is_logged_in = False
        return rx.redirect("/")
    
    @rx.event
    def login_on_enter_key(self, value, event: dict):
        if value and value == "Enter" and not any(list(event.values())):
            self.validate_user_credentials()

    @rx.event
    def validate_user_credentials(self):
        if self.username and self.password:
            with rx.session() as session:
                user = session.exec(User.select().where(User.username == self.username)).first()
                if user:
                    is_valid_password = bcrypt.checkpw(self.password.encode('utf-8'), user.password.encode('utf-8'))
                    self.is_logged_in = is_valid_password
                    self.invalid_credentials = not is_valid_password
                    return rx.redirect("/")
        self.invalid_credentials = True
        self.is_logged_in = False
                    

    @rx.event
    def create_default_user(self):
        # Check if any users exist
        with rx.session() as session:
            users = session.exec(User.select()).all()
            if users:
                self.is_default_user_created = False
            else:
                hashed_password = bcrypt.hashpw("password123".encode('utf-8'), bcrypt.gensalt())
                default_user = User(username="admin", password=hashed_password)
                session.add(default_user)
                session.commit()
                self.is_default_user_created = True