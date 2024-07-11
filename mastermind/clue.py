from logic import *
import termcolor

mustard = Symbol("ColMustard") 
plum = Symbol("ProfPlum") 
scarlet = Symbol("MsScarlet")
chracters = [mustard, plum, scarlet]

ballroom = Symbol("ballroom")
kitchen = Symbol("kitchen")
library = Symbol("library")
rooms = [ballroom, kitchen, library]

knife = Symbol("knife")
revolver = Symbol("revolver")
wrench = Symbol("wrench")
weapons = [knife, revolver, wrench]

symbols = chracters + rooms + weapons

def check_knowledge(knowledge):
    for symbol in symbols:
        if model_check(knowledge, symbol): # If there is an entailment (if True)
            termcolor.cprint(f"{symbol}: YES", "green") 
        elif not model_check(knowledge, Not(symbol)): # If "not symbol" is false
            termcolor.cprint(f"{symbol}: MAYBE", "yellow")

#implement the assumptions from the game

# your initial cards:
# it's not Col. Mustard
# it's not Col. kitchen
# it's not Col. revolver
# Someone guesses Miss Scarlet in the library with the wrench. 
# And we know that that card was revealed, which means that one of those three cards at minimum, 
# must not be inside of the envelope.
# someone shows Pr. Plum card
# someone shows ballroom card

Knowledge = And(
    Or(mustard, plum, scarlet),
    Or(ballroom, kitchen, library),
    Or(knife, wrench, revolver),
    )

Knowledge.add(Not(mustard))
Knowledge.add(Not(revolver))
Knowledge.add(Not(kitchen))

Knowledge.add(Or(Not(scarlet),Not(wrench),Not(library)))

Knowledge.add(Not(plum))
Knowledge.add(Not(ballroom))

#print(Knowledge.formula())
check_knowledge(Knowledge)