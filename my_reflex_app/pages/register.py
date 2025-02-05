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


class State(rx.State):
    """The app state."""

    filename: str = ""

    @rx.event
    async def handle_upload(
        self, files: list[bytes]
    ):
        """Handle the upload of file(s).

        Args:
            files: The uploaded files.
        """
        current_file = files[0]
        register_df = pd.read_csv(io.StringIO(current_file.decode("utf-8")))
        print(register_df)

color = "rgb(107,99,246)"

rx.page(route="/register")
def register():
    return rx.container(
        rx.vstack(
            navbar(),
            rx.heading("Register"),
            rx.vstack(
        rx.upload(
            rx.vstack(
                rx.button(
                    "Select File",
                    color=color,
                    bg="white",
                    border=f"1px solid {color}",
                ),
                rx.text(
                    "Drag and drop files here or click to select files"
                ),
            ),
            id="upload1",
            border=f"1px dotted {color}",
            padding="5em",
            accept={
                "text/csv": [".csv"],
            },
            max_files=5,
            multiple=True,
            on_drop=State.handle_upload,
        ),
        rx.button(
            "Upload",
            on_click=State.handle_upload(
                rx.upload_files(upload_id="upload1")
            ),
        ),
        # rx.button(
        #     "Clear",
        #     on_click=rx.clear_selected_files("upload1"),
        # ),
        rx.cond(
            State.filename,
            rx.text(f"File uploaded: {State.filename}"),
            rx.text("No file uploaded"),
        )
     )
    )
)
