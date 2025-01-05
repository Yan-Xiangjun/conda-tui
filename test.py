import subprocess
import os

os.environ['test'] = 'test1'
subprocess.run(['python', 'test2.py'])
print(os.environ['test'])
