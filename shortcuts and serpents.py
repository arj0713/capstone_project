import random
import textwrap

class Player:
    def __init__(self, name, player_class):
        self.name = name
        self.position = 0
        self.class_type = player_class
class Tank(Player):
    def __init__(self, name):
        super().__init__(name,"Tank")

    def move(self):
        roll = random.randint(1,6)
        if roll == 1:
            print("Roll Forward")
            roll = random.randint(2,3)
        return roll
    def block_serpent(self):
        return random.random() < 0.5
class Beastmaster(Player):
    def __init__(self, name):
        super().__init__(name,"Beastmaster")

    def move(self):
       return random.randint(1, 6)
    def tame_serpent(self):
       return random.random() < 0.75
class Rogue(Player):
    def __init__(self,name):
        super().__init__(name,"Rogue")
    
    def move(self):
        rolls = []
        reroll_chance = {1:0,2:0.05,3:0.1,4:0.2,5:0.5,6:1}
        while True:
            roll = random.randint(1,6)
            rolls.append(roll)
            if random.random() > reroll_chance[roll]:
                break
        if len(rolls) > 1:
            print(f"You rolled {','.join(map(str,rolls))}")
        return sum(rolls)
class Explorer(Player):
    def __init__(self, name):
        super().__init__(name,"Explorer")

    def move(self):
       return random.randint(1, 6)
    def explore_shortcut(self):
        rand = random.random()
        if rand > 0.4:
            return 2
        elif rand < 0.1:
            return 0.5
        else:
            return 1


