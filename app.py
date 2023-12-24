# External packages
import streamlit as st

# Setting page layout
st.set_page_config(
    page_title="Поиск вакансий по резюме",
    page_icon="🤖",
    layout="centered",
)

source_radio = st.radio(
    "Выберите задачу", ["Поиск вакансий", "Поиск резюме"])

if source_radio == "Поиск вакансий":
    vacancy_name = st.text_area(
        "Желаемая должность", max_chars=60
    )
    cv_text = st.text_area(
        "Текст вашего резюме",
        placeholder="Введите текст своего резюме",
        height=250)
elif source_radio == "Поиск резюме":
    vacancy_name = st.text_area(
        "Название вакансии", max_chars=60
    )
    vacancy_text = st.text_area(
        "Текст вашей вакансии",
        placeholder="Введите текст своей вакансии",
        height=250)
