from pydantic_settings import BaseSettings, SettingsConfigDict


class LLMSettings(BaseSettings):
    """LLM API 配置——通过 .env 注入。"""
    LLM_PROVIDER: str = "openai"          # "openai" | "anthropic" | "custom"
    LLM_BASE_URL: str = ""               # 留空则用各提供商默认地址
    LLM_API_KEY: str = ""
    LLM_MODEL: str = "gpt-4o-mini"
    LLM_TEMPERATURE: float = 0.8
    LLM_MAX_TOKENS: int = 500

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


llm_settings = LLMSettings()
