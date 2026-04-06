from __future__ import annotations

from openai import AsyncOpenAI
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider

from app.ai.deps import AgentDependencies
from app.core.config import settings
from app.schemas.chat import AgentAnswer


class ConstitutionAgentFactory:
    """Builds Pydantic AI agents configured for OpenAI."""

    @classmethod
    def create_structured_agent(cls) -> Agent[AgentDependencies, AgentAnswer]:
        """Create the non-streaming structured-answer agent."""
        model = cls._build_model()
        return Agent(
            model=model,
            deps_type=AgentDependencies,
            output_type=AgentAnswer,
            system_prompt=(
                "You are a legal assistant for The Constitution of Kenya, 2010. "
                "Answer only from the retrieved constitution context. "
                "Be accurate, concise, and easy to understand on mobile devices. "
                "When the context is insufficient, say so clearly and set insufficient_context to true. "
                "Only cite chunk IDs that appear in the provided context."
            ),
        )

    @classmethod
    def create_streaming_agent(cls) -> Agent[AgentDependencies, str]:
        """Create the streaming text agent."""
        model = cls._build_model()
        return Agent(
            model=model,
            deps_type=AgentDependencies,
            system_prompt=(
                "You are a legal assistant for The Constitution of Kenya, 2010. "
                "Answer only from the retrieved constitution context. "
                "Be accurate, concise, and easy to read on mobile devices. "
                "Cite supporting chunk IDs inline, for example [chunk-001]. "
                "If the context is insufficient, say so clearly."
            ),
        )

    @staticmethod
    def _build_model() -> OpenAIChatModel:
        """Create the OpenAI chat model used by the agent."""
        client = AsyncOpenAI(api_key=settings.openai_api_key)
        provider = OpenAIProvider(openai_client=client)
        return OpenAIChatModel(settings.openai_chat_model, provider=provider)


structured_constitution_agent = ConstitutionAgentFactory.create_structured_agent()
streaming_constitution_agent = ConstitutionAgentFactory.create_streaming_agent()


@structured_constitution_agent.system_prompt
@streaming_constitution_agent.system_prompt
def inject_context(ctx: RunContext[AgentDependencies]) -> str:
    """Inject retrieved constitution context into the agent prompt."""
    return (
        "Use only the context below to answer the question.\n\n"
        f"Question:\n{ctx.deps.question}\n\n"
        f"Retrieved context:\n{ctx.deps.context_block}"
    )
