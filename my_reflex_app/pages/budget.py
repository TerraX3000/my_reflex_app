import reflex as rx
from typing import List, Tuple
from my_reflex_app.templates.page_template import template
from my_reflex_app.models.models import Budget, BudgetType, Category, TimePeriod
        
class BudgetState(rx.State):
    budget_items: List[BudgetType]
    categories: List[Category]
    category_options: List[Tuple[int, str]]
    time_period_options: List[str]
    category: str
    amount: float
    time_period: str
    edit_category: str
    edit_time_period: str
    edit_amount: float
    

    @rx.event
    def get_budget_items(self):
        with rx.session() as session:
            budget_items = session.exec(Budget.select()).all()
            budget_items = [item.to_dataclass() for item in budget_items]
            self.budget_items = budget_items

    @rx.event
    def get_categories(self):
        with rx.session() as session:
            categories = session.exec(Category.select()).all()
            categories = [category.to_dataclass() for category in categories]
            self.categories = categories
            category_options = [(category.id,category.name) for category in categories]
            self.category_options = category_options

    
    @rx.event
    def add_budget_item(self):
        with rx.session() as session:
            budget_item = Budget(
                category_id=int(self.category),
                amount=self.amount,
                time_period=self.time_period
            )
            session.add(budget_item)
            session.commit()
        self.get_budget_items()

    @rx.event
    def set_time_period_options(self):
        # Use values of TimePeriod enum
        self.time_period_options = [value for value in TimePeriod]

    @rx.event
    def initialize_state(self):
        self.get_budget_items()
        self.get_categories()
        self.set_time_period_options()

    @rx.event
    def reset_selections(self):
        self.category = ""
        self.time_period = ""
        self.amount = 0

    @rx.event
    def delete_budget_item(self, budget_item_id):
        with rx.session() as session:
            budget_item = session.exec(Budget.select().where(Budget.id == budget_item_id)).first()
            session.delete(budget_item)
            session.commit()
        self.get_budget_items()

    @rx.event
    def set_edit_budget_item(self, item: BudgetType):
        print("set edit budget item", item)
        self.edit_category = str(item.category_id)
        self.edit_time_period = item.time_period
        self.edit_amount = item.amount

    @rx.event
    def edit_budget_item(self, budget_item_id):
        with rx.session() as session:
            budget_item = session.exec(Budget.select().where(Budget.id == budget_item_id)).first()
            budget_item.category_id = int(self.edit_category)
            budget_item.time_period = self.edit_time_period
            budget_item.amount = self.edit_amount
            session.add(budget_item)
            session.commit()
            print("edit budget item", budget_item)
        self.get_budget_items()


def add_budget_item_dialog() -> rx.Component:
    return rx.dialog.root(
    rx.dialog.trigger(rx.hstack(rx.icon("plus"), rx.text("Add Budget Item"))),
    rx.dialog.content(
        rx.dialog.title("Add Budget Item"),
        rx.text("Select a category, time period, and amount"),
        add_budget_item(),
        rx.hstack(
            rx.dialog.close(
                rx.button("Close"),
            ),
            rx.dialog.close(
                rx.button("Add", on_click=lambda: BudgetState.add_budget_item()),
            ),
        ),
        
    ),
)

def add_budget_item() -> rx.Component:
    return rx.container(
        rx.hstack(
            rx.select.root(
                rx.select.trigger(placeholder="Select a category"),
                rx.select.content(
                    rx.foreach(
                        BudgetState.category_options,
                        lambda option: rx.select.item(
                            option[1],
                            value=option[0].to_string(),
                        )
                    )
                ),
                on_change=lambda category: BudgetState.set_category(category),
                value=BudgetState.category
                ),
            rx.select(
                BudgetState.time_period_options,
                placeholder="Select Time Period",
                on_change=lambda time_period: BudgetState.set_time_period(time_period),
                value=BudgetState.time_period
            ),
            rx.input(value=BudgetState.amount, on_change=lambda amount: BudgetState.set_amount(amount)),
            
            rx.button("Reset Fields", on_click=lambda: BudgetState.reset_selections())
            ),
    )

def show_delete_budget_item_dialog(item: BudgetType) -> rx.Component:
    return rx.dialog.root(
            rx.dialog.trigger(rx.icon("trash")),
            rx.dialog.content(
                rx.dialog.title("Delete Budget Item"),
                rx.vstack(
                    rx.text(f"Are you sure you want to delete {item.category_name}?"),
                    rx.hstack(
                        rx.dialog.close(
                            rx.button(
                                "Cancel",
                                variant="soft",
                                color_scheme="gray",
                            ),
                        ),
                        rx.dialog.close(
                            rx.button("Delete", on_click=lambda: BudgetState.delete_budget_item(item.id)),
                        ),
                        spacing="5",
                    ),
                ),
            ),
        ),

def edit_budget_item() -> rx.Component:
    return rx.container(
        rx.hstack(
            rx.select.root(
                rx.select.trigger(placeholder="Select a category"),
                rx.select.content(
                    rx.foreach(
                        BudgetState.category_options,
                        lambda option: rx.select.item(
                            option[1],
                            value=option[0].to_string(),
                        )
                    )
                ),
                on_change=lambda category: BudgetState.set_edit_category(category),
                value=BudgetState.edit_category
                ),
            rx.select(
                BudgetState.time_period_options,
                placeholder="Select Time Period",
                on_change=lambda time_period: BudgetState.set_edit_time_period(time_period),
                value=BudgetState.time_period
            ),
            rx.input(value=BudgetState.edit_amount, on_change=lambda amount: BudgetState.set_edit_amount(amount)),
            ),
    )

def edit_budget_item_dialog(item: BudgetType) -> rx.Component:
    return rx.dialog.root(
            rx.dialog.trigger(rx.icon("pencil", on_click=lambda: BudgetState.set_edit_budget_item(item))),
            rx.dialog.content(
                rx.dialog.title("Edit Budget Item"),
                rx.vstack(
                    edit_budget_item(),
                    rx.hstack(
                        rx.dialog.close(
                            rx.button(
                                "Cancel",
                                variant="soft",
                                color_scheme="gray",
                            ),
                        ),
                        rx.dialog.close(
                            rx.button("Update", on_click=lambda: BudgetState.edit_budget_item(item.id)),
                        ),
                        spacing="5",
                    ),
                ),
            ),
        ),

def show_budget_items() -> rx.Component:
    return rx.container(
        rx.table.root(
            rx.table.header(
                rx.table.row(
                    rx.table.column_header_cell("Category"),
                    rx.table.column_header_cell("Subcategory"),
                    rx.table.column_header_cell("Amount"),
                    rx.table.column_header_cell("Time Period"),
                    rx.table.column_header_cell("Actions")
                )
            ),
            rx.foreach(
                BudgetState.budget_items,
                lambda item: rx.table.row(
                    rx.table.cell(item.category_name),
                    rx.table.cell(item.sub_category_name),
                    rx.table.cell(item.amount),
                    rx.table.cell(item.time_period),
                    rx.table.cell(
                        rx.hstack(
                            edit_budget_item_dialog(item),
                            show_delete_budget_item_dialog(item),
                        )
                    ),
                )
            )
        ))


@rx.page(route="/budget", on_load=BudgetState.initialize_state)
@template
def budget():
    return rx.container(
        # add_budget_item_dialog(),
        add_budget_item_dialog(),
        show_budget_items()
    )
