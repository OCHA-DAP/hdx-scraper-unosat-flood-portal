#!/usr/bin/python
# -*- coding: utf-8 -*-

from termcolor import colored as color


def item(i):
  dictionary = {
    'prompt_bullet': color(" →", "blue", attrs=['bold']),
    'prompt_error':  color(" ERROR:", "red", attrs=['bold']),
    'prompt_success': color(" SUCCESS:", "green", attrs=['bold']),
    'prompt_warn': color(" WARN:", "yellow", attrs=['bold'])
  }

  return dictionary[i].decode('utf-8')


if __name__ == '__main__':
  item()
