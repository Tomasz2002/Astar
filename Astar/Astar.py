import heapq
import math

# Funkcja obliczająca odległość między dwoma punktami (heurystyka euklidesowa)
def heuristic(point_a, point_b):
    return math.sqrt((point_a[0] - point_b[0])**2 + (point_a[1] - point_b[1])**2)

# Funkcja zamieniająca współrzędne (odwrócenie osi Y, jeśli mapa zaczyna się od dolnego-lewego rogu)
def changePlace(position):
    return 19 - position[0], position[1]

# Główna funkcja algorytmu A* do znajdowania najkrótszej ścieżki
def astar(grid, start, goal):
    # Zamiana współrzędnych punktu startowego i docelowego
    start = changePlace(start)
    print(start)
    goal = changePlace(goal)

    # Wymiary siatki (liczba wierszy i kolumn)
    rows, cols = len(grid), len(grid[0])

    if(grid[start[0]][start[1]]==5):
        print("Pozycja startowa na przeszkodzie")
        return 0;

    # Kolejka priorytetowa dla punktów do sprawdzenia
    open_set = []
    heapq.heappush(open_set, (0 + heuristic(start, goal), 0, start))

    # Słownik przechowujący skąd przyszliśmy do każdego punktu
    came_from = {}
    # Słownik przechowujący najniższy koszt dotarcia do każdego punktu
    g_score = {start: 0}

    # Główna pętla - dopóki są punkty do sprawdzenia
    while open_set:
        # Pobierz punkt z najniższym kosztem (f-score)
        _, current_cost, current = heapq.heappop(open_set)

        # Sprawdź, czy dotarliśmy do celu
        if current == goal:
            # Odtwórz ścieżkę od celu do startu
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()  # Odwróć kolejność, aby zaczynała się od punktu startowego
            return path

        # Lista sąsiadów (góra, dół, lewo, prawo)
        neighbors = [
            (current[0] - 1, current[1]),
            (current[0] + 1, current[1]),
            (current[0], current[1] - 1),
            (current[0], current[1] + 1)
        ]

        # Przetwarzanie każdego sąsiada
        for neighbor in neighbors:
            row, col = neighbor

            # Sprawdź, czy sąsiad jest w granicach siatki i nie jest przeszkodą
            if 0 <= row < rows and 0 <= col < cols and grid[row][col] != 5:
                # Oblicz tymczasowy koszt dotarcia do sąsiada
                tentative_g_score = g_score[current] + 1

                # Zaktualizuj koszty i ścieżkę, jeśli znaleziono lepszą trasę
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    g_score[neighbor] = tentative_g_score
                    f_score = tentative_g_score + heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_score, tentative_g_score, neighbor))
                    came_from[neighbor] = current

    # Zwróć None, jeśli nie znaleziono ścieżki
    return None

# Funkcja oznaczająca znalezioną ścieżkę na siatce
def mark_path(grid, path):
    for r, c in path:
        if grid[r][c] == 0:  # Zmienia tylko pola, które nie są przeszkodami lub punktami startu/celu
            grid[r][c] = 3
    return grid

# Funkcja ładująca siatkę z pliku tekstowego
def load_grid_from_file(file_path):
    with open(file_path, "r") as file:
        return [list(map(int, line.split())) for line in file]

if __name__ == "__main__":
    # Załaduj siatkę z pliku
    grid = load_grid_from_file("grid.txt")

    # Współrzędne punktu startowego i docelowego
    start = (1,0)  # Punkt startowy
    goal = (18, 18)  # Punkt docelowy

    # Uruchom algorytm A*
    path = astar(grid, start, goal)

    # Wyświetl wynik
    if path:
        grid = mark_path(grid, path)
        for row in grid:
            print(" ".join(map(str, row)))
    else:
        print("No path found.")
