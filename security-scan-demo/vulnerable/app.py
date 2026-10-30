# Deliberately vulnerable sample for the security scan demo. Do not deploy.
# settings.py next to this file holds intentionally FAKE credentials so the secret scan has
# something to find.
import subprocess
import yaml


def run(cmd):
    return subprocess.call(cmd, shell=True)


def load(s):
    return yaml.load(s)


def calc(expr):
    return eval(expr)
