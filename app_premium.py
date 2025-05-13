import streamlit as st
import streamlit.components.v1 as components
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json
import os
from langdetect import detect
from memory import load_memory, save_memory, get_user_id, manage_memory
from chathun_direct import chat_with_groq
from config_direct import SMTP_SERVER, SMTP_PORT, SENDER_EMAIL, SENDER_PASSWORD, DEFAULT_SENDER_NAME, RECIPIENT_EMAIL
from datetime import datetime

# Fonction pour détecter la langue de la question
def detect_language(text):
    try:
        lang = detect(text)
        return lang
    except:
        return 'fr'

# Fonction pour obtenir le message de réponse non pertinente dans la bonne langue
def get_not_relevant_message(lang):
    if lang in ['fr', 'fr-fr']:
        return "Je suis désolé, mais je ne peux répondre qu'aux questions concernant le Big Data, l'IA, le Machine Learning, le Business Intelligence, le Marketing Digital, la Data Science et des sujets connexes. N'hésitez pas à me poser une question dans ces domaines."
    elif lang in ['es', 'es-es']:
        return "Lo siento, pero solo puedo responder preguntas sobre Big Data, IA, Machine Learning, Business Intelligence, Marketing Digital, Data Science y temas relacionados. No dude en hacerme una pregunta en estas áreas."
    else:
        return "I'm sorry, but I can only answer questions about Big Data, AI, Machine Learning, Business Intelligence, Digital Marketing, Data Science, and related topics. Feel free to ask me a question in these areas."

# Fonction pour vérifier si la question est liée aux domaines autorisés
def is_relevant_question(question):
    relevant_keywords = [
        "big data", "hadoop", "spark", "data lake", "data warehouse", "nosql",
        "ai", "artificial intelligence", "intelligence artificielle", "ia", "machine learning", "ml",
        "deep learning", "apprentissage profond", "neural network", "réseau de neurones",
        "marketing", "seo", "sem", "référencement", "analytics", "google analytics",
        "bi", "business intelligence", "tableau", "power bi", "dashboard", "tableau de bord",
        "data mining", "fouille de données", "clustering", "classification", "regression",
        "nlp", "natural language processing", "traitement du langage naturel",
        "ai ethics", "éthique de l'ia", "responsible ai", "ia responsable",
        "data science", "science des données", "statistiques", "statistics"
    ]
    question_lower = question.lower()
    for keyword in relevant_keywords:
        if keyword in question_lower:
            return True
    return False

# Fonction pour envoyer un email
def send_lead_email(name, email, phone):
    try:
        message_text = f"""
        Nouveau lead du chatbot:
        Nom: {name}
        Email: {email}
        Téléphone: {phone}
        Timestamp: {str(st.session_state.get("form_submitted_at", ""))}
        """
        leads_file = os.path.join(os.path.dirname(__file__), "leads.json")
        if os.path.exists(leads_file):
            with open(leads_file, "r") as f:
                try:
                    leads = json.load(f)
                except:
                    leads = []
        else:
            leads = []

        leads.append({
            "name": name,
            "email": email,
            "phone": phone,
            "timestamp": str(st.session_state.get("form_submitted_at", ""))
        })

        with open(leads_file, "w") as f:
            json.dump(leads, f, indent=4)

        msg = MIMEMultipart()
        msg['From'] = f"{DEFAULT_SENDER_NAME} <{SENDER_EMAIL}>"
        msg['To'] = RECIPIENT_EMAIL
        msg['Subject'] = f'Nouveau lead du chatbot: {name}'
        msg.attach(MIMEText(message_text, 'plain'))

        import ssl
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
        return True, "Lead enregistré avec succès"
    except Exception as e:
        return False, str(e)

