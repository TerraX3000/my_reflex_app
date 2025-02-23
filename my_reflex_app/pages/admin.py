import reflex as rx
from my_reflex_app.templates.page_template import template
from my_reflex_app.models.users import User
import bcrypt

class AdminState(rx.State):
    username: str = ""
    password: str = ""
    form_data: dict = {}
    users: list[User] = []

    @rx.event
    def handle_submit(self, form_data: dict):
        """Handle the form submit."""
        self.form_data = form_data
        with rx.session() as session:
            password = bcrypt.hashpw(self.form_data["password"].encode('utf-8'), bcrypt.gensalt())
            user = User(
                username=self.form_data["username"],
                password=password,
            )
            session.add(user)
            session.commit()
        self.get_users()

    @rx.event
    def get_users(self):
        with rx.session() as session:
            users = session.exec(User.select()).all()
            self.users = users

    @rx.event
    def delete_user(self, user: dict):
        with rx.session() as session:
            user: User = session.exec(
                User.select().where(User.username == user["username"])
            ).first()
            session.delete(user)
            session.commit()
        self.get_users()


def add_user_form():
    return rx.vstack(
        rx.form(
            rx.vstack(rx.hstack(
                rx.text("Username"),
                rx.input(
                    name="username",
                ),
                rx.text("Password"),
                rx.input(type="password", name="password"),
            ),
            rx.button("Submit", type="submit"),
            ),
            on_submit=AdminState.handle_submit,
            reset_on_submit=True,
            spacing="3",
        ),
    )



def add_user_dialog() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.trigger(rx.hstack(rx.icon("plus"), rx.text("Add User"))),
        rx.dialog.content(
            rx.dialog.title("Add User"),
            add_user_form(),
            rx.dialog.close(rx.button("Close")),
        ),
    )

def user_table_action_cell(user: User):
    return rx.hstack(
        rx.dialog.root(
            rx.dialog.trigger(rx.icon("pencil")),
            rx.dialog.content(
                rx.dialog.title("Edit User"),
                rx.vstack(
                    rx.text("Username"),
                    rx.input(name="username", value=user.username),
                    rx.text("Password"),
                    rx.input(type="password", name="password", value=user.password),
                    rx.hstack(
                        rx.dialog.close(
                            rx.button(
                                "Cancel",
                                variant="soft",
                                color_scheme="gray",
                            ),
                        ),
                        rx.dialog.close(
                            rx.button(
                                "Save",
                                ),
                            ),
                    ),
                ),
            ),
        ),  
        rx.dialog.root(
            rx.dialog.trigger(rx.icon("trash")),
            rx.dialog.content(
                rx.dialog.title("Delete User"),
                rx.vstack(
                    rx.text(f"Are you sure you want to delete {user.username}?"),
                    rx.hstack(
                        rx.dialog.close(
                            rx.button(
                                "Cancel",
                                variant="soft",
                                color_scheme="gray",
                            ),
                        ),
                        rx.dialog.close(
                            rx.button(
                                "Delete",
                                on_click=lambda: AdminState.delete_user({"username": user.username}),
                            ),
                        ),
                    ),
                ),
            ),
        ),
    )

def user_table():
    return rx.table.root(
        rx.table.header(
            rx.table.row(
                rx.table.column_header_cell("Username"),
                rx.table.column_header_cell("Actions"),
            )
        ),
        rx.table.body(
            rx.foreach(
            AdminState.users,
            lambda user: rx.table.row(
                rx.table.cell(user.username),
                user_table_action_cell(user),
            ),
        )
        )
    ),


@rx.page(route="/admin", on_load=AdminState.get_users)
@template
def admin():
    return rx.container(
        rx.vstack(
            rx.heading("Admin"),
            add_user_dialog(),
            user_table(),
        ),
    )