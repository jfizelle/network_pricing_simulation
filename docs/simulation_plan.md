# Network Pricing: Simulation Development Plan

## Objectives
Estimate the affect of an opt-in network pricing model on elasticity of demand, electricity prices (customer bills),
the systems peak demand, grid expansion costs, fairness between customer groups and revenue outcomes for network companies. 

## Assumptions
- load profile diversity
- tariffs and price caps
- opt-in rules

Parameters to be stored in YAML config files

## Data 
Optimal: incorporates a realistic mix of customer load profiles eg. high and low demand users, financially vulnerable users,
ev owners and businesses. 
Sources may include a combination of publicly available data sets (AEMO, AER, CER, Ausgrid) and synthetic data.  

Available:

## Model
Load shifting behavior to be simulated using demand elasticity (usage reduction) and shift elasticity (change of usage time).

## Tariff Scenarios
The simulation will compare existing tariffs with new pricing designs. A Baseline scenario includes a flat tariff and a TOU
tariff. New designs include inverse capacity factor TOU, capped peak and weather dependent tariffs. 

Tariffs to be stored in YAML config files. 

## Equity Analysis
## Revenue Sufficiency 

## Parameter Testing
To ensure reliable results the simulation will test how outcomes change when important factors are varied eg. high vs low
shift elasticity, high vs low opt-in participants, ev and home battery uptake projections and increased weather events.
Additionally, it will test different customer types and price caps. By testing the model with a range of realistic parameter 
variations, we can make sure the proposed pricing approach remains effective under many different future scenarios.

## Outputs
