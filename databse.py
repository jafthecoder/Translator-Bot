import sqlite3

database = sqlite3.connect('tgbot.db')
cursor = database.cursor()


def create_table_history():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS history(
        history_id INTEGER PRIMARY KEY AUTOINCREMENT,
        telegram_id BIGINT,
        from_lang TEXT,
        to_lang TEXT,
        original_text TEXT,
        translated_text TEXT
    )
    ''')


create_table_history()
database.commit()
database.close()