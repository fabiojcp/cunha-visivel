import os
from loguru import logger
import mysql.connector
from mysql.connector import errorcode
from pydantic import BaseModel

class PDFPage(BaseModel):
    number: int
    text: str

class PDFInformation(BaseModel):
    hash_sha512: str
    path: str
    pages: list[PDFPage]
    name: str
    date: str
    year: str
    edition: str

class RelationalDB:
    def __init__(self):
        self._connect()
    
    def _connect(self):
        try:
            self.conn = mysql.connector.connect(
                user=os.getenv('MYSQL_USER'),
                password=os.getenv('MYSQL_PASSWORD'),
                host=os.getenv('MYSQL_HOST'),
                database=os.getenv('MYSQL_DATABASE'),
                port=os.getenv('MYSQL_PORT')
            )
            self.cursor = self.conn.cursor()
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                logger.error("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                logger.error("Database does not exist")
            else:
                logger.error(err)
            raise

    def url_exists(self, url: str) -> bool:
        query = "SELECT COUNT(*) FROM pdf_links WHERE url = %s"
        self.cursor.execute(query, (url,))
        count = self.cursor.fetchone()[0]
        return count > 0

    def insert_pdf_info(self, url: str, pdf_info: PDFInformation):
        if self.url_exists(url):
            return False

        query = """
        INSERT INTO pdf_links (url, hash_sha512, path, name, date, year, edition)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            url,
            pdf_info.hash_sha512,
            pdf_info.path,
            pdf_info.name,
            pdf_info.date,
            pdf_info.year,
            pdf_info.edition,
        )
        self.cursor.execute(query, values)
        self.conn.commit()
        return True

    def insert_pdf_pages(self, pdf_id: int, pages: list[PDFPage]):
        query = """
        INSERT INTO pdf_pages (pdf_id, number, text)
        VALUES (%s, %s, %s)
        """
        for page in pages:
            values = (pdf_id, page.number, page.text)
            self.cursor.execute(query, values)
        self.conn.commit()

    def get_pdf_id(self, url: str) -> int:
        query = "SELECT id FROM pdf_links WHERE url = %s"
        self.cursor.execute(query, (url,))
        result = self.cursor.fetchone()
        return result[0] if result else None

    def print_tables(self):
        query = "SHOW TABLES"
        self.cursor.execute(query)
        tables = self.cursor.fetchall()
        for table in tables:
            table_name = table[0]
            print(f"Table: {table_name}")