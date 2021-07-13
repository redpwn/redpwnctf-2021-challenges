from pwn import *


def solve_palindromes():
    transition = {
        'start': {
            '0': ('#', 'R', 'right-0'),
            '1': ('#', 'R', 'right-1'),
            '#': ('#', '#', 'accept')
        },
        'right-0': {
            '0': ('0', 'R', 'right-0'),
            '1': ('1', 'R', 'right-0'),
            '#': ('#', 'L', 'check-0'),
        },
        'right-1': {
            '0': ('0', 'R', 'right-1'),
            '1': ('1', 'R', 'right-1'),
            '#': ('#', 'L', 'check-1'),
        },
        'check-0': {
            '0': ('#', 'L', 'left'),
            '1': ('#', '#', 'reject'),
            '#': ('#', '#', 'accept'),
        },
        'check-1': {
            '0': ('#', '#', 'reject'),
            '1': ('#', 'L', 'left'),
            '#': ('#', '#', 'accept'),
        },
        'left': {
            '0': ('0', 'L', 'left'),
            '1': ('1', 'L', 'left'),
            '#': ('#', 'R', 'start')
        },
        'reject': {
            '0': ('#', 'L', 'reject'),
            '1': ('#', 'L', 'reject'),
            '#': ('#', 'L', 'reject')
        }
    }

    substitutions = []
    # first, set up the tape
    substitutions += [('$', '#')]
    for c in ['0', '1']:
        substitutions += [(f'^{c}', f'#[{c}]start')]
    for state in transition:
        for tape_symbol in transition[state]:
            write, move, target = transition[state][tape_symbol]
            if move == '#':
                substitutions += [(
                    f'[{tape_symbol}]{state}',
                    f'[{write}]{target}'
                )]
                continue
            for symbol in ['0', '1', '#']:
                if move == 'R':
                    substitutions += [(
                        f'[{tape_symbol}]{state}{symbol}',
                        f'{write}[{symbol}]{target}'
                    )]
                if move == 'L':
                    substitutions += [(
                        f'{symbol}[{tape_symbol}]{state}',
                        f'[{symbol}]{target}{write}'
                    )]
    substitutions += [('[#]accept', 'palindrome')]
    substitutions += [('[#]reject', 'not_palindrome')]

    # eat up #s around 'palindrome' and 'not_palindrome'
    substitutions += [('#palindrome', 'palindrome')]
    substitutions += [('#not_palindrome', 'not_palindrome')]
    substitutions += [('palindrome#', 'palindrome')]
    substitutions += [('not_palindrome#', 'not_palindrome')]

    return substitutions


