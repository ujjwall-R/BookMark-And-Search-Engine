import sqlite3
import pandas as pd


class DBStorage():
    def __init__(self):
        self.con = sqlite3.connect("links.db")
        self.con2 = sqlite3.connect("recommendations.db")
        self.setup_tables()

    def setup_tables(self):
        cur1 = self.con.cursor()
        cur2 = self.con2.cursor()
        results_table = r"""
            CREATE TABLE IF NOT EXISTS results (
                id INTEGER PRIMARY KEY,
                query TEXT,
                rank INTEGER,
                link TEXT,
                title TEXT,
                snippet TEXT,
                html TEXT,
                created DATETIME,
                relevance INTEGER,
                UNIQUE(query, link)
            );
            """
        recommendation_table = r"""
            CREATE TABLE IF NOT EXISTS recommendations (
                id INTEGER PRIMARY KEY,
                query TEXT,
                UNIQUE(query)
            );
            """

        cur1.execute(results_table)
        self.con.commit()
        cur1.close()
        cur2.execute(recommendation_table)
        self.con2.commit()
        cur2.close()

    def query_results(self, query):
        df = pd.read_sql(
            f"select * from results where query='{query}' order by rank asc", self.con)
        return df

    def insert_row(self, values):
        cur = self.con.cursor()
        try:
            cur.execute(
                'INSERT INTO results (query, rank, link, title, snippet, html, created) VALUES(?, ?, ?, ?, ?, ?, ?)', values)
            self.con.commit()
        except sqlite3.IntegrityError:
            pass
        cur.close()

    def query_recommendations(self, query):
        df = pd.read_sql(
            f"select * from recommendations where query='{query}'", self.con2)
        return df

    def all_recommendations(self):
        df = pd.read_sql(
            f"select * from recommendations", self.con2)
        return df

    def insert_row_recommendations(self, query):
        cur = self.con2.cursor()
        try:
            cur.execute(
                'INSERT INTO recommendations (query) VALUES(?)', [query])
            self.con2.commit()
        except sqlite3.IntegrityError:
            pass
        cur.close()
