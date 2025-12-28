from fastapi import FastAPI, Request
from dotenv import load_dotenv
from langchain_community.chat_models import ChatOllama
from langchain_community.embeddings import OllamaEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
from typing import List, Optional
from langchain_community.vectorstores import Chroma
import os
from mock_tickets import MOCK_TICKETS_DATA # Import the mock data
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

app = FastAPI()

# Initialize the LLM
llm = ChatOllama(model=os.getenv("OLLAMA_MODEL", "llama3.2"))

# Initialize embeddings for ChromaDB
embeddings = OllamaEmbeddings(model=os.getenv("OLLAMA_MODEL", "llama3.2"))

# Set up ChromaDB (in-memory for now)
vectorstore = Chroma(embedding_function=embeddings, persist_directory="./chroma_db")

# Ingest mock tickets into ChromaDB
if not vectorstore._collection.count(): # Only add if the collection is empty
    ticket_contents = [ticket["ticket_content"] for ticket in MOCK_TICKETS_DATA]
    ticket_ids = [ticket["ticket_id"] for ticket in MOCK_TICKETS_DATA]
    vectorstore.add_texts(texts=ticket_contents, metadatas=[{"ticket_id": id_} for id_ in ticket_ids])
    vectorstore.persist()

retriever = vectorstore.as_retriever()

class RootCauseAnalysis(BaseModel):
    summary: str = Field(description="A summary of the issue.")
    category: str = Field(description="The category of the issue, e.g., 'Payment Failure', 'Login Issue'.")
    root_cause: str = Field(description="The identified root cause of the issue.")
    issue_type: str = Field(description="Classification of the issue, e.g., 'Bug', 'UX gap', 'Performance', 'Misconfiguration', 'User error'.")
    severity: str = Field(description="The severity of the issue, e.g., 'High', 'Medium', 'Low'.")
    confidence: float = Field(description="A confidence score (0-1) in the analysis.")
    engineering_actions: List[str] = Field(description="Suggested actions for the engineering team.")
    product_actions: List[str] = Field(description="Suggested actions for the product team.")
    support_reply_suggestion: str = Field(description="A suggested reply for the support team.")
    similar_incidents: Optional[List[str]] = Field(default_factory=list, description="List of IDs of similar past incidents.")

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an AI customer support root cause analyzer. Your goal is to convert messy customer support tickets into clear root causes, actionable fixes, and product insights. Always output in the specified JSON format."),
    ("user", """Analyze the following support ticket and provide a summary (summary), the category of the issue (category), the root cause (root_cause) as a concise string, the issue type (issue_type), its severity (severity), a confidence score (confidence) between 0 and 1, a list of engineering actions (engineering_actions), a list of product actions (product_actions), and a suggested support reply (support_reply_suggestion). If similar incidents are provided, use them for pattern detection. Ensure all JSON keys are in snake_case as specified in parentheses.

Support Ticket:\n{ticket}\n
Similar Incidents:\n{similar_incidents}\n
Output JSON:""")
])

output_parser = JsonOutputParser(pydantic_object=RootCauseAnalysis)

analysis_chain = prompt | llm | output_parser

@app.get("/")
async def root():
    return {"message": "AI Customer Support Root Cause Analyzer is running!"}

@app.post("/analyze_ticket", response_model=RootCauseAnalysis)
async def analyze_ticket_endpoint(ticket: str, request: Request):
    logger.info(f"Received /analyze_ticket request.")
    logger.info(f"Headers: {request.headers}")
    try:
        body = await request.json()
        logger.info(f"Request body: {body}")
    except Exception as e:
        logger.error(f"Could not parse request body as JSON: {e}")

    # Perform similarity search for similar incidents
    similar_docs = retriever.invoke(ticket)
    similar_incidents_content = "\n".join([doc.page_content for doc in similar_docs])
    similar_incident_ids = [doc.metadata.get("ticket_id", "Unknown") for doc in similar_docs]
    logger.info(f"Found {len(similar_docs)} similar incidents.")
    logger.info(f"Similar Incident IDs: {similar_incident_ids}")

    analysis = await analysis_chain.ainvoke({"ticket": ticket, "similar_incidents": similar_incidents_content})
    analysis['similar_incidents'] = similar_incident_ids # Update the Pydantic model with actual IDs
    logger.info(f"Analysis result: {analysis}")
    return analysis
