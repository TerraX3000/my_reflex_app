"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx

from my_reflex_app.pages import (
    index,
    budget,
    accounts,
    analysis,
    register,
    api_test,
    api_transactions,
)

app = rx.App()
app.add_page(index)
app.add_page(budget)
app.add_page(accounts)
app.add_page(analysis)
app.add_page(register)
app.api.add_api_route("/items/{item_id}", api_test)
app.api.add_api_route("/transactions", api_transactions)

