import reflex as rx 
from typing import List 
from my_reflex_app.components.navbar import navbar
from my_reflex_app.components.render_functions import show_hamburger





class RegisterState(rx.State):
    entries: List[str] = [
        "Housing",
        "Utilities",
        "Food"
        ]
    bank_account_transactions: List[dict] = []

    @rx.event()
    def update_data(self):
        print("Updating data")
        self.bank_account_transactions: List[dict] = [
        {
            "account": "Primary Checking",
            "date": "2023-01-01",
            "amount": 100
        },
        {
            "account": "Savings",
            "date": "2023-01-01",
            "amount": 200
        },
        {
            "account": "Credit Card",
            "date": "2023-01-01",
            "amount": 300
        },
        {
            "account": "Checking",
            "date": "2023-01-01",
            "amount": 400
        },
        {
            "account": "Savings",
            "date": "2023-01-01",
            "amount": 500
        },
        {
            "account": "Credit Card",
            "date": "2023-01-01",
            "amount": 600
        }
    ]

def show_entry(entry: str):
    return rx.text(entry)


def show_transaction(transaction: dict):
    print(transaction)
    return rx.text(transaction)

class DataTableState(rx.State):
    data: List[dict] = []
    columns: List[dict] = [
        {
            "title": "Account",
            "data": "account"
        },
        {
            "title": "Date",
            "data": "date"
        },
        {
            "title": "Amount",
            "data": "amount",
            'render': ['number', ',', '.', 0, '$']
        }
    ]
    
    def draw_event(self):
        print("Draw event")

    def select_event(self):
        print("Select event")

    

    @rx.event()
    def update_data(self) -> List[dict]:
        print("Updating data")
        self.data = RegisterState.bank_account_transactions

class datatable(rx.Component):
    library = "datatables.net-react"
    tag = "DataTable"
    is_default = True
    lib_dependencies: list[str] = [
        "datatables.net-dt",
        "datatables.net-select-dt",
        "datatables.net-responsive-dt",
    ]
    def add_imports(self):
        return {"": [
            "datatables.net-select-dt",
            "datatables.net-responsive-dt",
            "datatables.net-dt/css/dataTables.dataTables.min.css"
            ]
            }
    
    def add_custom_code(self) -> List[str]:
        return [
            "import DT from 'datatables.net-dt';",
            "DataTable.use(DT);"
        ]
    
    # data: rx.Var[List[dict]] = DataTableState.data
    columns: rx.Var[List[dict]] = DataTableState.columns
    options: rx.Var[dict] = {}
    # onDraw: rx.EventHandler
    # onSelect: rx.EventHandler

rx.page(route="/register")
def register():
    return rx.container(
        rx.vstack(
            navbar(),
            rx.heading("Register"),
            rx.hstack(
                rx.text("Transactions"),
            
            ),
            rx.button(
                "Load Transactions",
                on_click=DataTableState.update_data
            ),
            
            rx.vstack(
                rx.foreach(
                RegisterState.bank_account_transactions,
                show_transaction,
            )
            ),
            
            datatable(
                # onDraw=DataTableState.draw_event,
                # onSelect=DataTableState.select_event,
                options={
                    "ajax": {
                        "url": "http://localhost:8000/transactions",
                        "type": "GET",
                        "dataSrc": "",
                     },
                    # "data": DataTableState.data,
                    "responsive": True,
                    "select": True,
                }
            ),
            rx.text(show_hamburger())

        ),
    )
