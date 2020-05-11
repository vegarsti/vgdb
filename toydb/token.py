from dataclasses import dataclass
from enum import Enum


class TokenType(Enum):
    INT = "int"
    STRING = "string"
    SELECT = "select"
    WHERE = "where"
    INSERT = "insert"
    INTO = "into"
    VALUES = "values"
    EQUALS = "="
    GT = ">"
    LT = "<"
    GTEQ = ">="
    LTEQ = "<="


keywords = {
    "select": TokenType.SELECT,
    "where": TokenType.WHERE,
    "insert": TokenType.INSERT,
    "into": TokenType.INTO,
    "values": TokenType.VALUES,
}

operators = {"=": TokenType.EQUALS, ">": TokenType.GT, "<": TokenType.LT, ">=": TokenType.GTEQ, "<=": TokenType.LTEQ}


@dataclass
class Token:
    token_type: TokenType
    literal: str

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Token):
            return False
        return self.token_type == other.token_type and self.literal == other.literal
