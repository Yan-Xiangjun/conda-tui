from textual.app import App
from textual import on
from textual.widgets import *
from textual.containers import *
from textual.screen import Screen
from utils import *
from concurrent.futures import ThreadPoolExecutor

print("conda env list...")
envs_lst = conda_env_list()
print("conda list...")
pool = ThreadPoolExecutor(max_workers=len(envs_lst))
pkgs_lst = list(pool.map(conda_list, envs_lst))
envs_pkgs = dict(zip(envs_lst, pkgs_lst))
prompts = {
    'create': ['New environment name', 'Python version'],
    'clone': ['New environment name'],
    'import': ['Path to environment file', 'New environment name'],
    'export': ['Path to environment file'],
}
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
            command = f'conda create -n {name.value} python={version.value}'
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
            command = f'conda env remove -n {selection}'
        with open('command.txt', 'w') as f:
            f.write(command)

        self.app.exit()

    @on(Button.Pressed, '#bu_cancel')
    def press_cancel(self):
        self.app.pop_screen()


class CondaTUI(App):
    DEFAULT_CSS = 'ButtonGroup { height: 1; } Button { height: 1; } Envs { height: auto; }'
    BINDINGS = [('c', 'create', '[+ create]'), ('o', 'clone', '[◪ clone]'),
                ('i', 'import', '[→ import]'), ('e', 'export', '[↑ export]'),
                ('r', 'remove', '[× remove]')]

    def compose(self):
        """Create child widgets for the app."""
        yield Header()
        yield HorizontalGroup(
            ListView(*list(map(lambda x: ListItem(Label(x)), envs_lst)), id="lst"),
            Log(id="log", auto_scroll=False),
        )
        yield Footer()

    def on_ready(self):
        pass

    @on(ListView.Highlighted, '#lst')
    def show_pkgs(self):
        name = self.query('#lst')[0].highlighted_child.children[0].renderable
        global selection
        selection = name
        log: Log = self.query('#log')[0]
        log.clear()
        log.write_line(envs_pkgs[name])

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


if __name__ == "__main__":
    app = CondaTUI()
    app.run()
