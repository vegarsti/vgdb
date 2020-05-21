from toydb.lexer import Lexer
from toydb.sql_token import Token, TokenType


class TestLexer:
    def test_lexer(self):
        program = (
            "SeLeCT WhErE INsERT inTo vaLues 'abc' 'a b' 1, 2, 3 1234 = ('a', 'b', 1) < > <= "
            ">= a_column_name another ( ) FROM b != CREATE TABLE TEXT INT * and or ;"
        )
        lexer = Lexer(program)
        assert lexer.next_token() == Token(token_type=TokenType.SELECT, literal="select")
        assert lexer.next_token() == Token(token_type=TokenType.WHERE, literal="where")
        assert lexer.next_token() == Token(token_type=TokenType.INSERT, literal="insert")
        assert lexer.next_token() == Token(token_type=TokenType.INTO, literal="into")
        assert lexer.next_token() == Token(token_type=TokenType.VALUES, literal="values")
        assert lexer.next_token() == Token(token_type=TokenType.STRING, literal="abc")
        assert lexer.next_token() == Token(token_type=TokenType.STRING, literal="a b")
        assert lexer.next_token() == Token(token_type=TokenType.INT, literal=1)
        assert lexer.next_token() == Token(token_type=TokenType.COMMA, literal=",")
        assert lexer.next_token() == Token(token_type=TokenType.INT, literal=2)
        assert lexer.next_token() == Token(token_type=TokenType.COMMA, literal=",")
        assert lexer.next_token() == Token(token_type=TokenType.INT, literal=3)
        assert lexer.next_token() == Token(token_type=TokenType.INT, literal=1234)
        assert lexer.next_token() == Token(token_type=TokenType.EQUALS, literal="=")
        assert lexer.next_token() == Token(token_type=TokenType.LPAREN, literal="(")
        assert lexer.next_token() == Token(token_type=TokenType.STRING, literal="a")
        assert lexer.next_token() == Token(token_type=TokenType.COMMA, literal=",")
        assert lexer.next_token() == Token(token_type=TokenType.STRING, literal="b")
        assert lexer.next_token() == Token(token_type=TokenType.COMMA, literal=",")
        assert lexer.next_token() == Token(token_type=TokenType.INT, literal=1)
        assert lexer.next_token() == Token(token_type=TokenType.RPAREN, literal=")")
        assert lexer.next_token() == Token(token_type=TokenType.LT, literal="<")
        assert lexer.next_token() == Token(token_type=TokenType.GT, literal=">")
        assert lexer.next_token() == Token(token_type=TokenType.LTEQ, literal="<=")
        assert lexer.next_token() == Token(token_type=TokenType.GTEQ, literal=">=")
        assert lexer.next_token() == Token(token_type=TokenType.IDENTIFIER, literal="a_column_name")
        assert lexer.next_token() == Token(token_type=TokenType.IDENTIFIER, literal="another")
        assert lexer.next_token() == Token(token_type=TokenType.LPAREN, literal="(")
        assert lexer.next_token() == Token(token_type=TokenType.RPAREN, literal=")")
        assert lexer.next_token() == Token(token_type=TokenType.FROM, literal="from")
        assert lexer.next_token() == Token(token_type=TokenType.IDENTIFIER, literal="b")
        assert lexer.next_token() == Token(token_type=TokenType.NOT_EQUALS, literal="!=")
        assert lexer.next_token() == Token(token_type=TokenType.CREATE, literal="create")
        assert lexer.next_token() == Token(token_type=TokenType.TABLE, literal="table")
        assert lexer.next_token() == Token(token_type=TokenType.TEXT_TYPE, literal="text")
        assert lexer.next_token() == Token(token_type=TokenType.INT_TYPE, literal="int")
        assert lexer.next_token() == Token(token_type=TokenType.STAR, literal="*")
        assert lexer.next_token() == Token(token_type=TokenType.AND, literal="and")
        assert lexer.next_token() == Token(token_type=TokenType.OR, literal="or")
        assert lexer.next_token() is None
        assert lexer.next_token() is None
