from datetime import datetime
from typing import Dict, List, Any
from .twitch_analyzer import TwitchAnalyzer

class ChatProcessor:
    def __init__(self):
        self.conversation_history = []
        
    def process_message(self, user_message: str, channel_data: Dict, context: Dict = None) -> Dict:
        self.conversation_history.append({
            "user": user_message,
            "timestamp": datetime.now().isoformat()
        })
        
        if len(self.conversation_history) > 10:
            self.conversation_history = self.conversation_history[-10:]
        
        analyzer = TwitchAnalyzer()
        analysis = analyzer.analyze_question(user_message)
        response = analyzer.generate_response(
            question_type=analysis["type"],
            keywords=analysis["keywords"],
            intent=analysis["intent"]
        )
        
        response = self._add_contextual_info(response, context, user_message)
        return response
    
    def _add_contextual_info(self, response: Dict, context: Dict, user_message: str) -> Dict:
        if context and context.get('is_first_message', False):
            response['answer'] = "👋 **Olá! Bem-vindo ao assistente do canal pedromartss007!**\n\n" + response['answer']
        
        if 'próxima' in user_message.lower() or 'proxima' in user_message.lower():
            response['answer'] += "\n\n📅 **Próxima stream:** Amanhã às 19:00 - Valorant!"
        
        return response
