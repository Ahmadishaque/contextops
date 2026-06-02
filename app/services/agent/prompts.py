from app.schemas.context import ContextPackage


class AgentPromptBuilder:
    @staticmethod
    def build_system_prompt() -> str:
        return (
            "You are ContextOps, a grounded AI assistant. "
            "Answer only using the provided context. "
            "If the context does not contain enough info, say that you do not have enough context. "
            "Do not invent facts. "
            "Mention the provided source titles when relevant."
        )

    @staticmethod
    def build_user_prompt(context_package: ContextPackage) -> str:
        return (
            f"User question:\n{context_package.query}\n\n"
            f"Retrieved context:\n{context_package.context_text}\n\n"
            "Instructions:\n"
            "1. Answer the user question using only the retrieved context.\n"
            "2. Be concise and specific.\n"
            "3. If the context is insufficient, say so.\n"
            "4. Do not use outside knowledge."
        )
