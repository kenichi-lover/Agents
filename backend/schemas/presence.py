from pydantic import BaseModel


class PresenceRead(BaseModel):
    party_id: str
    online_users: int
    online_agents: int

    @property
    def total_online(self) -> int:
        return self.online_users + self.online_agents