def solve_addition():
    transition = {
        'start': {
            '0': ('0', 'R', 'start'),
            '1': ('1', 'R', 'start'),
            '#': ('#', 'R', 'start'),
            '+': ('+', 'L', 'first_read')
        },
        'first_read': {
            '0': ('+', 'R', 'find_second_zero'),
            '1': ('+', 'R', 'find_second_one'),
            '#': ('#', 'R', 'find_second_zero')
        },
        'find_second_zero': {
            '0': ('0', 'R', 'find_second_zero'),
            '1': ('1', 'R', 'find_second_zero'),
            '+': ('+', 'R', 'find_second_zero'),
            '=': ('=', 'L', 'second_read_zero')
        },
        'find_second_one': {
            '0': ('0', 'R', 'find_second_one'),
            '1': ('1', 'R', 'find_second_one'),
            '+': ('+', 'R', 'find_second_one'),
            '=': ('=', 'L', 'second_read_one')
        },
        'second_read_zero': {
            '0': ('=', 'R', 'find_carry_zero'),
            '1': ('=', 'R', 'find_carry_one'),
            '+': ('+', 'R', 'find_carry_zero')
        },
        'second_read_one': {
            '0': ('=', 'R', 'find_carry_one'),
            '1': ('=', 'R', 'find_carry_carry'),
            '+': ('+', 'R', 'find_carry_one')
        },
        'find_carry_zero': {
            '0': ('0', 'R', 'find_carry_zero'),
            '1': ('1', 'R', 'find_carry_zero'),
            '=': ('=', 'R', 'find_carry_zero'),
            '#': ('#', 'L', 'check_zero'),
            'C': ('#', 'L', 'check_one')
        },
        'find_carry_one': {
            '0': ('0', 'R', 'find_carry_one'),
            '1': ('1', 'R', 'find_carry_one'),
            '=': ('=', 'R', 'find_carry_one'),
            '#': ('#', 'L', 'check_one'),
            'C': ('#', 'L', 'check_carry_zero')
        },
        'find_carry_carry': {
            '0': ('0', 'R', 'find_carry_carry'),
            '1': ('1', 'R', 'find_carry_carry'),
            '=': ('=', 'R', 'find_carry_carry'),
            '#': ('#', 'L', 'check_carry_zero'),
            'C': ('#', 'L', 'check_carry_one')
        },
        'check_zero': {
            '0': ('#', 'L', 'find_start'),
            '1': ('#', '#', 'reject'),
            '=': ('#', 'L', 'check_accept')
        },
        'check_one': {
            '0': ('#', '#', 'reject'),
            '1': ('#', 'L', 'find_start'),
            '=': ('#', 'L', 'reject')
        },
        'check_carry_zero': {
            '0': ('C', 'L', 'find_start'),
            '1': ('#', '#', 'reject'),
            '=': ('#', 'L', 'check_accept')
        },
        'check_carry_one': {
            '0': ('#', '#', 'reject'),
            '1': ('C', 'L', 'find_start'),
            '=': ('#', '#', 'reject')
        },
        'find_start': {
            '0': ('0', 'L', 'find_start'),
            '1': ('1', 'L', 'find_start'),
            '+': ('+', 'L', 'find_start'),
            '=': ('=', 'L', 'find_start'),
            '#': ('#', 'R', 'start')
        },
        'check_accept': {
            '0': ('0', 'L', 'check_accept'),
            '1': ('#', '#', 'reject'),
            '+': ('+', 'L', 'check_accept'),
            '=': ('=', 'L', 'check_accept'),
            '#': ('#', '#', 'accept')
        },
        'reject': {
            '=': ('#', '#', 'reject')
        }
    }

    symbols = ['0', '1', '+', '=', '#', 'C']
    substitutions = []
    # first, set up the tape
    substitutions += [('$', '#')]
    for c in ['0', '1']:
        substitutions += [(f'^{c}', f'#[{c}]start')]
    for state in transition:
        for tape_symbol in transition[state]:
            write, move, target = transition[state][tape_symbol]
            if move == '#':
                substitutions += [(
                    f'[{tape_symbol}]{state}',
                    f'[{write}]{target}'
                )]
                continue
            for symbol in symbols:
                if move == 'R':
                    substitutions += [(
                        f'[{tape_symbol}]{state}{symbol}',
                        f'{write}[{symbol}]{target}'
                    )]
                if move == 'L':
                    if symbol not in transition[target]:
                        continue
                    substitutions += [(
                        f'{symbol}[{tape_symbol}]{state}',
                        f'[{symbol}]{target}{write}'
                    )]

    for symbol in ['0', '1', '+', '=', '#']:
        substitutions += [(f'{symbol}[#]reject', '[#]reject')]
        substitutions += [(f'{symbol}[#]accept', '[#]accept')]
        substitutions += [(f'[#]reject{symbol}', '[#]reject')]
        substitutions += [(f'[#]accept{symbol}', '[#]accept')]

    substitutions += [('[#]accept', 'correct')]
    substitutions += [('[#]reject', 'incorrect')]

    return substitutions


def main():
    context.log_level = 'debug'
    # r = remote('mc.ax', 31996)
    r = remote('localhost', 5000)

    solutions = [
        [('initial', 'target')],
        [('hello', 'goodbye'), ('ginkoid', 'ginky')],
        [('aa', 'a')],
        [('ggg', 'gg'), ('gg', 'ginkoid')],
        solve_palindromes(),
        solve_addition()
    ]

    for solution in solutions:
        r.recvuntil('(y/n) ')
        r.sendline('y')
        r.recvuntil('---\n')
        r.recvuntil('---\n')
        for i, substitution in enumerate(solution):
            if i > 0:
                r.recvuntil('(y/n) ')
                r.sendline('y')
            r.recvuntil(': ')
            r.sendline(' => '.join(substitution))
        r.recvuntil('(y/n) ')
        r.sendline('n')

    r.interactive()

main()