def main():
    # Configuration de la page
    st.set_page_config(
        page_title="BID Assistant",
        page_icon="https://i.postimg.cc/YjYPXYFm/logo.png ",
        layout="wide"
    )

    user_id = get_user_id()
    memory = load_memory()

    if "messages" not in st.session_state:
        if user_id in memory and "conversation" in memory[user_id]:
            st.session_state.messages = memory[user_id]["conversation"]
        else:
            st.session_state.messages = [{"role": "assistant", "content": "Bonjour ! Comment puis-je vous aider aujourd'hui ?"}]

    if "question_count" not in st.session_state:
        st.session_state.question_count = 0

    if "form_submitted" not in st.session_state:
        st.session_state.form_submitted = False

    # CSS personnalisé
    st.markdown("""
    <style>
    body {
        font-family: 'Poppins', sans-serif;
        background-color: #ffffff;
        margin: 0;
        padding: 0;
        color: #333;
    }
    .main .block-container {
        padding: 0;
        max-width: 100%;
        background: linear-gradient(180deg, #ffffff 0%, #f0f2ff 100%);
    }
    .stChatMessage {
        border-radius: 20px;
        margin-bottom: 16px;
        padding: 16px 20px;
        box-shadow: 0 3px 10px rgba(0,0,0,0.05);
        font-size: 15px;
        line-height: 1.6;
        transition: transform 0.2s ease;
    }
    .stChatMessage:hover {
        transform: translateY(-2px);
    }
    .stChatMessage[data-testid="stChatMessage-ASSISTANT"] {
        background: linear-gradient(135deg, #f0f2ff 0%, #ffffff 100%);
        color: #333;
        max-width: 80%;
        margin-right: auto;
        margin-left: 15px;
        position: relative;
        border-bottom-left-radius: 5px;
    }
    .stChatMessage[data-testid="stChatMessage-ASSISTANT"]::before {
        content: '';
        position: absolute;
        left: -10px;
        top: 15px;
        width: 0;
        height: 0;
        border-top: 10px solid transparent;
        border-right: 12px solid #f0f2ff;
        border-bottom: 10px solid transparent;
    }
    .stChatMessage[data-testid="stChatMessage-ASSISTANT"]::after {
        content: '';
        position: absolute;
        left: -40px;
        top: 0;
        width: 35px;
        height: 35px;
        background-image: url('https://i.postimg.cc/YjYPXYFm/logo.png ');
        background-size: contain;
        background-repeat: no-repeat;
        border-radius: 50%;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    .stChatMessage[data-testid="stChatMessage-USER"] {
        background: linear-gradient(135deg, #7f3fbf, #6a35b0);
        color: white;
        max-width: 80%;
        margin-left: auto;
        margin-right: 15px;
        position: relative;
        border-bottom-right-radius: 5px;
        box-shadow: 0 4px 15px rgba(127, 63, 191, 0.2);
    }
    .stChatMessage[data-testid="stChatMessage-USER"]::before {
        content: '';
        position: absolute;
        right: -10px;
        top: 15px;
        width: 0;
        height: 0;
        border-top: 10px solid transparent;
        border-left: 12px solid #6a35b0;
        border-bottom: 10px solid transparent;
    }
    .custom-header {
        background: linear-gradient(135deg, #8a4ec7, #6a35b0);
        color: white;
        padding: 18px 25px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        box-shadow: 0 4px 20px rgba(106, 53, 176, 0.2);
        position: sticky;
        top: 0;
        z-index: 1000;
        backdrop-filter: blur(10px);
    }
    .custom-header img {
        width: 42px;
        height: 42px;
        margin-right: 15px;
        filter: brightness(0) invert(1);
        transition: transform 0.3s ease;
    }
    .custom-header img:hover {
        transform: scale(1.1) rotate(5deg);
    }
    .custom-header .title-container {
        display: flex;
        flex-direction: column;
    }
    .custom-header .title {
        font-weight: 600;
        font-size: 20px;
        letter-spacing: 0.5px;
        margin-bottom: 2px;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    .custom-header .subtitle {
        font-size: 13px;
        opacity: 0.9;
        font-weight: 300;
        letter-spacing: 0.3px;
    }
    .custom-footer {
        background: rgba(255, 255, 255, 0.95);
        color: #666;
        padding: 12px 25px;
        font-size: 12px;
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-top: 1px solid rgba(127, 63, 191, 0.1);
        z-index: 99;
        backdrop-filter: blur(10px);
        box-shadow: 0 -2px 15px rgba(0, 0, 0, 0.03);
    }
    </style>
    <!-- En-tête -->
    <div class="custom-header">
        <div style="display: flex; align-items: center;">
            <img src="https://i.postimg.cc/YjYPXYFm/logo.png " alt="Logo">
            <div class="title-container">
                <div class="title">BID Assistant</div>
                <div class="subtitle">Votre expert en Big Data & IA</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    with st.container():
        for msg in st.session_state.messages:
            st.chat_message(msg["role"]).write(msg["content"])

        if st.session_state.question_count >= 3 and not st.session_state.form_submitted:
            with st.form(key="contact_form"):
                st.markdown("<h3>Let us know how to contact you</h3>", unsafe_allow_html=True)
                name = st.text_input("Name")
                email = st.text_input("Email")
                phone = st.text_input("Phone Number")
                submit_button = st.form_submit_button("Submit")
                if submit_button:
                    if name and email and phone:
                        st.session_state.form_submitted_at = datetime.now()
                        st.session_state.form_submitted = True
                        success, _ = send_lead_email(name, email, phone)
                        if success:
                            st.session_state.messages.append({"role": "assistant", "content": f"Merci {name} ! Nous vous contacterons bientôt à {email}."})
                            save_memory(user_id, st.session_state.messages)
                            st.rerun()
                    else:
                        st.error("Veuillez remplir tous les champs")

    st.markdown("</div>", unsafe_allow_html=True)

    # Footer
    st.markdown("""
    <div class="custom-footer">
        © 2024 BID Consulting. Tous droits réservés.
    </div>
    """, unsafe_allow_html=True)

    # Logique de traitement des questions
    if prompt := st.chat_input("Posez votre question..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.question_count += 1
        detected_lang = detect_language(prompt)

        if is_relevant_question(prompt):
            lang_instruction = {"role": "system", "content": f"Please respond in the same language as the user's question. The detected language is: {detected_lang}."}
            messages_with_lang = st.session_state.messages.copy()
            messages_with_lang.insert(0, lang_instruction)
            try:
                response = chat_with_groq(messages_with_lang)
                if "trouble connecting" in response or "error occurred" in response:
                    response = "Je suis désolé, mais je rencontre actuellement des problèmes de connexion avec mon service d'IA. Veuillez réessayer plus tard."
            except Exception as e:
                print(f"Erreur lors de l'appel à l'API Groq: {str(e)}")
                response = "I'm sorry, but I'm currently experiencing connection issues with my AI service. Please try again later."
            st.session_state.messages.append({"role": "assistant", "content": response})
        else:
            response = get_not_relevant_message(detected_lang)
            st.session_state.messages.append({"role": "assistant", "content": response})

        st.session_state.messages = manage_memory(st.session_state.messages)
        save_memory(user_id, st.session_state.messages)

        if st.session_state.question_count == 3 and not st.session_state.form_submitted:
            st.rerun()

if __name__ == "__main__":
    main()