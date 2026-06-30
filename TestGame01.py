import curses
import random

def create_apple(snake, height, width):
    while True:
        apple = (
            random.randint(1, height - 2),
            random.randint(1, width - 2)
        )
        if apple not in snake:
            return apple

def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.keypad(True)

    height, width = stdscr.getmaxyx()
    window = curses.newwin(height, width, 0, 0)
    window.keypad(True)
    window.nodelay(True)
    window.timeout(100)

    snake = [
        (height // 2, width // 2 + 1),
        (height // 2, width // 2),
        (height // 2, width // 2 - 1),
    ]
    direction = curses.KEY_RIGHT
    apple = create_apple(snake, height, width)
    score = 0

    while True:
        window.clear()
        window.border()

        window.addstr(0, 2, f" Score: {score} ")
        window.addstr(0, width - 12, " q:退出 ")

        window.addch(apple[0], apple[1], "@")
        for y, x in snake:
            window.addch(y, x, "#")

        key = window.getch()
        if key in [curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT]:
            if (direction, key) not in [
                (curses.KEY_UP, curses.KEY_DOWN),
                (curses.KEY_DOWN, curses.KEY_UP),
                (curses.KEY_LEFT, curses.KEY_RIGHT),
                (curses.KEY_RIGHT, curses.KEY_LEFT),
            ]:
                direction = key
        elif key in [ord("q"), ord("Q")]:
            break

        head_y, head_x = snake[0]
        if direction == curses.KEY_UP:
            head_y -= 1
        elif direction == curses.KEY_DOWN:
            head_y += 1
        elif direction == curses.KEY_LEFT:
            head_x -= 1
        elif direction == curses.KEY_RIGHT:
            head_x += 1

        new_head = (head_y, head_x)

        if (
            head_y == 0
            or head_y == height - 1
            or head_x == 0
            or head_x == width - 1
            or new_head in snake
        ):
            break

        snake.insert(0, new_head)

        if new_head == apple:
            score += 1
            apple = create_apple(snake, height, width)
        else:
            snake.pop()

    window.nodelay(False)
    window.addstr(height // 2, width // 2 - 5, "游戏结束")
    window.addstr(height // 2 + 1, width // 2 - 9, f"最终得分: {score}")
    window.addstr(height // 2 + 3, width // 2 - 12, "按任意键退出...")
    window.getch()

if __name__ == "__main__":
    curses.wrapper(main)