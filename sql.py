import sqlite3


class DB:
    db_name = 'server.db'

    @classmethod
    def init_db(cls):
        """
        create table in DB
        """
        db = sqlite3.connect(DB.db_name)
        sql = db.cursor()

        query = """ CREATE TABLE IF NOT EXISTS users (
            tg_id INTEGER NOT NULL PRIMARY KEY,
            first_name TEXT NOT NULL,
            city TEXT NOT NULL,
            lang TEXT NOT NULL,
            subscribe INTEGER DEFAULT 0 
        ); """

        sql.execute(query)

        db.commit()
        db.close()

    def _add_new_user(self):
        """
        add new user in database
        user attributes:
        1. tg_id
        2. first_name
        3.city
        4.lang
        """

        db = sqlite3.connect(DB.db_name)
        sql = db.cursor()
        query = """
            INSERT INTO users(tg_id, first_name, city, lang) VALUES (?,?,?,?)
            """
        sql.execute(query, (self.tg_id, self.first_name, self.city, self.lang))
        db.commit()

        db.close()

    def _get_user_data(self, user_id):
        """

        :param user_id: id user in telegram
        :return: None if not found else tuple with user data(tg_id, first name, city, lang, subscribe)
        """
        db = sqlite3.connect(DB.db_name)
        sql = db.cursor()

        query = """
            SELECT tg_id, first_name, city, lang, subscribe FROM users WHERE tg_id = (?);
        """
        user_data = sql.execute(query, (user_id,)).fetchone()

        return user_data

    def _update_user_data(self, user_id, column, value):
        """

        :param user_id: id of user telegram it is searched in db
        :param column: which column will be changed
        :param value: what will be changed
        """
        db = sqlite3.connect(DB.db_name)
        sql = db.cursor()

        query = f"""
            UPDATE users SET {column} = ? WHERE tg_id = ?
        """
        sql.execute(query, (value, user_id))
        db.commit()

