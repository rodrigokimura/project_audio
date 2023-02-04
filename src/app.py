from subprocess import PIPE, run
from typing import NamedTuple

from speech import speak


class Profile(NamedTuple):
    value: str
    name: str


A2DP = Profile("a2dp_sink", "high fidelity")
HFP = Profile("handsfree_head_unit", "call")


def main():
    profile = HFP if is_a2dp_active() else A2DP
    change_profile(profile)
    speak(f"{profile.name} profile")


def get_card():
    result = run(["pactl", "list"], stdout=PIPE)
    cards = map(lambda s: s.decode(), result.stdout.split(b"\n"))
    card = list(filter(lambda x: "bluez_card" in x, cards))[0].split(" ")[-1]
    return card


def get_device():
    results = run(["pacmd", "list-sinks"], stdout=PIPE)
    devices = map(lambda s: s.decode(), results.stdout.split(b"\n"))
    device = list(filter(lambda x: "bluez_sink" in x, devices))[0].split(" ")[-1]
    device = device.removeprefix("<").removesuffix(">")
    return device


def is_a2dp_active():
    results = run(["pacmd", "list-sinks"], stdout=PIPE)
    results = map(lambda s: s.decode(), results.stdout.split(b"\n"))
    results = list(filter(lambda x: "bluez_sink" in x and A2DP.value in x, results))
    return len(results) > 0


def change_profile(profile: Profile) -> None:
    card = get_card()
    run(["pactl", "set-card-profile", card, profile.value])
    run(["pactl", "set-default-sink", get_device()])


if __name__ == "__main__":
    main()
