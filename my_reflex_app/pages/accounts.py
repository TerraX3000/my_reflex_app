import reflex as rx
from typing import List
from my_reflex_app.components.navbar import navbar
from my_reflex_app.models.models import Account
from dataclasses import dataclass


@dataclass
class AccountForm:
    id: int = 0
    name: str = ""
    amount_field: str = ""
    description_field: str = ""
    original_description_field: str = ""
    bank_category_field: str = ""
    type_field: str = ""
    status_field: str = ""
    date_field: str = ""
    is_reverse_negative_values: bool = False
    include_pending_status: bool = False



class AccountState(rx.State):
    accounts: rx.Field[List[dict]] = rx.field([])

    current_values: rx.Field[dict[str, int | str | bool]] = rx.field({
        "id": 0,
        "name": "",
        "amount_field": "",
        "description_field": "",
        "original_description_field": "",
        "bank_category_field": "",
        "type_field": "",
        "status_field": "",
        "date_field": "",
        "is_reverse_negative_values": False,
        "include_pending_status": False
    })

    fields: rx.Field[dict[str, dict[str, str]]] = rx.field(
        {
        "id": {"type": "hidden", "label": "Account ID"},
        "name": {"type": "text", "label": "Account Name"},
        "date_field": {"type": "text", "label": "Date Field"},
        "amount_field": {"type": "text", "label": "Amount Field"},
        "description_field": {"type": "text", "label": "Description Field"},
        "original_description_field": {"type": "text", "label": "Original Description Field"},
        "bank_category_field": {"type": "text", "label": "Bank Category Field"},
        "type_field": {"type": "text", "label": "Type Field"},
        "status_field": {"type": "text", "label": "Status Field"},
        "is_reverse_negative_values": {"type": "checkbox", "label": "Is Reverse Negative Values"},
        "include_pending_status": {"type": "checkbox", "label": "Include Pending Status"},
    }
    )

    @rx.var
    def columns(self) -> List[str]:
        return [value["label"] for value in self.fields.values()]

    @rx.event
    def update_field(self, value: str, field: str | bool):
        self.current_values[field] = value

    @rx.event
    def handle_submit(self, form_data: dict):
        """Handle the form submit."""
        form_data["id"] = int(form_data["id"])
        if not form_data["id"]:
            self.add_account(form_data)
        else:
            self.update_account(form_data)

    def add_account(self, form_data: dict):
        form_data.pop("id", None)
        boolean_fields = [field for field in self.fields.keys() if self.fields[field]["type"] == "checkbox"]
        for field in boolean_fields:
            if field in form_data:
                form_data[field] = True
            else:
                form_data[field] = False
        with rx.session() as session:
            field_keys = [field for field in self.fields.keys()]
            field_keys.remove("id")
            field_values = {field: form_data[field] for field in field_keys}

            account = Account(
                **field_values
            )
            session.add(account)
            session.commit()
        self.clear_selected_account()
        self.get_accounts()
    
    def update_account(self, form_data: dict):
        boolean_fields = [field for field in self.fields.keys() if self.fields[field]["type"] == "checkbox"]
        for field in boolean_fields:
            if field in form_data:
                form_data[field] = True
            else:
                form_data[field] = False
        with rx.session() as session:
            account: Account = session.exec(
                Account.select().where(Account.id == int(form_data["id"]))
            ).first()
            for field in self.fields.keys():
                setattr(account, field, form_data[field])
            session.add(account)
            session.commit()
        self.clear_selected_account()
        self.get_accounts()


    @rx.event
    def set_edit_account(self, account: dict):
        self.clear_selected_account()
        for field in self.fields.keys():
            if self.fields[field]["type"] == "checkbox":
                self.current_values[field] = bool(account[field])
            else:
                self.current_values[field] = account[field]


    @rx.event
    def delete_account(self, account: dict):
        with rx.session() as session:
            account: Account = session.exec(
                Account.select().where(Account.id == int(account["id"]))
            ).first()
            session.delete(account)
            session.commit()
        self.clear_selected_account()
        self.get_accounts()

    @rx.event
    def get_accounts(self):
        with rx.session() as session:
            self.accounts = session.exec(Account.select()).all()

    @rx.event
    def clear_selected_account(self):
        for field in self.fields.keys():
            if field in self.current_values:
                if field == "id":
                    self.current_values[field] = 0
                else:
                    self.current_values[field] = ""
    
    @rx.event
    def initialize(self):
        self.get_accounts()
        self.clear_selected_account()

