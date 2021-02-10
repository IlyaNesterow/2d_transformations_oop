from typing import Any, Union


class UserIpnut:
    def __init__(self, type: Union[ int, float ] = int, prompt: str = 'Enter a number: ') -> None:
        self._type = type
        self._prompt = prompt

    def ask_for_many_items(self, amount: int, min = None, max = None) -> list:
        if(amount < 2):
            raise ValueError('This method is used for fetching many items, use ask_for_one_item instead')

        res = [ self.ask_for_one_item(min, max) for _ in range(0, amount) ]

        return res
    
    def ask_for_one_item(self, min = None, max = None) -> Union[ int, float ]:
        try:
            result = self._type(input(self._prompt))
            if (max and result > max) or (min and result < min):
                raise ValueError('Value out of range')

            return result
        except ValueError as err:
            if len(err.args) > 0:
                if type(err.args[0]) == str and err.args[0].startswith('invalid literal'):
                    print('Cannot convert string to number, try again')
                    return self.ask_for_one_item(min, max)

            print(f'Number cannot be smaller than {min} and connot be greater than {max}')
            return self.ask_for_one_item(min, max)

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, new_type: Union[ int, float ]):
        if not new_type in [ int, float ]:
            raise TypeError('Type can be only a numeric')
        self._type = new_type

    @property
    def prompt(self):
        return self._prompt

    @prompt.setter
    def prompt(self, new_prompt: str):
        if len(new_prompt) < 5: 
            raise ValueError('Prompt should be at least 5 characters')

        self._prompt = self.__format_prompt(new_prompt)

    def __format_prompt(self, prompt: str):
        if not prompt.endswith(':') and not prompt.endswith(' '):
            prompt += ':'
        if not prompt.endswith(' '):
            prompt += ' '

        return prompt

    def ask_smth(self, prompt, res_type: Any = str) -> Any:
        try:
            res = res_type(input(self.__format_prompt(prompt)))
            return res
        except ValueError:
            print(f'Cannot convert input into {res_type.__name__}')
            return self.ask_smth(prompt, res_type)
        except Exception as ex:
            if len(ex.args) > 0:
                print(ex.args[0])
            
            return self.ask_smth(prompt, res_type)

    def ask_yes_no(self, prompt: str) -> str:
        try:
            res = input(prompt + ' y/n: ').lower().strip()
            if res not in ['y', 'n']:
                raise ValueError('Wrong option')

            return res
        except ValueError:
            print('Wrong option, try again')
            return self.ask_yes_no(prompt)