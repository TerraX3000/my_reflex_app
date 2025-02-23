
import reflex as rx
from my_reflex_app.states.app_states import UserState


@rx.page(route="/initialize", on_load=UserState.create_default_user)
def initialize() -> rx.Component:
    return rx.container(
        rx.hstack(
            rx.vstack(
            rx.text("Welcome to the Budget App"),
            spacing="5",
            justify="center",
            ),
        ),
        rx.cond(
            UserState.is_default_user_created,
            rx.vstack(
                rx.text("Default user created"),
                rx.text("You may now log in with the default user"),
                rx.text("Username: admin"),
                rx.text("Password: password123"),
                rx.text("Once logged in you may navigate to the admin page to remove the default user and add additional users"),
                rx.link("Login", href="/"),
            ),
            
            rx.text("Users already exist so default user not created"),
        )
    )