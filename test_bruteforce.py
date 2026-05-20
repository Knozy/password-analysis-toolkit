from app.core.brute_force_simulator import BruteForceSimulator

simulator = BruteForceSimulator()

result = simulator.simulate_brute_force(
    "MyP@ss123",
    attack_type='gpu'
)

print(result)
