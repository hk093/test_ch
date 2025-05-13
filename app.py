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
    elif lang in ['de', 'de-de']:
        return "Es tut mir leid, aber ich kann nur Fragen zu Big Data, KI, maschinellem Lernen, Business Intelligence, digitalem Marketing, Data Science und verwandten Themen beantworten. Zögern Sie nicht, mir eine Frage zu diesen Bereichen zu stellen."
    elif lang in ['it', 'it-it']:
        return "Mi dispiace, ma posso rispondere solo a domande su Big Data, AI, Machine Learning, Business Intelligence, Digital Marketing, Data Science e argomenti correlati. Non esitare a farmi una domanda in queste aree."
    elif lang in ['pt', 'pt-pt', 'pt-br']:
        return "Desculpe, mas só posso responder a perguntas sobre Big Data, IA, Machine Learning, Business Intelligence, Marketing Digital, Data Science e tópicos relacionados. Não hesite em fazer-me uma pergunta nestas áreas."
    elif lang in ['ar']:
        return "آسف، لكنني أستطيع فقط الإجابة على الأسئلة المتعلقة بالبيانات الضخمة، والذكاء الاصطناعي، والتعلم الآلي، وذكاء الأعمال، والتسويق الرقمي، وعلوم البيانات والمواضيع ذات الصلة. لا تتردد في طرح سؤال في هذه المجالات."
    else:
        # Anglais par défaut
        return "I'm sorry, but I can only answer questions about Big Data, AI, Machine Learning, Business Intelligence, Digital Marketing, Data Science, and related topics. Feel free to ask me a question in these areas."

