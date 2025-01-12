import os
import sqlite3
from configparser import ConfigParser
from typing import Any, List, Optional

from ..models.models import AlleleEnum, ChromosomeEnum, GeneticData, User


class DatabaseHandler:
    def __init__(self, config_file: str):
        if not config_file:
            raise Exception("No Config file provided")
        self.config: ConfigParser = self._load_config(config_file)
        self.db_path: str = self.config.get("database", "db_path")

        if not self.db_path:
            raise ValueError("Database path not specified in the config file.")

        db_dir = os.path.dirname(self.db_path)
        if not os.path.exists(db_dir):
            os.makedirs(db_dir)

        self._initialise_tables_if_not_exist()

    def _load_config(self, config_file: str) -> ConfigParser:
        config = ConfigParser()
        if not os.path.exists(config_file):
            raise FileNotFoundError(f"Configuration file {config_file} not found.")
        config.read(config_file)
        return config

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        return conn

    def _close(self, conn: sqlite3.Connection) -> None:
        if conn:
            conn.close()

    def initialise_genetic_data_table(
        self, conn: sqlite3.Connection, cursor: sqlite3.Cursor
    ) -> None:
        create_table_query = """
            CREATE TABLE IF NOT EXISTS genetic_data_table (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            variant_id TEXT NOT NULL,
            chromosome TEXT CHECK(chromosome IN ('X', 'Y', '1', '2')) NOT NULL,
            position INTEGER NOT NULL,
            reference_allele TEXT CHECK(reference_allele IN ('A', 'G', 'C', 'T')) NOT NULL,
            alternate_allele TEXT CHECK(alternate_allele IN ('A', 'G', 'C', 'T')) NOT NULL,
            alternate_allele_frequency FLOAT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
        """

        try:
            cursor.execute(create_table_query)
            conn.commit()
        except sqlite3.DatabaseError as e:
            print(f"Error executing query: {e}")
            conn.rollback()

    def initialise_users_table(
        self, conn: sqlite3.Connection, cursor: sqlite3.Cursor
    ) -> None:
        create_table_query = """
            CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            individual_id TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );
        """

        try:
            cursor.execute(create_table_query)
            conn.commit()
        except sqlite3.DatabaseError as e:
            print(f"Error executing query: {e}")
            conn.rollback()

    def _initialise_tables_if_not_exist(self) -> None:
        conn = self._connect()
        cursor = conn.cursor()

        self.initialise_users_table(conn, cursor)
        self.initialise_genetic_data_table(conn, cursor)
        conn.close()

    def get_all_users(self) -> Optional[List[User]]:
        conn = self._connect()
        cursor = conn.cursor()

        fetch_all_users_query = """
            SELECT individual_id, id, created_at FROM users
        """

        try:
            cursor.execute(fetch_all_users_query)
            users = [
                User(username=row[0], id=row[1], date_created=row[2])
                for row in cursor.fetchall()
            ]
            # Convert each row to an instance of the User class
        except sqlite3.DatabaseError as e:
            print(f"Error executing query: {e}")
            conn.rollback()
        finally:
            self._close(conn)

        return None if not users else users

    def get_id_for_individual_id(self, individual_id: str) -> Optional[str]:
        conn = self._connect()
        cursor = conn.cursor()

        fetch_user_id = """
            SELECT id FROM users WHERE individual_id = ?
        """
        try:
            cursor.execute(fetch_user_id, (individual_id,))
            id = cursor.fetchone()
        except sqlite3.DatabaseError as e:
            print(f"Error executing query: {e}")
            conn.rollback()
            conn.close()
        return None if not id else id[0]

    def get_individual_data(
        self, individual_id: str, variants: Optional[str] = None
    ) -> Optional[Any]:
        conn = self._connect()
        cursor = conn.cursor()

        id = self.get_id_for_individual_id(individual_id)

        variants_list = None
        if variants:
            variants_list = variants.split(",")

        if id:
            fetch_genetic_data = """
                SELECT
                    variant_id,
                    chromosome,
                    position,
                    reference_allele,
                    alternate_allele,
                    alternate_allele_frequency
                FROM genetic_data_table
                WHERE user_id = ?
            """
            args = [id]

            if variants_list:
                placeholders = ", ".join("?" for _ in variants_list)
                fetch_genetic_data += f"AND variant_id IN ({placeholders})"
                args.extend(variants_list)

            try:
                cursor.execute(fetch_genetic_data, tuple(args))
                print(cursor.rowcount)
                genetic_data = [
                    GeneticData(
                        variant_id=row[0],
                        chromosome=ChromosomeEnum(row[1]),
                        position=row[2],
                        reference_allele=AlleleEnum(row[3]),
                        alternate_allele=AlleleEnum(row[4]),
                        alternate_allele_frequency=row[5],
                    )
                    for row in cursor.fetchall()
                ]
            except sqlite3.DatabaseError as e:
                print(f"Error executing query: {e}")
                conn.rollback()
            finally:
                conn.close()

            return genetic_data
        else:
            return "User not found"

    def insert_new_individual(self, new_individual_id: str) -> str:
        conn = self._connect()
        cursor = conn.cursor()

        insert_user_statement = """
            INSERT INTO users (
                individual_id
            ) VALUES (?)
        """
        args = (new_individual_id,)

        try:
            cursor.execute(insert_user_statement, args)
            conn.commit()
        except sqlite3.DatabaseError as e:
            print(f"Error executing query: {e}")
            conn.rollback()
        finally:
            self._close(conn)

        return f"User {new_individual_id} created"

    def insert_genetic_data_to_db(
        self, geneticdata_array: List[GeneticData], individual_id: str
    ) -> str:
        id = self.get_id_for_individual_id(individual_id)
        if id:
            conn = self._connect()
            cursor = conn.cursor()
            insert_row_statement = """
                    INSERT INTO genetic_data_table (
                        variant_id,
                        user_id,
                        chromosome,
                        position,
                        reference_allele,
                        alternate_allele,
                        alternate_allele_frequency
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """

            args = [
                (
                    geneticdata.variant_id,
                    id,
                    geneticdata.chromosome.value,
                    geneticdata.position,
                    geneticdata.reference_allele.value,
                    geneticdata.alternate_allele.value,
                    geneticdata.alternate_allele_frequency,
                )
                for geneticdata in geneticdata_array
            ]

            try:
                cursor.executemany(insert_row_statement, args)
                conn.commit()
            except sqlite3.DatabaseError as e:
                print(f"Error executing query: {e}")
                conn.rollback()
            finally:
                self._close(conn)
            return "Succesfully inserted data"
        else:
            return "Individual not found"
