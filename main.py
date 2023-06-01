import numpy as np
from collections import deque as queue
import argparse


# function that create grid with false
def create_false_board(row, col):
    grid = []
    for _ in range(row):
        row = []
        for _ in range(col):
            row.append(False)
        grid.append(row)
    return grid


# function that give me the possible moves for every point in the grid :
def possible_moves(grid, position):
    row, col = len(board), len(board[0])
    x, y = position[0], position[1]
    moves = []

    # check up :
    if x > 0 and grid[x - 1][y] != 1:
        moves.append((x - 1, y))
    # check down :
    if x < row - 1 and grid[x + 1][y] != 1:
        moves.append((x + 1, y))
    # check left :
    if y > 0 and grid[x][y - 1] != 1:
        moves.append((x, y - 1))
    # check right :
    if y < col - 1 and grid[x][y + 1] != 1:
        moves.append((x, y + 1))
    return moves


def BFS(board, ghost_position):
    row_len, col_len = len(board), len(board[0])

    visited = create_false_board(row_len, col_len)
    distances = [[0] * col_len for _ in range(row_len)]

    q = queue()
    q.append(pacman_location)
    visited[pacman_location[0]][pacman_location[1]] = True

    while q:
        curr_position = q.popleft()

        # check if I got the ghost:
        if curr_position == ghost_position:
            return distances[curr_position[0]][curr_position[1]]

        visited[curr_position[0]][curr_position[1]] = True
        moves = possible_moves(board, curr_position)
        for move in moves:
            if not visited[move[0]][move[1]]:
                # updates :
                q.append(move)
                visited[move[0]][move[1]] = True
                distances[move[0]][move[1]] = distances[curr_position[0]][curr_position[1]] + 1
    return -1


def get_ghosts_locations(board):
    ghosts_positions_np = np.where(board == 2)
    ghosts_positions = []
    for row, col in zip(ghosts_positions_np[0], ghosts_positions_np[1]):
        ghosts_positions.append((row, col))
    return ghosts_positions


# read the file :
parser = argparse.ArgumentParser(description="Read board file.")
parser.add_argument("--board", type=str, help="Path to the board file.")

args = parser.parse_args()
board_file = args.board
board = np.load(board_file)


# get the location of the pacman :
pacman_location = np.where(board == 3)
pacman_location = (pacman_location[0][0], pacman_location[1][0])

# get the location of the ghosts  :ghosts_positions_np = np.where(board == 2)
ghosts_positions = get_ghosts_locations(board)

# calculate the distance of the ghost according of bfs algorithm:
ghosts_dict = {}
for ghost in ghosts_positions:
    ghost_dis = BFS(board, ghost)
    if ghost_dis != -1:
        ghosts_dict[ghost] = ghost_dis

# sorting the distances:
sorted_dict = sorted(ghosts_dict.items(), key=lambda item: item[1])
output = []
for i in sorted_dict:
    ghost_loc = [i[0][0], i[0][1]]
    ghost_dis = i[1]
    output.append([ghost_loc, ghost_dis])

print(output)
