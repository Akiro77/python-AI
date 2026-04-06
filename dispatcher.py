from commands.time_module import get_time
from commands.system_control import shutdown
from commands.user import set_name, get_name
from commands.basic import hello


def dispatch(text, memory):
    text = text.lower()

    COMMANDS = [
        ("koniec", shutdown),
        ("cześć", hello),
        ("godzina", get_time),
        ("mam na imię", lambda t: set_name(t, memory)),
        ("jak mam na imię", lambda t: get_name(memory)),
    ]

    for keyword, func in COMMANDS:
        if keyword in text:
            return func(text)

    return "Nie rozumiem jeszcze, ale się uczę 😅"