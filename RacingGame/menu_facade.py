import menu_framework as framework
import tkinter

class TkinterMenuFacade:
    '''Class that creates the facade of the menu outside of the game,
    imports the menu framwork, and sets up the menu (created with Tkinter library) '''
    def __init__(self):
        self.framework = framework.TkinterFramework()
        self.type_car = tkinter.IntVar(0)
        self.type_track = tkinter.IntVar(0)

    def setup_menu(self)->None:
        '''Set up the menu with the framework'''
        self.framework.set_geometry("1366x920")
        self.framework.set_images("./RacingGame/assets/images/gtm.png","./RacingGame/assets/images/car_ico.ico")
        self.framework.create_frame(8)
        self.framework.create_label("Run GT Mexico", ("Unispace", 30))
        self.framework.create_Username_entry("Username", ("Unispace", 16))
        self.framework.create_label("Select your Track:", ("Unispace", 16))
        self.framework.create_radio_button("Track 1", variable=self.type_track, value=1,font= ("Unispace", 16))
        self.framework.create_separator()
        self.framework.create_label("Select your car: (speed changes...)", ("Unispace", 16))
        self.framework.create_radio_button("Ferrari 458 Italia", variable=self.type_car, value=1,font= ("Unispace", 16))
        self.framework.create_button("Run Game", ("Unispace", 16),self.framework.run_game_wrapper ) #self.framework.run_game_wrapper
        self.framework.create_quit_button("Quit Game", ("Unispace", 16))

    def get_username(self)->None:
        '''Set the username of the player'''
        return self.framework.get_username()

    def set_game_function(self, game_function)->None:
        '''Set the game function to run the game'''
        self.framework.set_game_function(game_function)

    def run_menu(self)->None:
        '''Run the menu with the framework '''
        self.framework.run()


if __name__ == '__main__':
    menu = TkinterMenuFacade()
    menu.setup_menu()
    menu.run_menu()
