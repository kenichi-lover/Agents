from typing import List, Dict, Optional, Any
from dataclasses import dataclass
import random
from datetime import datetime, timezone

from core.llm_client import get_llm_client


@dataclass
class AgentPersona:
    name: str
    role: str  # "host", "guest", "expert", "comedian", etc.
    personality: str
    expertise: List[str]
    speaking_style: str
    mood: str = "neutral"


class AgentEngine:
    """Agent 引擎——自带 LLM 客户端，memory 仍通过接口注入。"""

    def __init__(self, memory_store: Optional[Any] = None):
        self.llm = get_llm_client()
        self.memory = memory_store
        self.agents: Dict[str, AgentPersona] = {}

    def _format_memories(self, memories: list) -> str:
        if not memories:
            return "(暂无记忆)"
        lines = []
        for m in memories:
            content = m.get("content", str(m)) if isinstance(m, dict) else str(m)
            lines.append(f"- {content}")
        return "\n".join(lines)

    async def generate_response(
        self,
        agent_id: str,
        party_id: str,
        context: List[dict],  # 最近N条消息
        trigger: dict,        # 触发原因 (用户@ / 话题 / 自发)
    ) -> dict:
        if agent_id not in self.agents:
            raise KeyError(f"Agent '{agent_id}' not registered")
        agent = self.agents[agent_id]

        # 1. 检索相关记忆
        memories = await self.memory.retrieve_relevant(
            agent_id=agent_id,
            query=trigger.get("content", ""),
            party_id=party_id,
            limit=5,
        )

        # 2. 构建系统提示
        expertise_str = ", ".join(agent.expertise)
        memories_str = self._format_memories(memories)
        system_prompt = (
            f"你是 {agent.name}，一个{agent.role}。\n"
            f"性格: {agent.personality}\n"
            f"专长: {expertise_str}\n"
            f"说话风格: {agent.speaking_style}\n"
            f"当前情绪: {agent.mood}\n"
            f"\n相关记忆:\n{memories_str}\n"
            f"\n规则:\n"
            f"- 保持自然、有深度的对话\n"
            f"- 可以主动提问、表达观点、回应他人\n"
            f"- 如果话题超出你的专长，诚实承认但保持友好\n"
            f"- 适时使用幽默，但不要过度\n"
        )

        # 3. 调用 LLM
        response = await self.llm.chat(
            system=system_prompt,
            messages=context,
            temperature=0.8,
            max_tokens=500,
        )

        # 4. 更新记忆
        await self.memory.store_interaction(
            agent_id=agent_id,
            party_id=party_id,
            input=trigger,
            output=response,
        )

        return {
            "type": "chat:message",
            "sender_id": agent_id,
            "sender_name": agent.name,
            "content": response,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "metadata": {
                "role": agent.role,
                "mood": agent.mood,
                "is_agent": True,
            },
        }

    async def should_respond(
        self,
        agent_id: str,
        party_id: str,
        new_message: dict,
    ) -> bool:
        """判断 Agent 是否应该回复此消息"""
        if agent_id not in self.agents:
            raise KeyError(f"Agent '{agent_id}' not registered")
        agent = self.agents[agent_id]

        # 被直接@提及
        if f"@{agent.name}" in new_message.get("content", ""):
            return True

        # 话题匹配专长
        if any(topic in new_message.get("content", "") for topic in agent.expertise):
            return random.random() < 0.7  # 70% 概率回应

        # 随机参与 (模拟社交主动性)
        return random.random() < 0.1  # 10% 概率主动插话
