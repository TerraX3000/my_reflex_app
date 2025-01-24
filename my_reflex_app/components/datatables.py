
def stringify_javascript_function(js_file_path, function_name):
    """Converts the specified JavaScript function in a JavaScript file to a string for use in JSON serializaion.
    JavaScript functions must be defined as: 

    function _function_name_( _args_ ) { _javascript_code_ }"""
    with open(js_file_path, 'r') as file:
        js_code = file.read()
        start_marker = f"function {function_name}("
        start_idx = js_code.find(start_marker)
        if start_idx == -1:
            raise ValueError(
                f"Function {function_name} not found in {js_file_path}")

        # Find the start of the function body
        body_start_idx = js_code.find("{", start_idx) + 1
        if body_start_idx == 0:
            raise ValueError(
                f"Function body for {function_name} not found in {js_file_path}")

        # Initialize a counter for opening and closing braces
        open_braces = 1
        end_idx = body_start_idx

        # Iterate through the code to find the matching closing brace
        while open_braces > 0 and end_idx < len(js_code):
            if js_code[end_idx] == '{':
                open_braces += 1
            elif js_code[end_idx] == '}':
                open_braces -= 1
            end_idx += 1

        if open_braces != 0:
            raise ValueError(
                f"Unmatched braces in function {function_name} in {js_file_path}")

        # Extract the full function code
        function_code = js_code[start_idx:end_idx]

        return function_code


def stringify_file(file_path):
    """Converts the specified file to a string for use in JSON serializaion."""
    with open(file_path, 'r') as file:
        file_string = file.read()
        return file_string