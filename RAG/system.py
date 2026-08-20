#using langchain framework for RAG, open source model: Tencet Hy-3


import os
import pandas as pd
from dotenv import load_dotenv

# LangChain components for our RAG system
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser
from langchain.prompts import PromptTemplate
from langchain.schema import Document


# Load your environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

print("All libraries loaded successfully!")


# Load your CSV file

'csv_file_path = '

# Replace with your actual file path
data_frame = pd.read_csv(csv_file_path)

print(f"Successfully loaded {len(data_frame)} rows from CSV")
print(f"Columns available: {list(data_frame.columns)}")
print(f"Data shape: {data_frame.shape}")

# Look at the first few rows to understand our data structure
print("First 5 rows of data:")
print(data_frame.head())

#Transforming tabular into language description
def create_readable_text_from_row(row):
    """
    Convert a single CSV row into a natural language description
    """
    # Customize this based on your CSV structure
    # This example assumes columns: Name, HEX, RGB
    description_parts = []
    for column_name, value in row.items():
        if pd.notna(value):  # Only include non-empty values
            description_parts.append(f"{column_name}: {value}")
    # Join everything into one readable sentence
    return ". ".join(description_parts) + "."


# Convert all rows to readable text documents
text_documents = []

for index, row in data_frame.iterrows():
    # Convert each row to readable text
    readable_description = create_readable_text_from_row(row)
    # Create a Document object (LangChain's format)
    doc = Document(page_content=readable_description)
    text_documents.append(doc)
  
print(f"Created {len(text_documents)} document objects")

# A few examples of what we created

print("\nExamples of converted documents:")
for i in range(min(3, len(text_documents))):
    print(f"Document {i+1}: {text_documents[i].page_content}")

