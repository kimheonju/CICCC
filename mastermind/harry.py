from logic import *

#if it didn't rain, Harry visited Hagrid today
#Harry visited Hagrid or Dumbledore today, but not both.
#Harry visited Dumbledore today.
#Harry did not visit Hagrid today
#It rained today


rain = Symbol("rain") # it is raining
hagrid = Symbol("hagrid") #Harry visited Hagrid 
dumboledore = Symbol("dumboledore") # Harry visited Dumboledore today

knowledge = And(
    Implication(Not(rain), hagrid),
    Or(hagrid, dumboledore),
    Not(And(hagrid, dumboledore)),
    dumboledore
    )

#print(knowledge.formula())
print(model_check(knowledge, rain))