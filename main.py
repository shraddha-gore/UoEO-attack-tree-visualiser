import argparse
import os
from core import run_analysis

SUPPORTED_EXTENSIONS = ['.json', '.yaml', '.yml', '.xml']


def main():
    parser = argparse.ArgumentParser(
        description="Visualise and analyse an attack tree with user-defined values."
    )
    parser.add_argument(
        "file", help="Path to attack tree file (supported formats: .json, .yaml, .yml, .xml)"
    )
    args = parser.parse_args()
    file_path = args.file

    # Validate file extension early
    _, ext = os.path.splitext(file_path)
    if ext.lower() not in SUPPORTED_EXTENSIONS:
        print("Error: Unsupported file format. Please use JSON, YAML or XML.")
        return

    # Show guidance to the user
    print("\nNOTE: Your input file should follow the expected format:")
    print("- Each node must have a 'name' field (string).")
    print("- Leaf nodes must include a 'value' field (float or int).")
    print("- Child nodes must be nested under a 'children' list.")
    print("Incorrect or inconsistent structure may cause unpredictable results.\n")

    try:
        # Ask user how to interpret values
        value_mode = None
        while value_mode is None:
            print("How should node values be interpreted?")
            print("1. Monetary impact (e.g., £5000)")
            print("2. Probability of attack success (0.0 – 1.0)")
            choice = input("> ").strip()
            if choice == "1":
                value_mode = "monetary"
            elif choice == "2":
                value_mode = "probability"
            else:
                print("Invalid selection. Please enter 1 or 2.")

        run_analysis(file_path, value_mode)

    except ValueError as ve:
        print(f"\nError: {ve}")
        print("Hint: The selected value mode may not match the data in the file.")
        print("Try choosing the other interpretation mode (monetary vs probability).")

    except Exception as e:
        print(f"\nUnexpected error: {e}")


if __name__ == "__main__":
    main()
