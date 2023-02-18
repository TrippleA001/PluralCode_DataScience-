from room import Room
from textUI import TextUI

"""
    This Game class is the main class of the "Cookery Book". This game is a simple
    textbase adventure game. A Player can move around different locations or rooms in search
    of the stolen Cookery Book.
    
    To play the game, the player enters any of the command word to begin and types in direction to move 
    in various locations while searching for the book.
    
    This main class creates and initializes all the others. It creates the rooms, creates the parser
    and starts the game. It also evaluates and executes the command that the parser returns.
"""

class Game:

    def __init__(self):
        """
        Initialises the game.
        """
        self.create_rooms()
        self.current_room = self.courtyard
        self.textUI = TextUI()
        self.back_pack_content = []

    def create_rooms(self):
        """
            Sets up all rooms,assets and location.
        :return: None
        """
        
        #Create Rooms
        self.courtyard = Room("You are in the courtyard")
        self.ballroom = Room("in the ballroom")
        self.princess_room = Room("in the Princess' Room")
        self.kitchen = Room("in the kitchen")
        self.pantry = Room("in a pantry")
        self.buttery = Room("in a buttery")
        self.undercroft = Room("in the undercroft")
        self.dungeon = Room("in the dungeon")
        self.graveyard = Room("in the graveyard")
        self.armoury = Room("in the armoury")
        
        #Define exits for locations
        self.courtyard.set_exit("north", self.ballroom)
        self.ballroom.set_exit("south", self.courtyard)
        self.ballroom.set_exit("west", self.kitchen)
        self.ballroom.set_exit("east", self.princess_room)
        self.ballroom.set_exit("north", self.undercroft)
        self.kitchen.set_exit("north", self.pantry)
        self.pantry.set_exit("north", self.buttery)
        self.buttery.set_exit("west", self.ballroom)
        self.buttery.set_exit("north", self.dungeon)
        self.dungeon.set_exit("east", self.undercroft)
        self.dungeon.set_exit("west", self.buttery)
        self.undercroft.set_exit("east", self.ballroom)
        self.undercroft.set_exit("north", self.graveyard)
        self.undercroft.set_exit("west", self.dungeon)
        self.undercroft.set_exit("east", self.armoury)
        self.armoury.set_exit("east", self.courtyard)
        self.armoury.set_exit("south", self.undercroft)
        self.dungeon.set_exit("east", self.graveyard)
        self.princess_room.set_exit("west", self.ballroom)
        self.graveyard.set_exit("south", self.undercroft)

        #define items to pick
        self.courtyard.set_items("nametag", 0) 
        self.ballroom.set_items("menu", 1)
        self.pantry.set_items("rice", 20)
        self.buttery.set_items("wine", 5)
        self.kitchen.set_items("chicken", 5)
        self.armoury.set_items("shield", 30)
        self.dungeon.set_items("keys", 55)
        self.graveyard.set_items("skull", 15)
        self.princess_room.set_items("wish_list", 100)
        self.undercroft.set_items("cookery_book", 1)

    def play(self):
        """
            The main play loop.
        :return: None
        """
        self.print_welcome()
        finished = False
        while not finished:  # while (finished == False):
            command = self.textUI.get_command()  # Returns a 2-tuple
            finished = self.process_command(command)
        print("Thank you for playing 'Cookery Book!")

    def print_welcome(self):
        """
            Displays a welcome message.
        :return:
        """
        self.textUI.print_to_textUI("You are a new chef in the royal palace.")
        self.textUI.print_to_textUI("To prove your competence, you are required ")
        self.textUI.print_to_textUI("to prepare a feast for the Princess' 18th.")
        self.textUI.print_to_textUI("birthday. However someone in the palace ")
        self.textUI.print_to_textUI("is trying to sabotage everything and stole your cookery book...")
        self.textUI.print_to_textUI("Gossips have it that its been hidden in a dungeon")
        self.textUI.print_to_textUI("down the old castle....... ")
        self.textUI.print_to_textUI("")
        self.textUI.print_to_textUI(f'Your command words are: {self.show_command_words()}')

    def show_command_words(self):
        """
            Shows a list of available commands.
        :return: None
        """
        return ['help', 'go', 'pick', 'drop', 'quit']

    def process_command(self, command):
        """
            Process a command from the TextUI.
        :param command: a 2-tuple of the form (command_word, second_word)
        :return: True if the game has been quit, False otherwise
        """
        command_word, second_word = command
        if command_word != None:
            command_word = command_word.upper()

        want_to_quit = False
        if command_word == "HELP":
            self.print_help()
        elif command_word == "GO":
            self.do_go_command(second_word)
        elif command_word == "PICK":
            self.do_pick_command(second_word)
        elif command_word == "DROP":
            self.do_drop_command(second_word)
        elif command_word == "QUIT":
            want_to_quit = True
        else:
            # Unknown command input...
            self.textUI.print_to_textUI("Don't know what you mean.")

        return want_to_quit

    def print_help(self):
        """
            Display some useful help text.
        :return: None
        """
        self.textUI.print_to_textUI("Look for the 'Undercroft' ")
        self.textUI.print_to_textUI("keys to the dungeon is in the undercroft. Watch out for saboteurs")
        self.textUI.print_to_textUI("It will take you days to find this room, so grab some food or drink")
        self.textUI.print_to_textUI("from the 'kitchen' or 'buttery' to keep you alive")
        self.textUI.print_to_textUI("pick up shield from the armoury to protect you from harm")
        self.textUI.print_to_textUI("the box where the book is locked, is in the 'graveyard' ")
        self.textUI.print_to_textUI("enter the graveyard and find the box")
        self.textUI.print_to_textUI("use the keys gotten to open the box and get your cookery book")
        self.textUI.print_to_textUI("")
        self.textUI.print_to_textUI(f'Your command words are: {self.show_command_words()}.')

    def do_go_command(self, second_word):
        """
            Performs the GO command.
        :param second_word: the direction the player wishes to travel in
        :return: None
        """
        if second_word == None:
            # Missing second word...
            self.textUI.print_to_textUI("Where do you want to Go?")
            return

        next_room = self.current_room.get_exit(second_word)
        if next_room == None:
            self.textUI.print_to_textUI("There is no exit!")
        elif (next_room == self.undercroft) and ('keys' not in self.back_pack_content):
            self.textUI.print_to_textUI("No access, no key found in your backpack")
        else:
            self.current_room = next_room
            self.textUI.print_to_textUI(self.current_room.get_long_description())
            
    def do_pick_command(self, second_word):
        """
            Performs the PICK command.
        :param second_word: the item the player wishes to pick
        :return: None
        """
        if second_word == None:
            # Missing second word...
            self.textUI.print_to_textUI("What do you want to Pick?")
            return
        if second_word in self.current_room.get_items():
            self.back_pack_content.append(second_word)
            if second_word == "cookery_book":
                self.textUI.print_to_textUI("Congratulations, you have the award winning cookery book")
        else:
            self.textUI.print_to_textUI(f"{second_word} not found in current room")


            
    def do_drop_command(self, second_word):
        """
            Performs the DROP command.
        :param second_word: the item the player wishes to drop
        :return: None
        """
        if second_word == None:
            # Missing second word...
            self.textUI.print_to_textUI("What do you want to Drop?")
            return
        if second_word in self.back_pack_content:
            self.back_pack_content.append(second_word)
        else:
            self.textUI.print_to_textUI(f"{second_word} not found in backpack")

            

def main():
    game = Game()
    game.play()

if __name__ == "__main__":
    main()
