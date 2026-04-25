from typing import TypedDict
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage,HumanMessage
from langgraph.graph import StateGraph,END
import os

load_dotenv()

class BotState(TypedDict):
    bot_id:str
    search_query:str
    search_results:str
    topic:str
    post_content:str

BOT_PERSONAS ={
    "bot_a":{
        "name":"Tech Maximalist",
        "system_prompt":"You are a Bot A, the Tech Maximalist. You always believe AI and crypto will solve all human problems.you are very optimistic about technology, Elon Musk, and space exploration. You dismiss regulatory concerns. Your tone is confident and slightly arrogant. You never break character. " 
        },

    "bot_b":{
        "name":"Doomer Skeptic",
        "system_prompt" : "You are Bot B, the Doomer Skeptic. You always believe late-stage capitalism and tech monopolies are destroying society. you are highly critical of AI, social media, and billionaires. You value privacy and nature. Your tone is cynical and sarcastic. You never break character. " 


    },

    "bot_c":{
        "name":"Finance Bro",
        "system_prompt" : "You are Bot C, the Finance Bro. You strictly care about markets, interest rates, trading algorithms, and making money. You speak in finance jargon. You view everything through the lens of ROI.You never break character. "
}
}

def mock_searxng_search(query):
    query = query.lower()
    if 'crypto' in query or 'bitcoin' in query:
        return "Bitcoin hits all time high amid regulatory ETF approvals. Ethereum Layer-2 processes 1M transactions per second. "
    elif "ai" in query or "openai" in query or "model" in query:
        return "OpenAI release GPT-5 claming human level reasoning. AI replace 40% of junior developer jobs in Silicaon Valley."
    elif "market" in query or "stock" in query or "interest" in query:
        return "Fedral Reserve signals three rates cuts in 2026.S&P 500 hits record high as inflation cools to 2.1%. "
    elif "privacy" in query or "bigh tech" in query or "monopoly" in query:
        return "Meta fined 2 billion for illegal data harvesting. Leaked docs show Google tracks users even in Incognito mode."
    elif "space" in query or "elon" in query or "tesla" in query:
        return "SpaceX Starship completes first crewed Mars mission test. Tesla FSD achieves zero accident record across 10 billion miles"
    else:
        return "Tech sector leads global economic growth in 2026.World Economic Forum warns of AI driven inequality gap."
    

def create_llm():
    return ChatGroq(
        model = "llama-3.3-70b-versatile",
        temperature=0.7,
        api_key=os.getenv("GROQ_API_KEY")


    )

def node_decide_search(state:BotState):
    bot_id = state['bot_id']
    persona = BOT_PERSONAS[bot_id]

    llm= create_llm()

    messages = [
        SystemMessage(content=persona['system_prompt']),
        HumanMessage(content = 'What topic do you wnat to post about today? Give me a short 3 to 5 word search query only. No explanation.')
    ]

    response = llm.invoke(messages)
    search_query = response.content.strip().strip('"')
    

    print(f"Node 1: {bot_id} wants to search for: {search_query}")
    return {"search_query":search_query,"topic":search_query}

def node_web_search(state: BotState):
    search_query = state["search_query"]

    results = mock_searxng_search(search_query)

    print(f"Node 2: Search results: {results[:60]}...")
    
    return {"search_results":results}

def node_draft_post(state:BotState):
    bot_id = state["bot_id"]
    persona = BOT_PERSONAS[bot_id]
    search_results = state["search_results"]

    llm = create_llm()

    messages = [
        SystemMessage(content = persona["system_prompt"]),
        HumanMessage(content=f"Here are today's news headlines:\n{search_results}\n\nWrite a single optionated social media post under 280 characters based on these headlines. Stay in character. Return only the post text, nothing else.")

    ]
    response = llm.invoke(messages)
    post_content = response.content.strip()

    if len(post_content)>200:
        post_content = post_content[:277] + "..."

    print(f"Node 3: Post drafted: {post_content}")
    return {"post_content":post_content}


def build_graph():
    graph = StateGraph(BotState)

    graph.add_node("decide_search",node_decide_search)
    graph.add_node("web_search", node_web_search)
    graph.add_node("draft_post",node_draft_post)

    graph.set_entry_point("decide_search")
    graph.add_edge("decide_search","web_search")
    graph.add_edge("web_search","draft_post")
    graph.add_edge("draft_post",END)

    return graph.compile()


def run_content_engine(bot_id):
    app =build_graph()

    initial_state = {
        "bot_id": bot_id,
        "search_query":"",
        "topic":"",
        "post_content":""
    }

    result = app.invoke(initial_state)

    return {
        "bot_id":bot_id,
        "topic":result["topic"],
        "post_content": result["post_content"]
    }

print(run_content_engine("bot_a"))

print(run_content_engine("bot_b"))

print(run_content_engine("bot_c"))

