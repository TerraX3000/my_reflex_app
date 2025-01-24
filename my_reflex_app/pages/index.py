
import reflex as rx

from rxconfig import config
from my_reflex_app.components.navbar import navbar

class State(rx.State):
    @rx.var
    def current_url(self) -> str:
        return self.router.page.full_raw_path
    
    @rx.var
    def query_params(self) -> str:
        return str(self.router.page.params)



def index() -> rx.Component:
    # Welcome Page (Index)
    return rx.container(
        rx.color_mode.button(position="top-right"),
        navbar(),
        rx.hstack(
            rx.vstack(
            rx.text("one"),
            rx.text("two"),
            rx.text("three"),
            spacing="5",
            justify="center",
            ),
            rx.vstack(
            rx.text("one"),
            rx.text("two"),
            rx.text("three"),
            spacing="9",
            justify="start",
            ),
            rx.vstack(
            rx.text("one"),
            rx.text("two"),
            rx.text("three"),
            spacing="1",
            justify="end",
            ),
        ),
        rx.vstack(
            rx.heading("Welcome to Reflex!", size="9"),
            rx.text(
                "Get started by editing ",
                rx.code(f"{config.app_name}/{config.app_name}.py"),
                size="5",
            ),
            rx.link(
                rx.button("Check out our docs!"),
                href="https://reflex.dev/docs/getting-started/introduction/",
                is_external=True,
            ),
            rx.text(State.current_url),
            rx.text(State.query_params),
            spacing="5",
            justify="center",
            min_height="85vh",
        ),
        rx.logo(),
    )