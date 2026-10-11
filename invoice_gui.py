import os
import sys
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer,
    Image,
)
from reportlab.lib.styles import (
    getSampleStyleSheet,
    ParagraphStyle,
)
from reportlab.lib.enums import TA_RIGHT


VAT_RATE = 0.15


class InvoiceGenerator:

    def __init__(self, root):

        self.root = root
        self.root.title("Professional Invoice Generator")
        self.root.geometry("950x760")

        self.items = []
        self.logo_path = None

        self.create_ui()

    def create_ui(self):

        main = ttk.Frame(
            self.root,
            padding=15
        )

        main.pack(
            fill="both",
            expand=True
        )

        ttk.Label(
            main,
            text="Professional Invoice Generator",
            font=("Segoe UI", 20, "bold")
        ).pack(
            pady=(0, 15)
        )

        # COMPANY

        company = ttk.LabelFrame(
            main,
            text="Company Information",
            padding=10
        )

        company.pack(
            fill="x",
            pady=5
        )

        ttk.Label(
            company,
            text="Company Name"
        ).grid(
            row=0,
            column=0,
            padx=5,
            pady=5,
            sticky="w"
        )

        self.company_name = ttk.Entry(
            company,
            width=35
        )

        self.company_name.grid(
            row=0,
            column=1,
            padx=5,
            pady=5
        )

        ttk.Label(
            company,
            text="Email"
        ).grid(
            row=0,
            column=2,
            padx=5,
            pady=5
        )

        self.company_email = ttk.Entry(
            company,
            width=30
        )

        self.company_email.grid(
            row=0,
            column=3,
            padx=5,
            pady=5
        )

        ttk.Label(
            company,
            text="VAT Number"
        ).grid(
            row=1,
            column=0,
            padx=5,
            pady=5
        )

        self.vat_number = ttk.Entry(
            company,
            width=35
        )

        self.vat_number.grid(
            row=1,
            column=1,
            padx=5,
            pady=5
        )

        self.logo_label = ttk.Label(
            company,
            text="No logo selected"
        )

        self.logo_label.grid(
            row=1,
            column=2,
            padx=5,
            pady=5
        )

        ttk.Button(
            company,
            text="Choose Logo",
            command=self.choose_logo
        ).grid(
            row=1,
            column=3,
            padx=5,
            pady=5
        )

        # CLIENT

        client = ttk.LabelFrame(
            main,
            text="Client Information",
            padding=10
        )

        client.pack(
            fill="x",
            pady=5
        )

        ttk.Label(
            client,
            text="Client Name"
        ).grid(
            row=0,
            column=0,
            padx=5,
            pady=5
        )

        self.client_name = ttk.Entry(
            client,
            width=35
        )

        self.client_name.grid(
            row=0,
            column=1,
            padx=5,
            pady=5
        )

        ttk.Label(
            client,
            text="Client Email"
        ).grid(
            row=0,
            column=2,
            padx=5,
            pady=5
        )

        self.client_email = ttk.Entry(
            client,
            width=30
        )

        self.client_email.grid(
            row=0,
            column=3,
            padx=5,
            pady=5
        )

        # ITEMS

        item_frame = ttk.LabelFrame(
            main,
            text="Add Product / Service",
            padding=10
        )

        item_frame.pack(
            fill="x",
            pady=5
        )

        ttk.Label(
            item_frame,
            text="Description"
        ).grid(
            row=0,
            column=0,
            padx=5
        )

        ttk.Label(
            item_frame,
            text="Quantity"
        ).grid(
            row=0,
            column=1,
            padx=5
        )

        ttk.Label(
            item_frame,
            text="Price (SAR)"
        ).grid(
            row=0,
            column=2,
            padx=5
        )

        self.description = ttk.Entry(
            item_frame,
            width=45
        )

        self.description.grid(
            row=1,
            column=0,
            padx=5,
            pady=5
        )

        self.quantity = ttk.Entry(
            item_frame,
            width=12
        )

        self.quantity.grid(
            row=1,
            column=1,
            padx=5,
            pady=5
        )

        self.price = ttk.Entry(
            item_frame,
            width=15
        )

        self.price.grid(
            row=1,
            column=2,
            padx=5,
            pady=5
        )

        ttk.Button(
            item_frame,
            text="Add Item",
            command=self.add_item
        ).grid(
            row=1,
            column=3,
            padx=10
        )

        # TABLE

        table_frame = ttk.Frame(
            main
        )

        table_frame.pack(
            fill="both",
            expand=True,
            pady=10
        )

        columns = (
            "description",
            "quantity",
            "price",
            "total"
        )

        self.table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=10
        )

        self.table.heading(
            "description",
            text="Description"
        )

        self.table.heading(
            "quantity",
            text="Quantity"
        )

        self.table.heading(
            "price",
            text="Price"
        )

        self.table.heading(
            "total",
            text="Total"
        )

        self.table.column(
            "description",
            width=400
        )

        self.table.column(
            "quantity",
            width=100,
            anchor="center"
        )

        self.table.column(
            "price",
            width=140,
            anchor="center"
        )

        self.table.column(
            "total",
            width=140,
            anchor="center"
        )

        self.table.pack(
            fill="both",
            expand=True
        )

        ttk.Button(
            main,
            text="Remove Selected Item",
            command=self.remove_item
        ).pack(
            pady=5
        )

        # BOTTOM

        bottom = ttk.Frame(
            main
        )

        bottom.pack(
            fill="x",
            pady=10
        )

        ttk.Label(
            bottom,
            text="Discount %"
        ).pack(
            side="left",
            padx=5
        )

        self.discount = ttk.Entry(
            bottom,
            width=8
        )

        self.discount.insert(
            0,
            "0"
        )

        self.discount.pack(
            side="left"
        )

        ttk.Button(
            bottom,
            text="Calculate",
            command=self.update_totals
        ).pack(
            side="left",
            padx=10
        )

        self.total_label = ttk.Label(
            bottom,
            text="Total: 0.00 SAR",
            font=("Segoe UI", 14, "bold")
        )

        self.total_label.pack(
            side="left",
            padx=25
        )

        ttk.Button(
            bottom,
            text="Generate Invoice",
            command=self.generate_invoice
        ).pack(
            side="right"
        )

    # LOGO

    def choose_logo(self):

        file_path = filedialog.askopenfilename(
            title="Choose Company Logo",
            filetypes=[
                (
                    "Image Files",
                    "*.png *.jpg *.jpeg"
                )
            ]
        )

        if file_path:

            self.logo_path = file_path

            self.logo_label.config(
                text=os.path.basename(
                    file_path
                )
            )

    # ADD ITEM

    def add_item(self):

        description = (
            self.description
            .get()
            .strip()
        )

        if not description:

            messagebox.showerror(
                "Error",
                "Enter a description."
            )

            return

        try:

            quantity = int(
                self.quantity.get()
            )

            price = float(
                self.price.get()
            )

            if quantity <= 0:
                raise ValueError

            if price < 0:
                raise ValueError

        except ValueError:

            messagebox.showerror(
                "Error",
                "Enter a valid quantity and price."
            )

            return

        self.items.append({
            "description": description,
            "quantity": quantity,
            "price": price
        })

        self.table.insert(
            "",
            "end",
            values=(
                description,
                quantity,
                f"{price:.2f} SAR",
                f"{quantity * price:.2f} SAR"
            )
        )

        self.description.delete(
            0,
            tk.END
        )

        self.quantity.delete(
            0,
            tk.END
        )

        self.price.delete(
            0,
            tk.END
        )

        self.update_totals()

    # REMOVE ITEM

    def remove_item(self):

        selected = (
            self.table.selection()
        )

        if not selected:

            messagebox.showwarning(
                "Warning",
                "Select an item first."
            )

            return

        indexes = sorted(
            (
                self.table.index(item)
                for item in selected
            ),
            reverse=True
        )

        for item in selected:

            self.table.delete(
                item
            )

        for index in indexes:

            del self.items[index]

        self.update_totals()

    # CALCULATE

    def calculate_totals(self):

        subtotal = sum(
            item["quantity"]
            * item["price"]

            for item in self.items
        )

        try:

            discount_percent = float(
                self.discount.get()
            )

        except ValueError:

            discount_percent = 0

        discount_percent = max(
            0,
            min(
                discount_percent,
                100
            )
        )

        discount_amount = (
            subtotal
            * discount_percent
            / 100
        )

        taxable_amount = (
            subtotal
            - discount_amount
        )

        vat = (
            taxable_amount
            * VAT_RATE
        )

        total = (
            taxable_amount
            + vat
        )

        return {
            "subtotal": subtotal,
            "discount_percent": discount_percent,
            "discount_amount": discount_amount,
            "vat": vat,
            "total": total
        }

    def update_totals(self):

        totals = (
            self.calculate_totals()
        )

        self.total_label.config(
            text=(
                f"Total: "
                f"{totals['total']:.2f} SAR"
            )
        )

    # GENERATE PDF

    def generate_invoice(self):

        company = (
            self.company_name
            .get()
            .strip()
        )

        client = (
            self.client_name
            .get()
            .strip()
        )

        if not company:

            messagebox.showerror(
                "Error",
                "Company name is required."
            )

            return

        if not client:

            messagebox.showerror(
                "Error",
                "Client name is required."
            )

            return

        if not self.items:

            messagebox.showerror(
                "Error",
                "Add at least one item."
            )

            return

        invoice_number = (
            datetime.now()
            .strftime(
                "INV-%Y%m%d-%H%M%S"
            )
        )

        output_file = (
            filedialog
            .asksaveasfilename(
                title="Save Invoice",
                defaultextension=".pdf",
                initialfile=(
                    f"{invoice_number}.pdf"
                ),
                filetypes=[
                    (
                        "PDF Files",
                        "*.pdf"
                    )
                ]
            )
        )

        if not output_file:
            return

        totals = (
            self.calculate_totals()
        )

        doc = SimpleDocTemplate(
            output_file,
            pagesize=A4,
            rightMargin=18 * mm,
            leftMargin=18 * mm,
            topMargin=15 * mm,
            bottomMargin=18 * mm
        )

        styles = (
            getSampleStyleSheet()
        )

        normal = ParagraphStyle(
            "InvoiceNormal",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=9,
            leading=13
        )

        bold = ParagraphStyle(
            "InvoiceBold",
            parent=normal,
            fontName="Helvetica-Bold",
            fontSize=12,
            leading=15
        )

        title = ParagraphStyle(
            "InvoiceTitle",
            parent=styles["Heading1"],
            fontName="Helvetica-Bold",
            fontSize=26,
            leading=30,
            alignment=TA_RIGHT
        )

        right = ParagraphStyle(
            "InvoiceRight",
            parent=normal,
            alignment=TA_RIGHT
        )

        story = []

        # HEADER LEFT

        company_info = []

        if self.logo_path:

            try:

                logo = Image(
                    self.logo_path,
                    width=30 * mm,
                    height=18 * mm
                )

                logo.hAlign = "LEFT"

                company_info.append(
                    logo
                )

                company_info.append(
                    Spacer(
                        1,
                        3 * mm
                    )
                )

            except Exception:
                pass

        company_info.append(
            Paragraph(
                company,
                bold
            )
        )

        email = (
            self.company_email
            .get()
            .strip()
        )

        if email:

            company_info.append(
                Paragraph(
                    email,
                    normal
                )
            )

        vat_number = (
            self.vat_number
            .get()
            .strip()
        )

        if vat_number:

            company_info.append(
                Paragraph(
                    f"VAT Number: {vat_number}",
                    normal
                )
            )

        # HEADER RIGHT

        invoice_info = [
            Paragraph(
                "INVOICE",
                title
            ),

            Spacer(
                1,
                2 * mm
            ),

            Paragraph(
                (
                    "<b>Invoice No.</b>"
                    f"<br/>{invoice_number}"
                ),
                right
            ),

            Spacer(
                1,
                2 * mm
            ),

            Paragraph(
                (
                    "<b>Date</b>"
                    f"<br/>{datetime.now().strftime('%d %B %Y')}"
                ),
                right
            )
        ]

        header = Table(
            [
                [
                    company_info,
                    invoice_info
                ]
            ],
            colWidths=[
                95 * mm,
                75 * mm
            ]
        )

        header.setStyle(
            TableStyle([
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "TOP"
                ),

                (
                    "ALIGN",
                    (1, 0),
                    (1, 0),
                    "RIGHT"
                ),

                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    10
                )
            ])
        )

        story.append(
            header
        )

        story.append(
            Spacer(
                1,
                8 * mm
            )
        )

        # BILL TO

        client_email = (
            self.client_email
            .get()
            .strip()
        )

        client_text = (
            "<b>BILL TO</b>"
            "<br/><br/>"
            f"<b>{client}</b>"
        )

        if client_email:

            client_text += (
                f"<br/>{client_email}"
            )

        bill = Table(
            [
                [
                    Paragraph(
                        client_text,
                        normal
                    )
                ]
            ],
            colWidths=[
                170 * mm
            ]
        )

        bill.setStyle(
            TableStyle([
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, -1),
                    colors.HexColor(
                        "#F5F5F5"
                    )
                ),

                (
                    "BOX",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.HexColor(
                        "#DDDDDD"
                    )
                ),

                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    10
                ),

                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    10
                ),

                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    10
                ),

                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    10
                )
            ])
        )

        story.append(
            bill
        )

        story.append(
            Spacer(
                1,
                7 * mm
            )
        )

        # PRODUCT TABLE

        rows = [
            [
                Paragraph(
                    "<b>Description</b>",
                    normal
                ),

                Paragraph(
                    "<b>Qty</b>",
                    right
                ),

                Paragraph(
                    "<b>Unit Price</b>",
                    right
                ),

                Paragraph(
                    "<b>Amount</b>",
                    right
                )
            ]
        ]

        for item in self.items:

            amount = (
                item["quantity"]
                * item["price"]
            )

            rows.append([
                Paragraph(
                    item["description"],
                    normal
                ),

                str(
                    item["quantity"]
                ),

                (
                    f"{item['price']:,.2f} "
                    "SAR"
                ),

                (
                    f"{amount:,.2f} "
                    "SAR"
                )
            ])

        items_table = Table(
            rows,
            colWidths=[
                85 * mm,
                18 * mm,
                33 * mm,
                34 * mm
            ],
            repeatRows=1
        )

        items_table.setStyle(
            TableStyle([
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor(
                        "#EAEAEA"
                    )
                ),

                (
                    "FONTNAME",
                    (0, 0),
                    (-1, 0),
                    "Helvetica-Bold"
                ),

                (
                    "ALIGN",
                    (1, 0),
                    (-1, -1),
                    "RIGHT"
                ),

                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE"
                ),

                (
                    "LINEBELOW",
                    (0, 0),
                    (-1, 0),
                    1,
                    colors.HexColor(
                        "#BBBBBB"
                    )
                ),

                (
                    "LINEBELOW",
                    (0, 1),
                    (-1, -1),
                    0.3,
                    colors.HexColor(
                        "#DDDDDD"
                    )
                ),

                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    8
                ),

                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    8
                )
            ])
        )

        story.append(
            items_table
        )

        story.append(
            Spacer(
                1,
                7 * mm
            )
        )

        # TOTALS

        total_rows = [
            [
                "Subtotal",
                (
                    f"{totals['subtotal']:,.2f} "
                    "SAR"
                )
            ]
        ]

        if totals["discount_amount"] > 0:

            total_rows.append([
                (
                    f"Discount "
                    f"({totals['discount_percent']:.1f}%)"
                ),

                (
                    f"-{totals['discount_amount']:,.2f} "
                    "SAR"
                )
            ])

        total_rows.append([
            "VAT (15%)",
            (
                f"{totals['vat']:,.2f} "
                "SAR"
            )
        ])

        total_rows.append([
            "TOTAL",
            (
                f"{totals['total']:,.2f} "
                "SAR"
            )
        ])

        totals_table = Table(
            total_rows,
            colWidths=[
                45 * mm,
                45 * mm
            ],
            hAlign="RIGHT"
        )

        totals_table.setStyle(
            TableStyle([
                (
                    "ALIGN",
                    (0, 0),
                    (-1, -1),
                    "RIGHT"
                ),

                (
                    "FONTNAME",
                    (0, 0),
                    (-1, -2),
                    "Helvetica"
                ),

                (
                    "FONTNAME",
                    (0, -1),
                    (-1, -1),
                    "Helvetica-Bold"
                ),

                (
                    "FONTSIZE",
                    (0, 0),
                    (-1, -2),
                    9
                ),

                (
                    "FONTSIZE",
                    (0, -1),
                    (-1, -1),
                    12
                ),

                (
                    "BACKGROUND",
                    (0, -1),
                    (-1, -1),
                    colors.HexColor(
                        "#EAEAEA"
                    )
                ),

                (
                    "LINEABOVE",
                    (0, -1),
                    (-1, -1),
                    1,
                    colors.black
                ),

                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    7
                ),

                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    7
                )
            ])
        )

        story.append(
            totals_table
        )

        story.append(
            Spacer(
                1,
                15 * mm
            )
        )

        story.append(
            Paragraph(
                "<b>Thank you for your business.</b>",
                normal
            )
        )

        # CREATE

        try:

            doc.build(
                story
            )

        except Exception as error:

            messagebox.showerror(
                "Error",
                (
                    "Could not create invoice."
                    "\n\n"
                    f"{error}"
                )
            )

            return

        messagebox.showinfo(
            "Success",
            "Invoice created successfully!"
        )

        self.open_file(
            output_file
        )

    # OPEN PDF

    def open_file(
        self,
        file_path
    ):

        try:

            if sys.platform.startswith(
                "win"
            ):

                os.startfile(
                    file_path
                )

            elif sys.platform.startswith(
                "darwin"
            ):

                subprocess.run([
                    "open",
                    file_path
                ])

            else:

                subprocess.run([
                    "xdg-open",
                    file_path
                ])

        except Exception:
            pass


def main():

    root = tk.Tk()

    InvoiceGenerator(
        root
    )

    root.mainloop()


if __name__ == "__main__":
    main()