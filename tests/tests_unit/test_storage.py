import pytest

from vgdb.storage import Storage


@pytest.fixture
def storage():
    name = "a"
    s = Storage(name, columns=(("a", int), ("b", str)))
    s.persist()
    yield s
    s.delete()


class TestStorage:
    def test_already_exists(self):
        pass

    def test_delete_fails_if_not_found(self):
        with pytest.raises(FileNotFoundError):
            Storage("a", columns=(("a", int), ("b", str))).delete()

    def test_delete_ok_after_created(self):
        s = Storage("a", columns=(("a", int), ("b", str)))
        s.persist()
        s.delete()

    def test_initialize_from_existing(self, storage):
        s = Storage.from_file(storage._filename)
        assert s._columns == storage._columns
        assert s._header_bytes == storage._header_bytes

    def test_initialize_from_existing_fails_if_not_exists(self):
        with pytest.raises(FileNotFoundError):
            Storage.from_file("a")

    def test_write_row(self, storage):
        row = [1, "hei"]
        storage.insert(row)
        assert list(storage.read_rows()) == [row]
