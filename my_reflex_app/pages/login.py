import reflex as rx
from my_reflex_app.states.app_states import UserState


def login_page() -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.center(
                rx.heading(
                    "Sign in to your account",
                    size="6",
                    as_="h2",
                    text_align="center",
                    width="100%",
                ),
                direction="column",
                spacing="5",
                width="100%",
            ),
            rx.vstack(
                rx.cond(
                    UserState.invalid_credentials,
                    rx.text(
                        "Invalid credentials",
                        size="3",
                        color="red",
                        width="100%",
                    )),
                rx.text(
                    "Username",
                    size="3",
                    weight="medium",
                    text_align="left",
                    width="100%",
                ),
                rx.input(
                    placeholder="username",
                    type="text",
                    size="3",
                    width="100%",
                    on_blur=UserState.set_username
                ),
                justify="start",
                spacing="2",
                width="100%",
            ),
            rx.vstack(
                rx.hstack(
                    rx.text(
                        "Password",
                        size="3",
                        weight="medium",
                    ),
                    justify="between",
                    width="100%",
                ),
                rx.input(
                    placeholder="Enter your password",
                    type="password",
                    size="3",
                    width="100%",
                    on_change=UserState.set_password,
                    on_key_up=UserState.login_on_enter_key
                ),
                spacing="2",
                width="100%",
            ),
            rx.button("Sign in", size="3", width="100%", on_click=UserState.validate_user_credentials),
            spacing="6",
            width="100%",
        ),
        size="4",
        max_width="28em",
        width="100%",
    )

@rx.page(route="/logout", on_load=UserState.logout)
def logout_page() -> rx.Component:
    return rx.container(
        rx.center(
            rx.vstack(
                rx.text("You have been logged out"),
            )
        )
    )