# TODO
from cs50 import get_float

count = 0
while True:
    change = get_float("Change owed: ")
    # hasta que el cambio sea valido
    if change > 0:
        break
cent = round(change * 100)  # redondea el cambio

# contar los chelines
while cent >= 25:
    cent = cent - 25
    count += 1
# contar los decimos
while cent >= 10:
    cent = cent - 10
    count += 1

# contar los centavos de a 5
while cent >= 5:
    cent = cent - 5
    count += 1

# contar los peniques
while cent >= 1:
    cent = cent - 1
    count += 1

print(count)