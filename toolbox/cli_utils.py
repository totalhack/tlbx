import inspect

import climax

def st():
    import pdb
    pdb.Pdb().set_trace(inspect.currentframe().f_back)

@climax.parent()
@climax.argument('--dry_run', action='store_true')
@climax.argument('--force', action='store_true')
def cli():
    pass

@climax.parent()
@climax.argument('--debug', action='store_true')
def testcli():
    pass

def prompt_user(msg, answers):
    answer = None
    answers = [str(x).lower() for x in answers]
    display_answers = '[%s] ' % '/'.join(answers)
    while (answer is None) or (answer.lower() not in answers):
        answer = input('%s %s' % (msg, display_answers))
    return answer
