from collections import namedtuple

# Define state representations for both problem instances
# Using namedtuple helps keep track of what each position means.
ClassicState = namedtuple('State', ['farmer', 'wolf', 'goat', 'cabbage'])
SheepState = namedtuple('State', ['farmer', 'wolf', 'goat', 'cabbage', 'sheep'])

class WGCProblem:
    def __init__(self, instance='classic'):
        self.instance = instance

        if self.instance == 'classic':
            self.State = ClassicState
            self.initial_state = self.State(0, 0, 0, 0)
            self.goal_state = self.State(1, 1, 1, 1)
        elif self.instance == 'sheep':
            self.State = SheepState
            self.initial_state = self.State(0, 0, 0, 0, 0)
            self.goal_state = self.State(1, 1, 1, 1, 1)
        else:
            raise ValueError("Unknown problem instance specified.")

    def is_safe(self, state) -> bool:
        # Rule 1: Wolf and Goat cannot be alone
        if state.wolf == state.goat and state.farmer != state.wolf:
            return False
        # Rule 2: Goat and Cabbage cannot be alone
        if state.goat == state.cabbage and state.farmer != state.goat:
            return False

        if self.instance == 'sheep':
            # Rule 3: Wolf eats Sheep
            if state.wolf == state.sheep and state.farmer != state.wolf:
                return False
            # Rule 4: Sheep eats Cabbage
            if state.sheep == state.cabbage and state.farmer != state.sheep:
                return False
        
        return True

    def get_actions(self, state) -> list[str]:
        possible_actions = ["Move Alone"]
        # Determine which items are on the same bank as the farmer
        if state.farmer == state.wolf: possible_actions.append("Move Wolf")
        if state.farmer == state.goat: possible_actions.append("Move Goat")
        if state.farmer == state.cabbage: possible_actions.append("Move Cabbage")
        if self.instance == 'sheep' and state.farmer == state.sheep:
            possible_actions.append("Move Sheep")
        # Filter bad actions
        valid_actions = [
            action for action in possible_actions 
            if self.is_safe(self.get_result(state, action))
        ]
        return valid_actions

    def get_result(self, state, action: str):
        new_state_list = list(state)
        # The farmer always moves
        new_state_list[0] = 1 - state.farmer
        # Move item with the farmer
        if action == "Move Wolf": new_state_list[1] = 1 - state.wolf
        elif action == "Move Goat": new_state_list[2] = 1 - state.goat
        elif action == "Move Cabbage": new_state_list[3] = 1 - state.cabbage
        elif action == "Move Sheep": new_state_list[4] = 1 - state.sheep
        return self.State(*new_state_list)

    def is_goal(self, state) -> bool:
        return state == self.goal_state

    def path_cost(self, c: int, state1, action: str, state2) -> int:
        return c + 1

