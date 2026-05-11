opcode_table = {
    # Compute
    "ADD": {"compute": 3, "memory": 0, "state": 0, "access": 0, "size": 0, "history": 0},
    "SUB": {"compute": 3, "memory": 0, "state": 0, "access": 0, "size": 0, "history": 0},
    "MUL": {"compute": 5, "memory": 0, "state": 0, "access": 0, "size": 0, "history": 0},
    "EXP": {"compute": 10, "memory": 0, "state": 0, "access": 0, "size": 0, "history": 0},

    # Memory
    "MLOAD": {"compute": 3, "memory": 50, "state": 0, "access": 0, "size": 0, "history": 0},
    "MSTORE": {"compute": 3, "memory": 50, "state": 0, "access": 0, "size": 0, "history": 0},
    "CALLDATACOPY": {"compute": 10, "memory": 100, "state": 0, "access": 0, "size": 0, "history": 0},

    # Access (external reads)
    "BALANCE": {"compute": 100, "memory": 0, "state": 0, "access": 2500, "size": 0, "history": 0},
    "EXTCODESIZE": {"compute": 100, "memory": 0, "state": 0, "access": 2500, "size": 0, "history": 0},

    # Storage
    "SLOAD": {"compute": 100, "memory": 0, "state": 0, "access": 2000, "size": 0, "history": 0},
    "SSTORE": {"compute": 100, "memory": 0, "state": 20000, "access": 2000, "size": 0, "history": 0},

    # Logs (History + Size)
    "LOG0": {"compute": 375, "memory": 0, "state": 0, "access": 0, "size": 8, "history": 0},
    "LOG1": {"compute": 375, "memory": 0, "state": 0, "access": 0, "size": 8, "history": 375},
    "LOG2": {"compute": 375, "memory": 0, "state": 0, "access": 0, "size": 8, "history": 750},

    # Calls
    "CALL": {"compute": 100, "memory": 50, "state": 0, "access": 2500, "size": 0, "history": 0},
    "STATICCALL": {"compute": 100, "memory": 50, "state": 0, "access": 2500, "size": 0, "history": 0},

    # Creation
    "CREATE": {"compute": 32000, "memory": 100, "state": 32000, "access": 0, "size": 0, "history": 0},

    # Misc realistic
    "KECCAK256": {"compute": 30, "memory": 50, "state": 0, "access": 0, "size": 0, "history": 0},
}

def simulate(trace):
    totals = {
        "compute": 0,
        "memory": 0,
        "state": 0,
        "access": 0,
        "size": 0,
        "history": 0
    }

    for op in trace:
        costs = opcode_table.get(op, {})

        for key in totals:
            totals[key] += costs.get(key, 0)

    return totals

def simulate_block(traces):
    totals = {
        "compute": 0,
        "memory": 0,
        "state": 0,
        "access": 0,
        "size": 0,
        "history": 0
    }

    for trace in traces:
        tx_totals = simulate(trace)
        for k in totals:
            totals[k] += tx_totals[k]
    
    return totals

def get_bottleneck(totals):
    return max(totals, key=totals.get)

def compute_percentages(totals):
    total = sum(totals.values())
    return {k: (v / total) * 100 if total > 0 else 0 for k, v in totals.items()}

# Example traces
erc20_transfer = ["SLOAD", "SLOAD", "SUB", "ADD", "SSTORE", "SSTORE", "LOG2"]

contract_call = ["CALLDATACOPY", "CALL", "MLOAD", "MSTORE", "LOG1"]

compute_heavy = ["ADD", "MUL", "ADD"] * 20
storage_heavy = ["SLOAD", "SSTORE"] * 10
memory_heavy = ["MSTORE", "MSTORE", "MLOAD", "CALLDATACOPY", "KECCAK256"] * 10
realistic_tx = ["CALLDATACOPY", "SLOAD", "SLOAD", "SUB", "ADD", "SSTORE", "SSTORE", "LOG2"]

balanced_1 = ["SSTORE", "SLOAD", "ADD", "ADD", "LOG1"]
balanced_2 = ["MSTORE", "MSTORE", "MLOAD", "KECCAK256", "CALL"]

def print_table(results):
    print("\n=== Multidimensional Gas Results ===\n")
    header = f"{'Tx Type':<20} {'Total':<10} {'Compute':<10} {'Access':<10} {'State':<10} {'Memory':<10} {'Size':<10} {'History':<10} {'Bottleneck':<10}"
    print(header)
    print("-" * len(header))

    for name, totals in results:
        total = sum(totals.values())
        bottleneck = get_bottleneck(totals)

        print(f"{name:<20} {total:<10} {totals['compute']:<10} {totals['access']:<10} {totals['state']:<10} {totals['memory']:<10} {totals['size']:<10} {totals['history']:<10} {bottleneck:<10}")

results = []

for name, trace in [
    ("ERC20 Transfer", erc20_transfer),
    ("Compute Heavy", compute_heavy),
    ("Storage Heavy", storage_heavy),
    ("Contract Call", contract_call),
    ("Memory Heavy", memory_heavy),
    ("Balanced State", balanced_1),
    ("Balanced Memory", balanced_2),
    ("Realistic Tx", realistic_tx),
]:
    totals = simulate(trace)
    results.append((name, totals))

print_table(results)

block = [
    erc20_transfer,
    realistic_tx,
    compute_heavy,
    contract_call,
    memory_heavy
]

block_totals = simulate_block(block)

print("\n=== Block Simulation ===\n")
print("Block totals:", block_totals)
print("Block bottleneck:", get_bottleneck(block_totals))

# 👇 OPTIONAL
print("\n=== Percentage Breakdown (ERC20) ===\n")
erc20_totals = simulate(erc20_transfer)
percentages = compute_percentages(erc20_totals)

for k, v in percentages.items():
    print(f"{k}: {v:.2f}%")