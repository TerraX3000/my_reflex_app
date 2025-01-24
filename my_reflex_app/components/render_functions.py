from my_reflex_app.components.datatables import stringify_javascript_function

JAVASCRIPT_FILEPATH = "./my_reflex_app/components/render_functions.js"

def show_hamburger():
    return stringify_javascript_function(JAVASCRIPT_FILEPATH, "showHamburger")

