
import os
import json
import sqlite3


# Find the project folder
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Database location
DATABASE_PATH = os.path.join(BASE_DIR, "data", "jitendex.db")


def convert_row(row):
    """Convert a database row into a Python dictionary."""

    return {
        "word": row["word"],
        "reading": row["reading"],
        "term_tags": row["term_tags"],
        "rules": row["rules"],
        "score": row["score"],
        "entry_id": row["entry_id"],
        "part_of_speech": json.loads(row["part_of_speech"]),
        "definitions": json.loads(row["definitions"]),
        "examples": json.loads(row["examples"]),
        "attribution": json.loads(row["attribution"])
    }


def search_word(word):
    """Search dictionary entries by Japanese word."""

    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT *
            FROM terms
            WHERE word = ?
        """, (word,))

        rows = cursor.fetchall()

        results = []

        for row in rows:
            results.append(convert_row(row))

        return results

    finally:
        connection.close()


def search_reading(reading):
    """Search dictionary entries by reading."""

    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT *
            FROM terms
            WHERE reading = ?
        """, (reading,))

        rows = cursor.fetchall()

        results = []

        for row in rows:
            results.append(convert_row(row))

        return results

    finally:
        connection.close()


def get_word_count():
    """Count all dictionary entries."""

    connection = sqlite3.connect(DATABASE_PATH)

    try:
        cursor = connection.cursor()

        cursor.execute("SELECT COUNT(*) FROM terms")

        result = cursor.fetchone()

        return result[0]

    finally:
        connection.close()
