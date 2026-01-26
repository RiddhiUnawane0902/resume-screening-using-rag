from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from .vector_store import VectorStoreService

class RAGService:
    def __init__(self):
        self.vector_store_service = VectorStoreService()
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-flash-latest",
            temperature=0
        )

    def get_rag_chain(self):
        retriever = self.vector_store_service.get_retriever()
        
        system_prompt = (
            "You are a helpful assistant for resume screening. "
            "Use the following pieces of retrieved context to answer the question. "
            "If the answer is not in the context, say 'Not mentioned in resume'. "
            "Keep the answer concise."
            "\n\n"
            "{context}"
        )
        
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                ("human", "{input}"),
            ]
        )
        
        question_answer_chain = create_stuff_documents_chain(self.llm, prompt)
        rag_chain = create_retrieval_chain(retriever, question_answer_chain)
        
        return rag_chain

    def ask(self, question: str):
        chain = self.get_rag_chain()
        response = chain.invoke({"input": question})
        return response["answer"]
