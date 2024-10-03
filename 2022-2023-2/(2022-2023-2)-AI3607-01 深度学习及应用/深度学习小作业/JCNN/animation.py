# I'm tring to develep a common animation utils library
import time


def frame_counter(step):
    if not hasattr(frame_counter, 'counter'):
        frame_counter.counter = 0
    frame_counter.counter += step
    return frame_counter.counter


def rolling_ball(move_range: int = 10, delay=0.1, msg: str = ' '):
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
        time.sleep(delay)


if __name__ == '__main__':
    rolling_ball()
