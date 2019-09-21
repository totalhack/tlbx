import inspect

import climax


Parent = climax.parent


def st():
    __import__("pdb").Pdb().set_trace(inspect.currentframe().f_back)


class Arg:
    """Decorator around climax.argument that stores arg values"""

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.climax_arg = climax.argument(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        return self.climax_arg(*args, **kwargs)

    @property
    def name(self):
        return self.args[0]


class Script:
    """Decorator for main function in a script that provides CLI parsing"""

    parents = []  # Override as list of climax.parent objects to inherit args

    def __init__(self, *script_args):
        self.func = None
        self.script_args = script_args or []

    def get_injected_kwargs(self):
        return {}

    def clean_up(self, **kwargs):
        pass

    def __call__(self, func, *args, **kwargs):
        self.func = func

        def inner(*args, **kwargs):
            kwargs.update(self.get_injected_kwargs())
            try:
                result = func(*args, **kwargs)
            finally:
                self.clean_up(**kwargs)
            return result

        for script_arg in self.script_args:
            inner = script_arg(inner)
        inner = climax.command(parents=self.parents)(inner)
        return inner


def prompt_user(msg, answers):
    answer = None
    answers = [str(x).lower() for x in answers]
    display_answers = "[%s] " % "/".join(answers)
    while (answer is None) or (answer.lower() not in answers):
        answer = input("%s %s" % (msg, display_answers))
    return answer
