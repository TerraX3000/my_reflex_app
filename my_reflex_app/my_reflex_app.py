"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx
from my_reflex_app.pages import *


app = rx.App(
    theme=rx.theme(
        appearance="dark",
        has_background=True,
        radius="full",
        accent_color="blue",
        gray_color="slate",
    )
)
app.api.add_api_route("/items/{item_id}", api_test)
app.api.add_api_route("/transactions", api_transactions)

