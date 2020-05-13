from typing import List

from toydb.ast import Program
from toydb.lexer import Lexer
from toydb.statement import Select, Statement
from toydb.token import TokenType


class Parser:
    def __init__(self, lexer: Lexer) -> None:
        self.lexer = lexer
        self.current_token = self.lexer.next_token()
        self.next_token = self.lexer.next_token()

    def read_token(self) -> None:
        self.current_token = self.next_token
        self.next_token = self.lexer.next_token()

    def parse_select(self) -> Select:
        # invariant: previous token was select
        # read column names
        columns: List[str] = []
        if self.current_token is None or not self.current_token.token_type == TokenType.IDENTIFIER:
            raise ValueError("expected column identifier")
        while self.current_token.token_type == TokenType.IDENTIFIER:
            columns.append(self.current_token.literal)
            self.read_token()
        if self.current_token is None or not self.current_token.token_type == TokenType.FROM:
            raise ValueError("expected FROM")
        self.read_token()
        if self.current_token is None or not self.current_token.token_type == TokenType.IDENTIFIER:
            raise ValueError("expected table identifier")
        table_name = self.current_token.literal
        self.read_token()
        # do not read where yet
        statement = Select(columns=columns, table_name=table_name)
        return statement

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