def account_table() -> rx.Component:
    def set_cell(key_value: list):
        return rx.match(
            key_value[1].js_type(),
            ("number", rx.table.cell(key_value[1])),
            ("boolean", rx.table.cell(
                rx.checkbox(
                    checked=key_value[1].bool(),
                )
            )),
            ("string", rx.table.cell(
                key_value[1]
            )),
            rx.table.cell(key_value[1].js_type()),
            )

    def account_table_row(account: dict):
        return rx.table.row(
            rx.foreach(account, set_cell),
            rx.table.cell(
                rx.hstack(
                    rx.dialog.root(
                    rx.dialog.trigger(rx.icon("pencil", on_click=AccountState.set_edit_account(account))),
                    account_form_dialog(),
                ),
                delete_account_dialog(account),
                )
            )
        )
    
    def account_table_header(column_header: dict[str, str]):
        return rx.table.cell(column_header)

    return rx.table.root(
        rx.table.header(
            rx.table.row(
                rx.foreach(AccountState.columns, account_table_header),
            )
        ),
        rx.foreach(AccountState.accounts, account_table_row),
        on_mount=AccountState.initialize,
    )


def delete_account_dialog(account: dict):
    return rx.dialog.root(
        rx.dialog.trigger(rx.icon("trash", on_click=AccountState.set_edit_account(account))),
        rx.dialog.content(
            rx.dialog.title("Delete Account"),
            rx.vstack(
                rx.text(f"Are you sure you want to delete {account['name']}?"),
                rx.hstack(
                    rx.dialog.close(
                        rx.button(
                            "Cancel",
                            variant="soft",
                            color_scheme="gray",
                        ),
                    ),
                    rx.dialog.close(
                        rx.button("Delete", on_click=AccountState.delete_account(account)),
                    ),
                    spacing="5",
                ),
            ),
        ),
    )

def account_form_dialog() -> rx.Component:
    def set_input_cell(field: str):
        return rx.match(
            AccountState.fields[field]["type"],
            ("text", rx.vstack(
                        rx.text(AccountState.fields[field]["label"]),
                        rx.input(
                            value=AccountState.current_values[field],
                            on_change=lambda value: AccountState.update_field(value, field),
                            name=field,
                        )
                )
            )
        )
    def set_checkbox(field: str):
        return rx.match(
            AccountState.fields[field]["type"],
            ("checkbox", rx.checkbox(
                AccountState.fields[field]["label"],
                checked=AccountState.current_values[field].bool(),
                on_change=lambda value: AccountState.update_field(value, field),
                name=field,
                )
            )
        )

    
    return rx.dialog.content(
        rx.dialog.title(
            rx.cond(
                AccountState.current_values["id"],
                "Edit Account",
                "Add Account",
            )
            ),
        rx.vstack(
            rx.form(
                rx.flex(
                    rx.flex(
                        rx.foreach(
                            AccountState.fields.keys(),
                            set_input_cell,
                            ),
                            spacing="2",
                            flex_wrap="wrap"
                    ),
                    rx.flex(
                        rx.foreach(
                            AccountState.fields.keys(),
                            set_checkbox,
                            ),
                            spacing="2",
                            flex_wrap="wrap"
                    ),
                
                    rx.flex(
                        rx.dialog.close(
                            rx.button(
                                "Cancel",
                                variant="soft",
                                color_scheme="gray",
                            ),
                        ),
                        rx.dialog.close(
                            rx.button("Submit", type="submit"),
                        ),
                        spacing="5",
                        justify="end",
                    ),
                    rx.el.input(type="hidden", name="id", value=AccountState.current_values["id"]),
                    
                    direction="column",
                    spacing="5",
                ),
                on_submit=AccountState.handle_submit,
                reset_on_submit=True,
            ),
        ),
    )


@rx.page(route="/accounts")
def accounts():
    return rx.container(
        navbar(),
        rx.vstack(
            rx.heading("Accounts"),
            rx.dialog.root(
                rx.dialog.trigger(rx.button("Add Account", on_click=AccountState.clear_selected_account)),
                account_form_dialog(),
            ),
            rx.hstack(
                rx.text("Accounts"),
            ),
            account_table(),
        ),
    )
