from flask import Flask
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Configurações
app.config['JSON_SORT_KEYS'] = False

# Importar rotas
from api.ai.chat import chat_bp
from api.channel.stats import stats_bp
from api.health import health_bp

# Registrar blueprints
app.register_blueprint(chat_bp, url_prefix='/api/ai')
app.register_blueprint(stats_bp, url_prefix='/api/channel')
app.register_blueprint(health_bp)

# Handler para Vercel
@app.route('/')
def home():
    return {
        'status': 'online',
        'service': 'Twitch Channel AI Assistant',
        'endpoints': {
            'chat': '/api/ai/chat',
            'stats': '/api/channel/stats',
            'upcoming': '/api/channel/upcoming',
            'health': '/health'
        }
    }

# Para desenvolvimento local
if __name__ == '__main__':
    app.run(debug=True, port=5000)
