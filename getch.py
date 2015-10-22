import sys
import select
import time

class _Getch:
    """Gets a single character from standard input.  Does not echo to the
screen."""
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self): return self.impl()


class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()

# [JRdP 2012-06-13] The following functions (_isData and getch_noblock) are heaviliy based on 'Non blocking console
# input in Python and Java' by Graham King:# http://www.darkcoding.net/software/non-blocking-console-io-is-not-possible/.
# Method used in a nutshell: The terminal is switched out of line mode into character mode (and restored
# before the function quits). There is no portable way to do this across operating systems.
# The tty module has an interface to set the terminal to character mode, the termios module allows you to save
# and restore the console setup, and the select module lets you know if there is any input available.

def _isData():
    return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])

def getch_noblock(character_in, wait_time, list_of_break_characters=[]):
    """
    By default the console on Linux and Windows is buffered: It does not send you character data until the Enter key
    is pressed.This function waits for key input for a specified time, expecting one of the characters given
    in an input list. The function returns either immediately when a valid key is pressed, or if no key was pressed
    when the specified waiting time has elapsed.

    @param c:Character: This character will be returned if no input is received during the allowed time.
    @param wait_time: The duration in seconds that the function will wait for input.
    @param list_of_break_characters: List of characters allowed as input. All other characters (except Escape)
            will be ignored.
    @return: The character pressed by the user, or the character given at input if no valid key was pressed.
    """

    import tty
    import termios

    old_settings = termios.tcgetattr(sys.stdin)
    time_zero = time.time()
    time_passed = 0.0
    character_out = character_in

    try:
        tty.setcbreak(sys.stdin.fileno())
        while time_passed < wait_time:
            if _isData():
                _c = sys.stdin.read(1)
                if _c == '\x1b': # escape
                    break
                elif _c in list_of_break_characters or not list_of_break_characters:
                    character_out = _c
                    break

            time_passed = time.time() - time_zero
            time.sleep(0.1)  # Sleep 100 ms
    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)

    return character_out


getch = _Getch()
