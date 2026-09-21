def grams_to_ounces(grams):
    ounces = 28.3495231 * grams
    return ounces


grams = float(input("Enter grams: "))
print("Ounces:", grams_to_ounces(grams))


F = float(input("Enter Fahrenheit: "))

C = (5 / 9) * (F - 32)

print("Centigrade:", C)



def solve(numheads, numlegs):
    rabbits = (numlegs - 2 * numheads) // 2
    chickens = numheads - rabbits

    return chickens, rabbits


chickens, rabbits = solve(35, 94)

print("Chickens:", chickens)
print("Rabbits:", rabbits)


def filter_prime(numbers):
    result = []

    for num in numbers:
        if num < 2:
            continue

        prime = True

        for i in range(2, num):
            if num % i == 0:
                prime = False
                break

        if prime:
            result.append(num)

    return result


numbers = list(map(int, input("Enter numbers: ").split()))

print(filter_prime(numbers))


from itertools import permutations

def print_permutations():
    text = input("Enter a string: ")

    for p in permutations(text):
        print("".join(p))


print_permutations()