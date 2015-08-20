# -*- coding: utf-8 -*-
# pep8: disable-msg=E501
# pylint: disable=C0301

from acidentes import __version__, log
import argparse

def main():
    log.info("Acidentes-POA v" + __version__)
