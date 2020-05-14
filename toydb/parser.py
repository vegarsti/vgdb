from typing import List, Optional, Union

from toydb.ast import Program
from toydb.lexer import Lexer
from toydb.statement import Insert, Select
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
        column = str(self.current_token.literal)
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
        value = self.current_token.literal
        self.read_token()
        return Where(column=column, predicate=predicate, value=value)

    def parse_select_column(self) -> List[str]:
        done = False
        columns: List[str] = []
        while not done:
            if self.current_token is None or not self.current_token.token_type == TokenType.IDENTIFIER:
                raise ValueError(f"expected column identifier token, was {self.current_token}")
            columns.append(str(self.current_token.literal))
            self.read_token()
            if self.current_token.token_type == TokenType.COMMA:
                self.read_token()
            else:
                done = True
        return columns

    def parse_select(self) -> Select:
        if self.current_token is None or not self.current_token.token_type == TokenType.IDENTIFIER:
            raise ValueError(f"expected column identifier token, was {self.current_token}")
        columns = self.parse_select_column()
        if self.current_token is None or not self.current_token.token_type == TokenType.FROM:
            raise ValueError(f"expected FROM token, was {self.current_token}")
        self.read_token()
        if self.current_token is None or not self.current_token.token_type == TokenType.IDENTIFIER:
            raise ValueError(f"expected table identifier token, was {self.current_token}")
        table_name = str(self.current_token.literal)
        self.read_token()
        where: Optional[Where] = None
        if self.current_token is not None and self.current_token.token_type == TokenType.WHERE:
            self.read_token()
            where = self.parse_where()
        return Select(columns=columns, table_name=table_name, where=where)

    def parse_insert_values(self) -> List[Union[str, int]]:
        values = []
        done = False
        while not done:
            if self.current_token is None or not any(
                self.current_token.token_type == type_ for type_ in (TokenType.STRING, TokenType.INT)
            ):
                raise ValueError(f"expected string or int token, was {self.current_token}")
            value = self.current_token.literal
            values.append(value)
            self.read_token()
            if self.current_token.token_type == TokenType.COMMA:
                self.read_token()
            else:
                done = True
        return values

    def parse_insert(self) -> Insert:
        if self.current_token is None or not self.current_token.token_type == TokenType.INTO:
            raise ValueError(f"expected INTO token, was {self.current_token}")
        self.read_token()
        if self.current_token is None or not self.current_token.token_type == TokenType.IDENTIFIER:
            raise ValueError(f"expected table identifier token, was {self.current_token}")
        table_name = str(self.current_token.literal)
        self.read_token()
        if self.current_token is None or not self.current_token.token_type == TokenType.VALUES:
            raise ValueError(f"expected VALUES token, was {self.current_token}")
        self.read_token()
        if self.current_token is None or not self.current_token.token_type == TokenType.LPAREN:
            raise ValueError(f"expected LPAREN token, was {self.current_token}")
        self.read_token()
        values = self.parse_insert_values()
        print(self.current_token)
        if self.current_token is None or not self.current_token.token_type == TokenType.RPAREN:
            raise ValueError(f"expected RPAREN token, was {self.current_token}")
        self.read_token()
        return Insert(values=values, table_name=table_name)

    def parse(self) -> Program:
        statements: List[Union[Select, Insert]] = []
        statement: Union[Select, Insert]
        if self.current_token is None:
            return Program(statements)
        if self.current_token.token_type == TokenType.SELECT:
            self.read_token()
            statement = self.parse_select()
        elif self.current_token.token_type == TokenType.INSERT:
            self.read_token()
            statement = self.parse_insert()
        else:
            raise ValueError("Unsupported token type")
        statements.append(statement)
        return Program(statements)
