from pomegranate import *

from collections import Counter

from model import model


def generate_weighted_sample(evidence):
    sample = {}
    parents = {}
    weight = 1.0
    
    for state in model.states:
        if state.name in evidence:
            sample[state.name] = evidence[state.name]
            # Calculate the weight based on the evidence probability
            if isinstance(state.distribution, DiscreteDistribution):
                weight *= state.distribution.probability(evidence[state.name])
            elif isinstance(state.distribution, ConditionalProbabilityTable):
                parent_values = [sample[parent.name] for parent in model.parents(state)]
                weight *= state.distribution.probability(parent_values + [evidence[state.name]])
        else:
            if isinstance(state.distribution, ConditionalProbabilityTable):
                sample[state.name] = state.distribution.sample(parent_values=parents)
            else:
                sample[state.name] = state.distribution.sample()
        
        parents[state.distribution] = sample[state.name]
    
    return sample, weight

# Likelihood weighting
# Compute distribution of Work Productivity given that weather is cloudy
N = 10000 # Number of samples to generate
data = []
weights = []
evidence = {"weather": "sunny"}

for _ in range(N):
    sample, weight = generate_weighted_sample(evidence)
    data.append((sample["meetingattendance"], weight))

# Aggregate the results by considering the weights
weighted_counts = Counter()
for outcome, weight in data:
    weighted_counts[outcome] += weight

# 결과 출력
print(weighted_counts)