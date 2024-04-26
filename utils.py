import ast

def convert_text_2_tuple(str):
    # Convert string to a tuple using ast.literal_eval
        try:
            size_tuple = ast.literal_eval(str)
            if isinstance(size_tuple, tuple) and len(size_tuple) == 2:
                return size_tuple
            else:
                print("Invalid tuple format")
        except (SyntaxError, ValueError) as e:
            print(f"Error: {e}")     