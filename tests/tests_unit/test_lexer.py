from toydb.lexer import Lexer
from toydb.token import Token, TokenType


class TestLexer:
    def test_lexer(self):
        program = """SeLeCT WhErE INsERT inTo vaLues 'abc' 1 2 3 1234 = < > <= >= a_column_name another FROM b !=;"""
        lexer = Lexer(program)
        assert lexer.next_token() == Token(token_type=TokenType.SELECT, literal="select")
        assert lexer.next_token() == Token(token_type=TokenType.WHERE, literal="where")
        assert lexer.next_token() == Token(token_type=TokenType.INSERT, literal="insert")
        assert lexer.next_token() == Token(token_type=TokenType.INTO, literal="into")
        assert lexer.next_token() == Token(token_type=TokenType.VALUES, literal="values")
        assert lexer.next_token() == Token(token_type=TokenType.STRING, literal="abc")
        assert lexer.next_token() == Token(token_type=TokenType.INT, literal="1")
        assert lexer.next_token() == Token(token_type=TokenType.INT, literal="2")
        assert lexer.next_token() == Token(token_type=TokenType.INT, literal="3")
        assert lexer.next_token() == Token(token_type=TokenType.INT, literal="1234")
        assert lexer.next_token() == Token(token_type=TokenType.EQUALS, literal="=")
        assert lexer.next_token() == Token(token_type=TokenType.LT, literal="<")
        assert lexer.next_token() == Token(token_type=TokenType.GT, literal=">")
        assert lexer.next_token() == Token(token_type=TokenType.LTEQ, literal="<=")
        assert lexer.next_token() == Token(token_type=TokenType.GTEQ, literal=">=")
        assert lexer.next_token() == Token(token_type=TokenType.IDENTIFIER, literal="a_column_name")
        assert lexer.next_token() == Token(token_type=TokenType.IDENTIFIER, literal="another")
        assert lexer.next_token() == Token(token_type=TokenType.FROM, literal="from")
        assert lexer.next_token() == Token(token_type=TokenType.IDENTIFIER, literal="b")
        assert lexer.next_token() == Token(token_type=TokenType.NOT_EQUALS, literal="!=")
        assert lexer.next_token() is None
        assert lexer.next_token() is None
