
import reflex as rx
from my_reflex_app.templates.page_template import template
from my_reflex_app.states.app_states import UserState


@rx.page(route="/", on_load=UserState.create_default_user)
@template
def index() -> rx.Component:
    return rx.container(
        rx.hstack(
            rx.vstack(
            rx.text("Welcome to the Budget App"),
            rx.text("Let's get saving!"),
            spacing="5",
            justify="center",
            ),
        ),
    )