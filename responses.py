import random

# Réponses prédéfinies par catégorie et par langue
responses = {
    "big_data": {
        "fr": [
            "Le Big Data fait référence à des ensembles de données extrêmement volumineux qui peuvent être analysés pour révéler des modèles et des tendances.",
            "Les technologies Big Data comme Hadoop et Spark permettent de traiter d'énormes volumes de données de manière distribuée.",
            "Le Big Data est caractérisé par les 3V : Volume, Vélocité et Variété des données.",
            "Les lacs de données (Data Lakes) sont des référentiels centralisés qui permettent de stocker des données structurées et non structurées à n'importe quelle échelle.",
            "L'analyse de Big Data permet aux entreprises de prendre des décisions plus éclairées et d'identifier de nouvelles opportunités."
        ],
        "en": [
            "Big Data refers to extremely large data sets that may be analyzed to reveal patterns and trends.",
            "Big Data technologies like Hadoop and Spark allow processing huge volumes of data in a distributed manner.",
            "Big Data is characterized by the 3Vs: Volume, Velocity, and Variety of data.",
            "Data Lakes are centralized repositories that allow storing structured and unstructured data at any scale.",
            "Big Data analytics enables businesses to make more informed decisions and identify new opportunities."
        ],
        "es": [
            "Big Data se refiere a conjuntos de datos extremadamente grandes que pueden analizarse para revelar patrones y tendencias.",
            "Las tecnologías de Big Data como Hadoop y Spark permiten procesar enormes volúmenes de datos de manera distribuida.",
            "Big Data se caracteriza por las 3V: Volumen, Velocidad y Variedad de datos.",
            "Los Data Lakes son repositorios centralizados que permiten almacenar datos estructurados y no estructurados a cualquier escala.",
            "El análisis de Big Data permite a las empresas tomar decisiones más informadas e identificar nuevas oportunidades."
        ]
    },
    "ai": {
        "fr": [
            "L'intelligence artificielle (IA) est la simulation de l'intelligence humaine par des machines programmées pour penser et apprendre.",
            "Les applications de l'IA incluent la reconnaissance vocale, la vision par ordinateur et les systèmes de recommandation.",
            "L'IA peut être divisée en IA faible (spécialisée dans une tâche) et IA forte (capable de raisonnement général).",
            "L'apprentissage profond (Deep Learning) est une branche de l'IA qui utilise des réseaux de neurones artificiels avec plusieurs couches.",
            "L'IA générative peut créer de nouveaux contenus comme du texte, des images ou de la musique."
        ],
        "en": [
            "Artificial Intelligence (AI) is the simulation of human intelligence in machines programmed to think and learn.",
            "AI applications include speech recognition, computer vision, and recommendation systems.",
            "AI can be divided into Narrow AI (specialized in one task) and General AI (capable of general reasoning).",
            "Deep Learning is a branch of AI that uses artificial neural networks with multiple layers.",
            "Generative AI can create new content such as text, images, or music."
        ],
        "es": [
            "La Inteligencia Artificial (IA) es la simulación de la inteligencia humana en máquinas programadas para pensar y aprender.",
            "Las aplicaciones de IA incluyen reconocimiento de voz, visión por computadora y sistemas de recomendación.",
            "La IA puede dividirse en IA estrecha (especializada en una tarea) e IA general (capaz de razonamiento general).",
            "El Deep Learning es una rama de la IA que utiliza redes neuronales artificiales con múltiples capas.",
            "La IA generativa puede crear nuevo contenido como texto, imágenes o música."
        ]
    },
    "machine_learning": {
        "fr": [
            "Le Machine Learning est une branche de l'IA qui permet aux systèmes d'apprendre et de s'améliorer à partir de l'expérience sans être explicitement programmés.",
            "Les algorithmes de Machine Learning peuvent être classés en apprentissage supervisé, non supervisé et par renforcement.",
            "L'apprentissage supervisé utilise des données étiquetées pour entraîner des modèles à faire des prédictions ou prendre des décisions.",
            "L'apprentissage non supervisé trouve des structures cachées dans des données non étiquetées.",
            "L'apprentissage par renforcement entraîne des agents à prendre des actions dans un environnement pour maximiser une récompense."
        ],
        "en": [
            "Machine Learning is a branch of AI that allows systems to learn and improve from experience without being explicitly programmed.",
            "Machine Learning algorithms can be classified into supervised, unsupervised, and reinforcement learning.",
            "Supervised learning uses labeled data to train models to make predictions or decisions.",
            "Unsupervised learning finds hidden structures in unlabeled data.",
            "Reinforcement learning trains agents to take actions in an environment to maximize a reward."
        ],
        "es": [
            "El Machine Learning es una rama de la IA que permite a los sistemas aprender y mejorar a partir de la experiencia sin ser programados explícitamente.",
            "Los algoritmos de Machine Learning pueden clasificarse en aprendizaje supervisado, no supervisado y por refuerzo.",
            "El aprendizaje supervisado utiliza datos etiquetados para entrenar modelos para hacer predicciones o tomar decisiones.",
            "El aprendizaje no supervisado encuentra estructuras ocultas en datos no etiquetados.",
            "El aprendizaje por refuerzo entrena agentes para tomar acciones en un entorno para maximizar una recompensa."
        ]
    },
    "business_intelligence": {
        "fr": [
            "La Business Intelligence (BI) utilise des outils et des technologies pour transformer des données brutes en informations significatives pour la prise de décision.",
            "Les tableaux de bord de BI permettent de visualiser les KPIs et les métriques importantes de l'entreprise.",
            "Les outils de BI populaires incluent Tableau, Power BI et QlikView.",
            "La BI aide les entreprises à identifier les tendances, à analyser les performances et à prendre des décisions basées sur les données.",
            "L'analyse prédictive est une composante de la BI qui utilise des données historiques pour prédire les tendances futures."
        ],
        "en": [
            "Business Intelligence (BI) uses tools and technologies to transform raw data into meaningful information for decision-making.",
            "BI dashboards allow visualizing important company KPIs and metrics.",
            "Popular BI tools include Tableau, Power BI, and QlikView.",
            "BI helps businesses identify trends, analyze performance, and make data-driven decisions.",
            "Predictive analytics is a component of BI that uses historical data to predict future trends."
        ],
        "es": [
            "Business Intelligence (BI) utiliza herramientas y tecnologías para transformar datos brutos en información significativa para la toma de decisiones.",
            "Los dashboards de BI permiten visualizar KPIs y métricas importantes de la empresa.",
            "Las herramientas populares de BI incluyen Tableau, Power BI y QlikView.",
            "BI ayuda a las empresas a identificar tendencias, analizar el rendimiento y tomar decisiones basadas en datos.",
            "El análisis predictivo es un componente de BI que utiliza datos históricos para predecir tendencias futuras."
        ]
    },
    "marketing_digital": {
        "fr": [
            "Le Marketing Digital englobe tous les efforts marketing qui utilisent un appareil électronique ou Internet.",
            "Le SEO (Search Engine Optimization) améliore la visibilité d'un site web dans les résultats de recherche organiques.",
            "Le marketing de contenu consiste à créer et distribuer du contenu pertinent pour attirer un public cible.",
            "Le marketing des médias sociaux utilise des plateformes comme Facebook, Instagram et LinkedIn pour promouvoir des produits ou services.",
            "L'email marketing reste l'un des canaux de marketing digital les plus efficaces en termes de retour sur investissement."
        ],
        "en": [
            "Digital Marketing encompasses all marketing efforts that use an electronic device or the internet.",
            "SEO (Search Engine Optimization) improves a website's visibility in organic search results.",
            "Content marketing involves creating and distributing relevant content to attract a target audience.",
            "Social media marketing uses platforms like Facebook, Instagram, and LinkedIn to promote products or services.",
            "Email marketing remains one of the most effective digital marketing channels in terms of return on investment."
        ],
        "es": [
            "El Marketing Digital abarca todos los esfuerzos de marketing que utilizan un dispositivo electrónico o Internet.",
            "El SEO (Search Engine Optimization) mejora la visibilidad de un sitio web en los resultados de búsqueda orgánicos.",
            "El marketing de contenidos consiste en crear y distribuir contenido relevante para atraer a una audiencia objetivo.",
            "El marketing en redes sociales utiliza plataformas como Facebook, Instagram y LinkedIn para promocionar productos o servicios.",
            "El email marketing sigue siendo uno de los canales de marketing digital más efectivos en términos de retorno de inversión."
        ]
    },
    "data_science": {
        "fr": [
            "La Data Science combine des domaines comme les statistiques, l'informatique et l'expertise métier pour extraire des connaissances et des insights à partir des données.",
            "Le processus de Data Science comprend la collecte, le nettoyage, l'analyse et la visualisation des données.",
            "Les data scientists utilisent des langages comme Python et R pour analyser les données.",
            "La Data Science est utilisée dans de nombreux secteurs, notamment la finance, la santé, le e-commerce et les transports.",
            "Les techniques de Data Science incluent la régression, la classification, le clustering et la réduction de dimensionnalité."
        ],
        "en": [
            "Data Science combines fields like statistics, computer science, and domain expertise to extract knowledge and insights from data.",
            "The Data Science process includes collecting, cleaning, analyzing, and visualizing data.",
            "Data scientists use languages like Python and R to analyze data.",
            "Data Science is used in many industries including finance, healthcare, e-commerce, and transportation.",
            "Data Science techniques include regression, classification, clustering, and dimensionality reduction."
        ],
        "es": [
            "La Ciencia de Datos combina campos como estadística, informática y experiencia en el dominio para extraer conocimiento e insights de los datos.",
            "El proceso de Ciencia de Datos incluye recopilar, limpiar, analizar y visualizar datos.",
            "Los científicos de datos utilizan lenguajes como Python y R para analizar datos.",
            "La Ciencia de Datos se utiliza en muchas industrias, incluyendo finanzas, salud, comercio electrónico y transporte.",
            "Las técnicas de Ciencia de Datos incluyen regresión, clasificación, clustering y reducción de dimensionalidad."
        ]
    },
    "default": {
        "fr": [
            "Je suis un assistant spécialisé dans les domaines du Big Data, de l'IA, du Machine Learning, de la Business Intelligence, du Marketing Digital et de la Data Science.",
            "Je peux vous aider à comprendre les concepts clés dans ces domaines et à répondre à vos questions spécifiques.",
            "N'hésitez pas à me poser des questions sur ces sujets pour obtenir des informations détaillées.",
            "Je suis là pour vous aider à naviguer dans le monde complexe des données et de l'intelligence artificielle.",
            "Comment puis-je vous aider aujourd'hui dans votre projet lié aux données ou à l'IA ?"
        ],
        "en": [
            "I am an assistant specialized in the fields of Big Data, AI, Machine Learning, Business Intelligence, Digital Marketing, and Data Science.",
            "I can help you understand key concepts in these areas and answer your specific questions.",
            "Feel free to ask me questions about these topics to get detailed information.",
            "I'm here to help you navigate the complex world of data and artificial intelligence.",
            "How can I assist you today with your data or AI-related project?"
        ],
        "es": [
            "Soy un asistente especializado en los campos de Big Data, IA, Machine Learning, Business Intelligence, Marketing Digital y Ciencia de Datos.",
            "Puedo ayudarte a entender conceptos clave en estas áreas y responder a tus preguntas específicas.",
            "No dudes en hacerme preguntas sobre estos temas para obtener información detallada.",
            "Estoy aquí para ayudarte a navegar por el complejo mundo de los datos y la inteligencia artificial.",
            "¿Cómo puedo ayudarte hoy con tu proyecto relacionado con datos o IA?"
        ]
    }
}

