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
    
    formatted_chat = []
    for user, msg in GAME_STATE["chat_history"]:
        if user == "🤖 ScribbleBuddy":
            # Bot messages go under the "assistant" role
            formatted_chat.append({"role": "assistant", "content": f"**{user}**: {msg}"})
        else:
            # Player guesses and chats go under the "user" role
            formatted_chat.append({"role": "user", "content": f"**{user}**: {msg}"})
            
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
    gr.Markdown("<p style='text-align: center; color: #b3b3cc;'>Draw, guess with your squad, and vibe with your AI bestie who has literally zero filter.</p>")
    
    # --- STEP 1: LOGIN SECTION ---
    with gr.Row() as login_row:
        username_input = gr.Textbox(label="Enter your gamer tag:", placeholder="e.g., xX_NoobMaster_Xx")
        btn_login = gr.Button("Join Lobby 🔥", variant="primary", elem_classes=["primary-btn"])

    # --- STEP 2: MAIN GAME AREA ---
    with gr.Row(visible=False) as game_row:
        
        # Left Side: Drawing Tool
        with gr.Column(scale=2):
            status_lbl = gr.Label("🎨 Current Drawer: System", label="Game Status")
            drawing_pad = gr.Sketchpad(label="Draw here if it's your turn!", type="pil")
            
            with gr.Accordion("🤫 Drawer's Cheat Sheet (Click if you are drawing!)", open=False):
                word_display = gr.Markdown(f"Your secret word to draw is: <span style='color: #00ffcc; font-size: 1.25rem;'>**{GAME_STATE['current_word']}**</span>")
                btn_new_word = gr.Button("Skip / New Word 🔄")

        # Right Side: Leaderboard & Chat Space
        with gr.Column(scale=1):
            leaderboard_box = gr.Textbox(label="Leaderboard", value="No players yet...", interactive=False, lines=5, elem_id="leaderboard-text")
            
            # REMOVED type="messages" to resolve the component initialization error
            chat_space = gr.Chatbot(label="Main Chat & Guessing Arena")
            guess_input = gr.Textbox(label="Type your guess or message here...", placeholder="Press Enter to send")
            
            btn_reset = gr.Button("Reset Board 🧹", elem_classes=["reset-btn"])

    # --- EVENT FLOW CONTROL ---
    def execution_login(name):
        final_name = join_game(name)
        return gr.update(visible=False), gr.update(visible=True), final_name
        
    btn_login.click(execution_login, inputs=[username_input], outputs=[login_row, game_row, user_session])
    username_input.submit(execution_login, inputs=[username_input], outputs=[login_row, game_row, user_session])

    guess_input.submit(handle_guess_or_chat, inputs=[user_session, guess_input], outputs=[guess_input])
    
    def skip_word():
        GAME_STATE["current_word"] = random.choice(WORD_BANK)
        return f"Your secret word to draw is: <span style='color: #00ffcc; font-size: 1.25rem;'>**{GAME_STATE['current_word']}**</span>"
    btn_new_word.click(skip_word, outputs=[word_display])
    
    btn_reset.click(reset_game)

    # AUTOMATIC REFRESH LOOP
    auto_refresh = gr.Timer(value=1.0, active=True)
    auto_refresh.tick(refresh_game_area, outputs=[leaderboard_box, chat_space, status_lbl])

if __name__ == "__main__":
    demo.launch()