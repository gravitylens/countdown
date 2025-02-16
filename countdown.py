import argparse
from datetime import datetime, timedelta
import time
import curses

DIGITS = {
    '0': ["██████",
          "██  ██",
          "██  ██",
          "██  ██",
          "██████"],
    '1': ["  ██  ",
          "  ██  ",
          "  ██  ",
          "  ██  ",
          "  ██  "],
    '2': ["██████",
          "    ██",
          "██████",
          "██    ",
          "██████"],
    '3': ["██████",
          "    ██",
          " █████",
          "    ██",
          "██████"],
    '4': ["██  ██",
          "██  ██",
          "██████",
          "    ██",
          "    ██"],
    '5': ["██████",
          "██    ",
          "██████",
          "    ██",
          "██████"],
    '6': ["█████ ",
          "██    ",
          "██████",
          "██  ██",
          "██████"],
    '7': ["██████",
          "    ██",
          "    ██",
          "    ██",
          "    ██"],
    '8': ["██████",
          "██  ██",
          "██████",
          "██  ██",
          "██████"],
    '9': ["██████",
          "██  ██",
          "██████",
          "    ██",
          "██████"],
    ':': ["      ",
          "  ██  ",
          "      ",
          "  ██  ",
          "      "],
    '.': ["      ",
          "      ",
          "      ",
          "      ",
          "  ██  "]
}

LABELS = ["Hours", "Minutes", "Seconds"]
DAYS_LABEL = "Days"

def parse_arguments():
    parser = argparse.ArgumentParser(description='Countdown Timer')
    parser.add_argument('-D', '--days', type=int, help='Number of days to countdown')
    parser.add_argument('-H', '--hours', type=int, help='Number of hours to countdown')
    parser.add_argument('-M', '--minutes', type=int, help='Number of minutes to countdown')
    parser.add_argument('-S', '--seconds', type=int, help='Number of seconds to countdown')
    parser.add_argument('-d', '--date', type=str, help='Specific date to countdown to (format: YYYY-MM-DD)')
    parser.add_argument('-t', '--time', type=str, help='Specific time to countdown to (format: HH:MM or HH:MM AM/PM)')
    parser.add_argument('-m', '--message', type=str, help='Message to display above the countdown timer')
    return parser.parse_args()

def calculate_time_left(args):
    description = []
    if args.date or args.time:
        date_str = args.date if args.date else datetime.now().strftime('%Y-%m-%d')
        time_str = args.time if args.time else '00:00'
        try:
            if 'AM' in time_str or 'PM' in time_str:
                target_time = datetime.strptime(f'{date_str} {time_str}', '%Y-%m-%d %I:%M %p')
            else:
                target_time = datetime.strptime(f'{date_str} {time_str}', '%Y-%m-%d %H:%M')
        except ValueError as e:
            print(f'Invalid date/time format: {e}. Use YYYY-MM-DD, HH:MM, or HH:MM AM/PM.')
            exit(1)
        time_left = (target_time - datetime.now()).total_seconds()
        if time_left < 0:
            print('The specified time is in the past!')
            exit(1)
        description.append(f"Countdown until {date_str} {time_str}")
        return time_left, ', '.join(description)
    else:
        total_seconds = 0
        if args.days:
            total_seconds += args.days * 86400
            description.append(f"{args.days} days")
        if args.hours:
            total_seconds += args.hours * 3600
            description.append(f"{args.hours} hours")
        if args.minutes:
            total_seconds += args.minutes * 60
            description.append(f"{args.minutes} minutes")
        if args.seconds:
            total_seconds += args.seconds
            description.append(f"{args.seconds} seconds")
        if total_seconds == 0:
            print('No valid time specified. Please provide days, hours, minutes, or seconds.')
            exit(1)
        return total_seconds, ', '.join(description)

def render_large_block_characters(stdscr, time_str, message, show_days=False):
    lines = [""] * 5
    if show_days:
        days = time_str.split()[0]
        for char in days:
            if char in DIGITS:
                for i in range(5):
                    lines[i] += DIGITS[char][i] + "  "
    else:
        for char in time_str:
            if char in DIGITS:
                for i in range(5):
                    lines[i] += DIGITS[char][i] + "  "
    height, width = stdscr.getmaxyx()
    start_y = (height // 2) - 5
    start_x = (width // 2) - (len(lines[0]) // 2)
    
    # Add message
    if message:
        message_x = (width // 2) - (len(message) // 2)
        stdscr.addstr(start_y - 2, message_x, message)
    
    for i, line in enumerate(lines):
        stdscr.addstr(start_y + i, start_x, line)
    
    # Add labels
    if show_days:
        label_x = (width // 2) - (len(DAYS_LABEL) // 2) - 1
        stdscr.addstr(start_y + 6, label_x, DAYS_LABEL)
    else:
        label_positions = [start_x + 2 , start_x + 27, start_x + 51]  # Adjust positions based on character width and spacing
        for i, label in enumerate(LABELS):
            label_x = label_positions[i] + (10 - len(label)) // 2  # Center the label under the two digits
            stdscr.addstr(start_y + 6, label_x, label)

def countdown_timer(stdscr, seconds, message, description):
    curses.curs_set(0)
    stdscr.nodelay(1)
    show_days = seconds >= 86400  # Show days if the amount of time is more than 24 hours
    try:
        while seconds > 0:
            stdscr.clear()
            time_str = str(timedelta(seconds=seconds)).split('.')[0]  # Remove microseconds
            # Ensure hours always have a leading zero
            if not show_days and len(time_str.split(':')[0]) == 1:
                time_str = '0' + time_str
            render_large_block_characters(stdscr, time_str, message, show_days)
            # Display the countdown description in the lower right corner
            height, width = stdscr.getmaxyx()
            stdscr.addstr(height - 1, width - len(description) - 1, description)
            stdscr.refresh()
            time.sleep(1)
            seconds -= 1
            # Check for Escape or 'q' key press
            key = stdscr.getch()
            if key == 27 or key == ord('q'):  # 27 is the ASCII code for Escape, ord('q') is the ASCII code for 'q'
                break
    except KeyboardInterrupt:
        pass
    finally:
        stdscr.clear()
        stdscr.refresh()
        stdscr.getch()

def main(stdscr):
    args = parse_arguments()
    try:
        seconds, description = calculate_time_left(args)
        if seconds > 0:
            countdown_timer(stdscr, seconds, args.message, description)
        else:
            print('The specified time is in the past!')
    except Exception as e:
        print(f'Error: {e}')

if __name__ == '__main__':
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        print("Countdown interrupted by user.")
