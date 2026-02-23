#!/usr/bin/env python3
"""
Streamlit-приложение: Heatmap визуализация пиковых часов спроса такси.
Вариант 40 — Логистика / Управление парком такси.
"""

import os

import pandas as pd
import plotly.express as px
import streamlit as st
import psycopg2

# --- Подключение к БД ---
DB_HOST = os.getenv("DB_HOST", "db")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("POSTGRES_DB", "taxi")
DB_USER = os.getenv("POSTGRES_USER", "taxi_user")
DB_PASS = os.getenv("POSTGRES_PASSWORD", "changeme")


@st.cache_data(ttl=300)
def load_data() -> pd.DataFrame:
    """Загрузка данных из PostgreSQL."""
    conn = psycopg2.connect(
        host=DB_HOST, port=DB_PORT,
        dbname=DB_NAME, user=DB_USER, password=DB_PASS,
    )
    df = pd.read_sql("SELECT * FROM rides;", conn)
    conn.close()
    return df


# --- Интерфейс ---
st.set_page_config(page_title="Такси-парк: Анализ спроса", layout="wide")
st.title("🚕 Управление парком такси — Анализ пиковых часов")

try:
    df = load_data()
except Exception as e:
    st.error(f"Не удалось подключиться к БД: {e}")
    st.info("Убедитесь, что контейнер loader завершил загрузку данных.")
    st.stop()

st.sidebar.header("Фильтры")
districts = st.sidebar.multiselect(
    "Район подачи", options=sorted(df["pickup"].unique()), default=sorted(df["pickup"].unique())
)
df_filtered = df[df["pickup"].isin(districts)]

# --- Метрики ---
col1, col2, col3, col4 = st.columns(4)
col1.metric("Всего поездок", f"{len(df_filtered):,}")
col2.metric("Средняя дистанция", f"{df_filtered['distance_km'].mean():.1f} км")
col3.metric("Средняя стоимость", f"{df_filtered['fare_rub'].mean():.0f} ₽")
col4.metric("Средняя длительность", f"{df_filtered['duration_min'].mean():.0f} мин")

# --- Heatmap: День недели × Час ---
st.subheader("Тепловая карта спроса: День недели × Час")

day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
day_labels = {
    "Monday": "Пн", "Tuesday": "Вт", "Wednesday": "Ср",
    "Thursday": "Чт", "Friday": "Пт", "Saturday": "Сб", "Sunday": "Вс",
}

pivot = (
    df_filtered.groupby(["day_of_week", "hour"])
    .size()
    .reset_index(name="rides")
)
pivot["day_of_week"] = pd.Categorical(pivot["day_of_week"], categories=day_order, ordered=True)
pivot = pivot.sort_values("day_of_week")
pivot["day_label"] = pivot["day_of_week"].map(day_labels)

heatmap = pivot.pivot(index="day_label", columns="hour", values="rides").fillna(0)
day_label_order = [day_labels[d] for d in day_order]
heatmap = heatmap.reindex(day_label_order)

fig_heat = px.imshow(
    heatmap,
    labels=dict(x="Час", y="День недели", color="Поездок"),
    color_continuous_scale="YlOrRd",
    aspect="auto",
)
fig_heat.update_layout(height=350)
st.plotly_chart(fig_heat, use_container_width=True)

# --- Гистограмма по часам ---
st.subheader("Распределение поездок по часам")
hourly = df_filtered.groupby("hour").size().reset_index(name="rides")
fig_bar = px.bar(hourly, x="hour", y="rides", labels={"hour": "Час", "rides": "Поездок"})
fig_bar.update_layout(height=300)
st.plotly_chart(fig_bar, use_container_width=True)

# --- Топ маршрутов ---
st.subheader("Топ-10 маршрутов")
routes = (
    df_filtered.groupby(["pickup", "dropoff"])
    .size()
    .reset_index(name="count")
    .sort_values("count", ascending=False)
    .head(10)
)
routes["route"] = routes["pickup"] + " → " + routes["dropoff"]
fig_routes = px.bar(routes, x="count", y="route", orientation="h",
                    labels={"count": "Поездок", "route": "Маршрут"})
fig_routes.update_layout(height=350, yaxis=dict(autorange="reversed"))
st.plotly_chart(fig_routes, use_container_width=True)

st.caption("Данные: синтетический датасет taxi_rides.csv • Streamlit + Plotly + PostgreSQL")