# Fonction pour vérifier si la question est liée aux domaines autorisés
def is_relevant_question(question):
    # Liste des mots-clés et domaines autorisés
    relevant_keywords = [
        # Big Data
        "big data", "hadoop", "spark", "data lake", "data warehouse", "nosql", "mongodb", "cassandra",
        # IA
        "ai", "artificial intelligence", "intelligence artificielle", "ia", "machine learning", "ml",
        "deep learning", "apprentissage profond", "neural network", "réseau de neurones",
        # Marketing
        "marketing", "seo", "sem", "référencement", "analytics", "google analytics", "social media",
        "réseaux sociaux", "content marketing", "marketing de contenu", "email marketing",
        # BI & Dashboarding
        "bi", "business intelligence", "tableau", "power bi", "qlik", "dashboard", "tableau de bord",
        "kpi", "reporting", "data visualization", "visualisation de données",
        # Data Mining
        "data mining", "fouille de données", "clustering", "classification", "regression", "régression",
        "association rules", "règles d'association", "pattern recognition", "reconnaissance de formes",
        # NLP
        "nlp", "natural language processing", "traitement du langage naturel", "text mining",
        "sentiment analysis", "analyse de sentiment", "chatbot", "chat bot", "language model",
        # AI Ethics
        "ai ethics", "éthique de l'ia", "responsible ai", "ia responsable", "bias", "biais",
        "fairness", "équité", "transparency", "transparence", "explainability", "explicabilité",
        # Data Science
        "data science", "science des données", "statistiques", "statistics", "predictive analytics",
        "analytique prédictive", "forecasting", "prévision", "data analysis", "analyse de données"
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

        # Sauvegarder dans un fichier JSON (comme sauvegarde)
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

        # Essayer d'envoyer un email
        try:
            # Configurer l'email
            msg = MIMEMultipart()
            msg['From'] = 'chatbot@example.com'  # Remplacer par votre adresse email
            msg['To'] = 'Houssemeddinekamkoum@gmail.com'  # Votre adresse email
            msg['Subject'] = f'Nouveau lead du chatbot: {name}'

            # Ajouter le corps du message
            msg.attach(MIMEText(message_text, 'plain'))

            # Configurer le serveur SMTP - Vous devrez remplacer ces valeurs
            # Note: Pour Gmail, vous devrez activer "Less secure apps" ou utiliser un mot de passe d'application
            # server = smtplib.SMTP('smtp.gmail.com', 587)
            # server.starttls()
            # server.login('votre_email@gmail.com', 'votre_mot_de_passe')
            # server.send_message(msg)
            # server.quit()

            # Pour l'instant, nous ne faisons que simuler l'envoi d'email
            print(f"Email envoyé à Houssemeddinekamkoum@gmail.com avec les informations du lead: {name}, {email}, {phone}")

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

    # CSS pour le design du popup
    popup_css = """
    <style>
    @keyframes fadeIn {
        from { opacity: 0; transform: scale(0.95); }
        to { opacity: 1; transform: scale(1); }
    }

    @keyframes fadeOut {
        from { opacity: 1; transform: scale(1); }
        to { opacity: 0; transform: scale(0.95); }
    }

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

    /* Style pour la zone de chat */
    .stChatContainer {
        display: flex;
        flex-direction: column;
    }

    /* Style pour les messages du chat */
    .stChatMessage {
        margin-bottom: 10px;
    }

    /* Style pour le champ de saisie */
    .stChatInputContainer {
        margin-top: 20px;
        border-top: 1px solid #f0f0f0;
        padding-top: 15px;
    }
    </style>
    """

    # JavaScript pour gérer le popup
    popup_js = """
    <script>
    // Créer le bouton et le popup
    document.body.insertAdjacentHTML('beforeend', `
        <!-- Bouton violet rond avec logo BID -->
        <button id="chatbotButton" style="
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
            z-index: 9999;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
        ">
            <img src="https://i.postimg.cc/YjYPXYFm/logo.png" alt="BID Logo" style="
                width: 32px;
                height: 32px;
                filter: brightness(0) invert(1); /* Pour un logo blanc */
            ">
        </button>

        <!-- Pop-up du chatbot -->
        <div id="chatbotPopup" style="
            display: none;
            position: fixed;
            bottom: 20px;
            right: 20px;
            width: 380px;
            height: 600px;
            background: white;
            border-radius: 20px;
            overflow: hidden;
            box-shadow: 0 15px 50px rgba(127, 63, 191, 0.2);
            z-index: 9999;
            animation: fadeIn 0.3s ease-in-out;
            font-family: Arial, sans-serif;
        ">
            <!-- En-tête du pop-up -->
            <div style="
                background: #7f3fbf;
                color: white;
                padding: 16px;
                font-size: 18px;
                font-weight: bold;
                display: flex;
                align-items: center;
                justify-content: space-between;
            ">
                <span>Assistance Chatbot</span>
                <button id="closeButton" style="
                    background: none;
                    border: none;
                    font-size: 20px;
                    color: white;
                    cursor: pointer;
                ">✖</button>
            </div>

            <!-- En-tête avec logo BID -->
            <div style="
                padding: 15px;
                display: flex;
                align-items: center;
                border-bottom: 1px solid #f0f0f0;
            ">
                <div style="
                    display: flex;
                    align-items: center;
                ">
                    <img src="https://i.postimg.cc/YjYPXYFm/logo.png" alt="BID Logo" style="
                        width: 40px;
                        height: 40px;
                        margin-right: 10px;
                    ">
                    <div>
                        <div style="font-weight: bold;">BID Consulting</div>
                    </div>
                </div>
                <div style="margin-left: auto; color: #666; font-size: 20px;">⋮</div>
            </div>

            <!-- Formulaire de contact -->
            <div id="contactForm" style="
                display: none;
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: white;
                z-index: 10000;
                padding: 20px;
                box-sizing: border-box;
                animation: fadeIn 0.3s ease-in-out;
            ">
                <div style="
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    margin-bottom: 20px;
                ">
                    <h3 style="margin: 0; font-size: 18px;">Let us know how to contact you</h3>
                    <button id="closeFormButton" style="
                        background: none;
                        border: none;
                        font-size: 20px;
                        cursor: pointer;
                    ">✖</button>
                </div>

                <div style="margin-bottom: 15px;">
                    <label for="name" style="display: block; margin-bottom: 5px; font-weight: bold;">Name</label>
                    <input type="text" id="name" style="
                        width: 100%;
                        padding: 10px;
                        border: 1px solid #ddd;
                        border-radius: 5px;
                        box-sizing: border-box;
                    ">
                </div>

                <div style="margin-bottom: 15px;">
                    <label for="email" style="display: block; margin-bottom: 5px; font-weight: bold;">Email</label>
                    <input type="email" id="email" style="
                        width: 100%;
                        padding: 10px;
                        border: 1px solid #ddd;
                        border-radius: 5px;
                        box-sizing: border-box;
                    ">
                </div>

                <div style="margin-bottom: 20px;">
                    <label for="phone" style="display: block; margin-bottom: 5px; font-weight: bold;">Phone Number</label>
                    <input type="tel" id="phone" style="
                        width: 100%;
                        padding: 10px;
                        border: 1px solid #ddd;
                        border-radius: 5px;
                        box-sizing: border-box;
                    ">
                </div>

                <button id="submitForm" style="
                    background: #7f3fbf;
                    color: white;
                    border: none;
                    padding: 10px 15px;
                    border-radius: 5px;
                    cursor: pointer;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                ">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" style="margin-right: 5px;">
                        <path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z" fill="white"/>
                    </svg>
                    Submit
                </button>
            </div>

            <!-- Contenu du chatbot -->
            <div id="chatbotContent" style="width: 100%; height: calc(100% - 120px); overflow-y: auto;"></div>
        </div>
    `);

    // Variables pour suivre le nombre de questions
    let questionCount = 0;
    let formShown = false;

    // Fonction pour montrer le formulaire
    function showContactForm() {
        const form = document.getElementById("contactForm");
        form.style.display = "block";
        formShown = true;
    }

    // Fonction pour cacher le formulaire
    function hideContactForm() {
        const form = document.getElementById("contactForm");
        form.style.display = "none";
    }

    // Fonction pour soumettre le formulaire
    function submitContactForm() {
        const name = document.getElementById("name").value;
        const email = document.getElementById("email").value;
        const phone = document.getElementById("phone").value;

        if (!name || !email || !phone) {
            alert("Veuillez remplir tous les champs");
            return;
        }

        // Envoyer les données à Streamlit
        window.parent.postMessage({
            type: 'streamlit:setComponentValue',
            value: {
                action: 'submit_form',
                name: name,
                email: email,
                phone: phone
            }
        }, '*');

        // Cacher le formulaire
        hideContactForm();

        // Afficher un message de confirmation
        const chatContent = document.getElementById("chatbotContent");
        const streamlitChat = chatContent.querySelector('.stChatContainer');
        if (streamlitChat) {
            const thankYouMessage = document.createElement('div');
            thankYouMessage.innerHTML = `
                <div style="
                    background: #f0f0f0;
                    padding: 12px;
                    border-radius: 18px;
                    margin: 10px 0;
                    max-width: 80%;
                    color: #333;
                ">
                    Merci pour vos informations ! Nous vous contacterons bientôt.
                </div>
            `;
            streamlitChat.appendChild(thankYouMessage);
        }
    }

    // Fonctions pour ouvrir et fermer le chatbot
    function openChatbot() {
        const popup = document.getElementById("chatbotPopup");
        popup.style.display = "block";
        popup.style.animation = "fadeIn 0.3s ease-in-out";

        // Déplacer le contenu Streamlit dans le popup
        const mainContent = document.querySelector('.main .block-container');
        const chatContent = document.getElementById("chatbotContent");
        if (mainContent && chatContent && chatContent.children.length === 0) {
            chatContent.appendChild(mainContent.cloneNode(true));

            // Appliquer des styles supplémentaires pour améliorer l'apparence
            setTimeout(() => {
                // Ajouter un peu d'espace en haut pour que les messages ne soient pas collés à l'en-tête
                const chatContainer = chatContent.querySelector('.stChatContainer');
                if (chatContainer) {
                    chatContainer.style.paddingTop = '20px';
                }
            }, 500);
        }
    }

    function closeChatbot() {
        const popup = document.getElementById("chatbotPopup");
        popup.style.animation = "fadeOut 0.3s ease-in-out";
        setTimeout(() => {
            popup.style.display = "none";
        }, 300);
    }

    // Observer pour détecter les nouveaux messages de l'utilisateur
    function setupChatObserver() {
        // Utiliser un MutationObserver pour détecter les nouveaux messages
        const chatContent = document.getElementById("chatbotContent");
        if (!chatContent) return;

        const observer = new MutationObserver(function(mutations) {
            mutations.forEach(function(mutation) {
                if (mutation.type === 'childList' && mutation.addedNodes.length > 0) {
                    // Chercher les nouveaux messages de l'utilisateur
                    const userMessages = chatContent.querySelectorAll('.stChatMessage[data-testid="stChatMessage-USER"]');

                    // Si le nombre de messages a augmenté et que nous n'avons pas encore montré le formulaire
                    if (userMessages.length > questionCount && !formShown) {
                        questionCount = userMessages.length;

                        // Après 3 questions, montrer le formulaire
                        if (questionCount >= 3) {
                            setTimeout(showContactForm, 1000);
                        }
                    }
                }
            });
        });

        // Observer les changements dans le contenu du chat
        observer.observe(chatContent, { childList: true, subtree: true });
    }

    // Ajouter les événements aux boutons
    document.addEventListener('DOMContentLoaded', function() {
        document.getElementById("chatbotButton").addEventListener("click", function() {
            openChatbot();
            // Mettre en place l'observateur après un court délai pour s'assurer que le contenu est chargé
            setTimeout(setupChatObserver, 500);
        });
        document.getElementById("closeButton").addEventListener("click", closeChatbot);
        document.getElementById("closeFormButton").addEventListener("click", hideContactForm);
        document.getElementById("submitForm").addEventListener("click", submitContactForm);
    });
    </script>
    """

    # Injecter le CSS et le JavaScript
    st.markdown(popup_css, unsafe_allow_html=True)
    components.html(popup_js, height=0)

    # Contenu principal (sera caché dans le popup)
    with st.container():
        st.title("Bienvenue sur notre site")
        st.write("Cliquez sur le bouton en bas à droite pour discuter avec notre assistant IA.")

        st.header("Contenu du site")
        st.write("Ce contenu sera visible sur la page principale mais pas dans le popup.")

    # Traiter les soumissions du formulaire
    form_data = st.query_params.get("streamlitForm", None)
    if form_data:
        try:
            import json
            form_data = json.loads(form_data[0])
            if form_data.get("action") == "submit_form":
                name = form_data.get("name", "")
                email = form_data.get("email", "")
                phone = form_data.get("phone", "")

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
        except Exception as e:
            st.error(f"Erreur lors du traitement du formulaire: {str(e)}")

    # Interface du chatbot (sera déplacée dans le popup par JavaScript)
    with st.container():
        # Afficher l'historique des messages (en haut)
        # Afficher les messages dans l'ordre chronologique (du plus ancien au plus récent)
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

            # Ajouter la langue détectée à la session pour référence future
            st.session_state.detected_lang = detected_lang

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

                response = chat_with_groq(messages_with_lang)
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