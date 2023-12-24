from config import VACANCY_DF, CV_DF, VECTORS_PATH, MODELS_PATH
import pandas as pd
from sentence_transformers import SentenceTransformer
import os
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


class RankingModel:

    def __init__(self, best_num):
        self.loaded_model_name = None
        self.current_task = None
        self.cvs = pd.read_csv(CV_DF)
        self.vacancies = pd.read_csv(VACANCY_DF)
        self.models_path = MODELS_PATH
        self.current_model = None
        self.best_num = best_num

    def model_path_by_name(self, model_name):
        model_path = self.models_path.get(model_name)

        if model_path is None:
            raise ValueError(f"Model path for {model_name} is not defined in config.py")

        return model_path

    def update_model(self, model_name):
        if self.loaded_model_name == model_name:
            return
        model_path = self.model_path_by_name(model_name)
        self.current_model = SentenceTransformer(model_path)
        self.loaded_model_name = model_name

    def vectorize_text(self, text):
        return self.current_model.encode(text)

    def get_current_vectors(self):
        table_name = self.current_task.replace("search", "") + self.loaded_model_name + ".npy"
        table_path = os.path.join(VECTORS_PATH, table_name)

        if not os.path.exists(table_path):
            raise ValueError(f"No such vectors table: {table_name}")

        return np.load(table_path)

    def get_similarity(self, text_embedding):
        vectors = self.get_current_vectors()
        similarity = cosine_similarity([text_embedding], vectors).reshape(-1)

        return similarity

    def get_relevant_candidates(self, text, model_name, task):
        if task not in ["vacancy_search", "cv_search"]:
            raise ValueError(f"No such task: {task}")

        self.current_task = task
        self.update_model(model_name)
        text_embedding = self.vectorize_text(text)
        similarity_scores = self.get_similarity(text_embedding)
        sorted_indices = np.argsort(similarity_scores)[::-1]
        best_indices = sorted_indices[:self.best_num]
        df_for_search = self.vacancies if task == "vacancy_search" \
            else self.cvs
        return df_for_search.iloc[best_indices]
