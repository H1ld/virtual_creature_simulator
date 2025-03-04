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
        type_creature = input("Choisissez un type.\n1. Chat\n2. Dragon\n3. Lapin\n4. Tortue\n\n> ").strip().lower()

        match(type_creature):
            case "1" | "chat":
                self.creature = Cat(name)
            case "2" | "dragon":
                self.creature = Dragon(name)
            case "3" | "lapin":
                self.creature = Rabbit(name)
            case "4" | "tortue":
                self.creature = Turtle(name)
            case _:
                print("Type inconnu, creation d'un chat par defaut.")
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
                    return self.creature.kill()
                
    def _eatingEnding(self):
        """5th quitting ending interaction."""
        timesAvoided = 0
        while (True):
            if (timesAvoided > 5):
                temp = list(self.creature.name)
                random.shuffle(temp)
                self.creature.name = ''.join(temp)

            action = input(f"{bcolors.red}\n\nQue voulez-vous faire de {self.creature.name}?\n1. manger\n2. ...\n3. ...\n4. ...\n5. ...\n\n> {bcolors.reset}").strip().lower()
            if action in {"1","manger"}:
                print(f"Vous ne mangez qu'un petit bout {f"du peu que vous reconnaissez " if timesAvoided>5 else ""}de {self.creature.name}")
                print(f"{bcolors.lightgreen}+5 nourriture{bcolors.reset}")
                break
            else:
                print(f"{bcolors.red}Vous contemplez le cadavre de {self.creature.name}, esperant repousser l'inevitable.{bcolors.reset}")
                timesAvoided+=1


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
                    eaten = self._quit()
                    break
                case _:
                    actionSuccess = False
                    print("Action non reconnue.")
            
            if actionSuccess and self.creature.alive:
                self._endOfTurnManager()
                sleep(1)
        
        if eaten:
            self._eatingEnding()