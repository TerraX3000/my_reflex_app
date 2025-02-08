import reflex as rx
from my_reflex_app.components.navbar import navbar
from my_reflex_app.models.models import Category
from typing import List, Dict
import sqlalchemy
from sqlalchemy import select

class CategoryState(rx.State):
    categories: list[Category] = []
    new_category: str = ""
    parent_category: str = ""
    description: str = ""
    
    category_options: List[str] = []

    def get_category_options(self):
        self.category_options = [str(category.name) for category in self.categories if category.parent is None]

    @rx.event
    def set_new_category(self, value):
        self.new_category = value

    def get_category_from_name(self, name: str):
        with rx.session() as session:
            return session.exec(Category.select().where(Category.name == name)).first()
    @rx.event
    def add_category(self):
        parent = self.get_category_from_name(self.parent_category)
        if parent:
            new_category = Category(name=self.new_category, parent_id=parent.id, description=self.description)
        else:
            new_category = Category(name=self.new_category, description=self.description)
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

    @rx.event
    def get_categories(self):
        with rx.session() as session:
            self.categories = session.exec(
                Category.select()
            ).all()
            for category in self.categories:
                if category.parent:
                    print(category.parent.name)
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
            rx.table.cell(category.name),
            rx.table.cell(
            rx.cond(
                category.parent,
                category.parent.name,
                ""
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
                rx.table.column_header_cell("Parent Category"),
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
def categories() -> rx.Component:
    return rx.container(
        navbar(),
        rx.vstack(
            rx.heading("Categories"),
            rx.hstack(
                rx.vstack(
                    rx.text("New Category"),
                    rx.input(value=CategoryState.new_category,  on_change=CategoryState.set_new_category),
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
                ),
                rx.vstack(
                    rx.text("Description (Optional)"),
                    rx.input(value=CategoryState.description, on_change=CategoryState.set_description),
                ),
            ),
            rx.hstack(
                rx.button("Add category", on_click=CategoryState.add_category),
                rx.button("Reset", on_click=CategoryState.reset_inputs)
            ),
            show_categories_table(),
        ),
    )