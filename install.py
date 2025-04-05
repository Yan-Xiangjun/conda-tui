import os
import subprocess
import sys
import platform

sh = lambda x: subprocess.run(x, check=True, shell=True)
os_type = platform.system()
if os_type not in ['Windows', 'Darwin', 'Linux']:
    print(f'The current operating system ({os_type}) is not supported!')
    exit(1)
DIR = os.path.dirname(os.path.abspath(__file__))
env_path = f'{DIR}/condat_venv'
print('Creating a virtual environment ...')
python_name = sys.executable[sys.executable.rfind('python'):]
if not os.path.exists(env_path):
    sh(f'{python_name} -m venv {env_path}')

print('Installing dependencies ...')
scripts_path = f'{env_path}\\Scripts\\' if os_type == 'Windows' else f'{env_path}/bin/'
url = 'https://mirrors.ustc.edu.cn/pypi/simple'
sh(f'{scripts_path}pip3 install -i {url} textual==1.0.0')

print('Adding the directory to PATH ...')
if os_type == 'Windows':
    with open('temp.txt', 'w') as f:
        f.write(DIR)
    sh(f'clip < temp.txt')
    os.remove('temp.txt')
    sh('''mshta "javascript:alert('Conda-TUI所在路径已复制到剪贴板，请将其添加到用户变量Path中！');close()"''')
    sh(f'rundll32.exe sysdm.cpl,EditEnvironmentVariables')
else:
    sh(f'chmod +x "{DIR}/condat"')
    sh(f'echo "export PATH={DIR}:\$PATH" >> ~/.$(basename "$SHELL")rc')

print('Done! Please restart the terminal.')
