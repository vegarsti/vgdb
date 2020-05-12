from typing import Optional

from toydb.token import Token, TokenType, keywords, operators


class Lexer:
    def __init__(self, program: str):
        self.program = program
        self.pos = 0
        self.current_character = ""

    @property
    def next_character(self) -> str:
        if len(self.program) <= self.pos:
            return ";"
        return self.program[self.pos]

    def read_char(self) -> None:
        self.current_character = self.next_character
        self.pos += 1

    def read_identifier(self) -> Token:
        start_position = self.pos
        while self.next_character.isalpha() or self.next_character == "_":
            self.read_char()
        end_position = self.pos
        identifier = self.program[start_position:end_position].lower()
        keyword_token = keywords.get(identifier)
        if keyword_token is None:
            token_type = TokenType.IDENTIFIER
        else:
            token_type = keyword_token
        self.read_char()
        return Token(token_type=token_type, literal=identifier)

    def read_string(self) -> Token:
        start_position = self.pos
        while self.next_character.isalpha():
            self.read_char()
        if not self.next_character == "'":
            raise ValueError("String needs to end with a '")
        end_position = self.pos
        self.read_char()
        return Token(token_type=TokenType.STRING, literal=self.program[start_position:end_position])

    def read_integer(self) -> Token:
        start_position = self.pos
        while self.next_character.isnumeric():
            self.read_char()
        end_position = self.pos
        self.read_char()
        return Token(token_type=TokenType.INT, literal=self.program[start_position:end_position])

    def read_operator(self) -> Token:
        start_position = self.pos
        while self.next_character != " " and self.next_character != ";":
            self.read_char()
        end_position = self.pos
        possible_operator = self.program[start_position:end_position]
        token_type = operators.get(possible_operator)
        if token_type is None:
            raise ValueError(f"{possible_operator} is not a supported operator")
        self.read_char()
        return Token(token_type=token_type, literal=possible_operator)

    def next_token(self) -> Optional[Token]:
        if self.next_character == ";":
            return None
        if self.next_character == " ":
            self.read_char()
            return self.next_token()
        elif self.next_character == "'":
            self.read_char()
            return self.read_string()
        elif self.next_character.isdigit():
            return self.read_integer()
        elif self.next_character.isdigit():
            return self.read_integer()
        elif self.next_character == "=" or self.next_character == ">" or self.next_character == "<":
            return self.read_operator()
        else:
            return self.read_identifier()
