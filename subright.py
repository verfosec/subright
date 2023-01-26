#!/usr/bin/env python3

"""🆂🆄🅱🆁🅸🅶🅷🆃
version: v0.1.0
author: Verfosec
contact me: verfosec@gmail.com
"""

import argparse
import sys
from colorama import Fore as colorize

import search_engines


def arguments_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--domain',
                        help="Domain name to enumerate it's subdomains")
    parser.add_argument('-i', '--input-file',
                        help="Domains name file")
    parser.add_argument('-o', '--output', help='Save the results to text file')
    parser.add_argument('-s', '--silent', help='Silent mode(default=False)',
                        default=False, action='store_true')

    args = parser.parse_args()

    input_methods = [args.domain is not None,
                     args.input_file is not None,
                     not sys.stdin.isatty()]

    if not any(input_methods):
        print(
            colorize.RED + "[-]",
            colorize.LIGHTRED_EX + "No input provided. Use -d or -i or stdin."
        )
        sys.exit(1)

    elif sum(input_methods) > 1:
        print(
            colorize.RED + "[-]",
            colorize.LIGHTRED_EX + "Use only one input."
        )
        sys.exit(1)

    return args


def banner():
    if args.silent:
        return None

    print(colorize.LIGHTMAGENTA_EX + """
            _          _       _     _
           | |        (_)     | |   | |
  ___ _   _| |__  _ __ _  __ _| |__ | |_
 / __| | | | '_ \\| '__| |/ _` | '_ \\| __|
 \\__ \\ |_| | |_) | |  | | (_| | | | | |_
 |___/\\__,_|_.__/|_|  |_|\\__, |_| |_|\\__|
                          __/ |
                         |___/  v1.0

        Made with ❤ by Verfosec
    """)


def main():
    domain = args.domain
    input_file = args.input_file
    output = args.output
    silent = args.silent

    subdomains = []

    if domain:
        subdomains += search_engines.google_enumerator(domain, silent)
    else:
        domains = []
        with open(input_file, 'r') as file:
            domains = file.read().splitlines()

        for domain in domains:
            subdomains += search_engines.google_enumerator(domain, silent)

    if output:
        with open(output, 'w') as output_file:
            output_file.write(subdomains)
    else:
        for subdomain in subdomains:
            print(subdomain)


if __name__ == '__main__':
    global args
    args = arguments_parser()
    main()
