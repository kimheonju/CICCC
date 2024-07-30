# from pomegranate import Node, DiscreteDistribution, ConditionalProbabilityTable, BayesianNetwork
from pomegranate import *

class Node:
    def __init__(self, distribution, name):
        self.distribution = distribution
        self.name = name


# Rain node has no parents
weather = Node(DiscreteDistribution({
    "sunny": 0.6,
    "cloudy": 0.3,
    "stormy": 0.1
}), name="weather")

# Track maintenance node is conditional on rain
poweroutage = Node(ConditionalProbabilityTable([
    ["sunny", "yes", 0.05],
    ["sunny", "no", 0.95],
    ["cloudy", "yes", 0.1],
    ["cloudy", "no", 0.9],
    ["stormy", "yes", 0.4],
    ["stormy", "no", 0.6]
], [weather.distribution]), name="poweroutage")

# Train node is conditional on rain and maintenance
internetconnectivity = Node(ConditionalProbabilityTable([
    ["yes", "connected", 0.2],
    ["yes", "disconnected", 0.8],
    ["no", "connected", 0.9],
    ["no", "disconnected", 0.1]
], [poweroutage.distribution]), name="internetconnectivity")

# Appointment node is conditional on train
workproductivity = Node(ConditionalProbabilityTable([
    ["connected", "high", 0.8],
    ["connected", "low", 0.2],
    ["disconnected", "high", 0.3],
    ["disconnected", "low", 0.7]
], [internetconnectivity.distribution]), name="workproductivity")

meetingattendance = Node(ConditionalProbabilityTable([
    ["high", "attend", 0.9],
    ["high", "miss", 0.1],
    ["low", "attend", 0.6],
    ["low", "miss", 0.4]
], [workproductivity.distribution]), name="meetingattendance")

# Create a Bayesian Network and add states
model = BayesianNetwork()
model.add_states(weather, poweroutage, internetconnectivity, workproductivity, meetingattendance)

# Add edges connecting nodes
model.add_edge(weather, poweroutage)
model.add_edge(poweroutage, internetconnectivity)
model.add_edge(internetconnectivity, workproductivity)
model.add_edge(workproductivity, meetingattendance)

# Finalize model
model.bake()