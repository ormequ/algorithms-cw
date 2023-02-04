import string
from tests import *
import random


def get_all_insert_tests(key_check):
    avg_coef = 0
    rand_data = [''.join(random.choices(string.ascii_letters, k=10)) for i in range(int(1e4))]
    tests = {
        'worst': test_insert(['worst_case' for i in range(int(1e4))], 10, key_check, avg_coef=avg_coef),
        'rand': test_insert(rand_data, 10, key_check, avg_coef=avg_coef),
        'best': test_insert(get_best_rb_case(rand_data), 10, key_check, avg_coef=avg_coef, embedded_hash=True)
    }
    tests['worst']['color'] = '#E85172'
    tests['worst']['label'] = f"{key_check} insert: worst"
    tests['rand']['color'] = '#9267D1'
    tests['rand']['label'] = f"{key_check} insert: random"
    tests['best']['color'] = '#5ED167'
    tests['best']['label'] = f"{key_check} insert: best"
    return tests


def rb_insert_test():
    tests = get_all_insert_tests("RB-tree")
    plots = {
        'worst': {
            'n': tests['worst']['n'],
            'data': tests['worst']['logs']['avg']
        },
        'rand': {
            'n': tests['rand']['n'],
            'data': tests['rand']['logs']['avg']
        },
        'best': {
            'n': tests['best']['n'],
            'data': tests['best']['logs']['avg']
        },
        'sup': {
            'n': tests['worst']['n'],
            'data': tests['worst']['logs']['sup']
        },
    }
    plots['rand']['color'] = '#7700FF'
    plots['rand']['label'] = 'Average log2(n): random'
    plots['worst']['color'] = '#9E0100'
    plots['worst']['label'] = 'Average log2(n): worst'
    plots['best']['color'] = '#007826'
    plots['best']['label'] = 'Average log2(n): best'
    plots['sup']['color'] = '#000000'
    plots['sup']['label'] = 'Supremum log2(n)'

    display_tests(tests.values(), additional_plots=plots.values())


def hash_table_insert_test_full():
    tests = get_all_insert_tests("Hash-table")
    display_tests(tests.values())


def hash_table_insert_test():
    avg_coef = 3
    rand_data = [''.join(random.choices(string.ascii_letters, k=10)) for i in range(int(1e4))]
    tests = {
        'rand': test_insert(rand_data, 10, "Hash-table", avg_coef=avg_coef),
        'best': test_insert(get_best_rb_case(rand_data), 10, "Hash-table", avg_coef=avg_coef, embedded_hash=True)
    }
    tests['rand']['color'] = '#9267D1'
    tests['rand']['label'] = f"Hash-table insert: random"
    tests['best']['color'] = '#5ED167'
    tests['best']['label'] = f"Hash-table insert: best"
    display_tests(tests.values())


def hash_vs_rb_insert_test():
    avg_coef = 3
    rand_data = [''.join(random.choices(string.ascii_letters, k=10)) for i in range(int(1e4))]
    tests = get_all_insert_tests("RB-Tree")
    tests.update({
        'hash_rand': test_insert(rand_data, 10, "Hash-table", avg_coef=avg_coef),
        'hash_best': test_insert(get_best_rb_case(rand_data), 10, "Hash-table", avg_coef=avg_coef, embedded_hash=True)
    })
    tests['hash_rand']['color'] = '#1B5AC7'
    tests['hash_rand']['label'] = f"Hash-table insert: random"
    tests['hash_best']['color'] = '#56C7C0'
    tests['hash_best']['label'] = f"Hash-table insert: best"
    display_tests(tests.values())

# n >= 2 ** (bh - 1) - 1, log2(n); h
def hash_vs_rb_erase_test():
    avg_coef = 3
    rand_data = [''.join(random.choices(string.ascii_letters, k=10)) for i in range(int(1e4))]
    tests = {
        'rb': test_erase(rand_data, "RB-tree", avg_coef=avg_coef, shuffle=True),
        'hash': test_erase(rand_data, "Hash-table", avg_coef=avg_coef, shuffle=True),
    }
    tests['rb']['color'] = '#9267D1'
    tests['rb']['label'] = f"RB-tree erase: random"
    tests['hash']['color'] = '#1B5AC7'
    tests['hash']['label'] = f"Hash-table erase: random"
    plots = {
        'avg': {
            'n': tests['rb']['n'],
            'data': tests['rb']['logs']['avg']
        },
        'sup': {
            'n': tests['rb']['n'],
            'data': tests['rb']['logs']['sup']
        },
    }
    plots['avg']['color'] = '#7700FF'
    plots['avg']['label'] = 'Average log2(n): random'
    plots['sup']['color'] = '#000000'
    plots['sup']['label'] = 'Supremum log2(n)'
    display_tests(tests.values(), additional_plots=plots.values())


rb_insert_test()

