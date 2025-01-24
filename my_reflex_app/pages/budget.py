import reflex as rx


class HelloState(rx.State):
    def handle_click(self, button_name: str):
        print(f"Button clicked: {button_name}")

    def on_input_blur(self, data: dict):
        input_name = data.get("input_name", "unknown")
        value = data.get("value", "")
        print(f"Input blurred: {input_name} = {value}")


class Hello(rx.Component):
    library = "/public/hello.js"
    tag = "Hello"
    on_click: rx.EventHandler[lambda button_name: [button_name]]
    on_blur: rx.EventHandler[lambda data: [data]]


@rx.page(route="/budget")
def budget():
    return rx.container(
        Hello(
            on_click=HelloState.handle_click,
            on_blur=HelloState.on_input_blur,  # Bind the onBlur event
        ),
    )
