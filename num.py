
def countDigit(n):
    count = 0
    while n != 0:
        n //= 10
        count += 1
    return count

def averaGe(avg, amount):
    total = avg + amount
    possibility = total / 2

    return possibility