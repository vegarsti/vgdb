from dataclasses import dataclass
from enum import Enum
from typing import Union


class TokenType(Enum):
    INT = "int"
    STRING = "string"
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


keywords = {
    "select": TokenType.SELECT,
    "where": TokenType.WHERE,
    "insert": TokenType.INSERT,
    "into": TokenType.INTO,
    "values": TokenType.VALUES,
    "from": TokenType.FROM,
}

operators = {
    "=": TokenType.EQUALS,
    ">": TokenType.GT,
    "<": TokenType.LT,
    ">=": TokenType.GTEQ,
    "<=": TokenType.LTEQ,
    "!=": TokenType.NOT_EQUALS,
}


@dataclass
class Token:
    token_type: TokenType
    literal: Union[int, str]

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Token):
            return False
        return self.token_type == other.token_type and self.literal == other.literal
