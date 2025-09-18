import argparse
from pkg.calculator import Calculator
from pkg.render import format_json_output

def parse_args():
    parser = argparse.ArgumentParser(
        description="CLI calci",
        epilog="Example: uv run main '3 + 5'"
    )
    parser.add_argument(
        "expression",
        type=str,
        nargs="?",
        help="The mathematical expression to evaluate (e.g., '3 + 5')"
    )
    return parser.parse_args()

def main():
    args = parse_args()
    calculator = Calculator()

    if not args.expression:
        print("❌ No expression provided!\n")
        print('Usage: python main.py "<expression>"')
        print('Example: python main.py "3 + 5"')
        return
    
    try:
        result = calculator.evaluate(args.expression)
        if result is not None:
            to_print = format_json_output(args.expression, result)
            print(to_print)
        else:
            print("Error: Expression is empty or contains only whitespace.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()