import os
import re
import vecs
import json
import dotenv
import hashlib
from openai import OpenAI
from supabase import create_client, Client

dotenv.load_dotenv()

def create_embeddings_from_markdown(file_path):
	openai_key: str = os.environ.get("OPENAI_KEY")
	client = OpenAI(api_key=openai_key)
	"""
	Reads a markdown file, splits it at line breaks, and creates embeddings for the content.
	
	Args:
	- file_path (str): The path to the markdown file.
	
	Returns:
	A list of embeddings corresponding to each non-empty line in the markdown file.
	"""
	# Check if the file exists
	if not os.path.exists(file_path):
		print(f"The file {file_path} does not exist.")
		return []
	
	embeddings = []
	with open(file_path, 'r') as file:
		content = file.read()
		
		chunks = re.split(r'(?m)^(?:#{1,2}\s)', content, flags=re.MULTILINE)
		chunks = list(dict.fromkeys([chunk for chunk in chunks if chunk.strip()]))

		vx = vecs.create_client("postgresql://postgres:postgres@localhost:54322/postgres")
		docs = vx.get_or_create_collection(name="docs", dimension=64)
		questions = vx.get_or_create_collection(name="questions", dimension=64)
		url: str = os.environ.get("SUPABASE_URL")
		key: str = os.environ.get("SUPABASE_KEY")
		supabase: Client = create_client(url, key)

		total_lines = len(chunks)
		print("Starting embeddings creation...")
		
		summary_embeddings = []
		chunk_embeddings = []
		hashes = []
		docs_records = []
		questions_records = []
		supabase_records = []
		for i, chunk in enumerate(chunks):
			print(len(chunk))
			summary = client.chat.completions.create(
				model="gpt-3.5-turbo",
				messages=[
					{"role": "system", "content": "Provide a one-sentence summary of the each block of text the user sends. Phrase each summary like a question. Ensure that key words are emphasized"},
					{"role": "user", "content": "Farcaster is a sufficiently decentralized social network built on Ethereum. Users can create profiles, post short messages or 'casts', follow others and organize into communities. It is a public social network similar in design to Twitter and Reddit. Since Farcaster is public and decentralized, anyone can build an app to read and write data. Users own their accounts and relationships with other users and are free to move between different apps. Learn more by diving into these concepts: Accounts - users on Farcaster. Usernames - human-readable names for accounts. Messages - public interactions between accounts. Apps - software that helps people create accounts, get usernames and post messages."},
					{"role": "system", "content": "What is Farcaster?"},
					{"role": "user", "content": chunk}
				]
			)
			summary = summary.choices[0].message.content
			
			

			chunk_embedding = client.embeddings.create(
				input=chunk,
				model="text-embedding-3-small",
				dimensions=64
			)
			summary_embedding = client.embeddings.create(
				input=summary,
				model="text-embedding-3-small",
				dimensions=64
			)
			chunk_embeddings.append(chunk_embedding)
			summary_embeddings.append(summary_embedding)
			hashes.append(hashlib.sha3_256(chunk.encode('utf-8')).hexdigest())
			percent_complete = ((i + 1) / total_lines) * 100
			print(f"Progress: {percent_complete:.2f}% complete.")

			metadata = {"v": 1}
			metadata_string = json.dumps(metadata)
			if (i + 1) % 10 == 0 or (i + 1) == total_lines:
				docs_records += [(hashlib.sha3_256((ch + metadata_string).encode('utf-8')).hexdigest(), ce.data[0].embedding, metadata) for ch, ce in zip(chunks[i-9:i+1], chunk_embeddings[i-9:i+1])]
				questions_records += [(hashlib.sha3_256((ch + metadata_string).encode('utf-8')).hexdigest(), se.data[0].embedding, metadata) for ch, se in zip(chunks[i-9:i+1], summary_embeddings[i-9:i+1])]
				supabase_records += [{"hash": hashlib.sha3_256((ch + metadata_string).encode('utf-8')).hexdigest(), "content": ch} for ch in chunks[i-9:i+1]]

				docs.upsert(records=docs_records)
				questions.upsert(records=questions_records)
				supabase.table('docs').upsert(supabase_records).execute()
				
				# Clear the records to avoid re-inserting
				docs_records = []
				questions_records = []
				supabase_records = []
		
	return

embeddings = create_embeddings_from_markdown('./combined_markdown.md')
print(embeddings)

