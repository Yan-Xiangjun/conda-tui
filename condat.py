import subprocess

while True:
    subprocess.run('python main.py', shell=True, check=True)
    with open('command.txt', 'r') as f:
        command = f.read()
    subprocess.run(command, shell=True, check=True)
    print('回主菜单？(y/n)')
    inp = input()
    while inp not in ['y', 'n']:
        print('输入错误！请输入y或n')
        inp = input()

    if inp == 'y':
        continue
    else:
        break
