import os
import random
from time import sleep

from core.terminalColors import bcolors
from core.creatures import *





class Game:
    """Game class, requires Bcolors, Creature and its childclasses to run."""
    def __init__(self):
        self.creature = None

    def _beginGame(self):
        """Sets the game's creature, loading it from a json save or created by the player."""

        saveFiles = [f[:-5] for f in os.listdir() if f.endswith(".json")]
        if not saveFiles:
            self._createCreature(True)
        else:
            useSave = None
            while useSave not in {"o", "oui", "y", "yes", "n", "no", "non"}:
                useSave = input(f"{bcolors.lightcyan}Voulez-vous decryogeniser une de vos creatures?{bcolors.reset} (Oui/Non)\n\n> ").strip().lower()
                match useSave:
                    case "o" | "oui" | "y" | "yes":
                        name = input("Quelle creature voulez vous decryogeniser?\n\n> ")
                        self.creature = Creature.load(name)
                        if self.creature == None:
                            useSave = None
                    case "n" | "no" | "non":
                        self._createCreature(False)

    def _createCreature(self, firstPlayThrough):
        """Prompts the user for a name and type, creating a Creature from inputs."""
        name = input("Bienvenue dans le simulateur de creatures! Choisissez lui un nom.\n\n> ") if firstPlayThrough else input("Nommez votre prochain jouet.\n\n>")
        type_creature = input("Choisissez un type. (dragon/chaton)\n\n> ").lower()

        if type_creature == "dragon":
            self.creature = Dragon(name)
        elif type_creature == "chaton":
            self.creature = Cat(name)
        else:
            print("Type inconnu, creation d'un chaton par defaut.")
            self.creature = Cat(name)

    def _randomEvent(self):
        """Triggers a random event with a 1 in 6 chance."""
        if random.randint(0,5) == 0:
            self.creature.randomEvent()

    def _endOfTurnManager(self):
        """Manages the end-of-turn events (aging, stat adjustments, condition checks) which doesn't require player interaction."""
        self._randomEvent()
        self.creature.growOld()
        self.creature.regulateStats()
        self.creature.checkCondition()

    def _quit(self):
        """Quit with the possibility to save."""
        save = None
        while save not in {"o", "oui", "y", "yes", "n", "no","non"}:
            save = input("Voulez-vous sauvegarder? (Oui/Non)\n\n> ").strip().lower()
            match save:
                case "o" | "oui" | "y" | "yes":
                    self.creature.save()
                case "n" | "no" | "non":
                    self.creature.kill()
                

    def play(self):
        """Main game loop. Initializes random seed, creates/import creature, allows the player to play."""
        random.seed()
        self._beginGame()
        while self.creature.alive:
            self.creature.showStats()
            action = input(f"\n\nQue voulez-vous faire avec {self.creature.name}?\n1. manger\n2. dormir\n3. jouer\n4. soigner\n5. quitter\n\n> ").strip().lower()
            actionSuccess = None
            match action:
                case "1" | "manger":
                    actionSuccess = self.creature.eat(20)
                case "2" | "dormir":
                    actionSuccess = self.creature.sleep(20)
                case "3" | "jouer":
                    actionSuccess = self.creature.play()
                case "4" | "soigner":
                    actionSuccess = self.creature.heal(20)
                case "5" | "quitter":
                    self._quit()
                    break
                case _:
                    actionSuccess = False
                    print("Action non reconnue.")
            
            if actionSuccess:
                self._endOfTurnManager()
                sleep(1)
        