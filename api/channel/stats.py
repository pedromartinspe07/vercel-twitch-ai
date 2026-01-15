from flask import Blueprint, jsonify
import datetime

stats_bp = Blueprint('stats', __name__)

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
    "community_vibe": "Descontraído, humorístico, interativo"
}

@stats_bp.route('/stats', methods=['GET'])
def get_channel_stats():
    return jsonify({
        'success': True,
        'data': CHANNEL_DATA,
        'timestamp': datetime.datetime.now().isoformat()
    })

@stats_bp.route('/upcoming', methods=['GET'])
def get_upcoming_streams():
    today = datetime.datetime.now().strftime('%A').lower()
    
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    today_index = days.index(today) if today in days else 0
    
    upcoming = []
    for i in range(1, 8):  # Próximos 7 dias
        day_index = (today_index + i) % 7
        day_name = days[day_index]
        if CHANNEL_DATA['stream_schedule'][day_name] != 'Descanso':
            upcoming.append({
                'day': day_name.capitalize(),
                'schedule': CHANNEL_DATA['stream_schedule'][day_name],
                'days_from_today': i
            })
            if len(upcoming) >= 3:
                break
    
    return jsonify({
        'success': True,
        'upcoming_streams': upcoming,
        'timestamp': datetime.datetime.now().isoformat()
    })
