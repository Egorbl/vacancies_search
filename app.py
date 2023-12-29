# External packages
import streamlit as st
from src.ranking import RankingModel
from bs4 import BeautifulSoup


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
                 "Обязанности: " + position_responsibilities

    button_text = 'Найти подходящих кандидатов'

if st.button(button_text):
    model = RankingModel(10)
    best_candidates = model.get_relevant_candidates(final_text, model_name, task_name)

    best_candidates = best_candidates.fillna("Не указано")

    if task_name == "vacancy_search":
        html_columns = ['position_requirements','position_responsibilities']
        for col in html_columns:
            best_candidates[col] = best_candidates[col].apply(lambda x: BeautifulSoup(x, 'html.parser').get_text())

        for index, row in best_candidates.iterrows():
            st.header(row['vacancy_name'])
            st.subheader(f"**Компания:** {row['full_company_name']}")
            st.write(f"**Тип занятости:** {row['schedule_type']}, {row['busy_type']}")
            st.write(f"**Регион:** {row['regionName']}")
            st.write('\n')

            st.write(f"**Зарплата:** {row['salary']}")
            st.write(f"**Требования:** {row['position_requirements']}")

            st.write(f"**Образование:** {row['education']}")
            st.write('\n')

            st.write(f"**Обязанности:** {row['position_responsibilities']}")
            st.write(f"**Контактная информация:** {row['contact_person']}")

            st.markdown('---')
    else:
        st.title('Candidate Details')
        html_columns = ['workExperienceList']
        for col in html_columns:
            best_candidates[col] = best_candidates[col].apply(lambda x: BeautifulSoup(x, 'html.parser').get_text())

        for index, row in best_candidates.iterrows():
            st.header(f"Кандидат {index + 1}")
            st.write(f"**Пол:** {row['gender']}, **Возраст:** {row['age']}")
            st.write(f"**Зарплата:** {row['salary']}")
            st.write('\n')

            st.write(f"**Должность:** {row['positionName']}")
            st.write(f"**Место положения:** {row['localityName']}")
            st.write(f"**Занятость:** {row['busyType']}, {row['scheduleType']}")
            st.write('\n')

            st.write(f"**Hard Skills:** {row['hardSkills']}")
            st.write(f"**Soft Skills:** {row['softSkills']}")
            st.write(f"**Образование:** {row['educationList']}")
            st.write(f"**Academic Degree:** {row['academicDegree']}")
            st.write(f"**Опыт работы:** {row['workExperienceList']}")
            st.write('\n')

            st.write(f"**Готов ли к обучению:** {row['retrainingCapability']}")
            st.write(f"**Готов ли к команировкам:** {row['businessTrip']}")
            st.write(f"**Готов ли к переездам:** {row['relocation']}")

            st.markdown('---')  # Adding a horizontal line between candidates
