import math
import random
import copy
from player import Player

class MCTSNode:
    def __init__(self, state, move=None):
        self.state = state
        self.move = move
        self.children = []
        self.visits = 0
        self.total_reward = 0
        self.parent = None

    @staticmethod
    def uct_value(node, exploration_weight=1.41):
        if node.visits == 0:
            return float('inf')
        return (node.total_reward / node.visits) + exploration_weight * math.sqrt(math.log(node.parent.visits) / node.visits)

    @staticmethod
    def select(node):
        while node.children:
            node = max(node.children, key=MCTSNode.uct_value)
        return node

    @staticmethod
    def expand_node(node):
        legal_moves = [key for key, value in node.state.items() if value['player'] == Player.UNOCCUPIED.value]
        if legal_moves:
            move = random.choice(legal_moves)
            new_state = copy.deepcopy(node.state)
            new_state[move]['player'] = Player.PLAYER_O.value
            child_node = MCTSNode(new_state, move)
            child_node.parent = node
            node.children.append(child_node)
            return child_node
        else:
            return None

    @staticmethod
    def simulate(node, winning_conditions):
        current_state = node.state.copy()
        while not MCTSNode.is_terminal(current_state, winning_conditions):
            legal_moves = [key for key, value in current_state.items() if value['player'] == Player.UNOCCUPIED.value]
            move = random.choice(legal_moves)
            current_state[move]['player'] = Player.PLAYER_X.value
        return MCTSNode.get_winner(current_state, winning_conditions)

    @staticmethod
    def backpropagate(node, result):
        while node is not None:
            node.visits += 1
            node.total_reward += result
            node = node.parent

    @staticmethod
    def is_terminal(state, winning_conditions):
        return any(MCTSNode.check_winning_condition(state, condition) for condition in winning_conditions) or all(
            value['player'] != Player.UNOCCUPIED.value for value in state.values())

    @staticmethod
    def check_winning_condition(state, condition):
        for direction, indices in condition.items():
            values = [state[index]['player'] for index in indices]
            if all(value == Player.PLAYER_O.value for value in values):
                return True
        return False

    @staticmethod
    def get_winner(state, winning_conditions):
        for condition in winning_conditions:
            direction, indices = list(condition.items())[0]
            values = [state[index]['player'] for index in indices]
            if all(value == Player.PLAYER_O.value for value in values):
                return Player.PLAYER_O.value
        return Player.UNOCCUPIED.value
