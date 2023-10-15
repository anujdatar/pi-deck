import subprocess


def print_command(a: str) -> None:
    print(f"commend: {a}")


def reboot():
    subprocess.run(
        ["systemctl", "reboot"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def shutdown():
    subprocess.run(
        ["systemctl", "poweroff"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
