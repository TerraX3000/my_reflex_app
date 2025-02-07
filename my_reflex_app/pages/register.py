import reflex as rx 
from typing import List 
from my_reflex_app.components.navbar import navbar
from my_reflex_app.models.models import Account, Transaction
import pandas as pd
import io 
from datetime import date, datetime, timedelta



class RegisterState(rx.State):
    accounts: List[dict] = []
    account_options: List[str] = []
    selected_account: str = ""
    transactions: List[dict] = []
    start_date: str = str(date.today() - pd.Timedelta(days=30))
    end_date: str = str(date.today())

    @rx.event
    def handle_start_date_change(self, value):
        self.start_date = value
        self.load_transactions()
    @rx.event
    def handle_end_date_change(self, value):
        self.end_date = value
        self.load_transactions()

    def get_selected_account(self):
        for account in self.accounts:
            if account.name == self.selected_account:
                return account
            
    @rx.event
    def load_transactions(self):
        account: Account = self.get_selected_account()
        if not all([account, self.start_date, self.end_date]):
            self.transactions = []
            return
        with rx.session() as session:
            self.transactions = session.exec(
                Transaction.select()
                .where(Transaction.account_id == account.id)
                .where(Transaction.date >= self.start_date)
                .where(Transaction.date <= self.end_date)
                .order_by(Transaction.date)
            ).all()

    @rx.event
    def get_accounts(self):
        with rx.session() as session:
            self.accounts: List[Account] = session.exec(Account.select()).all()
            self.account_options = []
            for account in self.accounts:
                self.account_options.append(str(account.name))

    @rx.event
    def handle_select(self, account: str):
        self.selected_account = account
        self.load_transactions()

    @rx.event
    def clear_selections(self):
        self.selected_account = ""
        self.start_date  = str(date.today() - pd.Timedelta(days=30))
        self.end_date = str(date.today())
        self.load_transactions()

def show_transaction_table():
    def transaction_row(transaction: dict):
        return rx.table.row(
            rx.table.cell(transaction["date"]),
            rx.table.cell(transaction["description"]),
            rx.table.cell(transaction["amount"]),
        )
    return rx.table.root(
        rx.table.header(
            rx.table.row(
                rx.table.column_header_cell("Date"),
                rx.table.column_header_cell("Description"),
                rx.table.column_header_cell("Amount"),
            )
        ),
        rx.table.body(
            rx.foreach(RegisterState.transactions, transaction_row)
        )
    )


@rx.page(route="/register", on_load=RegisterState.get_accounts)
def register():
    return rx.container(
        rx.vstack(
            navbar(),
            rx.heading("Register"),
            rx.hstack(
                rx.select(
                items=RegisterState.account_options,
                label="Select Account",
                placeholder="Select an account",
                on_change=RegisterState.handle_select,
                value=RegisterState.selected_account,
                ),
                rx.input(type="date", on_change=RegisterState.handle_start_date_change, value=RegisterState.start_date),
                rx.input(type="date", on_change=RegisterState.handle_end_date_change, value=RegisterState.end_date),
                rx.button("Clear", on_click=RegisterState.clear_selections),
            ),
            ),
            rx.vstack(
                show_transaction_table()
            )
        )
        
