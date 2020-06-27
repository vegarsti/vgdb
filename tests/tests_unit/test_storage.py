import pytest

from vgdb.storage import InMemoryStorage, PersistentStorage


@pytest.fixture
def storage():
    name = "a"
    s = PersistentStorage(name, columns=(("a", int), ("b", str)))
    s.persist()
    yield s
    s.delete()


class TestPersistentStorage:
    def test_already_exists(self):
        pass

    def test_delete_fails_if_not_found(self):
        with pytest.raises(FileNotFoundError):
            PersistentStorage("a", columns=(("a", int), ("b", str))).delete()

    def test_delete_ok_after_created(self):
        s = PersistentStorage("a", columns=(("a", int), ("b", str)))
        s.persist()
        s.delete()

    def test_initialize_from_existing(self, storage):
        s = PersistentStorage.from_file(storage._filename)
        assert s._columns == storage._columns
        assert s._header_bytes == storage._header_bytes

    def test_initialize_from_existing_fails_if_not_exists(self):
        with pytest.raises(FileNotFoundError):
            PersistentStorage.from_file("a")

    def test_write_row(self, storage):
        row = [1, "hei"]
        storage.insert(row)
        assert list(storage.read_rows()) == [row]


class TestInMemoryStorage:
    def test_insert_read(self):
        storage = InMemoryStorage(name="a", columns=(("a", int), ("b", str)))
        row = [1, "hei"]
        storage.persist()
        storage.insert(row)
        rows = list(storage.read_rows())
        assert rows == [row]
