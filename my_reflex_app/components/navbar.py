import reflex as rx
from typing import List, Tuple
from my_reflex_app.states.app_states import UserState

class NavbarState(rx.State):
    @rx.var(cache=False)
    async def menu_bar_items(self) -> List[Tuple[str, str]]:
        user_state = await self.get_state(UserState)
        if user_state.is_logged_in:
            return [
                ("Register","/register"),
                ("Categories","/categories"),
                ("Budget","/budget"),
                ("Analysis","/analysis"),
            ]
        else:
            return []
    @rx.var(cache=False)
    async def user_menu_items(self) -> List[Tuple[str, str]]:
        user_state = await self.get_state(UserState)
        if user_state.is_logged_in:
            return [
                ("Accounts", "/accounts"),
                ("Upload", "/upload"),
                ("Admin", "/admin"),
                ("Log out", "/logout"),
            ]
        else:
            return [
                ("Log in", "/login"),
            ]


def navbar_link(text: str, url: str) -> rx.Component:
    return rx.link(
        rx.text(text, size="4", weight="medium"), href=url
    )


def menu_item_link(text: str, url: str) -> rx.Component:
    return rx.link(
        rx.text(text, size="3", weight="medium"), href=url
    )

def navbar() -> rx.Component:
    return rx.box(
        rx.desktop_only(
            rx.hstack(
                rx.hstack(
                    rx.heading(
                        "Budget App", size="7", weight="bold"
                    ),
                    align_items="center",
                ),
                rx.hstack(
                    rx.foreach(
                        NavbarState.menu_bar_items,
                        lambda item: navbar_link(item[0], item[1])
                    ),
                    spacing="5",
                ),
                rx.menu.root(
                    rx.menu.trigger(
                        rx.icon_button(
                            rx.icon("user"),
                            size="2",
                            radius="full",
                        )
                    ),
                    rx.menu.content(
                        rx.foreach(
                            NavbarState.user_menu_items,
                            lambda item: rx.menu.item(rx.link(item[0], href=item[1]))
                        )
                    ),
                    justify="end",
                ),
                justify="between",
                align_items="center",
            ),
        ),
        rx.mobile_and_tablet(
            rx.hstack(
                rx.hstack(
                    rx.heading(
                        "Reflex", size="6", weight="bold"
                    ),
                    align_items="center",
                ),
                rx.menu.root(
                    rx.menu.trigger(
                        rx.icon_button(
                            rx.icon("user"),
                            size="2",
                            radius="full",
                        )
                    ),
                    rx.menu.content(
                        rx.foreach(
                            NavbarState.user_menu_items,
                            lambda item: rx.menu.item(rx.link(item[0], href=item[1]))
                        )
                    ),
                    justify="end",
                ),
                justify="between",
                align_items="center",
            ),
        ),
        bg=rx.color("accent", 3),
        padding="1em",
        # position="fixed",
        # top="0px",
        # z_index="5",
        width="100%",
    )

