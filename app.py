from ui.chat_interface import build_interface
from config import download_vector_store_if_needed

def main():
    """
    Função principal que inicia a aplicação.
    """
    build_interface()

if __name__ == "__main__":
    download_vector_store_if_needed()
    main()
