# Chatbot BID Consulting

Un chatbot intelligent spécialisé dans le Big Data, l'IA, le Machine Learning et le Marketing Digital, développé avec Streamlit et l'API Groq.

## 🌟 Fonctionnalités Principales

- Interface utilisateur moderne et responsive
- Support multilingue (Français, Anglais, Espagnol)
- Réponses intelligentes basées sur l'IA via l'API Groq
- Système de capture de leads intégré
- Historique des conversations
- Notification par email des nouveaux leads
- Interface popup élégante

## 📚 Documentation Détaillée des Fonctions

### 1. Gestion des Conversations (`app_new.py`)

#### Fonction Principale
```python
def main():
    """
    Fonction principale qui initialise et gère l'interface du chatbot.
    - Configure la page Streamlit
    - Initialise la mémoire des conversations
    - Gère l'interface utilisateur
    - Traite les interactions utilisateur
    """
```

#### Gestion des Messages
```python
def fallback_response(detected_lang):
    """
    Génère une réponse de secours si l'API ne fonctionne pas.
    Args:
        detected_lang (str): Code de la langue détectée ('fr', 'es', 'en')
    Returns:
        str: Message de secours dans la langue appropriée
    """
```

```python
def detect_language(text):
    """
    Détecte la langue du texte fourni.
    Args:
        text (str): Texte à analyser
    Returns:
        str: Code de la langue détectée
    """
```

```python
def is_relevant_question(question):
    """
    Vérifie si la question est liée aux domaines autorisés.
    Args:
        question (str): Question de l'utilisateur
    Returns:
        bool: True si la question est pertinente
    """
```

### 2. Gestion des Leads (`app_new.py`)

```python
def send_lead_email(name, email, phone):
    """
    Envoie un email de notification pour un nouveau lead.
    Args:
        name (str): Nom du lead
        email (str): Email du lead
        phone (str): Numéro de téléphone du lead
    Returns:
        tuple: (success: bool, message: str)
    """
```

### 3. Interface avec l'API Groq (`chathun.py`)

```python
def chat_with_groq(messages):
    """
    Communique avec l'API Groq pour obtenir des réponses.
    Args:
        messages (list): Liste des messages de la conversation
    Returns:
        str: Réponse de l'API Groq
    """
```

### 4. Gestion de la Mémoire (`memory.py`)

```python
def load_memory():
    """
    Charge l'historique des conversations depuis le fichier JSON.
    Returns:
        dict: Historique des conversations
    """
```

```python
def save_memory(user_id, messages):
    """
    Sauvegarde l'historique des conversations.
    Args:
        user_id (str): Identifiant unique de l'utilisateur
        messages (list): Messages à sauvegarder
    """
```

```python
def manage_memory(messages):
    """
    Gère la taille de l'historique des conversations.
    Args:
        messages (list): Liste des messages
    Returns:
        list: Messages filtrés
    """
```

### 5. Configuration (`config.py`)

```python
# Variables de Configuration
GROQ_API_KEY = "votre_clé_api"  # Clé API Groq
GROQ_CHAT_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = "mixtral-8x7b-32768"  # Modèle IA utilisé
MEMORY_FILE = "chat_memory.json"  # Fichier de stockage des conversations
MAX_MESSAGES = 20  # Nombre maximum de messages en mémoire
```

## 🔍 Domaines de Connaissances du Chatbot

Le chatbot est spécialisé dans les domaines suivants :

### Big Data
- Hadoop
- Spark
- Data Lake
- Data Warehouse
- NoSQL

### Intelligence Artificielle
- Machine Learning
- Deep Learning
- Réseaux de Neurones
- NLP
- Éthique de l'IA

### Marketing Digital
- SEO/SEM
- Analytics
- Référencement
- Marketing Digital

### Business Intelligence
- Tableau
- Power BI
- Dashboards
- Data Mining
- Statistiques

## 🛠️ Fonctionnalités Techniques

### Système de Détection de Langue
- Détection automatique du français, anglais et espagnol
- Adaptation des réponses à la langue détectée
- Messages d'erreur localisés

### Système de Vérification de Pertinence
- Liste de mots-clés par domaine
- Vérification de la pertinence des questions
- Réponses adaptées pour les questions hors sujet

### Système de Capture de Leads
- Déclenchement après 3 questions
- Validation des données
- Stockage sécurisé
- Notifications email

### Interface Utilisateur
- Mode popup responsive
- Animations fluides
- Adaptation au thème
- Gestion des erreurs

## 🔧 Configuration Avancée

### Configuration Email SMTP
```python
SMTP_CONFIG = {
    "server": "smtp.gmail.com",
    "port": 465,
    "sender": "votre_email@gmail.com",
    "password": "votre_mot_de_passe_app",
    "recipient": "destinataire@email.com"
}
```

### Configuration de la Mémoire
```python
MEMORY_CONFIG = {
    "file": "chat_memory.json",
    "max_messages": 20,
    "leads_file": "leads.json"
}
```

## 🚀 Installation et Démarrage

1. Installation des dépendances :
```bash
pip install -r requirements.txt
```

2. Configuration :
```bash
# .env
GROQ_API_KEY=votre_clé_api_groq
```

3. Lancement :
```bash
streamlit run app_new.py
```

## 📞 Support et Contact

Pour toute question technique ou assistance :
- Email : [votre_email@example.com]
- Issues GitHub : [lien_vers_issues]

## 🔒 Sécurité et Confidentialité

- Stockage sécurisé des clés API
- Protection des données utilisateur
- Validation des entrées
- Gestion sécurisée des emails

## 🤝 Contribution

Les contributions sont les bienvenues ! Voir CONTRIBUTING.md pour les détails.

## 📝 License

Ce projet est sous licence MIT. Voir LICENSE pour plus de détails.

## 📁 Structure du Projet

```
chatbot_site/
├── app_new.py          # Application principale
├── config.py           # Configuration (API keys, URLs)
├── memory.py           # Gestion de la mémoire des conversations
├── chathun.py         # Interface avec l'API Groq
├── leads.json         # Stockage des leads
├── chat_memory.json   # Historique des conversations
└── README.md          # Documentation
``` 