from toydb.lexer import Lexer
from toydb.token import Token, TokenType


class TestLexer:
    def test_keywords(self):
        program = """SeLeCT WhErE INsERT inTo vaLues 'abc' 1"""
        lexer = Lexer(program)
        assert lexer.next_token() == Token(token_type=TokenType.SELECT, literal="select")
        assert lexer.next_token() == Token(token_type=TokenType.WHERE, literal="where")
        assert lexer.next_token() == Token(token_type=TokenType.INSERT, literal="insert")
        assert lexer.next_token() == Token(token_type=TokenType.INTO, literal="into")
        assert lexer.next_token() == Token(token_type=TokenType.VALUES, literal="values")
        assert lexer.next_token() == Token(token_type=TokenType.STRING, literal="abc")
        assert lexer.next_token() == Token(token_type=TokenType.INT, literal="1")
