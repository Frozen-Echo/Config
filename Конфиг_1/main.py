import os
import sys
import tarfile
import time
import subprocess


class ShellEmulator:
    def __init__(self, username, hostname, fs_image, start_script):
        self.username = username
        self.hostname = hostname
        self.fs_image = fs_image
        self.start_script = start_script
        self.mount_fs()

    def mount_fs(self):
        """Монтируем виртуальную файловую систему из tar-архива."""
        self.fs_dir = "D:/tmp/vfs"
        if not os.path.exists(self.fs_dir):
            os.makedirs(self.fs_dir)

        with tarfile.open(self.fs_image, "r") as tar:
            tar.extractall(path=self.fs_dir)

    def run_script(self):
        """Запускаем команды из стартового скрипта."""
        if os.path.exists(self.start_script):
            with open(self.start_script, "r") as file:
                commands = file.readlines()
                for command in commands:
                    self.run_command(command.strip())

    def run_command(self, command):
        """Основная функция обработки команд."""
        args = command.split()
        if not args:
            return

        cmd = args[0]

        if cmd == "ls":
            self.ls(args[1:])
        elif cmd == "cd":
            self.cd(args[1:])
        elif cmd == "exit":
            self.exit_shell()
        elif cmd == "date":
            self.date()
        elif cmd == "touch":
            self.touch(args[1:])
        elif cmd == "rev":
            self.rev(args[1:])
        else:
            print(f"{cmd}: команда не найдена")

    def ls(self, args):
        """Команда ls."""
        path = args[0] if args else self.fs_dir
        try:
            for entry in os.listdir(path):
                print(entry)
        except FileNotFoundError:
            print(f"ls: не удается открыть каталог: {path}")

    def cd(self, args):
        """Команда cd."""
        if len(args) < 1:
            print("cd: недостаточно аргументов")
            return

        path = args[0]
        new_path = os.path.join(self.fs_dir, path)
        if os.path.isdir(new_path):
            os.chdir(new_path)
        else:
            print(f"cd: не удается найти каталог: {path}")

    def date(self):
        """Команда date."""
        print(time.strftime("%a %b %d %H:%M:%S %Y"))

    def touch(self, args):
        """Команда touch."""
        if len(args) < 1:
            print("touch: недостаточно аргументов")
            return

        file_path = os.path.join(self.fs_dir, args[0])
        with open(file_path, 'a'):
            os.utime(file_path, None)

    def rev(self, args):
        """Команда rev."""
        if len(args) < 1:
            print("rev: недостаточно аргументов")
            return

        file_path = os.path.join(self.fs_dir, args[0])
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding="utf8") as file:
                content = file.read()
                print(content[::-1])
        else:
            print(f"rev: не удается открыть файл: {args[0]}")

    def exit_shell(self):
        """Выход из эмулятора."""
        print("Выход из оболочки.")
        sys.exit(0)

    def prompt(self):
        """Отображение приглашения к вводу."""
        return f"{self.username}@{self.hostname}:~$ "


def main():
    if len(sys.argv) != 5:
        print("Использование: python main.py <user> <hostname> <fs_image> <start_script>")
        sys.exit(1)

    username, hostname, fs_image, start_script = sys.argv[1:]

    if not os.path.exists(fs_image):
        print(f"Ошибка: Файл образа {fs_image} не найден.")
        sys.exit(1)

    emulator = ShellEmulator(username, hostname, fs_image, start_script)
    emulator.run_script()

    while True:
        command = input(emulator.prompt())
        emulator.run_command(command)


if __name__ == "__main__":
    main()
