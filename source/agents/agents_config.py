import autogen

# build the gpt_configuration object
# AutoGen config list
config_list = autogen.config_list_from_dotenv(
    dotenv_file_path=".env",
    model_api_key_map={
        "gpt-4-1106-preview": "OPENAI_API_KEY",
    },
    filter_dict={
        "model": {
            "gpt-4-1106-preview",
        }
    },
)

# Base Configuration
base_config = {
    # "use_cache": False,
    "temperature": 0,
    "config_list": config_list,
    "timeout": 250,
}

# Configuration with "write_file"
write_file_config = {
    **base_config,  # Inherit base configuration
    "functions": [
        {
            "name": "write_file",
            "description": "Write a file to the filesystem",
            "parameters": {
                "type": "object",
                "properties": {
                    "fname": {
                        "type": "string",
                        "description": "The name of the file to write",
                    },
                    "content": {
                        "type": "string",
                        "description": "The content of the file to write",
                    },
                },
                "required": ["fname", "content"],
            },
        }
    ],
}

# Configuration with "write_json_file"
write_json_file_config = {
    **base_config,  # Inherit base configuration
    "functions": [
        {
            "name": "write_json_file",
            "description": "Write a json file to the filesystem",
            "parameters": {
                "type": "object",
                "properties": {
                    "fname": {
                        "type": "string",
                        "description": "The name of the file to write",
                    },
                    "json_str": {
                        "type": "string",
                        "description": "The content of the file to write",
                    },
                },
                "required": ["fname", "json_str"],
            },
        }
    ],
}
