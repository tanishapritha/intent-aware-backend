from typing import Optional

class MultilingualHandler:
    @staticmethod
    def normalize_language_code(lang: str) -> str:
        """
        Normalizes language codes (e.g., 'en-US' -> 'en').
        """
        if not lang:
            return "en"
        return lang.lower().split('-')[0]

    @staticmethod
    def is_language_match(agent_langs: list, visitor_lang: str) -> bool:
        """
        Checks if the agent speaks the visitor's language.
        """
        normalized_visitor_lang = MultilingualHandler.normalize_language_code(visitor_lang)
        normalized_agent_langs = [MultilingualHandler.normalize_code(l) for l in agent_langs]
        return normalized_visitor_lang in normalized_agent_langs

    @staticmethod
    def normalize_code(lang: str) -> str:
        return lang.lower().split('-')[0]
