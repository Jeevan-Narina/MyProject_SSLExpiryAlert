
def parse_purchase(text):
    if not isinstance(text, str):
        raise ValueError("Purchase input must be a string")

    if text.count(':') != 1:
        raise ValueError("Input must contain exactly one ':'")

    grade, litres = text.split(':')

    grade = grade.strip()
    if not grade:
        raise ValueError("Fuel grade cannot be empty")

    try:
        litres = float(litres)
    except ValueError:
        raise ValueError("Litres must be a valid number")

    if litres <= 0:
        raise ValueError("Litres must be positive")

    return grade.title(), litres


def volume_average(volumes_csv):
    if not isinstance(volumes_csv, str) or not volumes_csv.strip():
        raise ValueError("Volume input cannot be empty")

    try:
        values = [int(r.strip()) for r in volumes_csv.split(',')]
    except ValueError:
        raise ValueError("Volumes must contain valid integers")

    if any(value < 0 for value in values):
        raise ValueError("Volumes cannot be negative")

    return sum(values) // len(values)


def payable_bill(text):
    if not isinstance(text, str):
        raise ValueError("Bill input must be a string")

    if text.count('|') != 1:
        raise ValueError("Input must contain exactly one '|'")

    bill, discount = text.split('|')

    try:
        bill = float(bill)
        discount = float(discount)
    except ValueError:
        raise ValueError("Bill and discount must be valid numbers")

    if bill < 0 or discount < 0:
        raise ValueError("Bill and discount cannot be negative")

    total = bill * 1.18 - discount
    return max(total, 0)


def main():
    print("==== Running parse_purchase ====")
    user_input = input("Enter grade:litres (e.g. diesel:25): ")
    result = parse_purchase(user_input)
    print("Grade and Litres:", result)

    print("\n==== Running volume_average ====")
    user_input = input("Enter pump volumes in litres as CSV (e.g. 10,25,40): ")
    result = volume_average(user_input)
    print("Average Volume:", result)

    print("\n==== Running payable_bill ====")
    user_input = input("Enter bill|discount (e.g. 2500|100): ")
    result = payable_bill(user_input)
    print("Payable Bill:", result)


if __name__ == "__main__":
    main()
