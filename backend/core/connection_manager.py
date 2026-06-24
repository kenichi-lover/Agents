from typing import Dict


class ConnectionManager:
    def __init__(self):
        self.active_parties: Dict[str, Dict[str, object]] = {}  # party_id -> {user_id: WebSocket}
        self.user_locations: Dict[str, str] = {}  # user_id -> party_id

    async def connect(self, websocket: object, party_id: str, user_id: str):
        if party_id not in self.active_parties:
            self.active_parties[party_id] = {}
        self.active_parties[party_id][user_id] = websocket
        self.user_locations[user_id] = party_id

    def disconnect(self, user_id: str):
        party_id = self.user_locations.pop(user_id, None)
        if party_id and party_id in self.active_parties:
            self.active_parties[party_id].pop(user_id, None)

    def get_presence(self, party_id: str) -> dict:
        """Return online user count for a party."""
        users = self.active_parties.get(party_id, {})
        return {
            "party_id": party_id,
            "online_users": len(users),
            "online_agents": 0,  # TODO: track agent connections separately
        }

    async def broadcast(self, party_id: str, message: dict):
        if party_id in self.active_parties:
            for ws in self.active_parties[party_id].values():
                await ws.send_json(message)


manager = ConnectionManager()
