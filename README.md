# Simple Assembler and Simulator

## Overview

This project includes a simple assembler (`SimpleAssembler.py`) and a simulator (`SimpleSimulator.py`) for a basic instruction set architecture (ISA). The assembler translates assembly code into machine code, while the simulator executes the machine code and visualizes memory and register states.

## Features

- **Assembler**
  - Parses and validates assembly instructions
  - Converts assembly into binary machine code
  - Ensures correct syntax and error handling
- **Simulator**
  - Loads machine code into memory
  - Executes instructions according to the ISA
  - Implements arithmetic, logical, and memory operations
  - Provides real-time visualization of registers and memory access

## File Descriptions

### 1. `SimpleAssembler.py`

- Reads assembly instructions from standard input
- Checks for syntax errors and unsupported instructions
- Converts assembly code into binary instructions
- Outputs the binary machine code

### 2. `SimpleSimulator.py`

- Reads machine code from standard input
- Simulates execution based on predefined instruction formats
- Supports different instruction types (e.g., arithmetic, logical, memory, and control flow operations)
- Prints register states after each instruction execution
- Visualizes execution flow using `matplotlib`

## Usage

### Running the Assembler

To assemble an assembly program:

```sh
python3 SimpleAssembler.py < input.asm > output.mc
```

- `input.asm`: Assembly code file
- `output.mc`: Generated machine code

### Running the Simulator

To simulate the machine code:

```sh
python3 SimpleSimulator.py < output.mc
```

This will execute the instructions and print register states at each step.

## Instruction Set

The assembler and simulator support the following instruction types:

| Instruction | Type | Description                      |
| ----------- | ---- | -------------------------------- |
| `add`       | A    | Add two registers                |
| `sub`       | A    | Subtract two registers           |
| `mov`       | B, C | Move immediate or register value |
| `ld`        | D    | Load value from memory           |
| `st`        | D    | Store value to memory            |
| `mul`       | A    | Multiply two registers           |
| `div`       | C    | Divide two registers             |
| `rs`        | B    | Right shift register             |
| `ls`        | B    | Left shift register              |
| `xor`       | A    | Bitwise XOR                      |
| `or`        | A    | Bitwise OR                       |
| `and`       | A    | Bitwise AND                      |
| `not`       | C    | Bitwise NOT                      |
| `cmp`       | C    | Compare registers                |
| `jmp`       | E    | Unconditional jump               |
| `jlt`       | E    | Jump if less than                |
| `jgt`       | E    | Jump if greater than             |
| `je`        | E    | Jump if equal                    |
| `hlt`       | -    | Halt execution                   |

## Error Handling

The assembler includes error checks for:

- Invalid instruction names
- Incorrect number of operands
- Use of undefined labels or variables
- Multiple `hlt` instructions
- Incorrect use of registers and immediate values

## Dependencies

- Python 3.x
- `matplotlib` (for simulator visualization)

Install dependencies using:

```sh
pip install matplotlib
```

## License

This project is open-source and free to use for educational purposes.

## Authors

Developed by [Your Name] and contributors.

