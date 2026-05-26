# chatbot/services/chatbot_service.py
from langchain_community.llms import Ollama
from langchain_classic.chains import ConversationalRetrievalChain
# from langchain.chains import ConversationalRetrievalChain
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings


class CHRONOSIAChatbot:
    """
    Chatbot con RAG (Retrieval Augmented Generation).
    Responde preguntas sobre fichas, docentes, horarios
    usando los datos reales del sistema como contexto.
    """

    def __init__(self):
        self.llm = Ollama(model='llama3')
        self.embeddings = OllamaEmbeddings(model='llama3')
        self.vectorstore = Chroma(
            embedding_function=self.embeddings,
            persist_directory='./chroma_db',
        )
        self.chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=self.vectorstore.as_retriever(),
        )

    def responder(self, pregunta: str, historial: list) -> str:
        resultado = self.chain({
            'question': pregunta,
            'chat_history': historial,
        })
        return resultado['answer']