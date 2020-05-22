from typing import Dict, Type

type_to_string: Dict[Type, str] = {str: "text", int: "int"}
string_to_type: Dict[str, Type] = {"text": str, "int": int}
