import pytest

from toydb.command import Command, Insert


class TestCommand:
    def test_command_is_abstract(self):
        with pytest.raises(TypeError):
            Command()

    def test_insert(self):
        assert Insert(key="a", value="b").string == "i"
