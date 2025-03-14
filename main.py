from textual.app import App
from textual import on
from textual.widgets import *
from textual.containers import *
from textual.screen import Screen
from utils import *
from concurrent.futures import ThreadPoolExecutor
from rich.table import Table
import csv
import io

prompts = {
    'create': ['New environment name', 'Python version'],
    'clone': ['New environment name'],
    'import': ['Path to environment file', 'New environment name'],
    'export': ['Path to environment file'],
}


def reload():
    global envs_lst, pkgs_lst, envs_pkgs, selection, operation
    print("conda env list...")
    envs_lst = conda_env_list()
    print("conda list...")
    pool = ThreadPoolExecutor(max_workers=len(envs_lst))
    pkgs_lst = list(pool.map(conda_list, envs_lst))
    envs_pkgs = dict(zip(envs_lst, pkgs_lst))
    operation = ''
    selection = 'base'


class InputDialog(Screen):

    def compose(self):
        if operation != 'remove':
            widget_top = [
                Input(placeholder=prompt, id=f'textbox{i}')
                for i, prompt in enumerate(prompts[operation])
            ]
        else:
            widget_top = [Label(f"Are you sure you want to remove the environment?")]
        yield VerticalGroup(
            *widget_top,
            HorizontalGroup(Button("OK", variant="primary", id="bu_ok"),
                            Button("Cancel", variant="error", id="bu_cancel")))

    @on(Button.Pressed, '#bu_ok')
    def press_ok(self):
        if operation == 'create':
            name: Input = self.query('#textbox0')[0]
            version: Input = self.query('#textbox1')[0]
            command = f'conda create -n {name.value} python={version.value} -y'
        elif operation == 'clone':
            name: Input = self.query('#textbox0')[0]
            command = f'conda create -n {name.value} --clone {selection}'
        elif operation == 'import':
            path: Input = self.query('#textbox0')[0]
            name: Input = self.query('#textbox1')[0]
            command = f'conda env create -n {name.value} -f {path.value}'
        elif operation == 'export':
            path: Input = self.query('#textbox0')[0]
            command = f'conda env export -n {selection} -f {path.value}'
        elif operation == 'remove':
            command = f'conda env remove -n {selection} -y'
        self.app.exit(command)

    @on(Button.Pressed, '#bu_cancel')
    def press_cancel(self):
        self.app.pop_screen()


class CondaTUI(App):
    DEFAULT_CSS = 'ListView { width: 20; } '
    BINDINGS = [('c', 'create', '[+ create]'), ('o', 'clone', '[◪ clone]'),
                ('i', 'import', '[→ import]'), ('e', 'export', '[↑ export]'),
                ('r', 'remove', '[× remove]'), ('n', 'clean', '[- clean]')]

    def compose(self):
        """Create child widgets for the app."""
        yield Header()
        yield HorizontalGroup(
            ListView(*list(map(lambda x: ListItem(Label(x)), envs_lst)), id="lst"),
            RichLog(id="log", auto_scroll=False),
        )
        yield Footer()

    def on_ready(self):
        pass

    @on(ListView.Highlighted, '#lst')
    def show_pkgs(self):
        name = self.query('#lst')[0].highlighted_child.children[0].renderable
        global selection
        selection = name
        log: RichLog = self.query('#log')[0]
        log.clear()
        s = envs_pkgs[name]
        posi = s.find('# Name')
        head = s[:posi]
        pkgs_csv = s[posi + 2:]
        pkgs_csv = ' '.join(list(filter(lambda x: x != '', pkgs_csv.split(' '))))
        log.write(head)
        rows = iter(csv.reader(io.StringIO(pkgs_csv), delimiter=' '))
        table = Table(*next(rows))
        for row in rows:
            table.add_row(*row)

        log.write(table)

    def action_create(self):
        global operation
        operation = 'create'
        self.push_screen(InputDialog())

    def action_clone(self):
        global operation
        operation = 'clone'
        self.push_screen(InputDialog())

    def action_import(self):
        global operation
        operation = 'import'
        self.push_screen(InputDialog())

    def action_export(self):
        global operation
        operation = 'export'
        self.push_screen(InputDialog())

    def action_remove(self):
        global operation
        operation = 'remove'
        self.push_screen(InputDialog())

    def action_clean(self):
        self.app.exit('conda clean --all')


if __name__ == "__main__":
    import subprocess
    while True:
        reload()
        app = CondaTUI()
        ret = app.run()
        if not isinstance(ret, str):
            print('CondaTUI已退出！')
            break
        subprocess.run(ret, shell=True, check=True)
        print('回主菜单？(y/n)')
        inp = input()
        while inp not in ['y', 'n']:
            print('输入错误！请输入y或n')
            inp = input()
        if inp == 'y':
            continue
        else:
            break
