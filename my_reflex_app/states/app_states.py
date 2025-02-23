import reflex as rx
from my_reflex_app.models.users import User

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
            if user and user.password == self.password:
                self.is_logged_in = True
                self.invalid_credentials = False
                return rx.redirect("/")
            else:
                self.invalid_credentials = True
                self.is_logged_in = False