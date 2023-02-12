import sqlite3


def insert_translate_history(telegram_id, src, dest, org_text, tr_text):
    database = sqlite3.connect('tgbot.db')
    cursor = database.cursor()
    cursor.execute('''
    INSERT INTO history(telegram_id, from_lang, to_lang, original_text, translated_text)
    VALUES (?,?,?,?,?)
    ''', (telegram_id, src, dest, org_text, tr_text))
    database.commit()
    database.close()


def select_history(tg_id):
    database = sqlite3.connect('tgbot.db')
    cursor = database.cursor()
    cursor.execute('''
    SELECT from_lang, to_lang, original_text, translated_text
    FROM history
    WHERE telegram_id = ?
    ''', (tg_id,))
    translates = cursor.fetchall()
    database.close()
    return translates