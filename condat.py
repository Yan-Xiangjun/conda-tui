import subprocess

subprocess.run('python main.py', shell=True, check=True)
with open('command.txt', 'r') as f:
    command = f.read()
subprocess.run(command, check=True)
