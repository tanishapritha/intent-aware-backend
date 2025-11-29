import json
import os
from app.utils.logger import logger
from app.intent.multilingual import MultilingualHandler

class AgentRouter:
    def __init__(self):
        self.agents = self._load_agents()

    def _load_agents(self):
        path = os.path.join(os.path.dirname(__file__), '..', 'data', 'agents.json')
        try:
            with open(path, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load agents.json: {e}")
            return []

    def find_best_agent(self, intent: str, language: str):
        """
        Finds the best agent based on intent (skill) and language.
        Score = 0.7 * skill_match + 0.3 * language_match
        """
        best_agent = None
        highest_score = -1.0

        normalized_visitor_lang = MultilingualHandler.normalize_language_code(language)

        for agent in self.agents:
            if agent.get("status") != "online":
                continue

            # Skill Match (0 or 1)
            skill_match = 1.0 if intent in agent.get("skills", []) else 0.0

            # Language Match (0 or 1)
            lang_match = 1.0 if MultilingualHandler.is_language_match(agent.get("languages", []), normalized_visitor_lang) else 0.0

            # Calculate Score
            score = (0.7 * skill_match) + (0.3 * lang_match)

            logger.info(f"Agent {agent['name']} - Skill: {skill_match}, Lang: {lang_match}, Score: {score}")

            if score > highest_score:
                highest_score = score
                best_agent = agent
            elif score == highest_score:
                # Tie-breaking logic could go here (e.g., load balancing)
                pass
        
        return best_agent

agent_router = AgentRouter()
