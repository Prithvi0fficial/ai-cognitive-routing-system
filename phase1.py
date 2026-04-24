# Phase1: vector based parsonas matching
# convert bot personalities and incoming posts to vector
# uses cosine similarity to route pots to bots
# threshold used: 0.20 - tuned for all-MiniLM-L6-v2
# but assessment specific is 0.85 which is calibrated for OpenAI embeddings
# this model peoduces scores in 0.2-0.5 range for realted text


from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import chromadb

model = SentenceTransformer('all-MiniLM-L6-v2')
client = chromadb.Client()
collection = client.create_collection(name='bot_personas',metadata={'hnsw:space':'cosine'})

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

def route_post_to_bot(post,threshold = 0.20):
    post_vector = model.encode(post).tolist()
    results = collection.query(
        query_embeddings=[post_vector],
        n_results=3

    )

    matched_bot = []
    for i in range(len(results['ids'][0])):
        bot_id = results['ids'][0][i]
        distance = results['distances'][0][i]
        similarity =1 - distance

        if similarity >= threshold:
            matched_bot.append({
                'bot_id':bot_id,
                'similarity':round(similarity,4)
            })
        print(f"{bot_id} matches with similarity: {round(similarity,4)}")
    return matched_bot


post = 'Big tech companies are destroying democracy and invading our privacy'
matches = route_post_to_bot(post)
print(f"Macthed_bot:{matches}")




















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