import reflex as rx 
from typing import List , Tuple

class NavBarState(rx.State):
    menu_bar_items: List[Tuple[str, str]] = [
        ("Home","/"),
        ("Register","/register"),
        ("Budget","/budget"),
        ("Analysis","/analysis"),
        ("Accounts","/accounts"),
        ("Upload","/upload"),
        ("Admin","/admin"),
    ]


def show_menu_bar_item(menu_bar_item):
    # return rx.button(menu_bar_item, on_click=rx.redirect("/"))
    return rx.button(
        menu_bar_item[0],
        on_click=rx.redirect(
            menu_bar_item[1]
        )
    )



def navbar():
    return rx.container(
        rx.hstack(
            rx.foreach(
                NavBarState.menu_bar_items,
                show_menu_bar_item
            )
        )
    )