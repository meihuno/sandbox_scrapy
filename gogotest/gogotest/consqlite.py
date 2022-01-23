import sqlite3

class DBConnection():
    
    def __init__(self, dbpath='test.db') -> any:
        dbname = dbpath
        self.conn = sqlite3.connect(dbname)
        # SQLiteを操作するためのカーソルを作成
        self._create_db()
    
    def _create_db(self):
        # テーブル作成
        cursor = self.conn.cursor()
        cursor.execute(
            'CREATE TABLE IF NOT EXISTS book(\
                id INTEGER PRIMARY KEY AUTOINCREMENT, \
                name TEXT NOT NULL, \
                url TEXT UNIQUE NOT NULL, \
                refurl TEXT, \
                title TEXT NOT NULL \
            );')

    def close(self) -> any:
        self.conn.close()

    def save_book(self, item):
        """
        item を DB に保存する
        """
        if self.find_book(item['url']):
            # 既に同じURLのデータが存在する場合はスキップ
            return
        
        self.conn.execute(
            'INSERT INTO book (name, url, refurl, title) VALUES (?, ?, ?, ?)', (
                item['name'],
                item['url'],
                item['refurl'],
                item['title']
            )
        )
        self.conn.commit()

    def find_book(self, url):
        cursor = self.conn.execute(
            'SELECT * FROM book WHERE url=?',
            (url,)
        )
        return cursor.fetchone()

    def ret_find_book(self, name):
        cursor = self.conn.execute(
            'SELECT * FROM book WHERE name=?',
            (name,)
        )
        rdict = {}
        books = cursor.fetchall()
        for book in books:
            rdict[book[2]] = book[3]
        return rdict
        
if __name__ == "__main__":
    box = DBConnection()
    item1 = {'name':'book', 'url': 'http://book1', 'title': 'book1', 'refurl': 'dummy'}
    item2 = {'name':'book', 'url': 'http://book2', 'title': 'book2', 'refurl': 'dummy'}
    box.save_book(item1)
    box.save_book(item2)
    rdict = box.ret_find_book('book')
    # print(rdict)
    box.close()
