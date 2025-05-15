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

    def get_player_by_name(self, name):
        for player in self.players:
            if player.name == name:
                return player
        return None

    def get_player_index(self, player_name):
        for index, player in enumerate(self.players):
            if player.name == player_name:
                return index
        return -1