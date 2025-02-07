import reflex as rx
from my_reflex_app.components.navbar import navbar
from my_reflex_app.models.users import User
from my_reflex_app.models.models import Transaction


class ResetState(rx.State):

    @rx.event
    def reset_transactions(self):
        with rx.session() as session:
            session.query(Transaction).delete()
            session.commit()

class FormState(rx.State):
    form_data: dict = {}

    @rx.event
    def handle_submit(self, form_data: dict):
        """Handle the form submit."""
        self.form_data = form_data
        with rx.session() as session:
            user = User(
                username=self.form_data["username"],
                password=self.form_data["password"],
            )
            session.add(user)
            session.commit()


def add_user_form():
    return rx.vstack(
        rx.form(
            rx.vstack(
                rx.text("Username"),
                rx.input(
                    name="username",
                ),
                rx.text("Password"),
                rx.input(type="password", name="password"),
                rx.button("Submit", type="submit"),
            ),
            on_submit=FormState.handle_submit,
            reset_on_submit=True,
        ),
        rx.divider(),
        rx.heading("Results"),
        rx.text(FormState.form_data.to_string()),
    )




@rx.page(route="/admin")
def admin():
    return rx.container(
        rx.vstack(
            navbar(),
            rx.heading("Admin"),
            add_user_form(),
            rx.button("Reset", on_click=ResetState.reset_transactions),
        ),
    )