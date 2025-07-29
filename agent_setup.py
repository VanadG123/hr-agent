import chromadb
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import tempfile
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def setup_agent_executor(hr_leave_policy_file, hr_travel_policy_file, sample_offer_letter_file, employee_metadata_file):
    """
    Set up the agent executor with vector embeddings from uploaded policy documents.
    
    Args:
        hr_leave_policy_file: Uploaded HR Leave & Work from Home Policy PDF
        hr_travel_policy_file: Uploaded HR Travel Policy PDF
        sample_offer_letter_file: Uploaded Sample Offer Letter PDF
        employee_metadata_file: Uploaded Employee Metadata CSV
        
    Returns:
        agent_executor: Configured agent executor for generating offer letters
    """
    
    # 1. Load policy documents from uploaded files
    docs = []
    
    # Load HR Leave & Work from Home Policy
    if hr_leave_policy_file is not None:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            tmp_file.write(hr_leave_policy_file.getvalue())
            tmp_file_path = tmp_file.name
        
        try:
            loader_pdf = PyPDFLoader(tmp_file_path)
            docs.extend(loader_pdf.load())
        finally:
            os.unlink(tmp_file_path)  # Clean up temporary file
    
    # Load HR Travel Policy
    if hr_travel_policy_file is not None:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            tmp_file.write(hr_travel_policy_file.getvalue())
            tmp_file_path = tmp_file.name
        
        try:
            loader_pdf = PyPDFLoader(tmp_file_path)
            docs.extend(loader_pdf.load())
        finally:
            os.unlink(tmp_file_path)  # Clean up temporary file
    
    # Load Sample Offer Letter (for reference)
    if sample_offer_letter_file is not None:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            tmp_file.write(sample_offer_letter_file.getvalue())
            tmp_file_path = tmp_file.name
        
        try:
            loader_pdf = PyPDFLoader(tmp_file_path)
            docs.extend(loader_pdf.load())
        finally:
            os.unlink(tmp_file_path)  # Clean up temporary file
    
    # 2. Chunk documents with metadata
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, 
        chunk_overlap=200
    )
    chunks = text_splitter.split_documents(docs)
    
    # 3. Initialize sentence transformer embeddings
    embeddings = HuggingFaceEmbeddings(
        model_name=os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2"),
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'normalize_embeddings': True}
    )
    
    # 4. Create vector store with ChromaDB
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=os.getenv("CHROMA_PERSIST_DIRECTORY", "./chroma_db")
    )
    
    # 5. Set up LLM with CogCache integration
    llm = ChatOpenAI(
        base_url="https://proxy-api.cogcache.com/v1/",
        model=os.getenv("COGCACHE_LLM_MODEL", "gpt-4o-2024-08-06"),
        openai_api_key=os.getenv("COGCACHE_API_KEY"),
        default_headers={
            "Authorization": f"Bearer {os.getenv('COGCACHE_API_KEY')}"
        },
        temperature=float(os.getenv("TEMPERATURE", "0.7"))
    )
    
    # 6. Create prompt template for offer letter generation
    prompt_template = PromptTemplate(
        input_variables=["candidate_name", "context"],
        template="""
        You are an HR professional tasked with generating a professional offer letter.
        
        Based on the following company policies and sample offer letter:
        {context}
        
        Generate a complete, professional offer letter for {candidate_name}. 
        The offer letter should include:
        
        1. Company letterhead and formal greeting
        2. Position title and department
        3. Start date and reporting structure
        4. Compensation details (salary, benefits)
        5. Leave policy highlights
        6. Travel policy highlights (if applicable)
        7. Terms and conditions
        8. Professional closing
        
        Make sure the offer letter follows the company's policies and maintains a professional tone.
        """
    )
    
    # 7. Create LLM chain
    llm_chain = LLMChain(llm=llm, prompt=prompt_template)
    
    # 8. Create agent executor
    class AgentExecutor:
        def __init__(self, vector_store, llm_chain):
            self.vector_store = vector_store
            self.llm_chain = llm_chain
        
        def invoke(self, input_dict):
            """
            Generate offer letter using the uploaded policies and sample letter.
            
            Args:
                input_dict: Dictionary containing 'input' key with the request
                
            Returns:
                Dictionary with 'output' key containing the generated offer letter
            """
            try:
                # Extract candidate name from input
                candidate_name = input_dict.get("input", "").split("for ")[-1].split(".")[0]
                
                # Retrieve relevant context from vector store
                relevant_docs = self.vector_store.similarity_search(
                    "offer letter policies benefits salary", 
                    k=5
                )
                
                # Combine relevant context
                context = "\n\n".join([doc.page_content for doc in relevant_docs])
                
                # Generate offer letter
                response = self.llm_chain.run({
                    "candidate_name": candidate_name,
                    "context": context
                })
                
                return {"output": response}
                
            except Exception as e:
                return {"output": f"Error generating offer letter: {str(e)}"}
    
    # Return the agent executor
    return AgentExecutor(vector_store, llm_chain)

# Create a default agent executor (will be updated when files are uploaded)
agent_executor = None
