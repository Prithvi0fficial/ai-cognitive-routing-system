from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import chromadb

model = SentenceTransformer('all-MiniLM-L6-v2')
client = chromadb.Client()
collection = client.create_collection(name='bot_personas')

bot_a = "I believe AI and crypto will solve all human problems. I am highly optimistic about technology, Elon Musk, and space exploration. I dismiss regulatory concerns."

bot_b = "I believe late-stage capitalism and tech monopolies are destroying society. I am highly critical of AI, social media, and billionaires. I value privacy and nature."

bot_c = "I strictly care about markets, interest rates, trading algorithms, and making money. I speak in finance jargon and view everything through the lens of ROI."

vector_a = model.encode(bot_a).tolist()
vector_b = model.encode(bot_b).tolist()
vector_c = model.encode(bot_c).tolist()

collection.add(
    ids=["bot_a","bot_b","bot_c"],
    documents =[bot_a,bot_b,bot_c],
    embeddings=[vector_a,vector_b,vector_c]
)

print("Bot personas stored in chromadb successfully")





















# Test
# model = SentenceTransformer("all-MiniLM-L6-v2")
# sentence = "Bitcoin is hitting all time high"
# sentence2 = "crypto markets are reaching new highs"
# sentence3 = "i love hiking in the mountain"
# vector = model.encode(sentence)
# vector2 = model.encode(sentence2)
# vector3 = model.encode(sentence3)


# print(f"vector shape: {vector.shape}")

# print(f"First 5 numbers: {vector[:5]}")

# sim_1_2 = cosine_similarity([vector], [vector2])[0][0]
# sim_1_3 = cosine_similarity([vector], [vector3])[0][0]

# print(f"Bitcoin vs Crypto: {sim_1_2:.4f}")
# print(f"Bitcoin vs Hiking: {sim_1_3:.4f}")