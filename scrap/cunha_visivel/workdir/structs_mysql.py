from collections import defaultdict
import json
import os
import re
import time
from loguru import logger
import mysql.connector
from mysql.connector import errorcode
from pydantic import BaseModel
import uuid

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
        query = "SELECT COUNT(*) FROM PdfLink WHERE url = %s"
        self.cursor.execute(query, (url,))
        count = self.cursor.fetchone()[0]
        return count > 0

    def insert_pdf_info(self, newId: str, url: str, pdf_info: PDFInformation):
        if self.url_exists(url):
            return False
        query = """
        INSERT INTO PdfLink (id,url, hashSha512, path, name, date, year, edition)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """

        values = (
            newId,
            url,
            pdf_info.hash_sha512,
            str(pdf_info.path),
            pdf_info.name,
            pdf_info.date,
            pdf_info.year,
            pdf_info.edition,
        )
        self.cursor.execute(query, values)
        self.conn.commit()
        return True

    def insert_pdf_pages(self, pdf_id: str, pages: list[PDFPage]):
        query = """
        INSERT INTO Page (id, number, text, pdfLinkId)
        VALUES (%s, %s, %s, %s)
        """
        for page in pages:
            page_id = str(uuid.uuid4())
            values = (
                page_id,
                page.number,
                page.text,
                pdf_id
            )
            self.cursor.execute(query, values)
            time.sleep(0.001)

        self.conn.commit()

    def get_pdf_id(self, url: str) -> str:
        query = "SELECT id FROM PdfLink WHERE url = %s"
        self.cursor.execute(query, (url,))
        result = self.cursor.fetchone()
        return result[0] if result else None

    def print_tables(self):
        query = "SHOW TABLES"
        self.cursor.execute(query)
        tables = self.cursor.fetchall()
        for table in tables:
            table_name = table[0]
            print(f"\nTable: {table_name}")
            
            self.cursor.execute(f"SHOW COLUMNS FROM {table_name}")
            columns = self.cursor.fetchall()
            print("Columns:")
            for column in columns:
                print(column[0], end=" | ")
            print("\n")

    def find_or_create_inverted_index(self, word: str):
        query = "SELECT id FROM InvertedIndex WHERE word = %s"
        self.cursor.execute(query, (word,))
        result = self.cursor.fetchone()

        if not result:
            inverted_index_id = str(uuid.uuid4())
            query = """
            INSERT INTO InvertedIndex (id, word)
            VALUES (%s, %s)
            """
            values = (inverted_index_id, word)
            self.cursor.execute(query, values)
            self.conn.commit()
            time.sleep(0.001)
            logger.info(f"InvertedIndex word: {word} created.")

            return inverted_index_id

        return result[0]

    def create_page_inverted_index(self, pageId: str, invertedIndexId: str):
        find = "SELECT * from PageInvertedIndex WHERE pageId = %s AND invertedIndexId = %s"
        self.cursor.execute(find, (pageId, invertedIndexId))
        result = self.cursor.fetchone()
        if result:
            logger.info("PageInvertedIndex already exists.")
            return

        query = """
        INSERT INTO PageInvertedIndex (pageId, invertedIndexId)
        VALUES (%s, %s)
        """
        values = (pageId, invertedIndexId)
        self.cursor.execute(query, values)
        self.conn.commit()
        logger.info("PageInvertedIndex created.")
        
    def create_pdf_link_inverted_index(self, pdfLinkId: str, invertedIndexId: str):
        find = "SELECT * from PdfLinkInvertedIndex WHERE pdfLinkId = %s AND invertedIndexId = %s"
        self.cursor.execute(find, (pdfLinkId, invertedIndexId))
        result = self.cursor.fetchone()
        if result:
            logger.info("PdfLinkInvertedIndex already exists.")
            return
        
        query = """
        INSERT INTO PdfLinkInvertedIndex (pdfLinkId, invertedIndexId)
        VALUES (%s, %s)
        """
        values = (pdfLinkId, invertedIndexId)
        self.cursor.execute(query, values)
        self.conn.commit()
        logger.info("PdfLinkInvertedIndex created.")

    def invert_index(self):
        logger.info("Fetching all pages")
        # Recuperar todas as páginas e seus textos
        query = "SELECT id, pdfLinkId, text FROM Page"
        self.cursor.execute(query)
        pages = self.cursor.fetchall()

        # Construir o índice invertido
        for id, pdfLinkId, text in pages:
            palavras = re.findall(r'\b\w+\b', text.lower())
            for palavra in palavras:
                inverte_index_id = self.find_or_create_inverted_index(palavra)
                page_id = id
                self.create_page_inverted_index(page_id, inverte_index_id)
                self.create_pdf_link_inverted_index(pdfLinkId, inverte_index_id)
                logger.success("Word finished!")
                