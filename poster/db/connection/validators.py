"""
File will hold all connection validations
1 - All keys exists or not
2 - All values have data or None data
3 - Validate connection so if anyone needs to test connection
"""

LIST_OF_KEYS = ["host", "port", "database", "user", "password"]


def validate_keys(connection_obj: dict) -> None:
    """
    method will be responsible for validating connection object if valid or not
    and if empty values
    :connection_obj dict: will hold connection object which will be validated
    :return: true if all validations passed
    """
    for elem in connection_obj.keys():
        if elem not in LIST_OF_KEYS:
            raise KeyError(f"Invalid Key {elem}")
    missing_connection_keys = list(set(LIST_OF_KEYS) - set(connection_obj.keys()))
    if missing_connection_keys:
        raise AttributeError(f"Missing Key {','.join(missing_connection_keys)}")


def validate_not_none(connection_obj: dict) -> None:
    for key in LIST_OF_KEYS:
        if not connection_obj.get(key, None):
            raise AttributeError(f"{key} can not be none or empty")
