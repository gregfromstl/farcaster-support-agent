import os
import vecs
import dotenv

dotenv.load_dotenv()

SUPABASE_CONNECTION_STRING: str = os.environ.get("SUPABASE_CONNECTION_STRING")

# create vector store client
vx = vecs.create_client(SUPABASE_CONNECTION_STRING)

# create a collection of vectors with 3 dimensions
vx.delete_collection("docs")
vx.delete_collection("questions")
docs = vx.get_or_create_collection(name="docs", dimension=64)
docs = vx.get_or_create_collection(name="questions", dimension=64)