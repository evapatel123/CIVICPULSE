import gradio as gr
import random

# --- GLOBAL GAME STATE (Shared across all players) ---
GAME_STATE = {
    "current_word": "skate",
    "drawer": "System",
    "scores": {},      
    "chat_history": [], # Stores flat list of tuples: (username, message)
    "canvas_data": None 
}

WORD_BANK = ["skate", "pizza", "iphone", "laptop", "skull", "cactus", "guitar", "gaming"]

# --- GEN Z BESTIE BOT MESSAGES ---
CHILL_RESPONSES = [
    "nah that ain't it chief 💀 Try again!",
    "honestly? solid guess, but wrong. dynamic coding right here.",
    "fr fr? u thought it was that? try another word bestie!",
    "absolute npc energy with that guess. change my mind.",
    "not quite, but u got the spirit! keeping tracking of ur attempts 👀"
]

BESTIE_SUCCESS = [
    "OMG SLAYYY 👑 U actually guessed it right!",
    "sheesh! mind size: mega. u got it!",
    "period. correct answer! actual brainiac hours."
]

def join_game(username):
    if not username or username.strip() == "":
        return "Anonymous User"
    username = username.strip()
    if username not in GAME_STATE["scores"]:
        GAME_STATE["scores"][username] = 0
        GAME_STATE["chat_history"].append(("🤖 ScribbleBuddy", f"YOOO welcome to the lobby, {username}! ✨ Let's get it."))
    return username

def refresh_game_area():
    leaderboard = "🏆 SCOREBOARD 🏆\n" + "\n".join([f"✨ {u}: {s} pts" for u, s in GAME_STATE["scores"].items()])
    
    # Format the entire chat log safely as alternating display rows for the Chatbot component
    formatted_chat = []
    for user, msg in GAME_STATE["chat_history"]:
        if user == "🤖 ScribbleBuddy":
            # Display bot comments on the assistant (right) side
            formatted_chat.append((None, f"{msg}"))
        else:
            # Display user messages/guesses on the user (left) side
            formatted_chat.append((f"**{user}**: {msg}", None))
            
    return leaderboard, formatted_chat, f"🎨 Current Drawer: {GAME_STATE['drawer']}"

def handle_guess_or_chat(username, text):
    if not text.strip():
        return ""
    
    text_clean = text.lower().strip()
    
    if text_clean == GAME_STATE["current_word"]:
        GAME_STATE["scores"][username] = GAME_STATE["scores"].get(username, 0) + 100
        GAME_STATE["chat_history"].append((username, f"Guessed the word! 🎉"))
        
        bestie_msg = random.choice(BESTIE_SUCCESS) + f" The word was '{GAME_STATE['current_word']}'!"
        GAME_STATE["chat_history"].append(("🤖 ScribbleBuddy", bestie_msg))
        
        GAME_STATE["current_word"] = random.choice(WORD_BANK)
        GAME_STATE["drawer"] = username 
        GAME_STATE["chat_history"].append(("🤖 ScribbleBuddy", f"Alright bet, {username} is drawing now. New word generated! Drop your drawings!"))
        
    else:
        GAME_STATE["chat_history"].append((username, text))
        if len(text_clean) < 15: 
            bestie_msg = random.choice(CHILL_RESPONSES)
            GAME_STATE["chat_history"].append(("🤖 ScribbleBuddy", f"@{username} {bestie_msg}"))
            
    return "" 

def reset_game():
    GAME_STATE["current_word"] = random.choice(WORD_BANK)
    GAME_STATE["chat_history"].append(("🤖 ScribbleBuddy", "Game wiped clean. Brand new words ready to go. No cap."))
    return "Game Reset! Keep playing!"

# --- CUSTOM NEON & COLORFUL CSS ---
custom_css = """
.gradio-container {
    background: linear-gradient(135deg, #1e1e2f 0%, #2d1b4e 100%) !important;
    color: #ffffff !important;
}
#title-md h1 {
    background: linear-gradient(90deg, #ff007f, #7f00ff, #00f0ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-align: center;
    font-size: 2.5rem !important;
    font-weight: 900;
}
.primary-btn {
    background: linear-gradient(45deg, #ff007f, #7f00ff) !important;
    color: white !important;
    border: none !important;
    font-weight: bold !important;
}
.primary-btn:hover {
    transform: scale(1.02);
    box-shadow: 0 0 15px rgba(255, 0, 127, 0.6) !important;
}
.reset-btn {
    background: linear-gradient(45deg, #ff4e50, #f9d423) !important;
    color: black !important;
    font-weight: bold !important;
}
#leaderboard-text textarea {
    background-color: #121214 !important;
    color: #00ffcc !important;
    font-family: 'Courier New', Courier, monospace;
    font-weight: bold;
    border: 2px solid #7f00ff !important;
}
"""

with gr.Blocks(theme=gr.themes.Cyberpunk(), css=custom_css) as demo:
    
    user_session = gr.State("")
    
    gr.Markdown("# 🎨 **Skribbl.io Clone x Gen Z Bestie** 🚀", elem_id="title-md")
    gr.Markdown("<p style='text-align: center; color: #b3b3cc;'>Draw, guess with your squad, and vibe with