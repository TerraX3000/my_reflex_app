import reflex as rx
from typing import List, Dict, Literal
import requests
from my_reflex_app.templates.page_template import template
        

class DataTable(rx.Component):
    library = "/public/datatable_net.js"
    tag = "DataTableNet"
    data: rx.Var[list[dict]]
    columns: rx.Var[list[dict]]
    options: rx.Var[dict]
    className: rx.Var[str]
    slots: rx.Var[dict]
    is_processing: rx.Var[bool] = False
    on_cell_value_changed: rx.EventHandler[lambda event: [event]]

    lib_dependencies: list[str] = [
        "jquery",
        "jszip",
        "datatables.net-react",
        "datatables.net-dt",
        "datatables.net-select-dt",
        "datatables.net-responsive-dt",
        "datatables.net-buttons-dt",
    ]
    # @staticmethod
    # def render():
    #     def ellipsis(characters: int, truncate_middle: bool = False, escape_html: bool = False):
    #         return f"DataTable.render.ellipsis( {characters}, {truncate_middle}, {escape_html})"
        

    class render:
        @staticmethod
        def ellipsis(characters: int, truncate_middle: bool = False, escape_html: bool = False):
            return f"DataTable.render.ellipsis({characters}, {truncate_middle}, {escape_html})"
        
        def percentBar(
            bar: Literal["square"] = "square",
            text_color: str = "#000000",  # black
            border_color: str = "#cccccc",  # light gray
            bar_color: str = "#c6efce",  # light green
            background_color: str = "#f7f7f7",  # light gray
            round: int = 0,  # rounded to integer
            border_style: Literal["solid", "outside", "grooved", "ridge"] = "ridge"
        ):
            return f"DataTable.render.percentBar({bar}, {text_color}, {border_color}, {bar_color}, {background_color}, {round}, {border_style})"

class ProductsState(rx.State):
    data: list[dict] = None
    
    columns: list[dict] = [
        {"title": "Product Name", "data": "title"},
        {"title": "Price", "data": "price"},
        # {"title": "Description", "data": "description"},
        {"title": "Category", "data": "category"},
        {"title": "Rating", "data": "rating"},
        {"title": "Stock", "data": "stock"},
        {"title": "Tags", "data": "tags"},
        {"title": "SKU", "data": "sku"},
        {"title": "Weight", "data": "weight", "render": DataTable.render.percentBar("square", "#000000", "#cccccc", "#c6efce", "#f7f7f7", 0, "ridge")},
        {"title": "Dimensions", "data": "dimensions"},
        {"title": "Warranty Information", "data": "warrantyInformation"},
        {"title": "Shipping Information", "data": "shippingInformation"},
        {"title": "Availability Status", "data": "availabilityStatus"},
        {"title": "Reviews", "data": "reviews"},
        {"title": "Return Policy", "data": "returnPolicy"},
        {"title": "Minimum Order Quantity", "data": "minimumOrderQuantity"},
        {"title": "Meta", "data": "meta"},
        {"title": "Images", "data": "images"},
        {"title": "Thumbnail", "data": "thumbnail", "render": DataTable.render.ellipsis(10)},
    ]
    
    options = {
        "select": True,
        "responsive": True,
        "processing": True,
        "scrollX": True,
        "buttons": [
            'pageLength',
            {
            "text": 'Refresh Table'
            }
            ],
        "layout": {
            "topStart": ["buttons"]
        }
    }

    slots: dict = {
        "0": {
            "type": "text",
        },
        "1": {
            "type": "number",
        },
        "2": {
            "type": "select",
            "params": {
                "values": ["Option 1", "Option 2", "Option 3"]
            }
        },
        "3": {
            "type": "date",
        },
        "4": {
            "type": "checkbox",
        },
        "5": {
            "type": "radio",
            "params": {
                "values": ["Option 1", "Option 2", "Option 3"]
            }
        },
        "6": {
            "type" "large_text",
        },
        "7": {
            "type": "button",
            "params": {
                "text": "Open"
            }
        }
    }

    dataset = 1
    is_processing: bool = False

    @rx.event()
    def load_data(self):
        self.is_processing = True
        yield
        print("Loading data")
        response = requests.get("https://dummyjson.com/products?delay=0")
        print(response.status_code)
        self.data = response.json()["products"]
        self.is_processing = False

    @rx.event()
    def refresh_data(self):
        print("Getting API Data")
        self.is_processing = True
        yield
        
        self.dataset += 1
        rem = self.dataset % 3
        if rem == 0:
            response = requests.get(f"https://dummyjson.com/products?delay={1000*rem}")
            api_data = response.json()["products"]
            self.data = api_data[0:10]
        elif rem == 1:
            response = requests.get(f"https://dummyjson.com/products?delay={1000*rem}")
            api_data = response.json()["products"]
            self.data = api_data[10:20]
        else:
            response = requests.get(f"https://dummyjson.com/products?delay={1000*rem}")
            api_data = response.json()["products"]
            self.data = api_data[20:30]
        self.is_processing = False

    @rx.event()
    def toggle_processing(self):
        self.is_processing = not self.is_processing

    def get_input_on_blur(self, event: Dict[str, str]):
        print(event["value"])



class DataTable(rx.Component):
    library = "/public/datatable_net.js"
    tag = "DataTableNet"
    data: rx.Var[list[dict]]
    columns: rx.Var[list[dict]]
    options: rx.Var[dict]
    className: rx.Var[str]
    slots: rx.Var[dict]
    is_processing: rx.Var[bool] = False
    on_cell_value_changed: rx.EventHandler[lambda event: [event]]

    lib_dependencies: list[str] = [
        "jquery",
        "jszip",
        "datatables.net-react",
        "datatables.net-dt",
        "datatables.net-select-dt",
        "datatables.net-responsive-dt",
        "datatables.net-buttons-dt",
    ]

    def render(self):
        def ellipsis(characters: int, truncate_middle: bool = False, escape_html: bool = False):
            return f"ellipsis({characters}, {truncate_middle}, {escape_html})"


@rx.page(route="/budget", on_load=ProductsState.load_data)
@template
def budget():
    return rx.container(
        rx.button("Get API Data", on_click=ProductsState.refresh_data),
        rx.button("Toggle Processing", on_click=ProductsState.toggle_processing),
        DataTable(
            data=ProductsState.data,
            columns=ProductsState.columns,
            options=ProductsState.options,
            className="display",
            slots=ProductsState.slots,
            is_processing=ProductsState.is_processing,
            on_cell_value_changed=ProductsState.get_input_on_blur
        ),
    )
