#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

from clipboard import copy as pbcopy
from click import command, argument, option, echo
from inquirer import Checkbox, Text, prompt

from yaml import load as yaml_load
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader


def get_tags():
    tags = []
    for role in playbook[0]['roles']:
        if 'tags' not in role:
            continue
        for tag in role['tags']:
            if tag not in tags:
                tags.append(tag)

    return tags


def get_vars(tags):
    extra_vars = []
    passwords = []
    for role in playbook[0]['roles']:
        if 'vars' not in role:
            continue

        if any((tag in role['tags'] for tag in tags)):
            extra_vars.extend(role['vars'])
            if 'pass' in role:
                passwords.extend(role['pass'])

    return extra_vars, passwords


def gen_pass(length=10, digits=2):
    import string
    from time import time
    from itertools import chain
    from random import seed, choice, sample

    seed(time())
    lowercase = string.lowercase.translate(None, 'lo')
    uppercase = string.uppercase.translate(None, 'IO')
    letters = lowercase + uppercase
    password = list(
        chain(
            (choice(string.digits) for _ in range(digits)),
            (choice(letters) for _ in range(length - digits))
        )
    )

    return ''.join(sample(password, len(password)))


@command()
@argument('host')
@option('--user', '-u', default=None)
@option('--password', '-p', default=False, is_flag=True)
def main(host, user, password):
    questions = [
        Checkbox('tags', message='Tags', choices=get_tags())
    ]
    tags = prompt(questions)['tags']
    questions = []
    extra_vars, passwords = get_vars(tags)
    for var in extra_vars:
        questions.append(Text(var, var))
    extra_vars = prompt(questions)
    for item in passwords:
        extra_vars[item] = gen_pass()

    command = [
        'ansible-playbook',
        '-i %s,' % host,
        '-t %s' % ','.join(tags)
    ]
    if extra_vars:
        command.append('-e "%s"'
                       % ' '.join(('%s=%s' % (k, v)
                                  for k, v in extra_vars.items())))
    if user is not None:
        command.append('-u %s' % user)

    if password:
        command.append('-k')

    command.append('ansible.yml')
    res = ' '.join(command)
    pbcopy(res)
    echo('The follow command has been copied to clipboard:')
    echo(res)


if __name__ == '__main__':
    playbook_yaml = open('ansible.yml')
    playbook = yaml_load(playbook_yaml, Loader=Loader)
    main()
