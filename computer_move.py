import random as rnd
from player import Player


class Computer_Move():
    def __init__(self, winning_conditions):
        self.winning_array = []
        self.convert_winning_conditions(winning_conditions)

    def convert_winning_conditions(self, winning_conditions):
        for condition in winning_conditions:
            for key, value in condition.items():
                self.winning_array.append(value)

    def convert_field(self, field):
        converted_field = []
        for key, value in field.items():
            converted_field.append({key: value['player']})
        return converted_field

    def process_computer_move(self, field):
        current_field = self.convert_field(field)
        possible_moves = []
        count = {'offense': 0, 'defense': 0, 'random': 0}
        open_moves = {'offense': [], 'defense': [], 'random': [key for i in current_field for key, value in i.items() if
                                                               value == Player.UNOCCUPIED.value]}

        for condition in self.winning_array:
            for number in condition:
                if current_field[number - 1][number] == Player.UNOCCUPIED.value:
                    count['random'] += 1
                    possible_moves.append(number)
                elif current_field[number - 1][number] == Player.PLAYER_O.value:
                    count['offense'] += 1
                elif current_field[number - 1][number] == Player.PLAYER_X.value:
                    count['defense'] += 1

            if count['offense'] == 2:
                open_moves['offense'].extend(index for index in possible_moves)
            elif count['defense'] == 2:
                open_moves['defense'].extend(index for index in possible_moves)

            # Reset count for next iteration
            count = {'offense': 0, 'defense': 0, 'random': 0}
            possible_moves = []

        # print(f'My Current field: {current_field}')
        # print(f'Open moves: {open_moves}')

        if open_moves['offense']:
            return rnd.choice(open_moves['offense'])
        elif open_moves['defense']:
            return rnd.choice(open_moves['defense'])
        elif open_moves['random']:
            return rnd.choice(open_moves['random'])
        else:
            return None