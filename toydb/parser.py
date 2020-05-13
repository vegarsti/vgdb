from typing import List, Optional

from toydb.ast import Program
from toydb.lexer import Lexer
from toydb.statement import Select, Statement
from toydb.token import TokenType
from toydb.where import Predicate, Where


class Parser:
    def __init__(self, lexer: Lexer) -> None:
        self.lexer = lexer
        self.current_token = self.lexer.next_token()
        self.next_token = self.lexer.next_token()

    def read_token(self) -> None:
        self.current_token = self.next_token
        self.next_token = self.lexer.next_token()

    def parse_where(self) -> Where:
        if self.current_token is None or not self.current_token.token_type == TokenType.IDENTIFIER:
            raise ValueError(f"expected column identifier token, was {self.current_token}")
        column = self.current_token.literal
        self.read_token()
        if self.current_token is None or not any(
            self.current_token.token_type == type_
            for type_ in (TokenType.EQUALS, TokenType.NOT_EQUALS, TokenType.LTEQ, TokenType.GTEQ)
        ):
            raise ValueError(f"expected predicate token, was {self.current_token}")
        predicate = Predicate(self.current_token.literal)
        self.read_token()
        if self.current_token is None or not any(
            self.current_token.token_type == type_ for type_ in (TokenType.STRING, TokenType.INT)
        ):
            raise ValueError(f"expected string or int token, was {self.current_token}")
        value = self.current_token.literal  # TODO: make int
        self.read_token()
        return Where(column=column, predicate=predicate, value=value)

    def parse_select(self) -> Select:
        columns: List[str] = []
        if self.current_token is None or not self.current_token.token_type == TokenType.IDENTIFIER:
            raise ValueError(f"expected column identifier token, was {self.current_token}")
        while self.current_token.token_type == TokenType.IDENTIFIER:
            columns.append(self.current_token.literal)
            self.read_token()
        if self.current_token is None or not self.current_token.token_type == TokenType.FROM:
            raise ValueError(f"expected FROM token, was {self.current_token}")
        self.read_token()
        if self.current_token is None or not self.current_token.token_type == TokenType.IDENTIFIER:
            raise ValueError(f"expected table identifier token, was {self.current_token}")
        table_name = self.current_token.literal
        self.read_token()
        where: Optional[Where] = None
        if self.current_token.token_type is not None and self.current_token.token_type == TokenType.WHERE:
            self.read_token()
            where = self.parse_where()
        return Select(columns=columns, table_name=table_name, where=where)

    def parse(self) -> Program:
        statements: List[Statement] = []
        if self.current_token is None:
            return Program(statements)
        if self.current_token.token_type == TokenType.SELECT:
            self.read_token()
            statement = self.parse_select()
            statements.append(statement)
        else:
            raise ValueError("Unsupported token type")
        return Program(statements)
