import reflex as rx 
from typing import List 
from my_reflex_app.components.navbar import navbar
import pandas as pd
import io 

class RegisterState(rx.State):
    entries: List[str] = []
    bank_account_transactions: List[dict] = []

    @rx.event
    def handle_upload(self, event):
        self.entries = event.files


def show_entry(entry: str):
    return rx.text(entry)


def show_transaction(transaction: dict):
    print(transaction)
    return rx.text(transaction)


class UploadState(rx.State):
    """The app state."""

    filename: str = ""
    is_valid: bool = False

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
    
    rx.event
    def clear_selected_files(self,id_: str):
        rx.clear_selected_files(id_)
        self.filename = ""
        self.is_valid = False

    def validate_file(self, register_df: pd.DataFrame):

        self.is_valid = True


color = "rgb(107,99,246)"

rx.page(route="/upload")
def upload():
    return rx.container(
        rx.vstack(
            navbar(),
            rx.heading("Upload"),
            rx.vstack(
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
        )
        ),
     )
    )
)
