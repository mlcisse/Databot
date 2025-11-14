#!/usr/bin/env python3
"""
Script de test pour vérifier la configuration sauvegardée
"""
import json
import os
from openai import OpenAI

def test_config():
    print("=== Test de la configuration ===")
    
    config_file = 'databot_config.json'
    
    if not os.path.exists(config_file):
        print("❌ Fichier de configuration non trouvé")
        print("💡 Allez dans l'application, Settings, et configurez votre clé API")
        return
    
    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
        
        api_key = config.get('openai_api_key')
        
        if not api_key:
            print("❌ Aucune clé API dans la configuration")
            return
        
        print(f"🔑 Clé API trouvée: {api_key[:10]}...{api_key[-4:] if len(api_key) > 14 else '***'}")
        print(f"📏 Longueur: {len(api_key)}")
        print(f"🎯 Commence par 'sk-': {api_key.startswith('sk-')}")
        
        print("\n🧪 Test de l'API...")
        
        # Test simple avec un petit message
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": "Bonjour, dis juste 'Test réussi'"}
            ],
            max_tokens=10
        )
        
        print("✅ Test réussi!")
        print(f"📝 Réponse: {response.choices[0].message.content}")
        print(f"💰 Tokens utilisés: {response.usage.total_tokens}")
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        print(f"🔍 Type d'erreur: {type(e).__name__}")
        
        # Analyser le type d'erreur
        if "401" in str(e):
            print("🚫 Erreur 401: Clé API invalide ou expirée")
        elif "429" in str(e):
            print("⏰ Erreur 429: Limite de taux dépassée")
            print("💡 Solutions possibles:")
            print("   - Vérifiez votre quota sur https://platform.openai.com/usage")
            print("   - Vérifiez votre plan sur https://platform.openai.com/account/billing")
            print("   - Vérifiez si vous avez des limites de taux (rate limits)")
            print("   - Attendez quelques minutes avant de réessayer")
        elif "insufficient_quota" in str(e):
            print("💳 Quota insuffisant:")
            print("   - Vérifiez votre solde sur https://platform.openai.com/usage")
            print("   - Ajoutez des crédits si nécessaire")
        else:
            print("❓ Erreur inconnue - vérifiez votre connexion internet")

if __name__ == "__main__":
    test_config()
