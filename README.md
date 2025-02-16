# Countdown Timer

This is a countdown timer application written in Python. It displays a large countdown timer in the terminal using curses.

## Requirements

- Python 3.x
- curses module (usually included with Python)

## Usage

You can run the countdown timer with various options to specify the countdown duration or target date and time.

### Command Line Options

- `-D`, `--days`: Number of days to countdown
- `-H`, `--hours`: Number of hours to countdown
- `-M`, `--minutes`: Number of minutes to countdown
- `-S`, `--seconds`: Number of seconds to countdown
- `-d`, `--date`: Specific date to countdown to (format: YYYY-MM-DD)
- `-t`, `--time`: Specific time to countdown to (format: HH:MM or HH:MM AM/PM)
- `-m`, `--message`: Message to display above the countdown timer

### Examples

1. Countdown for 1 hour:
    ```sh
    python countdown.py -H 1
    ```

2. Countdown until a specific date and time:
    ```sh
    python countdown.py -d 2023-12-31 -t 23:59
    ```

3. Countdown with a custom message:
    ```sh
    python countdown.py -H 1 -m "Time left until the event"
    ```

### Exiting the Countdown

You can exit the countdown timer by pressing the `ESC` key or the `q` key.
