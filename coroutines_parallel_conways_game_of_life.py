# Author: gabri
# File: coroutines_parallel_conways_game_of_life
# Date: 12/07/2019
# Made with PyCharm

# Standard Library
from collections import namedtuple

# Third party modules

# Local application imports

ALIVE = '*'
EMPTY = '-'
Query = namedtuple('Query', ('y', 'x'))
Transition = namedtuple('Transition', ('y', 'x', 'state'))
TICK = object()


def count_neighbors(y, x):
    print('received state in count_neighbors')
    n_ = yield Query(y + 1, x + 0)  # North
    print('received state in count_neighbors')
    ne = yield Query(y + 1, x + 1)  # Northeast
    print('received state in count_neighbors')
    e_ = yield Query(y + 0, x + 1)  # East
    print('received state in count_neighbors')
    se = yield Query(y - 1, x + 1)  # Southeast
    print('received state in count_neighbors')
    s_ = yield Query(y - 1, x + 0)  # South
    print('received state in count_neighbors')
    sw = yield Query(y - 1, x - 1)  # Southwest
    print('received state in count_neighbors')
    w_ = yield Query(y + 0, x - 1)  # West
    print('received state in count_neighbors')
    nw = yield Query(y + 1, x - 1)  # Northwest

    neighbor_states = [n_, ne, e_, se, s_, sw, w_, nw]
    count = 0
    for state in neighbor_states:
        if state == ALIVE:
            count += 1
    return count


def game_logic(state, neighbors):
    if state == ALIVE:
        if neighbors < 2:
            return EMPTY  # Die: Too few
        elif neighbors > 3:
            return EMPTY  # Die: Too many
    elif neighbors == 3:
        return ALIVE  # Regenerate
    return state


def step_cell(y, x):
    state = yield Query(y, x)
    print('current state:', state)
    neighbors = await count_neighbors(y, x)
    next_state = game_logic(state, neighbors)
    yield Transition(y, x, next_state)


def simulate(height, width):
    while True:
        for y in range(height):
            for x in range(width):
                await step_cell(y, x)
        yield TICK


class Grid(object):
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.rows = []
        for _ in range(self.height):
            self.rows.append([EMPTY] * self.width)

    def query(self, y, x):
        print(Query(y % self.height, x % self.width))
        return self.rows[y % self.height][x % self.width]

    def assign(self, y, x, state):
        self.rows[y % self.height][x % self.width] = state

    def __str__(self):
        representation = ""
        for row in self.rows:
            representation += representation + ''.join(row) + '\n'
        return representation


def live_a_generation(grid, sim):
    progeny = Grid(grid.height, grid.width)
    item = next(sim)
    while item is not TICK:
        if isinstance(item, Query):
            # Get the item state
            state = grid.query(item.y, item.x)
            print('sent state from live_a_generation to count_neighbors')

            # Sends the state and receives a Query item of the neighbor
            item = sim.send(state)
        else:  # Must be a Transition
            print('Transition')
            progeny.assign(item.y, item.x, item.state)
            item = next(sim)
            print('')
    return progeny


def main():
    grid = Grid(3, 3)
    sim = simulate(3, 3)
    grid.assign(0, 2, ALIVE)
    print(grid)
    live_a_generation(grid, sim)

if __name__ == "__main__":
    main()
