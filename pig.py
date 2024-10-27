import random
import time
import argparse

class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0

class Die:
    def roll(self):
        return random.randint(1, 6)

class PigGame:
    def __init__(self, player1, player2):
        self.players = [player1, player2]
        self.die = Die()
        self.current_player = 0

    def playTurn(self):
        player = self.players[self.current_player]
        if isinstance(player, ComputerPlayer):
            turn_total = player.take_turn(self)
        else:
            turn_total = self.human_turn(player)
        player.score += turn_total
        print(f"{player.name}'s total score: {player.score}")
        self.current_player = 1 - self.current_player

    def human_turn(self, player):
        turn_total = 0
        while True:
            choice = input(f"{player.name}, roll or hold? (r/h): ").lower()
            if choice == 'r':
                roll = self.die.roll()
                print(f"{player.name} rolled: {roll}")
                if roll == 1:
                    print("Rolled a 1! Turn ends with no points added.")
                    return 0
                turn_total += roll
                print(f"{player.name}'s turn total: {turn_total}")
            elif choice == 'h':
                print(f"{player.name} holds with a turn total of {turn_total}.")
                return turn_total
            else:
                print("Invalid choice. Please enter 'r' to roll or 'h' to hold.")

class ComputerPlayer(Player):
    def take_turn(self, game):
        turn_total = 0
        while turn_total < min(25, 100 - self.score):
            roll = game.die.roll()
            print(f"{self.name} (Computer) rolled: {roll}")
            if roll == 1:
                print("Rolled a 1! Turn ends with no points added.")
                return 0
            turn_total += roll
        print(f"{self.name} holds with a turn total of {turn_total}.")
        return turn_total

class PlayerFactory:
    @staticmethod
    def create_player(player_type, name):
        if player_type == "human":
            return Player(name)
        elif player_type == "computer":
            return ComputerPlayer(name)
        else:
            raise ValueError("Unknown player type")

class TimedGameProxy:
    def __init__(self, game):
        self.game = game
        self.start_time = time.time()

    def play(self):
        while True:
            elapsed_time = time.time() - self.start_time
            if elapsed_time >= 60:
                print("Time's up! Determining the winner based on current scores...")
                self.determine_winner()
                break
            self.game.playTurn()
            if self.game.players[0].score >= 100 or self.game.players[1].score >= 100:
                break

    def winner(self):
        player1, player2 = self.game.players
        if player1.score > player2.score:
            print(f"The winner is {player1.name} with a score of {player1.score}!")
        elif player2.score > player1.score:
            print(f"The winner is {player2.name} with a score of {player2.score}!")
        else:
            print("It's a tie!")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--player1', required=True, choices=['human', 'computer'], help="Specify player 1 type: human or computer")
    parser.add_argument('--player2', required=True, choices=['human', 'computer'], help="Specify player 2 type: human or computer")
    parser.add_argument('--timed', action='store_true', help="Enable timed game mode")
    args = parser.parse_args()

    player1 = PlayerFactory.create_player(args.player1, "Player 1")
    player2 = PlayerFactory.create_player(args.player2, "Player 2")

    game = PigGame(player1, player2)
    if args.timed:
        timed_game = TimedGameProxy(game)
        timed_game.play()
    else:
        while player1.score < 100 and player2.score < 100:
            game.playTurn()
        winner = player1 if player1.score >= 100 else player2
        print(f"The winner is {winner.name} with a score of {winner.score}!")

if __name__ == "__main__":
    main()
