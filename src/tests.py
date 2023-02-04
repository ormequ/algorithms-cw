import gc
import random
import time
from math import log2
import matplotlib.pyplot as plt
import HashFunction
from HashTable import HashTable
from RBTree import RBTree


def test_insert(data, tests_quantity, struct_name, avg_coef=0, embedded_hash=False):
    times = [0 for _ in range(len(data))]
    for i in range(tests_quantity):
        if struct_name == "Hash-table":
            hash_first = HashFunction.embedded_hash if embedded_hash else HashFunction.horner_first
            hash_second = HashFunction.embedded_hash if embedded_hash else HashFunction.horner_second
            struct = HashTable(hash_first, hash_second, buffer=2**20, repeat_keys=True)
        else:
            struct = RBTree(repeat_keys=True)
        for j in range(len(data)):
            gc.disable()
            start = time.perf_counter_ns()
            struct.insert(data[j])
            times[j] += (time.perf_counter_ns() - start) // tests_quantity
            gc.enable()
        del struct
    avg = sum(times) / len(times)
    logs = {
        'avg': [],
        'sup': []
    }
    log_coefs = []
    res_times = []
    res_n = []
    for i in range(len(times)):
        if avg_coef <= 0 or times[i] / avg < avg_coef:
            res_n.append(i)
            res_times.append(times[i])
            lg = log2(i) if i > 1 else 0
            if lg > 1:
                log_coefs.append(times[i] / lg)

    max_log_coef = max(log_coefs)
    avg_log_coef = sum(log_coefs) / len(log_coefs)
    for i in res_n:
        lg = log2(i) if i > 1 else 0
        logs['avg'].append(avg_log_coef * lg)
        logs['sup'].append(max_log_coef * lg)
    return {
        'times': res_times,
        'n': res_n,
        'logs': logs
    }


def get_best_rb_case(data):
    tree = RBTree(repeat_keys=True)
    for i in range(len(data)):
        tree.insert(data[i])
    que = [tree.root]
    res = [tree.root.key]
    while que:
        tmp_que = []
        for el in que:
            if el.left_child and id(el.left_child) != id(tree.nil):
                res.append(el.left_child.key)
                tmp_que.append(el.left_child)
            if el.right_child and id(el.right_child) != id(tree.nil):
                res.append(el.right_child.key)
                tmp_que.append(el.right_child)
        que = tmp_que
    return res


def display_tests(tests, additional_plots=[]):
    fig, ax = plt.subplots()
    for test in tests:
        ax.scatter(test['n'], test['times'], s=0.5, color=test['color'], label=test['label'])
    for plot in additional_plots:
        ax.plot(plot['n'], plot['data'], color=plot['color'], label=plot['label'])
    ax.set_ylim(0)
    ax.set(xlabel='Quantity (n)', ylabel='Time (ns)', title=f"Time test")
    ax.grid()
    ax.legend(loc=2)
    plt.show()


def test_erase(data, struct_name, avg_coef=0, shuffle=False, embedded_hash=False):
    times = [0 for _ in range(len(data))]
    if struct_name == "Hash-table":
        hash_first = HashFunction.embedded_hash if embedded_hash else HashFunction.horner_first
        hash_second = HashFunction.embedded_hash if embedded_hash else HashFunction.horner_second
        struct = HashTable(hash_first, hash_second, buffer=2**20, repeat_keys=True)
    else:
        struct = RBTree(repeat_keys=True)
    for j in range(len(data)):
        struct.insert(data[j])
    if shuffle:
        random.shuffle(data)
    for j in range(len(data)):
        gc.disable()
        start = time.perf_counter_ns()
        struct.erase(data[j])
        times[-j] = time.perf_counter_ns() - start
        gc.enable()
    del struct
    avg = sum(times) / len(times)
    logs = {
        'avg': [],
        'sup': []
    }
    log_coefs = []
    res_times = []
    res_n = []
    for i in range(len(times)):
        if avg_coef <= 0 or times[i] / avg < avg_coef:
            res_n.append(i)
            res_times.append(times[i])
            lg = log2(i) if i > 1 else 0
            if lg > 1:
                log_coefs.append(times[i] / lg)

    max_log_coef = max(log_coefs)
    avg_log_coef = sum(log_coefs) / len(log_coefs)
    for i in res_n:
        lg = log2(i) if i > 1 else 0
        logs['avg'].append(avg_log_coef * lg)
        logs['sup'].append(max_log_coef * lg)
    return {
        'times': res_times,
        'n': res_n,
        'logs': logs
    }
