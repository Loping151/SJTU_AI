import time


def frame_counter(step):
    if not hasattr(frame_counter, 'counter'):
        frame_counter.counter = 0
    frame_counter.counter += step
    return frame_counter.counter


def rolling_ball(move_range: int = 10, delay=1 / 24, msg: str = ' '):
    assert move_range > 0 and delay >= 0
    position = 0
    rolling_ball.direction = getattr(rolling_ball, 'direction', 1)
    rolling_ball.speed = getattr(rolling_ball, 'speed', time.time())
    rolling_ball.start_time = getattr(rolling_ball, 'start_time', time.time())
    while True:
        if delay > 0 or time.time() - rolling_ball.speed > 1 / 24:
            rolling_ball.speed = time.time()
            position = frame_counter(rolling_ball.direction) if delay == 0 else position + rolling_ball.direction
            if position == 0 or position == move_range - 1:
                rolling_ball.direction = -rolling_ball.direction
        else:
            position = frame_counter(0) if delay == 0 else position + rolling_ball.direction
        ball = '\u25CF'
        text = f"\b\b\r\033[32m{'(' + ' ' * position}{ball}{' ' * (move_range - position - 1) + ')'}\033[m"
        print(text, end='')
        print(msg, end='')
        if delay == 0:
            break
        if not hasattr(rolling_ball, 'start_time'):
            rolling_ball.start_time = time.time()
        time.sleep(delay)
        if time.time() - rolling_ball.start_time > 5:
            break


def spinning_stick(num_space: int = 1, delay=1 / 24, msg: str = ' '):
    assert num_space >= 0 and delay >= 0
    shapes = ['|', '/', '—', '\\']
    state = 0
    spinning_stick.direction = getattr(spinning_stick, 'direction', 1)
    spinning_stick.speed = getattr(spinning_stick, 'speed', time.time())
    spinning_stick.start_time = getattr(spinning_stick, 'start_time', time.time())

    while True:
        if delay > 0 or time.time() - spinning_stick.speed > 1 / 24:
            spinning_stick.speed = time.time()
            state = frame_counter(1) if delay == 0 else state + 1
        else:
            state = frame_counter(0)
        stick = shapes[state % len(shapes)]
        text = f"\b\b\r\033[32m{' ' * num_space}{stick}{' ' * num_space}\033[m"
        print(text, end='')
        print(msg, end='')
        if delay == 0:
            break
        time.sleep(delay)
        if time.time() - spinning_stick.start_time > 5:
            break


if __name__ == '__main__':
    rolling_ball(msg='rolling_ball')
    print()
    spinning_stick(msg='spinning_stick')
