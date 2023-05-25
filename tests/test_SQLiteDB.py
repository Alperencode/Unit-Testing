import sqlite3, pytest
from SQLiteDB import SQLiteDataBase

@pytest.fixture
def db():
    db = SQLiteDataBase(':memory:')
    db.cursor.execute("CREATE TABLE test (id INT, name TEXT)")
    return db

def test_ExecuteSQL_without_parameters():
    db = SQLiteDataBase(':memory:')
    db.ExecuteSQL("CREATE TABLE test (id INT, name TEXT)")
    
    db.cursor.execute("PRAGMA table_info(test)")
    table_info = db.cursor.fetchall()
    
    assert len(table_info) == 2
    assert table_info[0][1] == 'id'
    assert table_info[1][1] == 'name'

def test_ExecuteSQL_with_parameters(db):
    db.ExecuteSQL("INSERT INTO test VALUES (?, ?)", (1, 'test'))
    
    db.cursor.execute("SELECT * FROM test")
    table_info = db.cursor.fetchall()
    
    assert len(table_info) == 1
    assert table_info[0][0] == 1
    assert table_info[0][1] == 'test'

def test_AddToTable_with_arguments(db):
    db.AddToTable("test", (1, 'test'))
    
    db.cursor.execute("SELECT * FROM test")
    table_info = db.cursor.fetchall()
    
    assert len(table_info) == 1
    assert table_info[0][0] == 1
    assert table_info[0][1] == 'test'

def test_AddToTable_without_arguments(db):
    db.AddToTable("test")
    
    db.cursor.execute("SELECT * FROM test")
    table_info = db.cursor.fetchall()
    
    assert len(table_info) == 0
    with pytest.raises(IndexError):
        table_info[0][0]

def test_GetTable(db):
    db.AddToTable("test", (1, 'test'))
    
    table_info = db.GetTable("test")
    
    assert len(table_info) == 1
    assert table_info[0][0] == 1
    assert table_info[0][1] == 'test'
    

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

