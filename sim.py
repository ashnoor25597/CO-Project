import sys

def read_binary_file(file_path):
    instructions = []
    
    try:
        with open(file_path, 'r') as file:
            for line_no, line in enumerate(file, start=1):
                line = line.strip()
                
                # Skip empty lines
                if line == "":
                    continue
                
                # Check if line contains only 0s and 1s
                if not all(c in '01' for c in line):
                    print(f"Error: Invalid binary at line {line_no}")
                    sys.exit(1)
                
                # Check if instruction is 32 bits
                if len(line) != 32:
                    print(f"Error: Instruction not 32 bits at line {line_no}")
                    sys.exit(1)
                
                instructions.append(line)
    
    except FileNotFoundError:
        print("Error: Input file not found")
        sys.exit(1)
    
    return instructions


def main():
    if len(sys.argv) != 3:
        print("Usage: python simulator.py <input_file> <output_file>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    instructions = read_binary_file(input_file)
    
    print("Instructions loaded successfully!")
    
    # Just printing for now (later you'll simulate)
    for i, instr in enumerate(instructions):
        print(f"{i}: {instr}")


if __name__ == "__main__":
    main()