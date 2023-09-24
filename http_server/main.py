def init():
    # Entrypoint for the HTTP Parser
    # Right now this will load a given file
    filename = input("Enter test request filepath: ")
    with open(filename) as f:
        # Parse!


if __name__ == "__main__":
    init()
