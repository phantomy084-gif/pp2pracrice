import re
import json


def parse_receipt(text):
    # Extract date and time
    date_time = re.search(
        r'Время:\s*(\d{2}\.\d{2}\.\d{4})\s+(\d{2}:\d{2}:\d{2})',
        text
    )

    date = date_time.group(1) if date_time else None
    time = date_time.group(2) if date_time else None

    # Extract payment method and amount
    payment = re.search(
        r'Банковская карта:\s*([\d\s]+,\d{2})',
        text
    )

    payment_method = "Банковская карта" if payment else None
    payment_amount = payment.group(1).replace(" ", "").replace(",", ".") if payment else None

    # Extract receipt number
    receipt = re.search(r'Чек №\s*(\d+)', text)
    receipt_number = receipt.group(1) if receipt else None

    # Extract total amount
    total = re.search(
        r'ИТОГО:\s*([\d\s]+,\d{2})',
        text
    )

    total_amount = total.group(1).replace(" ", "").replace(",", ".") if total else None

    # Extract products
    products = []

    # Product block:
    # 1.
    # Product name
    # 2,000 x 154,00
    # 308,00

    pattern = re.compile(
        r'(?m)^\s*(\d+)\.\s*\n'
        r'(.*?)\n'
        r'\s*([\d\s]+,\d{2})\s*x\s*([\d\s]+,\d{2})\s*\n'
        r'\s*([\d\s]+,\d{2})'
    )

    matches = pattern.findall(text)

    for match in matches:
        number = match[0]
        name = match[1].strip()
        quantity = match[2].replace(" ", "").replace(",", ".")
        unit_price = match[3].replace(" ", "").replace(",", ".")
        product_total = match[4].replace(" ", "").replace(",", ".")

        products.append({
            "number": int(number),
            "name": name,
            "quantity": float(quantity),
            "unit_price": float(unit_price),
            "total": float(product_total)
        })

    # Calculate total from products
    calculated_total = sum(product["total"] for product in products)

    result = {
        "receipt_number": receipt_number,
        "date": date,
        "time": time,
        "payment_method": payment_method,
        "payment_amount": float(payment_amount) if payment_amount else None,
        "total_amount": float(total_amount) if total_amount else None,
        "calculated_total": calculated_total,
        "products": products
    }

    return result


# Read receipt from raw.txt
with open("raw.txt", "r", encoding="utf-8") as file:
    receipt_text = file.read()


# Parse receipt
data = parse_receipt(receipt_text)


# Print readable output
print("=" * 50)
print("RECEIPT INFORMATION")
print("=" * 50)

print("Receipt number:", data["receipt_number"])
print("Date:", data["date"])
print("Time:", data["time"])
print("Payment method:", data["payment_method"])
print("Payment amount:", data["payment_amount"], "KZT")
print("Receipt total:", data["total_amount"], "KZT")
print("Calculated total:", data["calculated_total"], "KZT")

print("\nPRODUCTS")
print("=" * 50)

for product in data["products"]:
    print(
        f'{product["number"]}. {product["name"]} | '
        f'Qty: {product["quantity"]} | '
        f'Price: {product["unit_price"]:.2f} | '
        f'Total: {product["total"]:.2f}'
    )

print("\nTotal products:", len(data["products"]))

if data["total_amount"] == data["calculated_total"]:
    print("Total verification: OK")
else:
    print("Total verification: ERROR")


# Save structured data as JSON
with open("parsed_receipt.json", "w", encoding="utf-8") as file:
    json.dump(data, file, ensure_ascii=False, indent=4)