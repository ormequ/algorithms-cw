def horner(s, table_size, key):
    s = str(s)
    hash_res = 0
    for i in range(len(s)):
        hash_res = (key * hash_res + ord(s[i])) % table_size
    return (hash_res * 2 + 1) % table_size


def horner_first(s, table_size):
    return horner(s, table_size, 333667)


def horner_second(s, table_size):
    return horner(s, table_size, 426389)


def embedded_hash(s, table_size):
    return (hash(s) * 2 + 1) % table_size
