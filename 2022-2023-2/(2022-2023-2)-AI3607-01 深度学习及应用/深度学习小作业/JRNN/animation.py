import time


def frame_counter(step):
    if not hasattr(frame_counter, 'counter'):
        frame_counter.counter = 0
    frame_counter.counter += step
    return frame_counter.counter


def rolling_ball(move_range: int = 10, delay=1 / 30, msg: str = ' '):
    assert move_range > 0 and delay >= 0
    position = 0
    if not hasattr(rolling_ball, 'direction'):
        rolling_ball.direction = 1
    while True:
        position = frame_counter(rolling_ball.direction) if delay == 0 else position + rolling_ball.direction
        if position == 0 or position == move_range - 1:
            rolling_ball.direction = -rolling_ball.direction

        ball = '\u25CF'
        text = f"\r\033[32m{'(' + ' ' * position}{ball}{' ' * (move_range - position - 1) + ')'}\033[m"
        print(text, end='')
        print(msg, end='')
        if delay == 0:
            break
        if not hasattr(rolling_ball, 'start_time'):
            rolling_ball.start_time = time.time()
        time.sleep(delay)
        if time.time() - rolling_ball.start_time > 5:
            break


def spinning_stick(num_space: int = 1, delay=1 / 10, msg: str = ' '):
    assert num_space >= 0 and delay >= 0
    shapes = ['|', '/', '—', '\\']
    state = 0
    while True:
        state = frame_counter(1) if delay == 0 else state + 1

        stick = shapes[state % len(shapes)]
        text = f"\r\033[32m{' ' * num_space}{stick}{' ' * num_space}\033[m"
        print(text, end='')
        print(msg, end='')
        if delay == 0:
            break
        if not hasattr(spinning_stick, 'start_time'):
            spinning_stick.start_time = time.time()
        time.sleep(delay)
        if time.time() - spinning_stick.start_time > 5:
            break


if __name__ == '__main__':
    rolling_ball(msg='rolling_ball')
    print()
    spinning_stick(msg='spinning_stick')
