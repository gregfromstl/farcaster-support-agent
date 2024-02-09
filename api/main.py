import os
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
import vecs
import dotenv
from openai import OpenAI
from fastapi import FastAPI
from pydantic import BaseModel
from supabase import create_client, Client
from fastapi.middleware.cors import CORSMiddleware

dotenv.load_dotenv()

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
	return {"message": "Running"}

class Query(BaseModel):
    message: str

@app.post("/")
async def root(query: Query):
	message = query.message
	openai_key: str = os.environ.get("OPENAI_KEY")
	client = OpenAI(api_key=openai_key)

	embedding = client.embeddings.create(input=message, model="text-embedding-3-small", dimensions=64)

	SUPABASE_CONNECTION_STRING: str = os.environ.get("SUPABASE_CONNECTION_STRING")
	vx = vecs.create_client(SUPABASE_CONNECTION_STRING)

	docs = vx.get_or_create_collection(name="docs", dimension=64)
	questions = vx.get_or_create_collection(name="questions", dimension=64)
	docs_search_result = docs.query(
		data=embedding.data[0].embedding,      # required
		limit=3,                         # number of records to return
		filters={"v": {"$eq": 1}}, # metadata filters
	)
	questions_search_result = questions.query(
		data=embedding.data[0].embedding,      # required
		limit=5,                         # number of records to return
		filters={"v": {"$eq": 1}}, # metadata filters
	)

	print(docs_search_result)

	url: str = os.environ.get("SUPABASE_URL")
	key: str = os.environ.get("SUPABASE_KEY")
	supabase: Client = create_client(url, key)
	docs_results = supabase.table('docs').select("*").in_("hash", docs_search_result).execute()
	questions_results = supabase.table('docs').select("*").in_("hash", questions_search_result).execute()

	context = [item['content'] for item in [*questions_results.data, *docs_results.data]]
	
	answer = client.chat.completions.create(
		model="gpt-3.5-turbo",
		messages=[
			{"role": "system", "content": "You are a support agent for Farcaster and Warpcast (Farcaster's flagship client). Your job is to assist any questions users have based on the documentation you are provided."},
			{"role": "system", "content": "Be sure to disntinguish between Farcaster (the decentralized social network) and Warpcast (the app that allows users to use the Farcaster network)."},
			*[{"role": "system", "content": text} for text in context],
			{"role": "system", "content": "Find the answer to the user's question using the provided content. Only use the provided content to answer the user's question. Do not use any other information you may have. If the answer to the user's question is not content in the provided content, reply with 'I am not sure.' Be brief and to the point (1-2 sentences maximum)."},
			{"role": "user", "content": message}
		]
	)

	return {"message": answer.choices[0].message.content}
	
