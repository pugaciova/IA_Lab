import heapq

def initialize_world(size_x, size_y, num_blocks):
    grid = [[[] for _ in range(size_x)] for _ in range(size_y)]  # Изменено на список списков
    blocks = {}
    for _ in range(num_blocks):
        block_id = input("Введите идентификатор кубика: ")
        x = int(input(f"Введите X координату для кубика {block_id}: "))
        y = int(input(f"Введите Y координату для кубика {block_id}: "))
        grid[y][x].append(block_id)  # Изменено на y, x для вертикального представления
        blocks[block_id] = (x, y)
    return grid, blocks

def dijkstra(grid, start, end):
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    queue = [(0, start)]
    visited = set()
    prev = {start: None}

    while queue:
        dist, current = heapq.heappop(queue)
        if current == end:
            break

        for dx, dy in directions:
            nx, ny = current[0] + dx, current[1] + dy
            if 0 <= ny < len(grid) and 0 <= nx < len(grid[0]) and not grid[ny][nx] and (nx, ny) not in visited:
                visited.add((nx, ny))
                prev[(nx, ny)] = current
                heapq.heappush(queue, (dist + 1, (nx, ny)))

    path = []
    current = end
    while current != start:
        path.append(current)
        current = prev.get(current)
    path.append(start)
    return path[::-1]

def move_block(grid, blocks, block_id, target):
    if block_id not in blocks:
        print("Кубик не найден.")
        return
    start = blocks[block_id]
    grid[start[1]][start[0]].remove(block_id)
    path = dijkstra(grid, start, target)
    if path:
        print(f"Путь для кубика {block_id}: {path}")
        grid[target[1]][target[0]].append(block_id)
        blocks[block_id] = target
    else:
        print("Путь не найден.")
        grid[start[1]][start[0]].append(block_id)

# Представим, что size_x теперь является 'высотой', а size_y - 'шириной'
size_x, size_y = 5, 5
num_blocks = int(input("Сколько кубиков будете размещать? "))
grid, blocks = initialize_world(size_x, size_y, num_blocks)

while True:
    block_id = input("Какой кубик переместить? (введите 'quit' для выхода): ")
    if block_id == 'quit':
        break

    target_x = int(input("Конечная X координата: "))
    target_y = int(input("Конечная Y координата: "))
    move_block(grid, blocks, block_id, (target_x, target_y))

    print("\nТекущее состояние мира:")
    # Переворачиваем матрицу так, чтобы кубики располагались внизу
    for y in range(size_y - 1, -1, -1):  # Изменение порядка итерации по строкам
        for x in range(size_x):
            cell = grid[y][x]
            if cell:  # Если стопка кубиков не пуста
                print(cell[-1], end=' ')  # Печатаем идентификатор последнего кубика в стопке
            else:
                print('.', end=' ')  # Печатаем точку, если ячейка пуста
        print()  # Переход на новую строку

