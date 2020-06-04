from typing import Iterator, List, Optional, Sequence, Tuple, Type, Union

from vgdb.lexer import Lexer
from vgdb.sql_token import Token, TokenType
from vgdb.statement import Conjunction, CreateTable, Insert, OrderBy, Select, WhereStatement
from vgdb.type import string_to_type
from vgdb.where import Predicate, Where


class Parser:
    def __init__(self, lexer: Lexer) -> None:
        self.lexer = lexer
        self.current_token = self.lexer.next_token()
        self.next_token = self.lexer.next_token()

    def advance_token(self) -> None:
        self.current_token = self.next_token
        self.next_token = self.lexer.next_token()

    def current_token_is(self, token_type: TokenType) -> bool:
        return self.current_token is not None and self.current_token.token_type == token_type

    def current_token_in(self, token_types: Sequence[TokenType]) -> bool:
        return self.current_token is not None and self.current_token.token_type in token_types

    def expect_token_is(self, token_type: TokenType) -> Token:
        if self.current_token is None or not self.current_token.token_type == token_type:
            raise ValueError(f"expected {token_type}, was {self.current_token}")
        return self.current_token

    def expect_token_in(self, token_types: Sequence[TokenType]) -> Token:
        if self.current_token is None or self.current_token.token_type not in token_types:
            raise ValueError(f"expected any of {token_types}, was {self.current_token}")
        return self.current_token

    def parse_full_where(self) -> WhereStatement:
        where: List[Where] = []
        conjunctions: List[Conjunction] = []
        conjunction_map = {TokenType.OR: Conjunction.OR, TokenType.AND: Conjunction.AND}
        done = False
        while not done:
            where.append(self.parse_where_clause())
            if self.current_token is not None and self.current_token_in((TokenType.AND, TokenType.OR)):
                conjunctions.append(conjunction_map[self.current_token.token_type])
                self.advance_token()
            else:
                done = True
        return WhereStatement(conditions=where, conjunctions=conjunctions)

    def parse_where_clause(self) -> Where:
        token = self.expect_token_is(TokenType.IDENTIFIER)
        column = str(token.literal)
        self.advance_token()
        token = self.expect_token_in(
            (
                TokenType.EQUALS,
                TokenType.NOT_EQUALS,
                TokenType.LTEQ,
                TokenType.GTEQ,
                TokenType.LT,
                TokenType.GT,
                TokenType.LIKE,
            )
        )
        predicate = Predicate(token.literal)
        self.advance_token()
        if token.token_type == TokenType.LIKE:
            token = self.expect_token_is(TokenType.STRING)
        else:
            token = self.expect_token_in((TokenType.STRING, TokenType.INT))
        value = token.literal
        self.advance_token()
        return Where(column=column, predicate=predicate, value=value)

    def parse_select_column(self) -> List[str]:
        done = False
        columns: List[str] = []
        if self.current_token_is(TokenType.STAR):
            self.advance_token()
            return ["all"]
        while not done:
            token = self.expect_token_is(TokenType.IDENTIFIER)
            columns.append(str(token.literal))
            self.advance_token()
            if self.current_token_is(TokenType.COMMA):
                self.advance_token()
            else:
                done = True
        return columns

    def parse_int(self) -> int:
        token = self.expect_token_is(TokenType.INT)
        i = int(token.literal)
        self.advance_token()
        return i

    def parse_order_by(self) -> OrderBy:
        self.expect_token_is(TokenType.BY)
        self.advance_token()
        columns: List[str] = []
        descending: List[bool] = []
        done = False
        while not done:
            token = self.expect_token_is(TokenType.IDENTIFIER)
            columns.append(str(token.literal))
            self.advance_token()
            if self.current_token_is(TokenType.DESC):
                self.advance_token()
                descending.append(True)
            else:
                descending.append(False)
            if self.current_token_is(TokenType.COMMA):
                self.advance_token()
            else:
                done = True
        return OrderBy(columns=columns, descending=descending)

    def parse_select(self) -> Select:
        columns = self.parse_select_column()
        self.expect_token_is(TokenType.FROM)
        self.advance_token()
        token = self.expect_token_is(TokenType.IDENTIFIER)
        table_name = str(token.literal)
        self.advance_token()
        where: Optional[WhereStatement] = None
        if self.current_token_is(TokenType.WHERE):
            self.advance_token()
            where = self.parse_full_where()
        order_by: Optional[OrderBy] = None
        if self.current_token_is(TokenType.ORDER):
            self.advance_token()
            order_by = self.parse_order_by()
        limit: Optional[int] = None
        offset: Optional[int] = None
        if self.current_token_is(TokenType.LIMIT):
            self.advance_token()
            limit = self.parse_int()
            if limit < 1:
                raise ValueError("LIMIT must be a positive integer")
            if self.current_token_is(TokenType.OFFSET):
                self.advance_token()
                offset = self.parse_int()
                if offset < 0:
                    raise ValueError("OFFSET must be a positive integer")
        if self.current_token is not None and self.current_token.token_type is not TokenType.SEMICOLON:
            raise ValueError(f"Expected no more tokens, got {self.current_token}")
        return Select(
            columns=columns, table_name=table_name, where=where, limit=limit, order_by=order_by, offset=offset
        )

    def parse_insert_values(self) -> List[Union[str, int]]:
        values = []
        done = False
        while not done:
            if self.current_token is None or not any(
                self.current_token.token_type == type_ for type_ in (TokenType.STRING, TokenType.INT)
            ):
                raise ValueError(f"expected string or int value token, was {self.current_token}")
            if (
                self.current_token.token_type == TokenType.INT
                and not -2_147_483_648 <= int(self.current_token.literal) <= 2_147_483_647
            ):
                raise ValueError("int value must be a 4 byte int, between -2 147 483 648 and 2 147 483 647")
            value = self.current_token.literal
            values.append(value)
            self.advance_token()
            if self.current_token.token_type == TokenType.COMMA:
                self.advance_token()
            else:
                done = True
        return values

    def parse_insert(self) -> Insert:
        if self.current_token is None or not self.current_token.token_type == TokenType.INTO:
            raise ValueError(f"expected INTO token, was {self.current_token}")
        self.advance_token()
        if self.current_token is None or not self.current_token.token_type == TokenType.IDENTIFIER:
            raise ValueError(f"expected table identifier token, was {self.current_token}")
        table_name = str(self.current_token.literal)
        self.advance_token()
        if self.current_token is None or not self.current_token.token_type == TokenType.VALUES:
            raise ValueError(f"expected VALUES token, was {self.current_token}")
        self.advance_token()
        if self.current_token is None or not self.current_token.token_type == TokenType.LPAREN:
            raise ValueError(f"expected LPAREN token, was {self.current_token}")
        self.advance_token()
        values = self.parse_insert_values()
        if self.current_token is None or not self.current_token.token_type == TokenType.RPAREN:
            raise ValueError(f"expected RPAREN token, was {self.current_token}")
        self.advance_token()
        if self.current_token is not None and self.current_token.token_type is not TokenType.SEMICOLON:
            raise ValueError(f"Expected no more tokens, got {self.current_token}")
        return Insert(values=values, table_name=table_name)

    def parse_create_table_columns(self) -> List[Tuple[str, Type]]:
        columns: List[Tuple[str, Type]] = []
        done = False
        self.expect_token_is(TokenType.LPAREN)
        self.advance_token()
        while not done:
            token = self.expect_token_is(TokenType.IDENTIFIER)
            column_name = str(token.literal)
            self.advance_token()
            token = self.expect_token_in((TokenType.TEXT_TYPE, TokenType.INT_TYPE))
            value = string_to_type[str(token.literal)]
            columns.append((column_name, value))
            self.advance_token()
            if self.current_token_is(TokenType.COMMA):
                self.advance_token()
            else:
                done = True
        self.expect_token_is(TokenType.RPAREN)
        self.advance_token()
        return columns

    def parse_create_table(self) -> CreateTable:
        self.expect_token_is(TokenType.TABLE)
        self.advance_token()
        token = self.expect_token_is(TokenType.IDENTIFIER)
        table_name = str(token.literal)
        self.advance_token()
        columns = self.parse_create_table_columns()
        if self.current_token is not None and self.current_token.token_type is not TokenType.SEMICOLON:
            raise ValueError(f"Expected no more tokens, got {self.current_token}")
        return CreateTable(table_name=table_name, columns=columns)

    def parse(self) -> Iterator[Union[Select, Insert, CreateTable]]:
        statement: Union[Select, Insert, CreateTable]
        while self.current_token is not None:
            if self.current_token.token_type == TokenType.SEMICOLON:
                self.advance_token()
                continue
            if self.current_token.token_type == TokenType.SELECT:
                self.advance_token()
                yield self.parse_select()
            elif self.current_token.token_type == TokenType.INSERT:
                self.advance_token()
                yield self.parse_insert()
            elif self.current_token.token_type == TokenType.CREATE:
                self.advance_token()
                yield self.parse_create_table()
            else:
                raise ValueError(f"Statement beginning with token type {self.current_token} not supported")
