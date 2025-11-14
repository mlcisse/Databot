import streamlit as st
import os
import json

from src.app.project import Project
from src.app.speech2text import Speech2Text
from src.utils.session_state_keys import APP, NLP_LANGUAGE, NLP_STT_HF_MODEL, OPENAI_API_KEY, OPENAI_MODEL_NAME


class App:
    CONFIG_FILE = 'databot_config.json'

    def __init__(self):
        self.properties: dict = {
            OPENAI_API_KEY: None,
            OPENAI_MODEL_NAME: 'gpt-4o-mini',
            NLP_LANGUAGE: 'en',  # used for the speech2text component, there is 1 for all the projects
            NLP_STT_HF_MODEL: 'openai/whisper-tiny',
        }
        self.projects: list[Project] = []
        self.speech2text: Speech2Text = Speech2Text(self)
        self.load_config()

    def load_config(self):
        """Charge la configuration depuis le fichier"""
        if os.path.exists(self.CONFIG_FILE):
            try:
                with open(self.CONFIG_FILE, 'r') as f:
                    config = json.load(f)
                    self.properties.update(config)
                    print(f"DEBUG: Configuration chargée depuis {self.CONFIG_FILE}")
                    print(f"DEBUG: API Key chargée: {self.properties.get(OPENAI_API_KEY, 'None')}")
            except Exception as e:
                print(f"DEBUG: Erreur lors du chargement de la config: {e}")

    def save_config(self):
        """Sauvegarde la configuration dans le fichier"""
        try:
            with open(self.CONFIG_FILE, 'w') as f:
                json.dump(self.properties, f, indent=2)
                print(f"DEBUG: Configuration sauvegardée dans {self.CONFIG_FILE}")
        except Exception as e:
            print(f"DEBUG: Erreur lors de la sauvegarde de la config: {e}")

    def add_project(self, project: Project):
        self.projects.append(project)

    def get_project(self, name: str):
        for project in self.projects:
            if project.name == name:
                return project
        return None

    def delete_project(self, project: Project):
        index = self.projects.index(project)
        self.projects.remove(project)
        if self.projects:
            return self.projects[max(index-1, 0)]
        else:
            return None


def create_app():
    _app = App()
    return _app


def get_app():
    if APP not in st.session_state:
        st.session_state[APP] = create_app()
    return st.session_state[APP]
