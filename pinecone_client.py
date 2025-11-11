import pinecone
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize Pinecone with environment variables
pinecone.init(
    api_key=os.getenv('PINECONE_API_KEY'),
    environment=os.getenv('PINECONE_ENVIRONMENT')
)

index_name = "student-guidance"

try:
    # Check if the index already exists
    if index_name in pinecone.list_indexes():
        print(f"Using existing index: {index_name}")
    else:
        print(f"Index {index_name} not found. Please create it in the Pinecone console first.")
        print("Visit: https://app.pinecone.io/ to create your index")
        exit(1)
    
    # Connect to the index
    index = pinecone.Index(index_name)
except Exception as e:
    print(f"Error connecting to Pinecone: {str(e)}")
    exit(1)
