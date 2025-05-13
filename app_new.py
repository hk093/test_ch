import streamlit as st
import streamlit.components.v1 as components
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json
import os
from langdetect import detect
from memory import load_memory, save_memory, get_user_id, manage_memory
from chathun import chat_with_groq

# Fonction de secours si l'API Groq ne fonctionne pas
def fallback_response(detected_lang):
    """Génère une réponse de secours si l'API ne fonctionne pas"""
    # Réponses prédéfinies en fonction de la langue
    if detected_lang in ['fr', 'fr-fr']:
        return "Je suis désolé, mais je rencontre actuellement des problèmes de connexion avec mon service d'IA. Voici quelques informations générales sur le sujet : les technologies Big Data et l'IA sont en constante évolution. Pour des réponses plus précises, veuillez réessayer plus tard."
    elif detected_lang in ['es', 'es-es']:
        return "Lo siento, pero actualmente estoy experimentando problemas de conexión con mi servicio de IA. Aquí hay alguna información general sobre el tema: las tecnologías de Big Data e IA están en constante evolución. Para respuestas más precisas, por favor intente más tarde."
    else:
        return "I'm sorry, but I'm currently experiencing connection issues with my AI service. Here's some general information on the topic: Big Data and AI technologies are constantly evolving. For more precise answers, please try again later."

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
        # Importer les configurations depuis config.py
        from config import SMTP_SERVER, SMTP_PORT, SENDER_EMAIL, SENDER_PASSWORD, DEFAULT_SENDER_NAME, RECIPIENT_EMAIL

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
        page_title="Chatbot",
        page_icon="💬",
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

    # CSS pour le design du popup et pour afficher la conversation en haut
    st.markdown("""
    <style>
    /* Style pour les messages du chat */
    .stChatMessage {
        border-radius: 18px;
        margin-bottom: 10px;
        padding: 12px;
        box-shadow: none;
    }

    /* Style pour les messages de l'assistant */
    .stChatMessage[data-testid="stChatMessage-ASSISTANT"] {
        background: #f0f0f0;
        border-left: none;
        color: #333;
        max-width: 80%;
        margin-right: auto;
    }

    /* Style pour les messages de l'utilisateur */
    .stChatMessage[data-testid="stChatMessage-USER"] {
        background: #7f3fbf;
        border-left: none;
        color: white;
        max-width: 80%;
        margin-left: auto;
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
    }

    /* Style pour le champ de texte */
    .stChatInput {
        border: 1px solid #ddd;
        border-radius: 20px;
        padding: 12px;
    }

    /* Style pour le bouton d'envoi */
    .stChatInputContainer button {
        background: #7f3fbf;
        border: none;
        border-radius: 50%;
        color: white;
    }

    /* Masquer certains éléments Streamlit */
    .stDeployButton, .stToolbar, .stDecoration {
        display: none !important;
    }

    /* Style pour le popup du chatbot */
    #chatbotPopup {
        display: none;
        position: fixed;
        bottom: 20px;
        right: 20px;
        width: 380px;
        height: 600px;
        background: white;
        border-radius: 20px;
        box-shadow: 0 15px 50px rgba(127, 63, 191, 0.2);
        z-index: 9999;
        font-family: Arial, sans-serif;
        overflow: hidden;
    }

    #chatbotButton {
        position: fixed;
        bottom: 20px;
        right: 20px;
        background: linear-gradient(135deg, #7f3fbf, #5a2da1);
        border: none;
        border-radius: 50%;
        width: 64px;
        height: 64px;
        box-shadow: 0 6px 15px rgba(127, 63, 191, 0.3);
        cursor: pointer;
        z-index: 9998;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: transform 0.2s ease-in-out;
    }

    #chatbotButton:hover {
        transform: scale(1.1);
    }
    </style>
    """, unsafe_allow_html=True)

    # Ajouter le bouton du chatbot et le popup avec JavaScript sécurisé
    components.html("""
    <div id="chatbotButton">
        <img src="https://i.postimg.cc/YjYPXYFm/logo.png" alt="BID Logo" style="width: 32px; height: 32px; filter: brightness(0) invert(1);">
    </div>

    <div id="chatbotPopup">
        <div style="background: #7f3fbf; color: white; padding: 16px; font-size: 18px; font-weight: bold; display: flex; align-items: center; justify-content: space-between;">
            <span>Assistance Chatbot</span>
            <button id="closeButton" style="background: none; border: none; font-size: 20px; color: white; cursor: pointer;">✖</button>
        </div>

        <div style="padding: 15px; display: flex; align-items: center; border-bottom: 1px solid #f0f0f0;">
            <img src="https://i.postimg.cc/YjYPXYFm/logo.png" alt="BID Logo" style="width: 40px; height: 40px; margin-right: 10px;">
            <div>
                <div style="font-weight: bold;">BID Consulting</div>
            </div>
        </div>

        <div id="chatbotContent"></div>
    </div>

    <script>
    document.addEventListener('DOMContentLoaded', function() {
        const button = document.getElementById('chatbotButton');
        const popup = document.getElementById('chatbotPopup');
        const closeButton = document.getElementById('closeButton');
        const content = document.getElementById('chatbotContent');

        if (button && popup && closeButton && content) {
            button.addEventListener('click', function() {
                popup.style.display = 'block';
                button.style.display = 'none';

                // Déplacer le contenu Streamlit
                const mainContent = document.querySelector('.main .block-container');
                if (mainContent && content.children.length === 0) {
                    content.appendChild(mainContent.cloneNode(true));
                }
            });

            closeButton.addEventListener('click', function() {
                popup.style.display = 'none';
                button.style.display = 'flex';
            });
        }
    });
    </script>
    """, height=0)

    # Interface du chatbot
    with st.container():
        # Afficher l'historique des messages (en haut)
        for msg in st.session_state.messages:
            st.chat_message(msg["role"]).write(msg["content"])

        # Afficher le formulaire de contact après 3 questions
        if st.session_state.question_count >= 3 and not st.session_state.form_submitted:
            with st.form(key="contact_form", clear_on_submit=True):
                st.markdown("<h3 style='text-align: center;'>Let us know how to contact you</h3>", unsafe_allow_html=True)
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

        # Champ de saisie pour le chat (en bas)
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
                        # Utiliser la réponse de secours en cas d'erreur
                        response = fallback_response(detected_lang)
                except Exception as e:
                    # En cas d'erreur, utiliser la réponse de secours
                    print(f"Erreur lors de l'appel à l'API Groq: {str(e)}")
                    response = fallback_response(detected_lang)

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
