import reflex as rx 
from typing import List 
from my_reflex_app.components.navbar import navbar
from my_reflex_app.models.models import Account, Transaction, Category, TransactionType
import pandas as pd
import io 
from datetime import date, datetime, timedelta
import dataclasses

@dataclasses.dataclass
class SubCategoryOption:
    category_name: str
    sub_category_name: str

class RegisterState(rx.State):
    accounts: List[dict] = []
    account_options: List[str] = []
    selected_account: str = ""
    # transactions: List[dict[str, str]] = []
    transactions: List[TransactionType] = []
    transaction_categories: dict[str, str] = {}
    start_date: str = str(date.today() - pd.Timedelta(days=30))
    end_date: str = str(date.today())
    category_options: List[str] = []
    categories_with_sub_categories: List[str] = []
    sub_category_options: list[SubCategoryOption] = []

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
            transactions: List[Transaction] = session.exec(
                Transaction.select()
                .where(Transaction.account_id == account.id)
                .where(Transaction.date >= self.start_date)
                .where(Transaction.date <= self.end_date)
                .order_by(Transaction.date)
            ).all()
            self.transactions = [transaction.to_dataclass() for transaction in transactions]

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

    # @rx.event
    def get_category_options(self):
        with rx.session() as session:
            categories = session.exec(
                Category.select()
            ).all()
            self.category_options = []
            category_options = []
            categories_with_sub_categories = []
            categories_without_sub_categories = []
            categories_with_or_without_sub_categories = []
            self.sub_category_options = []
            sub_category_options: List[SubCategoryOption] = []
            for category in categories:
                if category.parent:
                    categories_with_sub_categories.append(str(category.parent.name))
                    categories_without_sub_categories.append(str(category.name))
                    sub_category_options.append(
                        SubCategoryOption(
                            category_name=str(category.parent.name), 
                             sub_category_name=str(category.name)
                        )
                    )
                else:
                    categories_with_or_without_sub_categories.append(str(category.name))
                    category_options.append(str(category.name))
            
            for category in categories_with_or_without_sub_categories:
                if category not in categories_with_sub_categories:
                    categories_without_sub_categories.append(str(category))


            category_options.sort()
            self.category_options = category_options
            sub_category_options.sort(key=lambda x: (x.category_name, x.sub_category_name))
            self.sub_category_options = sub_category_options
            self.categories_with_sub_categories = list(set(categories_with_sub_categories))

    @rx.event
    def initialize_state(self):
        self.get_accounts()
        self.get_category_options()

    @rx.event
    def set_category_for_transaction(self, category_name: str, transaction_id: str):
        # print("set category", category_name, transaction_id)
        with rx.session() as session:
            category: Category = session.exec(
                Category.select().where(Category.name == category_name)
            ).first()
            transaction: Transaction = session.exec(
                Transaction.select().where(Transaction.id == int(transaction_id))
            ).first()
            transaction.category_id = category.id
            session.add(transaction)
            session.commit()
        self.load_transactions()

def show_transaction_table():

    def render_sub_category_options(sub_category_option: SubCategoryOption, transaction: TransactionType):
        return rx.cond(
            transaction.category_name == sub_category_option.category_name,
            rx.select.item(sub_category_option.sub_category_name, value=sub_category_option.sub_category_name),
        )

    def transaction_row(transaction: TransactionType):
        return rx.table.row(
            rx.table.cell(transaction.date),
            rx.table.cell(transaction.description),
            rx.table.cell(transaction.amount),
            rx.table.cell(
                rx.select(
                    items=RegisterState.category_options,
                    label="Select Category",
                    placeholder="Select a category",
                    on_change=lambda category: RegisterState.set_category_for_transaction(category, transaction.id),
                    value=transaction.category_name,
                )
            ),
            rx.cond(
                RegisterState.categories_with_sub_categories.contains(transaction.category_name),
                rx.table.cell(
                    rx.select.root(
                        rx.select.trigger(placeholder="Select a category"),
                        rx.select.content(
                            rx.select.group(
                                rx.foreach(
                                    RegisterState.sub_category_options,
                                    lambda sub_category_option: render_sub_category_options(sub_category_option, transaction),
                                ),
                            ),
                        ),
                        on_change=lambda category: RegisterState.set_category_for_transaction(category, transaction["id"]),
                        value=transaction.sub_category_name,
                    ),
                ),
                rx.table.cell(""),
            )
        )
    return rx.table.root(
        rx.table.header(
            rx.table.row(
                rx.table.column_header_cell("Date"),
                rx.table.column_header_cell("Description"),
                rx.table.column_header_cell("Amount"),
                rx.table.column_header_cell("Category"),
                rx.table.column_header_cell("Sub Category"),
            )
        ),
        rx.table.body(
            rx.foreach(RegisterState.transactions, transaction_row)
        )
    )


@rx.page(route="/register", on_load=RegisterState.initialize_state)
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
        