def get_response(question, lang="en"):
    """Retourne une réponse prédéfinie en fonction de la question et de la langue"""
    question = question.lower()
    
    # Déterminer la catégorie de la question
    if any(kw in question for kw in ["big data", "hadoop", "spark", "data lake", "data warehouse", "nosql"]):
        category = "big_data"
    elif any(kw in question for kw in ["ai", "artificial intelligence", "intelligence artificielle", "ia", "chatgpt", "llm"]):
        category = "ai"
    elif any(kw in question for kw in ["machine learning", "ml", "deep learning", "apprentissage", "neural network", "réseau de neurones"]):
        category = "machine_learning"
    elif any(kw in question for kw in ["bi", "business intelligence", "tableau", "power bi", "dashboard", "tableau de bord", "kpi"]):
        category = "business_intelligence"
    elif any(kw in question for kw in ["marketing", "seo", "sem", "référencement", "analytics", "social media", "réseaux sociaux"]):
        category = "marketing_digital"
    elif any(kw in question for kw in ["data science", "science des données", "statistiques", "statistics", "predictive", "prédictive"]):
        category = "data_science"
    else:
        # Catégorie par défaut
        category = "default"
    
    # Sélectionner la langue (par défaut anglais)
    if lang in ["fr", "fr-fr"]:
        lang_key = "fr"
    elif lang in ["es", "es-es"]:
        lang_key = "es"
    else:
        lang_key = "en"
    
    # Si la langue n'est pas disponible, utiliser l'anglais
    if lang_key not in responses[category]:
        lang_key = "en"
    
    # Retourner une réponse aléatoire de la catégorie et langue appropriées
    return random.choice(responses[category][lang_key])
