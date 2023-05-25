from SQLiteDB import SQLiteDataBase
from book import Book

class BookDB(SQLiteDataBase):
    def __init__(self, databaseName):
        super().__init__(databaseName)
        self.CreateBookTable()

    def CreateBookTable(self):
        query = """CREATE TABLE IF NOT EXISTS books (
            isbn INTEGER PRIMARY KEY,
            title TEXT,
            author TEXT,
            publisher TEXT,
            year INTEGER,
            language TEXT
            )"""
        self.ExecuteSQL(query)

    def AddBook(self, book):
        self.AddToTable("books", (   
            book.GetISBN(),
            book.GetTitle(),
            book.GetAuthor(),
            book.GetPublisher(),
            book.GetYear(),
            book.GetLanguage()
        ))

    def GetBooks(self):
        return self.GetTable("books")

    def DeleteBook(self, isbn):
        query = "DELETE FROM books WHERE isbn = ?"
        self.ExecuteSQL(query, (isbn,))

    def SearchByArg(self, arg, value):
        """
        Example query: SELECT * FROM books WHERE (arg) LIKE (value)
        """
        query = "SELECT * FROM books WHERE {} LIKE ?".format(arg)
        self.cursor.execute(query, ('%' + str(value) + '%',))
        return self.cursor.fetchall()

    def __del__(self):
        self.conn.close()