# LLM Provider Abstraction

ContextOps uses an LLM provider abstraction so the agent runtime is not tightly coupled to one model vendor.

## Providers

- `mock`: deterministic local provider for development and tests
- `openai`: OpenAI-backed provider using the official Python SDK

## Environment Variables

```text
LLM_PROVIDER=mock
OPENAI_API_KEY=replace_me
OPENAI_MODEL=gpt-5.5
```

## Default Behavior

The default provider is `mock` so the project runs without external API credentials.

## OpenAI Mode

To use OpenAI-backed responses, create a local `.env` file and set:

```text
LLM_PROVIDER=openai
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=gpt-5.5
```

Do not commit `.env`.

## Design Goal

The agent runtime depends on a provider interface, not a specific API implementation. This makes it easier to add local vLLM, Ollama, Anthropic, or other model providers later.
