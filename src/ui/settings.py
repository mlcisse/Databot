import streamlit as st

from src.app.app import get_app
from src.utils.session_state_keys import NLP_STT_HF_MODEL, OPENAI_API_KEY, OPENAI_MODEL_NAME


def settings():
    app = get_app()
    col1, col2 = st.columns([0.5, 0.5])
    with col1:
        st.header('Settings')
        api_key_input = st.text_input(
            label='OpenAI API key',
            help='Introduce your OpenAI API key',
            type='password',
            value=app.properties[OPENAI_API_KEY]
        )
        
        # Sauvegarder automatiquement si la clé a changé
        if api_key_input != app.properties[OPENAI_API_KEY]:
            app.properties[OPENAI_API_KEY] = api_key_input
            app.save_config()
            st.success("Clé API sauvegardée!")
        
        # Debug info
        if st.button("Debug API Key"):
            st.write(f"Current API Key: {app.properties[OPENAI_API_KEY]}")
            st.write(f"API Key length: {len(app.properties[OPENAI_API_KEY]) if app.properties[OPENAI_API_KEY] else 0}")
            st.write(f"API Key is None: {app.properties[OPENAI_API_KEY] is None}")
            st.write(f"API Key starts with 'sk-': {app.properties[OPENAI_API_KEY].startswith('sk-') if app.properties[OPENAI_API_KEY] else False}")
        app.properties[OPENAI_MODEL_NAME] = st.text_input(
            label='OpenAI Model Name',
            help='Introduce the name of the OpenAI model to use in the AI features. Available models: https://platform.openai.com/docs/models',
            value=app.properties[OPENAI_MODEL_NAME]
        )
        app.properties[NLP_STT_HF_MODEL] = st.text_input(
            label='Voice recognition model (HuggingFace endpoint)',
            help='Introduce a model ID from HuggingFace',
            value=app.properties[NLP_STT_HF_MODEL],
            # disabled=True
        )
