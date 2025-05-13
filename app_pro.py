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

# Fonction pour détecter la langue de la question
def detect_language(text):
    try:
        # Détecter la langue
        lang = detect(text)
        return lang
    except:
        # En cas d'erreur, retourner 'fr' par défaut
        return 'fr'

# Fonction pour obtenir le message de réponse non pertinente dans la bonne langue
def get_not_relevant_message(lang):
    if lang in ['fr', 'fr-fr']:
        return "Je suis désolé, mais je ne peux répondre qu'aux questions concernant le Big Data, l'IA, le Machine Learning, le Business Intelligence, le Marketing Digital, la Data Science et des sujets connexes. N'hésitez pas à me poser une question dans ces domaines."
    elif lang in ['es', 'es-es']:
        return "Lo siento, pero solo puedo responder preguntas sobre Big Data, IA, Machine Learning, Business Intelligence, Marketing Digital, Data Science y temas relacionados. No dude en hacerme una pregunta en estas áreas."
    else:
        # Anglais par défaut
        return "I'm sorry, but I can only answer questions about Big Data, AI, Machine Learning, Business Intelligence, Digital Marketing, Data Science, and related topics. Feel free to ask me a question in these areas."

# Fonction pour vérifier si la question est liée aux domaines autorisés
def is_relevant_question(question):
    # Liste des mots-clés et domaines autorisés
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
    
    # Convertir la question en minuscules pour une comparaison insensible à la casse
    question_lower = question.lower()
    
    # Vérifier si l'un des mots-clés est présent dans la question
    for keyword in relevant_keywords:
        if keyword in question_lower:
            return True
    
    # Si aucun mot-clé n'est trouvé, la question n'est pas pertinente
    return False

# Fonction pour envoyer un email
def send_lead_email(name, email, phone):
    try:
        # Créer le message
        message_text = f"""
        Nouveau lead du chatbot:
        
        Nom: {name}
        Email: {email}
        Téléphone: {phone}
        Timestamp: {str(st.session_state.get("form_submitted_at", ""))}
        """
        
        # Sauvegarder dans un fichier JSON
        leads_file = os.path.join(os.path.dirname(__file__), "leads.json")
        
        # Charger les leads existants ou créer une liste vide
        if os.path.exists(leads_file):
            with open(leads_file, "r") as f:
                try:
                    leads = json.load(f)
                except:
                    leads = []
        else:
            leads = []
        
        # Ajouter le nouveau lead
        leads.append({
            "name": name,
            "email": email,
            "phone": phone,
            "timestamp": str(st.session_state.get("form_submitted_at", ""))
        })
        
        # Sauvegarder les leads
        with open(leads_file, "w") as f:
            json.dump(leads, f, indent=4)
        
        # Envoyer l'email
        try:
            # Configurer l'email
            msg = MIMEMultipart()
            msg['From'] = f"{DEFAULT_SENDER_NAME} <{SENDER_EMAIL}>"
            msg['To'] = RECIPIENT_EMAIL
            msg['Subject'] = f'Nouveau lead du chatbot: {name}'
            
            # Ajouter le corps du message
            msg.attach(MIMEText(message_text, 'plain'))
            
            # Configurer le serveur SMTP et envoyer l'email
            import ssl
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context) as server:
                server.login(SENDER_EMAIL, SENDER_PASSWORD)
                server.send_message(msg)
                print(f"Email envoyé à {RECIPIENT_EMAIL} avec les informations du lead: {name}, {email}, {phone}")
        except Exception as email_error:
            print(f"Erreur lors de l'envoi de l'email: {str(email_error)}")
            # Continuer même si l'email échoue, car nous avons sauvegardé les données
        
        # Retourner un succès
        return True, "Lead enregistré avec succès"
        
    except Exception as e:
        return False, str(e)

