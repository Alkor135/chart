import time


for i in range(1, 101):
    time.sleep(0.05)
    print("\r[ {}{} ] {}%".format(':'*i, '-'*(100-i), i), end='')
print()
