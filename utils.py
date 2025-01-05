import subprocess


def shell(command):
    return subprocess.run(command,
                          shell=True,
                          stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE,
                          universal_newlines=True).stdout


def conda_env_list():
    s = shell('conda env list').strip()
    envs_list = s.split('\n')[2:]
    envs_list = list(map(lambda x: x.split()[0], envs_list))
    return envs_list


def conda_list(name):
    pkgs = subprocess.run(f'conda activate {name} && conda list',
                          shell=True,
                          stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE,
                          encoding='utf-8').stdout

    return pkgs


conda_env_list()
