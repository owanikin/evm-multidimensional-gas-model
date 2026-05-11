# evm-multidimensional-gas-model
EVM Multidimensional Gas Model Experiments.

Experimental tooling and simulations exploring multidimensional gas metering and execution-layer resource pricing for Ethereum. Inspired by ongoing discussions around EIP-8011 and multidimensional fee markets.

# motivation
- current gas model compresses heterogeneous resources into one scalar
- different opcodes stress different bottlenecks
- want to empirically explore resource splits and pricing

# resource dimensions
| Dimension | Meaning                        |
| --------- | ------------------------------ |
| Compute   | CPU/execution work             |
| State     | Persistent state growth/writes |
| Access    | Trie/database reads            |
| Memory    | Transient memory expansion     |
| Size      | Calldata / tx size             |
| History   | Historical witness burden      |

# opcode mapping
You can find more detailed mapping in this [sheets](https://docs.google.com/spreadsheets/d/19dYtW3VOpYNHMpoU1lUXDACCLZ5Ex4xWUgVrWugh2w4/edit?usp=sharing).

Summarized:
| Opcode       | Compute | State     | Access |
| ------------ | ------- | --------- | ------ |
| SSTORE       | low     | very high | medium |
| SLOAD        | low     | none      | high   |
| CALLDATACOPY | medium  | none      | medium |


# example simulation output
Initial experiments show that standard ERC20 transfers are overwhelmingly dominated by persistent state writes (~81%), while computation itself accounts for less than 2% of resource consumption.

This suggests the current scalar gas model may obscure the true resource bottlenecks affecting Ethereum nodes.

<img width="861" height="459" alt="Screenshot 2026-05-08 at 13 38 58" src="https://github.com/user-attachments/assets/10555cc4-67e1-4b7b-ae11-b1135325afb0" />

# open questions
- What is the right resource split and limits?
- What about non-othorgonal resources?
- How much worse do base fee manipulations get, and are there other attacks?
- How can block builders deal with the added complexity of picking the optimal set of transactions to include?
- What are the price elasticities of the various resources?
- What is the impact of multidimensional metering and pricing on state growth and throughput?
- What other fee constructions could we use for persistent resources?
