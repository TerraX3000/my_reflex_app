import reflex as rx 
from typing import List 
from my_reflex_app.components.navbar import navbar
class BudgetState(rx.State):
    categories: List[str] = [
        "Housing",
        "Utilities",
        "Food"
        ]


def show_category(category: str):
    return rx.text(category)



rx.page(route="/analysis")
def analysis():
    return rx.container(
        rx.vstack(
            navbar(),
            rx.heading("Analysis"),
            rx.hstack(
                rx.text("Categories"),
            rx.foreach(
                BudgetState.categories,
                show_category,
            )
            )
        ),
    )
