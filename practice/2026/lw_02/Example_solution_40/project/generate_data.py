#!/usr/bin/env python3
"""
Генератор синтетических данных: поездки такси-парка.
Вариант 40 — Логистика / Управление парком такси / Анализ пиковых часов спроса.

Запуск: python generate_data.py
Результат: data/taxi_rides.csv
"""

import csv
import os
import random
from datetime import datetime, timedelta

SEED = 42
NUM_ROWS = 5_000
OUTPUT_DIR = "data"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "taxi_rides.csv")

# --- Параметры генерации ---

DISTRICTS = [
    "Центр", "Вокзал", "Аэропорт", "Спальный-Север",
    "Спальный-Юг", "Промзона", "ТЦ-Мега", "Университет",
]

# Весовое распределение поездок по часам (имитация пиков утро/вечер)
HOUR_WEIGHTS = {
    0: 2, 1: 1, 2: 1, 3: 1, 4: 2, 5: 4,
    6: 8, 7: 14, 8: 18, 9: 15, 10: 10, 11: 9,
    12: 11, 13: 12, 14: 10, 15: 9, 16: 11, 17: 16,
    18: 19, 19: 15, 20: 10, 21: 7, 22: 5, 23: 3,
}

random.seed(SEED)


def weighted_hour() -> int:
    """Выбор часа с учётом весов (пиковые часы чаще)."""
    hours = list(HOUR_WEIGHTS.keys())
    weights = list(HOUR_WEIGHTS.values())
    return random.choices(hours, weights=weights, k=1)[0]


def random_datetime(start: datetime, end: datetime, hour: int) -> datetime:
    """Случайная дата в диапазоне с заданным часом."""
    delta_days = (end - start).days
    day = start + timedelta(days=random.randint(0, delta_days))
    minute = random.randint(0, 59)
    second = random.randint(0, 59)
    return day.replace(hour=hour, minute=minute, second=second)


def generate() -> None:
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    start_date = datetime(2024, 1, 1)
    end_date = datetime(2024, 12, 31)

    fieldnames = [
        "ride_id",
        "timestamp",
        "hour",
        "day_of_week",
        "pickup_district",
        "dropoff_district",
        "passengers",
        "distance_km",
        "duration_min",
        "fare_rub",
    ]

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for i in range(1, NUM_ROWS + 1):
            hour = weighted_hour()
            dt = random_datetime(start_date, end_date, hour)
            distance = round(random.uniform(1.0, 35.0), 1)
            duration = round(distance * random.uniform(1.8, 4.5), 0)
            fare = round(100 + distance * random.uniform(12, 22) + duration * 2, 0)

            writer.writerow(
                {
                    "ride_id": i,
                    "timestamp": dt.strftime("%Y-%m-%d %H:%M:%S"),
                    "hour": hour,
                    "day_of_week": dt.strftime("%A"),
                    "pickup_district": random.choice(DISTRICTS),
                    "dropoff_district": random.choice(DISTRICTS),
                    "passengers": random.randint(1, 4),
                    "distance_km": distance,
                    "duration_min": int(duration),
                    "fare_rub": int(fare),
                }
            )

    print(f"Сгенерировано {NUM_ROWS} записей → {OUTPUT_FILE}")


if __name__ == "__main__":
    generate()
