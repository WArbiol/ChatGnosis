__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
from ui.chat_interface import build_interface
from config import download_vector_store_if_needed, create_folders
import streamlit as st

@st.cache_resource
def startup_routine():
    create_folders()
    download_vector_store_if_needed()


def main():
    startup_routine()
    build_interface()

if __name__ == "__main__":
    main()
