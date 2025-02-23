import reflex as rx 
from typing import List 
from my_reflex_app.templates.page_template import template
from my_reflex_app.models.models import Account, Transaction
import pandas as pd
import io 

class UploadState(rx.State):
    """The app state."""

    filename: str = ""
    is_valid: bool = False
    accounts: List[dict] = []
    account_options: List[str] = []
    selected_account: str = ""
    register_df: pd.DataFrame
    is_imported: bool = False

    @rx.event
    def get_accounts(self):
        with rx.session() as session:
            self.accounts: List[Account] = session.exec(Account.select()).all()
            self.account_options = []
            for account in self.accounts:
                self.account_options.append(str(account.name))
    
    def get_selected_account(self):
        for account in self.accounts:
            if account.name == self.selected_account:
                return account
            
    def rename_df_columns(self):
        account: Account = self.get_selected_account()
        rename_dict = {
            account.date_field: "Date",
            account.amount_field: "Amount",
            account.description_field: "Description",
            account.original_description_field: "Original Description",
            account.bank_category_field: "Bank Category",
            account.type_field: "Type",
            account.status_field: "Status",
        }
        self.register_df.rename(columns=rename_dict, inplace=True)
    
    def reverse_negative_values(self):
        account: Account = self.get_selected_account()
        if account.is_reverse_negative_values:
            self.register_df["Amount"] *= -1

    def convert_date(self):
        account: Account = self.get_selected_account()
        self.register_df["Date"] = pd.to_datetime(self.register_df["Date"], format=account.date_format)
        self.register_df["Date"] = self.register_df["Date"].astype(str)

    def add_missing_columns(self):
        # check if column is not in the dataframe and add it and fill it with empty string
        for column in ["Date", "Amount", "Description", "Original Description", "Bank Category", "Type", "Status"]:
            if column not in self.register_df.columns:
                self.register_df[column] = ""
    
    def add_transactions(self):
        account: Account = self.get_selected_account()
        for index, row in self.register_df.iterrows():
            if account.include_pending_status or row["Status"] != "Pending":
                transaction = Transaction(
                    account_id=account.id,
                    date=row["Date"],
                    description=row["Description"],
                    original_description=row["Original Description"],
                    bank_category=row["Bank Category"],
                    bank_status=row["Status"],
                    bank_type=row["Type"],
                    gross_amount=row["Amount"],
                    amount=row["Amount"],
                )
                with rx.session() as session:
                    session.add(transaction)
                    session.commit()
        self.is_imported = True

    @rx.event
    def handle_import_file(self):
        self.rename_df_columns()
        self.reverse_negative_values()
        self.convert_date()
        self.add_missing_columns()
        self.add_transactions()
        

    @rx.event
    async def handle_upload(
        self, files: list[rx.UploadFile]
    ):
        """Handle the upload of file(s).

        Args:
            files: The uploaded files.
        """
        self.is_valid = False
        current_file = files[0]
        self.filename = current_file.filename
        upload_data = await current_file.read()
        register_df = pd.read_csv(io.StringIO(upload_data.decode("utf-8")))
        self.validate_file(register_df)
    
    @rx.event
    def clear_selected_files(self,id_: str):
        rx.clear_selected_files(id_)
        self.filename = ""
        self.is_valid = False

    def validate_file(self, register_df: pd.DataFrame):
        self.is_valid = True
        self.register_df = register_df
    

    def handle_select(self, account: str):
        self.selected_account = account


@rx.page(route="/upload", on_load=UploadState.get_accounts)
@template
def upload():
    return rx.container(
        rx.vstack(
            rx.heading("Upload"),
            rx.vstack(
                rx.select(
                items=UploadState.account_options,
                label="Select Account",
                placeholder="Select an account",
                on_change=UploadState.handle_select,
            ),
                rx.upload.root(
                    rx.button("Upload File"),
                    id="upload2",
                    accept={
                        "text/csv": [".csv"],
                    },
                    on_drop=UploadState.handle_upload(rx.upload_files(upload_id="upload2")),
                ),
                rx.cond(
                    UploadState.filename,
                    rx.text(f"File uploaded: {UploadState.filename}"),
                    rx.text("No file uploaded"),
                ),
                rx.button(
                    "Clear Uploaded File",
                    on_click=UploadState.clear_selected_files("upload2"),
                ),
        rx.cond(
            UploadState.is_valid,
            rx.button(
            "Import File",
            on_click=UploadState.handle_import_file,
            )
        ),
        rx.cond(
            UploadState.is_imported,
            rx.text("File imported"),
        ),
     )
    )
)
