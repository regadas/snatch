#!/usr/bin/env python
"""
The main entry point.
"""
import logging
from cli import parser, prompt_values
from core import logger, GitSnatch
from github import Github


if __name__ == '__main__':
    args = parser.parse_args()

    if args.verbose:
        logger.setLevel(logging.INFO)

    pyer = Github(args.repo)
    pyer.clone()
    pyer.load_properties()
    pyer.properties = prompt_values(pyer.properties)
    pyer.generate_in(args.dst)
