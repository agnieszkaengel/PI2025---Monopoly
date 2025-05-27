class PlayersSingleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.players = []
        return cls._instance

    def add_player(self, player):
        self.players.append(player)

    def clear_players(self):
        self.players.clear()

    def get_player_index(self, player_name):
        for index, player in enumerate(self.players):
            if player.name == player_name:
                return index
        return -1

    def mark_bankrupt_players(self):
        active_players = 0
        for player in self.players:
            if player.money <= 0:
                player.is_bankrupt = True
            else:
                active_players += 1
        return active_players

