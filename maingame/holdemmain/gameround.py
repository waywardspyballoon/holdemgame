class GameRound:
    def __init__(self, players):
        self.players = players

    def setup_action(self):
        posit = 0
        for player in self.players:
            player.position = posit
            posit += 1
    
    def increment_position(self):
        for player in self.players:
            if player.position == len(self.players) - 1:
                player.position = 0
            else:
                player.position += 1
    
    def remove_player(self, player):
        self.players.remove(player)
        