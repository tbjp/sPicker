import random

def test_fairness():
    students = ["Alice", "Bob", "Charlie", "David"]
    pick_counts = {"Alice": 0, "Bob": 0, "Charlie": 0, "David": 0}

    # Simulate picking students across multiple rounds (restarts)
    for round_num in range(100):
        unpicked = students.copy()
        while unpicked:
            # Simple simulation of the weighted selection logic
            weights = [1.0 / (1.0 + pick_counts[s]) for s in unpicked]
            picked = random.choices(unpicked, weights=weights, k=1)[0]
            unpicked.remove(picked)
            pick_counts[picked] += 1

    print("Final pick counts after 100 rounds of picking everyone:")
    for s, count in pick_counts.items():
        print(f"{s}: {count}")

    # In this simulation, since everyone is picked in every round,
    # the counts should be exactly equal (100 each).
    # The real test is the distribution WITHIN a round after some bias is introduced.

    print("\nSimulating bias: Alice has been picked 5 times, others 0 times.")
    pick_counts = {"Alice": 5, "Bob": 0, "Charlie": 0, "David": 0}
    results = {"Alice": 0, "Bob": 0, "Charlie": 0, "David": 0}

    for _ in range(10000):
        weights = [1.0 / (1.0 + pick_counts[s]) for s in students]
        picked = random.choices(students, weights=weights, k=1)[0]
        results[picked] += 1

    print("Results after 10,000 picks with initial bias:")
    for s, count in results.items():
        percentage = (count / 10000) * 100
        print(f"{s}: {count} ({percentage:.2f}%)")

    expected_alice_weight = 1.0 / 6.0
    expected_others_weight = 1.0 / 1.0
    total_expected_weight = expected_alice_weight + 3 * expected_others_weight
    expected_alice_percent = (expected_alice_weight / total_expected_weight) * 100
    print(f"\nExpected Alice %: {expected_alice_percent:.2f}%")

if __name__ == "__main__":
    test_fairness()
