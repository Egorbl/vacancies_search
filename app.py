# External packages
import streamlit as st
from src.ranking import RankingModel

# Setting page layout
st.set_page_config(
    page_title="Поиск вакансий по резюме",
    page_icon="🤖",
    layout="centered",
)

task = st.radio(
    "Выберите задачу", ["Поиск вакансий", "Поиск резюме"])

model_name = st.radio(
    "Модель", ["distiluse", "miniLM", "rubert"])

final_text = ""
task_name = None

if task == "Поиск вакансий":
    task_name = "vacancy_search"
    position_name = st.text_area(
        "Желаемая должность", max_chars=60
    )
    skills = st.text_area(
        "Релевантные навыки",
        height=100)
    work_experience = st.text_area(
        "Опыт работы",
        height=100)
    education = st.text_area(
        "Образование",
        height=100)
    final_text = position_name + " Навыки: " + skills + " Опыт работы: " + work_experience + \
                 " Образование: " + education

    button_text = 'Найти подходящие вакансии'
else:
    task_name = "cv_search"
    vacancy_name = st.text_area(
        "Название вакансии", max_chars=60
    )
    position_requirements = st.text_area(
        "Требования к кандидату",
        height=100)
    position_responsibilities = st.text_area(
        "Обязанности",
        height=100
    )
    final_text = vacancy_name + " Требования: " + position_requirements +\
                 " Обязанности: " + position_responsibilities

    button_text = 'Найти подходящих кандидатов'

if st.button(button_text):
    model = RankingModel(10)
    best_candidates = model.get_relevant_candidates(final_text, model_name, task_name)
    st.write(best_candidates)
