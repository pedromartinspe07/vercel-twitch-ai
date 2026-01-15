import re
from typing import Dict, List, Any

class TwitchAnalyzer:
    def __init__(self):
        self.knowledge_base = self._load_knowledge_base()
    
    def _load_knowledge_base(self) -> Dict:
        return {
            "about_channel": {
                "name": "pedromartss007",
                "owner": "Pedro Martss",
                "content_focus": "Gameplay variado com ênfase em FPS e jogos multiplayer",
                "stream_style": "Interativo, humorístico e descontraído",
                "community_description": "Comunidade ativa e engajada"
            }
        }
    
    def analyze_question(self, question: str) -> Dict[str, Any]:
        question_lower = question.lower()
        
        keyword_mapping = {
            "horário": "schedule", "horario": "schedule", "quando": "schedule",
            "hora": "schedule", "stream": "schedule", "live": "schedule",
            "jogo": "games", "jogar": "games", "valorant": "games",
            "minecraft": "games", "fortnite": "games", "cs": "games",
            "doar": "donations", "doação": "donations", "apoio": "donations",
            "regra": "rules", "proibido": "rules", "chat": "rules",
            "discord": "community", "comunidade": "community", "grupo": "community",
            "setup": "technical", "pc": "technical", "equipamento": "technical",
            "sobre": "about", "quem": "about", "canal": "about",
            "dica": "tips", "ajuda": "tips", "como": "tips",
            "especial": "events", "evento": "events", "torneio": "events"
        }
        
        question_type = "general"
        for keyword, q_type in keyword_mapping.items():
            if keyword in question_lower:
                question_type = q_type
                break
        
        return {
            "type": question_type,
            "keywords": self._extract_keywords(question),
            "intent": self._determine_intent(question)
        }
    
    def _extract_keywords(self, text: str) -> List[str]:
        common_words = {"o", "a", "os", "as", "de", "do", "da", "dos", "das", 
                       "em", "no", "na", "nos", "nas", "por", "para", "com",
                       "que", "é", "são", "um", "uma", "uns", "umas"}
        
        words = re.findall(r'\b\w+\b', text.lower())
        keywords = [word for word in words if word not in common_words and len(word) > 2]
        
        return list(set(keywords))[:10]
    
    def _determine_intent(self, question: str) -> str:
        question_lower = question.lower()
        
        intents = {
            "information": ["qual", "quando", "onde", "como", "quem", "o que"],
            "confirmation": ["é verdade", "você joga", "tem", "faz"],
            "recommendation": ["recomenda", "sugere", "melhor", "prefere"],
            "explanation": ["por que", "como funciona", "explica"]
        }
        
        for intent, triggers in intents.items():
            for trigger in triggers:
                if trigger in question_lower:
                    return intent
        
        return "general_inquiry"
    
    def generate_response(self, question_type: str, keywords: List[str], intent: str) -> Dict:
        responses = {
            "schedule": self._get_schedule_response(),
            "games": self._get_games_response(keywords),
            "donations": self._get_donations_response(),
            "rules": self._get_rules_response(),
            "community": self._get_community_response(),
            "technical": self._get_technical_response(),
            "about": self._get_about_response(),
            "tips": self._get_tips_response(keywords),
            "events": self._get_events_response(),
            "general": self._get_general_response(keywords)
        }
        
        return responses.get(question_type, responses["general"])
    
    def _get_schedule_response(self) -> Dict:
        return {
            "answer": "📅 **Horário das Streams:**\n\n" +
                     "• **Segunda:** 19:00-22:00 - Valorant\n" +
                     "• **Terça:** 20:00-23:00 - Minecraft\n" +
                     "• **Quarta:** 18:00-21:00 - Fortnite\n" +
                     "• **Quinta:** 19:00-22:00 - Jogos Indies\n" +
                     "• **Sexta:** 20:00-00:00 - Variedades\n" +
                     "• **Sábado:** 15:00-19:00 - Especial da Semana\n" +
                     "• **Domingo:** Descanso\n\n" +
                     "Siga nas redes para atualizações! 🎮",
            "suggestions": ["Próxima stream", "Jogos que mais jogo", "Streams especiais"],
            "type": "schedule"
        }
    
    def _get_games_response(self, keywords: List[str]) -> Dict:
        games_info = {
            "valorant": "🎯 **Valorant:** Jogo principal! Foco em gameplay competitivo e dicas de agentes.",
            "minecraft": "⛏️ **Minecraft:** Para relaxar e ser criativo! Construções e aventuras.",
            "fortnite": "🏹 **Fortnite:** Diversão e momentos engraçados.",
            "the finals": "💥 **The Finals:** Jogo novo frenético - perfeito para conteúdo divertido.",
            "cs2": "🔫 **CS2:** O clássico dos FPS para treinar aim."
        }
        
        for keyword in keywords:
            for game, info in games_info.items():
                if game in keyword or keyword in game:
                    return {
                        "answer": info + "\n\nDica: Costumo jogar nas streams de segunda e quarta!",
                        "suggestions": ["Horário deste jogo", "Dicas específicas"],
                        "type": "game_specific"
                    }
        
        return {
            "answer": "🎮 **Jogos que mais transmito:**\n\n" +
                     "• **Valorant** (principal)\n" +
                     "• **Minecraft** (criatividade)\n" +
                     "• **Fortnite** (diversão)\n" +
                     "• **The Finals** (novidade)\n" +
                     "• **CS2** (clássico)\n\n" +
                     "Qual jogo você quer saber mais?",
            "suggestions": ["Valorant", "Minecraft", "Fortnite", "The Finals", "CS2"],
            "type": "games_general"
        }
    
    def _get_donations_response(self) -> Dict:
        return {
            "answer": "❤️ **Apoie o Canal:**\n\n" +
                     "• **Twitch Bits:** Use bits no chat\n" +
                     "• **Subs:** T1 (R$10), T2 (R$20), T3 (R$50)\n" +
                     "• **Presentes de Subs:** Presenteie outros viewers\n" +
                     "• **Streamlabs:** Doações diretas\n\n" +
                     "Todo apoio é MUITO importante! 🙏",
            "suggestions": ["Recompensas por subs", "Como usar bits", "Metas de doação"],
            "type": "donations"
        }
    
    def _get_rules_response(self) -> Dict:
        return {
            "answer": "📜 **Regras do Chat:**\n\n" +
                     "1. **Respeito é obrigatório**\n" +
                     "2. **Sem preconceito**\n" +
                     "3. **Nada de spam**\n" +
                     "4. **NSFW proibido**\n" +
                     "5. **Sem política/religião**\n" +
                     "6. **Use o bom senso**\n\n" +
                     "Ambiente saudável para todos! ✨",
            "suggestions": ["Consequências", "Como reportar", "Moderação"],
            "type": "rules"
        }
    
    def _get_community_response(self) -> Dict:
        return {
            "answer": "👥 **Comunidade & Discord:**\n\n" +
                     "• **Discord:** https://discord.gg/R5jmaFKK\n" +
                     "• **Canais:** #geral, #clipes, #memes\n" +
                     "• **Eventos:** Torneios, noites de jogos\n" +
                     "• **Sugestões:** A comunidade decide!\n\n" +
                     "Junte-se a nós para eventos exclusivos! 🎉",
            "suggestions": ["Regras do Discord", "Eventos recentes"],
            "type": "community"
        }
    
    def _get_technical_response(self) -> Dict:
        return {
            "answer": "🖥️ **Setup do Stream:**\n\n" +
                     "• **PC:** RTX 3060, Ryzen 5 5600X, 16GB RAM\n" +
                     "• **Microfone:** HyperX QuadCast\n" +
                     "• **Câmera:** Logitech C920\n" +
                     "• **Teclado:** Redragon Kumara\n" +
                     "• **Mouse:** Logitech G Pro X Superlight\n\n" +
                     "OBS Studio para streaming! 🎬",
            "suggestions": ["Configurações OBS", "Iluminação", "Overlay"],
            "type": "technical"
        }
    
    def _get_about_response(self) -> Dict:
        return {
            "answer": "ℹ️ **Sobre o Canal:**\n\n" +
                     "• **Criador:** Pedro Martss\n" +
                     "• **Início:** Março 2022\n" +
                     "• **Foco:** Gameplay variado com interação\n" +
                     "• **Estilo:** Descontraído e educativo\n" +
                     "• **Comunidade:** +5.2K seguidores\n\n" +
                     "Espaço acolhedor para curtir jogos! 🤝",
            "suggestions": ["História do canal", "Metas futuras"],
            "type": "about"
        }
    
    def _get_tips_response(self, keywords: List[str]) -> Dict:
        tips = {
            "valorant": "**Dicas Valorant:**\n• Treine aim no Range\n• Aprenda callouts dos mapas\n• Jogue com diferentes agentes",
            "minecraft": "**Dicas Minecraft:**\n• Sempre tenha tochas\n• Faça farm automática\n• Explore sistematicamente",
            "streaming": "**Dicas Streamers:**\n• Interaja com o chat\n• Horários consistentes\n• Seja você mesmo!"
        }
        
        for keyword in keywords:
            if "valorant" in keyword:
                return {
                    "answer": tips["valorant"],
                    "suggestions": ["Agentes", "Crosshair", "Estratégias"],
                    "type": "tips"
                }
            elif "minecraft" in keyword:
                return {
                    "answer": tips["minecraft"],
                    "suggestions": ["Farms", "Redstone", "Construções"],
                    "type": "tips"
                }
        
        return {
            "answer": "💡 **Dicas Gerais:**\n\n" +
                     "• **Para jogos:** Pratique consistentemente\n" +
                     "• **Para streaming:** Seja autêntico\n\n" +
                     "Sobre qual assunto você quer dicas?",
            "suggestions": ["Valorant dicas", "Minecraft dicas", "Streaming dicas"],
            "type": "tips"
        }
    
    def _get_events_response(self) -> Dict:
        return {
            "answer": "🎪 **Eventos Especiais:**\n\n" +
                     "• **Sábado de Especiais:** Jogos diferentes\n" +
                     "• **Torneios com Viewers:** Competições\n" +
                     "• **Maratonas Mensais:** Streams longas\n" +
                     "• **Aniversário do Canal:** Evento anual\n\n" +
                     "Fique de olho no Discord e Twitter! 📢",
            "suggestions": ["Próximo evento", "Como participar"],
            "type": "events"
        }
    
    def _get_general_response(self, keywords: List[str]) -> Dict:
        return {
            "answer": "🤖 **Assistente do Canal pedromartss007:**\n\n" +
                     "Posso te ajudar com:\n" +
                     "• Horários das streams\n" +
                     "• Jogos que transmito\n" +
                     "• Regras do chat\n" +
                     "• Informações do canal\n" +
                     "• Dicas e recomendações\n\n" +
                     "No que posso te ajudar hoje? 🎮",
            "suggestions": ["Horários", "Jogos", "Regras", "Discord", "Setup"],
            "type": "welcome"
        }
