import json

import yaml


def write_file(fname, content):
    """
    Write content to a file.

    Args:
        fname (str): The name of the file to write to.
        content (str): The content to write to the file.
    """
    with open(fname, "w") as f:
        f.write(content)


def write_json_file(fname, json_str: str):
    """
    Write content to a JSON file.

    Args:
        fname (str): The name of the file to write to.
        json_str (str): The JSON string to write to the file.
    """
    # convert ' to "
    json_str = json_str.replace("'", '"')

    # Convert the string to a Python object
    data = json.loads(json_str)

    # Write the Python object to the file as JSON
    with open(fname, "w") as f:
        json.dump(data, f, indent=4)


def write_yml_file(fname, json_str: str):
    """
    Write content to a YAML file.

    Args:
        fname (str): The name of the file to write to.
        json_str (str): The JSON string to write to the file.
    """
    # Try to replace single quotes with double quotes for JSON
    cleaned_json_str = json_str.replace("'", '"')

    # Safely convert the JSON string to a Python object
    try:
        data = json.loads(cleaned_json_str)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return

    # Write the Python object to the file as YAML
    with open(fname, "w") as f:
        yaml.dump(data, f)
