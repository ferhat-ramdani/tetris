def draw_termtris(x: int, y: int):
    file = open("pieces/a.txt", 'r')
    lines = [line.rstrip() for line in file]
    print(lines)

draw_termtris(2, 6)