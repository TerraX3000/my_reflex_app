import reflex as rx
from my_reflex_app.templates.page_template import template
from my_reflex_app.models.models import Category
from typing import List, Dict
import sqlalchemy
from sqlalchemy import select

class SpeedDialMenu(rx.ComponentState):
    is_open: bool = False

    @rx.event
    def toggle(self, value: bool):
        self.is_open = value

    @classmethod
    def get_component(cls, **props):
        def menu_item(icon: str, text: str) -> rx.Component:
            return rx.hstack(
                rx.icon(icon, padding="2px"),
                rx.text(text, weight="medium"),
                align="center",
                opacity="0.75",
                cursor="pointer",
                position="relative",
                _hover={
                    "opacity": "1",
                },
                width="100%",
                align_items="center",
            )

        def menu() -> rx.Component:
            return rx.box(
                rx.card(
                    rx.vstack(
                        menu_item("copy", "Copy"),
                        rx.divider(margin="0"),
                        menu_item("download", "Download"),
                        rx.divider(margin="0"),
                        menu_item("share-2", "Share"),
                        direction="column-reverse",
                        align_items="end",
                        justify_content="end",
                    ),
                    box_shadow="0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1)",
                ),
                position="absolute",
                bottom="100%",
                right="0",
                padding_bottom="10px",
            )

        return rx.box(
            rx.box(
                rx.icon_button(
                    rx.icon(
                        "plus",
                        style={
                            "transform": rx.cond(
                                cls.is_open,
                                "rotate(45deg)",
                                "rotate(0)",
                            ),
                            "transition": "transform 150ms cubic-bezier(0.4, 0, 0.2, 1)",
                        },
                        class_name="dial",
                    ),
                    variant="solid",
                    color_scheme="orange",
                    size="3",
                    cursor="pointer",
                    radius="full",
                    position="relative",
                ),
                rx.cond(
                    cls.is_open,
                    menu(),
                ),
                position="relative",
            ),
            on_mouse_enter=cls.toggle(True),
            on_mouse_leave=cls.toggle(False),
            on_click=cls.toggle(~cls.is_open),
            style={"bottom": "15px", "right": "15px"},
            position="absolute",
            # z_index="50",
            **props,
        )


speed_dial_menu = SpeedDialMenu.create


def render_menu():
    return rx.box(
        speed_dial_menu(),
        height="250px",
        position="relative",
        width="100%",
    )


class CategoryState(rx.State):
    categories: list[Category] = []
    new_category: str = ""
    parent_category: str = ""
    description: str = ""
    is_expense_category: bool
    
    category_options: List[str] = []

    def get_category_options(self):
        category_options = [str(category.name) for category in self.categories if category.parent is None]
        category_options.sort()
        self.category_options = category_options

    @rx.event
    def set_new_category(self, value):
        self.new_category = value

    @rx.var(cache=False)
    def get_is_expense_category(self) -> str:
        if self.is_expense_category:
            return "Expense"
        else:
            return "Income"

    @rx.event
    def set_is_expense_category(self, value):
        print("set is expense category", value, type(value))
        if value == "Expense":
            self.is_expense_category = True
        else:
            self.is_expense_category = False

    def get_category_from_name(self, name: str):
        with rx.session() as session:
            return session.exec(Category.select().where(Category.name == name)).first()
    @rx.event
    def add_category(self):
        if not self.new_category:
            return
        parent = self.get_category_from_name(self.parent_category)
        if parent and parent != "None":
            new_category = Category(
                name=self.new_category,
                parent_id=parent.id, 
                description=self.description,
                is_expense_category=self.is_expense_category
                )
        else:
            new_category = Category(
                name=self.new_category,
                description=self.description,
                is_expense_category=self.is_expense_category
                )
        with rx.session() as session:
            session.add(new_category)
            session.commit()
        self.get_categories()
        self.new_category = ""
        self.parent_category = ""
        self.description = ""
        self.get_category_options()

    @rx.event
    def reset_inputs(self):
        self.new_category = ""
        self.parent_category = ""
        self.description = ""
        self.is_expense_category = True

    @rx.event
    def get_categories(self):
        with rx.session() as session:
            self.categories = session.exec(
                Category.select()
            ).all()
            
            self.get_category_options()

    @rx.event
    def delete_category(self, category: dict):
        print("delete category", category)
        with rx.session() as session:
            category: Category = session.exec(
                Category.select().where(Category.id == category["id"])
            ).first()
            session.delete(category)
            session.commit()
        self.get_categories()
        self.get_category_options()


def show_categories_table():
    def show_category(category: Category):
        return rx.table.row(
            rx.table.cell(
            rx.cond(
                category.parent,
                category.parent.name,
                category.name
            )
            ),
            rx.table.cell(
            rx.cond(
                category.parent,
                category.name,
                ""
            )
            ),
            rx.table.cell(
                rx.cond(
                    category.is_expense_category,
                    "Expense",
                    "Income"
                )
            ),
            rx.table.cell(category.description),
            rx.table.cell(
                rx.hstack(
                    rx.dialog.root(
                        rx.dialog.trigger(rx.icon("trash")),
                        rx.dialog.content(
                            rx.dialog.title("Delete Category"),
                            rx.vstack(
                                rx.text(f"Are you sure you want to delete {category.name}?"),
                                rx.hstack(
                                    rx.dialog.close(
                                        rx.button(
                                            "Cancel",
                                            variant="soft",
                                            color_scheme="gray",
                                        ),
                                    ),
                                    rx.dialog.close(
                                        rx.button("Delete", on_click=lambda: CategoryState.delete_category(category)),
                                    ),
                                    spacing="5",
                                ),
                            ),
                        ),
                    ),
                )
            ),
        )
    return rx.table.root(
        rx.table.header(
            rx.table.row(
                rx.table.column_header_cell("Category"),
                rx.table.column_header_cell("Sub Category"),
                rx.table.column_header_cell("Type"),
                rx.table.column_header_cell("Description"),
                rx.table.column_header_cell("Actions"),
            )
        ),
        rx.table.body(
            rx.foreach(
            CategoryState.categories,
            show_category,
        ),
        ),
    )


@rx.page(route="/categories", on_load=CategoryState.get_categories)
@template
def categories() -> rx.Component:
    return rx.container(
        rx.vstack(
            rx.heading("Categories"),
            rx.hstack(
                rx.vstack(
                    rx.text("New Category"),
                    rx.input(value=CategoryState.new_category,  on_change=CategoryState.set_new_category),
                    align="center",
                ),
                rx.vstack(
                    rx.text("Parent Category (Optional)"),
                    rx.select(
                        items=CategoryState.category_options,
                        label="Select Category",
                        placeholder="Select a category",
                        on_change=CategoryState.set_parent_category,
                        value=CategoryState.parent_category
                    ),
                    align="center",
                ),
                rx.vstack(
                    rx.text("Type"),
                    rx.select(
                        items=["Expense", "Income"],
                        label="Select Category",
                        placeholder="Select a category",
                        on_change=CategoryState.set_is_expense_category,
                        value=CategoryState.get_is_expense_category
                    ),
                    align="center",
                ),
                rx.vstack(
                    rx.text("Description (Optional)"),
                    rx.input(value=CategoryState.description, on_change=CategoryState.set_description),
                    align="center",
                ),
            ),
            rx.hstack(
                rx.button("Add category", on_click=CategoryState.add_category),
                rx.button("Reset", on_click=CategoryState.reset_inputs)
            ),
            show_categories_table(),
        ),
    )