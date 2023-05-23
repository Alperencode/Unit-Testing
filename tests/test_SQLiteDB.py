import sqlite3, pytest
from SQLiteDB import SQLiteDataBase

@pytest.fixture
def db():
    db = SQLiteDataBase(':memory:')
    return db

def test_ExecuteSQL(db):
    # Execute a SQL query
    db.ExecuteSQL("CREATE TABLE test (id INT, name TEXT)")
    
    # Fetch the table information
    db.cursor.execute("PRAGMA table_info(test)")
    table_info = db.cursor.fetchall()
    
    # Assert that the table has the expected columns
    assert len(table_info) == 2
    assert table_info[0][1] == 'id'
    assert table_info[1][1] == 'name'

class TestSanitizeName:
    @staticmethod
    def test_valid_database_name():
        database_name = "my_database"
        expected = "my_database"
        assert SQLiteDataBase.SanitizeName(database_name) == expected

    @staticmethod
    def test_database_name_with_reserved_keywords():
        database_name = "SELECT FROM"
        with pytest.raises(ValueError):
            SQLiteDataBase.SanitizeName(database_name)

    @staticmethod
    def test_database_name_with_reserved_keyword():
        database_name = "SELECT"
        with pytest.raises(ValueError):
            SQLiteDataBase.SanitizeName(database_name)

    @staticmethod
    def test_database_name_starting_with_digit():
        database_name = "2nd_database"
        with pytest.raises(ValueError):
            SQLiteDataBase.SanitizeName(database_name)

    @staticmethod
    def test_database_name_with_invalid_characters():
        database_name = "my_database#"
        expected = "my_database"
        assert SQLiteDataBase.SanitizeName(database_name) == expected

    @staticmethod
    def test_database_name_with_only_invalid_characters():
        database_name = "#@$%^&*"
        with pytest.raises(ValueError):
            SQLiteDataBase.SanitizeName(database_name)

    @staticmethod
    def test_database_name_with_control_characters():
        database_name = "my_database\n"
        expected = "my_database"
        assert SQLiteDataBase.SanitizeName(database_name) == expected

