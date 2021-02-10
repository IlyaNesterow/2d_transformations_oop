from os import listdir
from string import ascii_lowercase
from random import choice
from typing import ClassVar

from ask_user import UserIpnut
from cords import Cords
from errors import *


class Menu:
    cords: ClassVar[ Cords ] 

    def __init__(self) -> None:
        self.input = UserIpnut()

    def __ask_cord_amount(self) -> int:
        self.input.type = int
        self.input.prompt = 'Enter amount of points'
        amount = self.input.ask_for_one_item(3, 50)

        return amount

    def fill_cords(self) -> None:
        self.input.type = float
        amount = self.__ask_cord_amount()
        
        self.input.prompt = 'Enter x values'
        x = self.input.ask_for_many_items(amount)
        self.input.prompt = 'Enter y values'
        y = self.input.ask_for_many_items(amount)
        self.cords = Cords(x, y)

    def ask_rotate_angle(self) -> None:
        self.input.type = float

        if self.input.ask_yes_no('Do you want to add rotation angle?') == 'y':
            self.input.prompt = 'Enter rotation angle'
            self.cords.rotate(self.input.ask_for_one_item())
    
    def ask_scale(self) -> None:
        self.input.type = float
        scale_x = 1
        scale_y = 1

        if self.input.ask_yes_no('Do you want to scale your figure on x?') == 'y':
            self.input.prompt = 'Enter scale x quotient'
            scale_x = self.input.ask_for_one_item(0.1, 100)

        if self.input.ask_yes_no('Do you want to scale your figure on y?') == 'y':
            self.input.prompt = 'Enter scale y quotient'
            scale_y = self.input.ask_for_one_item(0.1, 100)

        self.cords.scale(scale_x, scale_y)

    def ask_move(self) -> None:
        self.input.type = float
        move_x = 0
        move_y = 0

        if self.input.ask_yes_no('Do you want to move your figure on x?') == 'y':
            self.input.prompt = 'Enter pixels amount you want your figure to be moved horizontally by'
            move_x = self.input.ask_for_one_item()
        
        if self.input.ask_yes_no('Do you want to move your figure on y?') == 'y':
            self.input.prompt = 'Enter pixels amount you want your figure to be moved vertically by'
            move_y = self.input.ask_for_one_item()

        self.cords.move(move_x, move_y)

    def __verify_filename(self, fname: str) -> str: 
        files_in_pwd = list(filter(lambda f: f == fname, listdir('.')))
        extname = fname.split('.')[len(fname.split('.')) - 1]
        try:
            if fname in files_in_pwd:
                raise FileAlreadyExistsError('File already exists')
            return fname
        except FileAlreadyExistsError:
            randname = ''.join(choice(ascii_lowercase) for i in range(10)) 
            print(f'Random name of {randname} is assigned')
            return f'{randname}.{extname}'

    def ask_filename(self) -> str:
        fname: str = self.input.ask_smth('Enter a filename')
        if len(fname.strip()) == 0:
            fname = 'result'

        return fname

    def ask_for_extension(self) -> str:
        possible_extensions = {'jpg', 'jpeg', 'png', 'gif'}
        try:
            extname: str = self.input.ask_smth('Enter extension name of the image')
            extname = extname.strip().lower()
            if len(extname) == 0 or not extname in possible_extensions:
                raise WrongExtensionError('Wrong extension')
            return extname
        except WrongExtensionError:
            print('Wrong extension')
            return self.ask_for_extension()

    def get_full_filename(self) -> str:
        extname = self.ask_for_extension()
        full_filename = f'{self.ask_filename()}.{extname}'
        return self.__verify_filename(full_filename)

    def execute(self) -> None:
        self.fill_cords()
        self.ask_rotate_angle()
        self.ask_scale()
        self.ask_move()
        
        self.cords.to_plot(self.get_full_filename())