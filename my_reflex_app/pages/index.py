
import reflex as rx
from my_reflex_app.templates.page_template import template


@rx.page(route="/")
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