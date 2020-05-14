import dataclasses
from enum import Enum
from typing import Union


class TokenType(Enum):
    INT = "integer"
    STRING = "string"
    TEXT_TYPE = "text"
    INT_TYPE = "int"
    SELECT = "select"
    WHERE = "where"
    INSERT = "insert"
    INTO = "into"
    FROM = "from"
    VALUES = "values"
    EQUALS = "="
    NOT_EQUALS = "!="
    GT = ">"
    LT = "<"
    GTEQ = ">="
    LTEQ = "<="
    IDENTIFIER = "identifier"
    COMMA = ","
    LPAREN = "("
    RPAREN = ")"
    CREATE = "create"
    TABLE = "table"
    STAR = "*"


keywords = {
    "select": TokenType.SELECT,
    "where": TokenType.WHERE,
    "insert": TokenType.INSERT,
    "into": TokenType.INTO,
    "values": TokenType.VALUES,
    "from": TokenType.FROM,
    "create": TokenType.CREATE,
    "table": TokenType.TABLE,
    "text": TokenType.TEXT_TYPE,
    "int": TokenType.INT_TYPE,
    "star": TokenType.STAR,
}

operators = {
    "=": TokenType.EQUALS,
    ">": TokenType.GT,
    "<": TokenType.LT,
    ">=": TokenType.GTEQ,
    "<=": TokenType.LTEQ,
    "!=": TokenType.NOT_EQUALS,
}


@dataclasses.dataclass
class Token:
    token_type: TokenType
    literal: Union[int, str]

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Token):
            return False
        return self.token_type == other.token_type and self.literal == other.literal
