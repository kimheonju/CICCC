
from logic import *

# Define a list of colors

colors = ["red", "blue", "yellow", "green"]

# Initialize an empty list for symbols
symbols = []

# Generate symbols for each color and position (0-3)
for color in colors:
    for position in range(4):
        symbols.append(Symbol(f"{color}{position}"))

# Initialize an empty knowledge base
knowledge = And()

# Add the rule: Each color has a position.


for color in colors:
    knowledge.add(Or(
        Symbol(f"{color}0"),
        Symbol(f"{color}1"),
        Symbol(f"{color}2"),
        Symbol(f"{color}3")
    ))




# Add the rule: Only one position per color.
for color in colors:
    for h1 in range(4):
        for h2 in range(4):
            if h1 != h2:
                knowledge.add(
                    Implication(Symbol(f"{color}{h1}"), Not(Symbol(f"{color}{h2}"))))






# Add the rule: Only one color per position.
for position in range(4):
    for p1 in colors:
        for p2 in colors:
            if p1 != p2:
                knowledge.add(
                    Implication(Symbol(f"{p1}{position}"), Not(Symbol(f"{p2}{position}"))))









# Add specific constraints based on the problem requirements

    # Constraint: red is in position 0, blue is in position 1, green is not in position 2, yellow is not in position 3
knowledge.add(Or(
    And(Symbol("red0"), Symbol("blue1"), Not(Symbol("green2")), Not(Symbol("yellow3"))),
    And(Symbol("red0"), Symbol("green2"), Not(Symbol("blue1")), Not(Symbol("yellow3"))),
    And(Symbol("red0"), Symbol("yellow3"), Not(Symbol("blue1")), Not(Symbol("green2"))),
    And(Symbol("blue1"), Symbol("green2"), Not(Symbol("red0")), Not(Symbol("yellow3"))),
    And(Symbol("blue1"), Symbol("yellow3"), Not(Symbol("red0")), Not(Symbol("green2"))),
    And(Symbol("green2"), Symbol("yellow3"), Not(Symbol("red0")), Not(Symbol("blue1")))
))


# Add specific constraints to exclude certain symbols
    # Constraint: blue is not in position 0
knowledge.add(And(
    Not(Symbol("blue0")),
    Not(Symbol("red1")),
    Not(Symbol("green2")),
    Not(Symbol("yellow3"))

))

# Check the model for each symbol and print the valid symbols
for symbol in symbols:
    if model_check(knowledge, symbol):
        print(symbol)

#print(knowledge.formula())