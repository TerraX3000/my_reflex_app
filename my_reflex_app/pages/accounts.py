import reflex as rx 
from typing import List 
from my_reflex_app.components.navbar import navbar
class AccountState(rx.State):
    accounts: List[str] = [
        "Checking",
        "Savings",
        "Credit Card"
        ]


def show_account(category: str):
    return rx.text(category)



rx.page(route="/accounts")
def accounts():
    return rx.container(
        rx.vstack(
            navbar(),
            rx.heading("Accounts"),
            rx.hstack(
                rx.text("Accounts"),
            rx.foreach(
                AccountState.accounts,
                show_account,
            )
            )
        ),
    )
