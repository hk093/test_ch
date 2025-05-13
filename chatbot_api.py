import streamlit as st
from memory import load_memory, save_memory, get_user_id, manage_memory
from chathun import chat_with_groq
from config import GROQ_API_KEY
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/chat', methods=['POST'])
def chat():
    """API endpoint pour le chatbot"""
    try:
        # Récupérer les données de la requête
        data = request.json
        message = data.get('message', '')
        
        if not message:
            return jsonify({'error': 'Message vide'}), 400
        
        # Initialiser la mémoire
        user_id = get_user_id()
        memory = load_memory()
        
        # Récupérer ou initialiser les messages
        if user_id in memory and "conversation" in memory[user_id]:
            messages = memory[user_id]["conversation"]
        else:
            messages = [
                {"role": "assistant", "content": "Bonjour ! Comment puis-je vous aider aujourd'hui ?"}
            ]
        
        # Ajouter le message de l'utilisateur
        messages.append({"role": "user", "content": message})
        
        # Obtenir la réponse de l'IA
        response = chat_with_groq(messages)
        
        # Ajouter la réponse de l'IA
        messages.append({"role": "assistant", "content": response})
        
        # Gérer la longueur de la conversation et sauvegarder
        messages = manage_memory(messages)
        save_memory(user_id, messages)
        
        # Retourner la réponse
        return jsonify({
            'response': response,
            'conversation': messages
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/history', methods=['GET'])
def history():
    """API endpoint pour récupérer l'historique des messages"""
    try:
        # Initialiser la mémoire
        user_id = get_user_id()
        memory = load_memory()
        
        # Récupérer ou initialiser les messages
        if user_id in memory and "conversation" in memory[user_id]:
            messages = memory[user_id]["conversation"]
        else:
            messages = [
                {"role": "assistant", "content": "Bonjour ! Comment puis-je vous aider aujourd'hui ?"}
            ]
        
        # Retourner l'historique
        return jsonify({
            'messages': messages
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
