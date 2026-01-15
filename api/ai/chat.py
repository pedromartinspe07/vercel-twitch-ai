from flask import Blueprint, request, jsonify
import json
from datetime import datetime
import sys
import os

# Adicionar diretório pai ao path
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from utils.twitch_analyzer import TwitchAnalyzer
from utils.chat_processor import ChatProcessor

chat_bp = Blueprint('chat', __name__)

# Inicializar analisadores (cache em memória)
twitch_analyzer = None
chat_processor = None

def get_analyzers():
    global twitch_analyzer, chat_processor
    if twitch_analyzer is None:
        twitch_analyzer = TwitchAnalyzer()
    if chat_processor is None:
        chat_processor = ChatProcessor()
    return twitch_analyzer, chat_processor

# Dados do canal (cache)
CHANNEL_DATA = {
    "channel_name": "pedromartss007",
    "followers": 5200,
    "total_views": 125000,
    "created_at": "2022-03-15",
    "stream_schedule": {
        "monday": "19:00-22:00 - Valorant",
        "tuesday": "20:00-23:00 - Minecraft",
        "wednesday": "18:00-21:00 - Fortnite",
        "thursday": "19:00-22:00 - Jogos Indies",
        "friday": "20:00-00:00 - Variedades",
        "saturday": "15:00-19:00 - Especial da Semana",
        "sunday": "Descanso"
    },
    "most_popular_games": ["Valorant", "Minecraft", "Fortnite", "The Finals", "CS2"],
    "avg_viewers": 85,
    "peak_viewers": 215,
    "content_type": "Gameplay variado com foco em FPS e jogos multiplayer",
    "community_vibe": "Descontraído, humorístico, interativo",
    "special_events": ["Sábado de Especiais", "Torneios com Viewers", "Maratonas Mensais"],
    "chat_rules": [
        "Respeito é obrigatório",
        "Sem preconceito",
        "Nada de spam",
        "Conteúdo NSFW proibido"
    ]
}

@chat_bp.route('/chat', methods=['POST', 'OPTIONS'])
def chat_with_ai():
    if request.method == 'OPTIONS':
        return '', 200
    
    try:
        data = request.json
        if not data:
            return jsonify({
                'success': False,
                'error': 'No data provided'
            }), 400
        
        user_message = data.get('message', '').strip()
        if not user_message:
            return jsonify({
                'success': False,
                'error': 'Message is required'
            }), 400
        
        context = data.get('context', {})
        
        # Processar a mensagem
        twitch_analyzer, chat_processor = get_analyzers()
        response = chat_processor.process_message(
            user_message=user_message,
            channel_data=CHANNEL_DATA,
            context=context
        )
        
        return jsonify({
            'success': True,
            'response': response['answer'],
            'suggestions': response.get('suggestions', []),
            'data': response.get('data', {}),
            'type': response.get('type', 'text'),
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500
