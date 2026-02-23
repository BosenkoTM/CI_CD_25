#!/usr/bin/env python3
"""
ETL-загрузчик: читает taxi_rides.csv и загружает в PostgreSQL.
Запускается как init-контейнер (loader) после healthy-статуса БД.
"""

import csv
import os
import sys
import time

import psycopg2

# --- Настройки из переменных окружения ---
DB_HOST = os.getenv("DB_HOST", "db")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("POSTGRES_DB", "taxi")
DB_USER = os.getenv("POSTGRES_USER", "taxi_user")
DB_PASS = os.getenv("POSTGRES_PASSWORD", "changeme")
CSV_PATH = os.getenv("CSV_PATH", "/data/taxi_rides.csv")

DDL = """
CREATE TABLE IF NOT EXISTS rides (
    ride_id      INT PRIMARY KEY,
    timestamp    TIMESTAMP NOT NULL,
    hour         SMALLINT NOT NULL,
    day_of_week  VARCHAR(12) NOT NULL,
    pickup       VARCHAR(50) NOT NULL,
    dropoff      VARCHAR(50) NOT NULL,
    passengers   SMALLINT NOT NULL,
    distance_km  REAL NOT NULL,
    duration_min INT NOT NULL,
    fare_rub     INT NOT NULL
);
"""


def wait_for_db(max_retries: int = 30, delay: int = 2) -> psycopg2.extensions.connection:
    """Ожидание готовности PostgreSQL."""
    for attempt in range(1, max_retries + 1):
        try:
            conn = psycopg2.connect(
                host=DB_HOST, port=DB_PORT,
                dbname=DB_NAME, user=DB_USER, password=DB_PASS,
            )
            print(f"[loader] БД доступна (попытка {attempt})")
            return conn
        except psycopg2.OperationalError:
            print(f"[loader] Ожидание БД... ({attempt}/{max_retries})")
            time.sleep(delay)
    print("[loader] БД недоступна, завершение.")
    sys.exit(1)


def load_csv(conn: psycopg2.extensions.connection) -> int:
    """Загрузка CSV в таблицу rides."""
    cur = conn.cursor()
    cur.execute(DDL)
    conn.commit()

    cur.execute("SELECT COUNT(*) FROM rides;")
    if cur.fetchone()[0] > 0:
        print("[loader] Таблица уже содержит данные — пропуск загрузки.")
        return 0

    count = 0
    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            cur.execute(
                """
                INSERT INTO rides
                    (ride_id, timestamp, hour, day_of_week, pickup,
                     dropoff, passengers, distance_km, duration_min, fare_rub)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                ON CONFLICT (ride_id) DO NOTHING;
                """,
                (
                    int(row["ride_id"]),
                    row["timestamp"],
                    int(row["hour"]),
                    row["day_of_week"],
                    row["pickup_district"],
                    row["dropoff_district"],
                    int(row["passengers"]),
                    float(row["distance_km"]),
                    int(row["duration_min"]),
                    int(row["fare_rub"]),
                ),
            )
            count += 1

    conn.commit()
    cur.close()
    print(f"[loader] Загружено {count} строк в таблицу rides.")
    return count


def main() -> None:
    conn = wait_for_db()
    try:
        load_csv(conn)
    finally:
        conn.close()
    print("[loader] Готово.")


if __name__ == "__main__":
    main()
