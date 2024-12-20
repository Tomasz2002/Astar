import pygame
import heapq
import math
import time

# Funkcja heurystyczna (Euklidesowa)
def heuristic(a, b):
    return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)

def changePlace(poz):
    return 19 - poz[0], poz[1]

def astar(grid, start, goal):
    start = changePlace(start)
    goal = changePlace(goal)
    rows, cols = len(grid), len(grid[0])
    open_set = []
    heapq.heappush(open_set, (0 + heuristic(start, goal), 0, start))

    came_from = {}
    g_score = {start: 0}

    while open_set:
        _, current_cost, current = heapq.heappop(open_set)

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            return path

        neighbors = [
            (current[0] - 1, current[1]),
            (current[0] + 1, current[1]),
            (current[0], current[1] - 1),
            (current[0], current[1] + 1)
        ]

        for neighbor in neighbors:
            row, col = neighbor

            if 0 <= row < rows and 0 <= col < cols and grid[row][col] != 5:
                tentative_g_score = g_score[current] + 1

                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    g_score[neighbor] = tentative_g_score
                    f_score = tentative_g_score + heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_score, tentative_g_score, neighbor))
                    came_from[neighbor] = current

    return None

def load_grid_from_file(file_path):
    with open(file_path, "r") as f:
        return [list(map(int, line.split())) for line in f]

def draw_grid(screen, grid, cell_size, player_pos, optimal_path=None, visited_positions=None):
    colors = {
        0: (255, 255, 255),
        3: (0, 255, 0),
        5: (0, 0, 0),
    }

    rows, cols = len(grid), len(grid[0])
    for row in range(rows):
        for col in range(cols):
            color = colors.get(grid[row][col], (200, 200, 200))
            pygame.draw.rect(screen, color, (col * cell_size, row * cell_size, cell_size, cell_size))

    if visited_positions:
        for r, c in visited_positions:
            pygame.draw.rect(screen, (255, 0, 0), (c * cell_size, r * cell_size, cell_size, cell_size))

    if optimal_path:
        for r, c in optimal_path:
            pygame.draw.rect(screen, (0, 255, 0), (c * cell_size, r * cell_size, cell_size, cell_size))

    pygame.draw.rect(screen, (0, 0, 255), (player_pos[1] * cell_size, player_pos[0] * cell_size, cell_size, cell_size))

def main():

    pygame.init()
    cell_size = 30
    grid = load_grid_from_file("grid.txt")
    rows, cols = len(grid), len(grid[0])

    screen = pygame.display.set_mode((cols * cell_size, rows * cell_size))
    pygame.display.set_caption("A* Game")

    start = (0, 0)
    goal = (rows - 1, cols - 1)


    optimal_path = astar(grid, start, goal)
    if not optimal_path:
        print("No path found.")
        return

    player_pos = list(changePlace(start))
    visited_positions = [tuple(player_pos)]
    moves = 0
    clock = pygame.time.Clock()

    running = True
    reached_goal = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if not reached_goal:
                    new_pos = list(player_pos)
                    if event.key == pygame.K_UP:
                        new_pos[0] -= 1
                    elif event.key == pygame.K_DOWN:
                        new_pos[0] += 1
                    elif event.key == pygame.K_LEFT:
                        new_pos[1] -= 1
                    elif event.key == pygame.K_RIGHT:
                        new_pos[1] += 1


                    if (0 <= new_pos[0] < rows and 0 <= new_pos[1] < cols and grid[new_pos[0]][new_pos[1]] != 5):
                        player_pos = new_pos
                        visited_positions.append(tuple(player_pos))
                        moves += 1


                    if tuple(player_pos) == changePlace(goal):
                        reached_goal = True


        screen.fill((0, 0, 0))
        draw_grid(screen, grid, cell_size, player_pos, optimal_path if reached_goal else None, visited_positions)
        pygame.display.flip()


        clock.tick(60)


        if reached_goal:
            time.sleep(2)
            if moves == len(optimal_path) - 1:
                print("Wygrana! Optymalna liczba ruchów:", moves)
            else:
                print("Przegrana! Twoje ruchy:", moves, "Optymalna liczba ruchów:", len(optimal_path) - 1)
            running = False

    pygame.quit()

if __name__ == "__main__":
    main()
