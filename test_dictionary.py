from app.core.dictionary_simulator import DictionaryAttackSimulator

simulator = DictionaryAttackSimulator("sample_wordlist.txt")

result = simulator.simulate_dictionary_attack("MyP@ss123")

print(result)
