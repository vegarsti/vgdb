from toydb.token import Token, TokenType, keywords


class Lexer:
    def __init__(self, program: str):
        self.program = program
        self.pos = 0
        self.current_character = ""

    @property
    def next_character(self) -> str:
        if len(self.program) == self.pos:
            return ";"
        return self.program[self.pos]

    def read_char(self) -> None:
        self.current_character = self.next_character
        self.pos += 1

    def read_keyword(self) -> Token:
        start_position = self.pos
        while self.next_character.isalpha():
            self.read_char()
        end_position = self.pos
        possible_keyword = self.program[start_position:end_position].lower()
        token_type = keywords.get(possible_keyword)
        if token_type is None:
            raise ValueError(f"{possible_keyword} is not a recognized keyword")
        self.read_char()
        return Token(token_type=token_type, literal=possible_keyword)

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
        return Token(token_type=TokenType.INT, literal="1")

    def next_token(self) -> Token:
        if self.next_character == " ":
            self.read_char()
            return self.next_token()
        elif self.next_character == "'":
            self.read_char()
            return self.read_string()
        elif self.next_character.isdigit():
            return self.read_integer()
        else:
            return self.read_keyword()