class ShortcutsAndSerpents:
    def game_introduction(self):
        print(textwrap.fill("Embark on a journey in Serpents and Shortcuts, a captivating twist on snakes and ladders. Navigate through uncharted dungeon braving shortcuts, while avoiding sinuous serpents and uncovering the secrets hidden in each square.")+"\n")
        print(textwrap.fill("Serpents and Shortcuts has a class system to allow you to choose your character's abilities."))
        print(textwrap.fill("Tank: chance to block a serpent and move forward, always reroll a 1"))
        print(textwrap.fill("Beastmaster: chance to tame a serpent and use it as a shortcut"))
        print(textwrap.fill("Rogue: increasing chance for an additional roll depending on the previous roll"))
        print(textwrap.fill("Explorer: chance to find an additional route in a shortcut and travel double the distance, could get lost and only travel half way")+"\n")
    def add_player(self):
        while True:
            player_name = input("Enter player name: ")
            confirm = input(f"Input Y to confirm chosen player name, {player_name} ")
            if str.upper(confirm) == "Y":
                break
        print("\nClass options\n1: Tank\n2: Beastmaster\n3: Rogue\n4: Explorer")
        while True:
            try:
               player_class_type = int(input("Enter the number for selected character class: "))
               if player_class_type not in range(1,5):
                   raise ValueError
               break
            except ValueError:
                print("Invalid input")
        if player_class_type == 1:
            player = Tank(player_name)
        elif player_class_type == 2:
            player = Beastmaster(player_name)
        elif player_class_type == 3:
            player = Rogue(player_name)
        else:
            player = Explorer(player_name)
        return player
    def create_player_roster(self):
        players = []
        print("Add players to start the game")
        while True:
            while True:
                try: 
                    option = int(input("\nEnter 1 to add another player or 2 to start the game: "))
                    if option not in [1,2]:
                        raise ValueError
                    break
                except ValueError:
                    print("Invalid input")
            if option == 1:
                players.append(self.add_player())
            else:
                break
        return players
    def display_player_roster(self,players):
        print("\n\nPlayers")
        for player in players:
            print(f"Name:{player.name}   Class:{player.class_type}")
        input()

    def generate_interactable_start(self,players,interactable_positions):
        while True:
            interactable_start = random.randint(10,90)
            if interactable_start not in set(p.position for p in players) and interactable_start not in interactable_positions:
                break
        return interactable_start
    def generate_interactables(self,players):
        interactable_starts = set()
        while len(interactable_starts) < 16:
            interactable_starts.add(self.generate_interactable_start(players,interactable_starts))
        interactable_starts = list(interactable_starts)
        serpent_starts = interactable_starts[:8]
        serpents = [[start,random.randint(max(start-30,5),start-1)] for start in serpent_starts]
        shortcut_starts = interactable_starts[8:]
        shortcuts = [[start,random.randint(start+1,min(start+30,95))] for start in shortcut_starts]
        return serpents,shortcuts
 
    def display_board(self,players,serpents,shortcuts):
        board = [[j + (i * 10) for j in range(1,11)] for i in range(9,-1,-1)]
        for row in board:
            for num in row:
                player_at_position = next((player for player in players if player.position == num), None)
                if player_at_position:
                    print(f"{player_at_position.name[:3]:3}", end=" ")
                elif num in (serpent[0] for serpent in serpents):
                    print(" ψ ", end = " ")
                elif num in (shortcut[0] for shortcut in shortcuts):
                    print(" ↗️ ", end = " ")
                elif num == 1:
                    print("Ent", end = " ")
                elif num == 100:
                    print("Ext", end = " ")
                else:
                    print("   ", end = " ")
            print()
        print("\n")

    def serpent_interaction(self,player,serpent):
        if player.class_type == "Tank" and player.block_serpent():
            print("You defended yourself from the serpent")
            player.position += 6
        elif player.class_type == "Beastmaster" and player.tame_serpent():
            print("You tamed the serpent")
            player.position += serpent[0]-serpent[1]
        else:
            player.position = serpent[1]
        return player.position
    def shortcut_interaction(self,player,shortcut):
        if player.class_type == "Explorer":
            exploration_multiplier = player.explore_shortcut()
            if exploration_multiplier == 2:
                print("You found an extra pathway in the shortcut")
                player.position += (shortcut[1]-shortcut[0])*exploration_multiplier
            elif exploration_multiplier == 0.5:
                print("You got lost in the shortcut")
                player.position += int((shortcut[1]-shortcut[0])*exploration_multiplier)
        else:
            player.position = shortcut[1]
        return player.position
    def interaction_check(self,player,serpents,shortcuts):
        for serpent in serpents:
            if player.position == serpent[0]:
                print(f"You face a {serpent[0]-serpent[1]}m serpent")
                player.position = self.serpent_interaction(player,serpent)
                break
        for shortcut in shortcuts:
            if player.position == shortcut[0]:
                print(f"You found a {shortcut[1]-shortcut[0]}m shortcut")
                player.position = self.shortcut_interaction(player,shortcut)
                break
        return player.position

    def single_turn(self,player,serpents,shortcuts):
        print(f"{player.name}'s turn:")
        input("Press Enter to roll the dice...")
        dice_roll = player.move()
        print(f"{player.name} moves {dice_roll}m")

        player.position += dice_roll
        player.position = self.interaction_check(player,serpents,shortcuts)
        if player.position < 100:
            print(f"{player.name} is now {100 - player.position}m from the exit\n")
    def single_game(self,players):
        for round in range(1, 101):
            print(f"\nRound {turn}:\n")
            serpents,shortcuts = self.generate_interactables(players)
            self.display_board(players,serpents,shortcuts)
            for player in players:
                self.single_turn(player,serpents,shortcuts)
                if player.position >= 100:
                    print(f"{player.name} has won!\n")
                    return
    def restart_check(self):
        print("1. Restart with same player roster\n2. Change player roster\n3. Quit")
        while True:
            try:
                repeat = int(input("Select option: "))
                if repeat not in range(1,4):
                    raise ValueError
                break
            except ValueError:
                print("Invalid input")
        return repeat
    

if __name__ == "__main__":
    sas = ShortcutsAndSerpents()

    sas.game_introduction()
    while True:
        players = sas.create_player_roster()
        while True:
            for player in players:
                player.position = 0
            sas.display_player_roster(players)
            sas.single_game(players)
            repeat = sas.restart_check()
            if repeat != 1:
                break
        if repeat == 3:
            break