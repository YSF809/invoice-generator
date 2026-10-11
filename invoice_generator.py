from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from datetime import datetime
from pathlib import Path


VAT_RATE = 0.15


def get_float(prompt, default=0):
    while True:
        value = input(prompt).strip()

        if value == "":
            return default

        try:
            return float(value)
        except ValueError:
            print("Please enter a valid number.")


def get_int(prompt):
    while True:
        try:
            value = int(input(prompt))

            if value <= 0:
                print("Quantity must be greater than 0.")
                continue

            return value

        except ValueError:
            print("Please enter a valid whole number.")


def get_invoice_data():
    print("=" * 50)
    print("PROFESSIONAL INVOICE GENERATOR")
    print("=" * 50)

    company_name = input("Company name: ").strip()
    company_email = input("Company email: ").strip()

    print("\nCLIENT INFORMATION")

    client_name = input("Client name: ").strip()
    client_email = input("Client email: ").strip()

    items = []

    while True:
        print("\nADD ITEM")
        print("-" * 30)

        description = input("Description: ").strip()

        quantity = get_int("Quantity: ")

        price = get_float("Price per item: $")

        items.append({
            "description": description,
            "quantity": quantity,
            "price": price
        })

        more = input(
            "\nAdd another item? (y/n): "
        ).strip().lower()

        if more != "y":
            break

    discount = get_float(
        "\nDiscount percentage (press Enter for 0): ",
        0
    )

    return {
        "company_name": company_name,
        "company_email": company_email,
        "client_name": client_name,
        "client_email": client_email,
        "items": items,
        "discount": discount
    }


def create_invoice_number():
    return datetime.now().strftime(
        "INV-%Y%m%d-%H%M%S"
    )


def calculate_totals(items, discount_percentage):
    subtotal = sum(
        item["quantity"] * item["price"]
        for item in items
    )

    discount_amount = (
        subtotal * discount_percentage / 100
    )

    after_discount = subtotal - discount_amount

    vat = after_discount * VAT_RATE

    grand_total = after_discount + vat

    return {
        "subtotal": subtotal,
        "discount": discount_amount,
        "vat": vat,
        "total": grand_total
    }


def draw_header(pdf, width, height, invoice_number, data):
    pdf.setFont(
        "Helvetica-Bold",
        26
    )

    pdf.drawString(
        50,
        height - 60,
        "INVOICE"
    )

    pdf.setFont(
        "Helvetica-Bold",
        13
    )

    pdf.drawString(
        50,
        height - 100,
        data["company_name"]
    )

    pdf.setFont(
        "Helvetica",
        10
    )

    pdf.drawString(
        50,
        height - 118,
        data["company_email"]
    )

    pdf.drawRightString(
        width - 50,
        height - 90,
        invoice_number
    )

    pdf.drawRightString(
        width - 50,
        height - 110,
        datetime.now().strftime("%Y-%m-%d")
    )

    pdf.setFont(
        "Helvetica-Bold",
        11
    )

    pdf.drawString(
        50,
        height - 160,
        "Bill To:"
    )

    pdf.setFont(
        "Helvetica",
        10
    )

    pdf.drawString(
        50,
        height - 180,
        data["client_name"]
    )

    pdf.drawString(
        50,
        height - 197,
        data["client_email"]
    )


def draw_table_header(pdf, y):
    pdf.setFillColor(
        colors.lightgrey
    )

    pdf.rect(
        50,
        y,
        495,
        25,
        fill=True,
        stroke=False
    )

    pdf.setFillColor(
        colors.black
    )

    pdf.setFont(
        "Helvetica-Bold",
        10
    )

    pdf.drawString(
        60,
        y + 8,
        "Description"
    )

    pdf.drawString(
        300,
        y + 8,
        "Qty"
    )

    pdf.drawString(
        350,
        y + 8,
        "Price"
    )

    pdf.drawString(
        455,
        y + 8,
        "Total"
    )


def generate_invoice(data):
    invoice_number = create_invoice_number()

    totals = calculate_totals(
        data["items"],
        data["discount"]
    )

    output_folder = Path("invoices")

    output_folder.mkdir(
        exist_ok=True
    )

    file_name = (
        output_folder /
        f"{invoice_number}.pdf"
    )

    pdf = canvas.Canvas(
        str(file_name),
        pagesize=A4
    )

    width, height = A4

    draw_header(
        pdf,
        width,
        height,
        invoice_number,
        data
    )

    y = height - 250

    draw_table_header(
        pdf,
        y
    )

    y -= 25

    pdf.setFont(
        "Helvetica",
        10
    )

    for item in data["items"]:
        if y < 150:
            pdf.showPage()

            draw_header(
                pdf,
                width,
                height,
                invoice_number,
                data
            )

            y = height - 250

            draw_table_header(
                pdf,
                y
            )

            y -= 25

            pdf.setFont(
                "Helvetica",
                10
            )

        item_total = (
            item["quantity"]
            * item["price"]
        )

        pdf.drawString(
            60,
            y,
            item["description"][:35]
        )

        pdf.drawString(
            300,
            y,
            str(item["quantity"])
        )

        pdf.drawString(
            350,
            y,
            f"${item['price']:.2f}"
        )

        pdf.drawString(
            455,
            y,
            f"${item_total:.2f}"
        )

        y -= 25

    y -= 10

    pdf.line(
        330,
        y + 15,
        545,
        y + 15
    )

    pdf.setFont(
        "Helvetica",
        10
    )

    pdf.drawString(
        350,
        y,
        "Subtotal:"
    )

    pdf.drawRightString(
        540,
        y,
        f"${totals['subtotal']:.2f}"
    )

    y -= 22

    pdf.drawString(
        350,
        y,
        f"Discount ({data['discount']:.1f}%):"
    )

    pdf.drawRightString(
        540,
        y,
        f"-${totals['discount']:.2f}"
    )

    y -= 22

    pdf.drawString(
        350,
        y,
        "VAT (15%):"
    )

    pdf.drawRightString(
        540,
        y,
        f"${totals['vat']:.2f}"
    )

    y -= 25

    pdf.setFont(
        "Helvetica-Bold",
        13
    )

    pdf.drawString(
        350,
        y,
        "TOTAL:"
    )

    pdf.drawRightString(
        540,
        y,
        f"${totals['total']:.2f}"
    )

    pdf.setFont(
        "Helvetica",
        9
    )

    pdf.drawString(
        50,
        50,
        "Thank you for your business!"
    )

    pdf.save()

    print("\n" + "=" * 50)
    print("INVOICE CREATED SUCCESSFULLY")
    print("=" * 50)

    print(
        f"Invoice Number: {invoice_number}"
    )

    print(
        f"Subtotal: ${totals['subtotal']:.2f}"
    )

    print(
        f"Discount: ${totals['discount']:.2f}"
    )

    print(
        f"VAT: ${totals['vat']:.2f}"
    )

    print(
        f"Total: ${totals['total']:.2f}"
    )

    print(
        f"\nSaved to: {file_name}"
    )


def main():
    data = get_invoice_data()

    generate_invoice(
        data
    )


if __name__ == "__main__":
    main()