def main():
    # Configuration de la page
    st.set_page_config(
        page_title="BID Assistant",
        page_icon="https://i.postimg.cc/YjYPXYFm/logo.png",
        layout="wide"
    )

    # Initialiser la mémoire
    user_id = get_user_id()
    memory = load_memory()

    # Initialiser les variables de session
    if "messages" not in st.session_state:
        if user_id in memory and "conversation" in memory[user_id]:
            st.session_state.messages = memory[user_id]["conversation"]
        else:
            st.session_state.messages = [
                {"role": "assistant", "content": "Bonjour ! Comment puis-je vous aider aujourd'hui ?"}
            ]
    
    # Initialiser le compteur de questions
    if "question_count" not in st.session_state:
        st.session_state.question_count = 0
    
    # Initialiser l'état du formulaire
    if "show_form" not in st.session_state:
        st.session_state.show_form = False
    
    # Initialiser l'état de soumission du formulaire
    if "form_submitted" not in st.session_state:
        st.session_state.form_submitted = False

    # CSS pour le design du chatbot
    st.markdown("""
    <style>
    /* Masquer les éléments Streamlit par défaut */
    #MainMenu, footer, header {
        visibility: hidden;
    }
    
    /* Style pour le corps de la page */
    body {
        font-family: Arial, sans-serif;
        background-color: #f9f9f9;
        margin: 0;
        padding: 0;
    }
    
    /* Style pour le conteneur principal */
    .main .block-container {
        padding: 0;
        max-width: 100%;
    }
    
    /* Style pour les messages du chat */
    .stChatMessage {
        border-radius: 18px;
        margin-bottom: 10px;
        padding: 12px 16px;
        box-shadow: 0 1px 2px rgba(0,0,0,0.1);
        font-size: 15px;
        line-height: 1.5;
    }

    /* Style pour les messages de l'assistant */
    .stChatMessage[data-testid="stChatMessage-ASSISTANT"] {
        background: #f0f0f0;
        border-left: none;
        color: #333;
        max-width: 80%;
        margin-right: auto;
        margin-left: 10px;
    }

    /* Style pour les messages de l'utilisateur */
    .stChatMessage[data-testid="stChatMessage-USER"] {
        background: linear-gradient(135deg, #7f3fbf, #5a2da1);
        border-left: none;
        color: white;
        max-width: 80%;
        margin-left: auto;
        margin-right: 10px;
    }

    /* Style pour le champ de saisie */
    .stChatInputContainer {
        border-top: 1px solid #f0f0f0;
        padding: 15px;
        background: white;
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        z-index: 100;
        box-shadow: 0 -2px 10px rgba(0,0,0,0.05);
    }

    /* Style pour le champ de texte */
    .stChatInput {
        border: 1px solid #ddd;
        border-radius: 20px;
        padding: 12px 15px;
        font-size: 15px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        transition: all 0.2s ease;
    }
    
    .stChatInput:focus {
        border-color: #7f3fbf;
        box-shadow: 0 0 0 2px rgba(127, 63, 191, 0.2);
    }

    /* Style pour le bouton d'envoi */
    .stChatInputContainer button {
        background: linear-gradient(135deg, #7f3fbf, #5a2da1);
        border: none;
        border-radius: 50%;
        color: white;
        width: 36px;
        height: 36px;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 2px 5px rgba(127, 63, 191, 0.3);
        transition: all 0.2s ease;
    }
    
    .stChatInputContainer button:hover {
        transform: scale(1.05);
        box-shadow: 0 3px 8px rgba(127, 63, 191, 0.4);
    }

    /* Masquer certains éléments Streamlit */
    .stDeployButton, .stToolbar, .stDecoration {
        display: none !important;
    }
    
    /* Style pour le formulaire */
    .stForm {
        background-color: white;
        border-radius: 18px;
        padding: 25px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin: 20px 10px;
        border: 1px solid #f0f0f0;
    }
    
    .stForm h3 {
        color: #7f3fbf;
        font-size: 20px;
        margin-bottom: 20px;
        text-align: center;
    }
    
    .stForm input[type="text"], .stForm input[type="email"], .stForm input[type="tel"] {
        border: 1px solid #ddd;
        border-radius: 8px;
        padding: 10px 12px;
        font-size: 15px;
        margin-bottom: 5px;
        transition: all 0.2s ease;
    }
    
    .stForm input[type="text"]:focus, .stForm input[type="email"]:focus, .stForm input[type="tel"]:focus {
        border-color: #7f3fbf;
        box-shadow: 0 0 0 2px rgba(127, 63, 191, 0.2);
    }
    
    .stForm button {
        background: linear-gradient(135deg, #7f3fbf, #5a2da1);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 20px;
        font-size: 16px;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.2s ease;
        box-shadow: 0 2px 5px rgba(127, 63, 191, 0.3);
        width: 100%;
        margin-top: 10px;
    }
    
    .stForm button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(127, 63, 191, 0.4);
    }
    
    /* Ajouter un en-tête personnalisé */
    .custom-header {
        background: linear-gradient(135deg, #7f3fbf, #5a2da1);
        color: white;
        padding: 15px 20px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    
    .custom-header img {
        width: 40px;
        height: 40px;
        margin-right: 10px;
    }
    
    /* Ajouter un espace pour le contenu du chat */
    .chat-content {
        padding: 20px 10px;
        padding-bottom: 80px; /* Espace pour le champ de saisie fixe */
        overflow-y: auto;
        height: calc(100vh - 70px); /* Hauteur moins l'en-tête */
    }
    </style>
    
    <!-- En-tête personnalisé -->
    <div class="custom-header">
        <div style="display: flex; align-items: center;">
            <img src="https://i.postimg.cc/YjYPXYFm/logo.png" alt="BID Logo">
            <div>
                <div style="font-weight: bold; font-size: 18px;">BID Assistant</div>
            </div>
        </div>
    </div>
    
    <!-- Conteneur pour le contenu du chat -->
    <div class="chat-content">
    """, unsafe_allow_html=True)

    # Interface du chatbot
    with st.container():
        # Afficher l'historique des messages
        for msg in st.session_state.messages:
            st.chat_message(msg["role"]).write(msg["content"])
        
        # Afficher le formulaire de contact après 3 questions
        if st.session_state.question_count >= 3 and not st.session_state.form_submitted:
            with st.form(key="contact_form", clear_on_submit=True):
                st.markdown("<h3>Let us know how to contact you</h3>", unsafe_allow_html=True)
                name = st.text_input("Name")
                email = st.text_input("Email")
                phone = st.text_input("Phone Number")
                submit_button = st.form_submit_button("Submit")
                
                if submit_button:
                    if name and email and phone:
                        # Enregistrer l'heure de soumission
                        from datetime import datetime
                        st.session_state.form_submitted_at = datetime.now()
                        
                        # Marquer le formulaire comme soumis
                        st.session_state.form_submitted = True
                        
                        # Envoyer l'email ou sauvegarder les données
                        success, _ = send_lead_email(name, email, phone)
                        
                        if success:
                            # Ajouter un message de confirmation dans le chat
                            st.session_state.messages.append({
                                "role": "assistant", 
                                "content": f"Merci {name} pour vos informations ! Nous vous contacterons bientôt à {email}."
                            })
                            
                            # Sauvegarder la conversation mise à jour
                            save_memory(user_id, st.session_state.messages)
                            
                            # Recharger la page pour afficher le message de confirmation
                            st.rerun()
                    else:
                        st.error("Veuillez remplir tous les champs")
    
    # Fermer les balises div ouvertes
    st.markdown("</div>", unsafe_allow_html=True)
        
    # Champ de saisie pour le chat
    if prompt := st.chat_input("Posez votre question..."):
        # Ajouter le message de l'utilisateur
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Incrémenter le compteur de questions
        st.session_state.question_count += 1
        
        # Détecter la langue de la question
        detected_lang = detect_language(prompt)
        
        # Vérifier si la question est pertinente
        if is_relevant_question(prompt):
            # Obtenir la réponse de l'IA pour les questions pertinentes
            # Ajouter une instruction pour répondre dans la même langue que la question
            lang_instruction = {
                "role": "system", 
                "content": f"Please respond in the same language as the user's question. The detected language is: {detected_lang}."
            }
            
            # Créer une copie des messages avec l'instruction de langue
            messages_with_lang = st.session_state.messages.copy()
            messages_with_lang.insert(0, lang_instruction)
            
            try:
                # Essayer d'obtenir une réponse de l'API Groq
                response = chat_with_groq(messages_with_lang)
                
                # Vérifier si la réponse contient un message d'erreur
                if "trouble connecting" in response or "error occurred" in response:
                    # Utiliser une réponse de secours en cas d'erreur
                    if detected_lang in ['fr', 'fr-fr']:
                        response = "Je suis désolé, mais je rencontre actuellement des problèmes de connexion avec mon service d'IA. Veuillez réessayer plus tard."
                    else:
                        response = "I'm sorry, but I'm currently experiencing connection issues with my AI service. Please try again later."
            except Exception as e:
                # En cas d'erreur, utiliser une réponse de secours
                print(f"Erreur lors de l'appel à l'API Groq: {str(e)}")
                if detected_lang in ['fr', 'fr-fr']:
                    response = "Je suis désolé, mais je rencontre actuellement des problèmes de connexion avec mon service d'IA. Veuillez réessayer plus tard."
                else:
                    response = "I'm sorry, but I'm currently experiencing connection issues with my AI service. Please try again later."
            
            st.session_state.messages.append({"role": "assistant", "content": response})
        else:
            # Réponse standard pour les questions non pertinentes dans la langue détectée
            response = get_not_relevant_message(detected_lang)
            st.session_state.messages.append({"role": "assistant", "content": response})

        # Gérer la longueur de la conversation et sauvegarder
        st.session_state.messages = manage_memory(st.session_state.messages)
        save_memory(user_id, st.session_state.messages)
        
        # Recharger la page si nous avons atteint 3 questions pour afficher le formulaire
        if st.session_state.question_count == 3 and not st.session_state.form_submitted:
            st.rerun()

if __name__ == "__main__":
    main()
