# PDF Report Generator for Student/Company Data
# Requirements: reportlab, pandas

import os
import json
import csv
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

# ---------------------- DATA STORAGE ----------------------
data_store = []

# ---------------------- FUNCTIONS ----------------------
def add_data():
    print("\nEnter Details:")
    name = input("Name: ")
    id_ = input("ID: ")
    email = input("Email: ")
    role = input("Course/Department or Role: ")
    performance = input("Performance/Details: ")

    if not name or not id_:
        print("❌ Name and ID are required!")
        return

    record = [name, id_, email, role, performance]
    data_store.append(record)
    print("✅ Data added successfully!")


def load_from_csv(file_path):
    try:
        with open(file_path, newline='') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # skip header
            for row in reader:
                data_store.append(row)
        print("✅ Data loaded from CSV!")
    except Exception as e:
        print(f"❌ Error loading CSV: {e}")


def load_from_json(file_path):
    try:
        with open(file_path) as f:
            data = json.load(f)
            for item in data:
                record = [
                    item.get("name"),
                    item.get("id"),
                    item.get("email"),
                    item.get("role"),
                    item.get("performance")
                ]
                data_store.append(record)
        print("✅ Data loaded from JSON!")
    except Exception as e:
        print(f"❌ Error loading JSON: {e}")


def generate_pdf(report_type="Student Report"):
    if not data_store:
        print("❌ No data available to generate report!")
        return

    if not os.path.exists("reports"):
        os.makedirs("reports")

    filename = f"reports/{report_type.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"

    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []

    # Title
    elements.append(Paragraph(report_type, styles['Title']))
    elements.append(Spacer(1, 12))

    # Date
    elements.append(Paragraph(f"Generated on: {datetime.now()}", styles['Normal']))
    elements.append(Spacer(1, 12))

    # Table Data
    table_data = [["Name", "ID", "Email", "Role", "Performance"]] + data_store

    table = Table(table_data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))

    elements.append(table)

    try:
        doc.build(elements)
        print(f"✅ PDF generated: {filename}")
    except Exception as e:
        print(f"❌ Error generating PDF: {e}")


def menu():
    while True:
        print("""
===== PDF REPORT GENERATOR =====
1. Add Data
2. Load Data from CSV
3. Load Data from JSON
4. Generate Student Report
5. Generate Company Report
6. Exit
""")

        choice = input("Enter your choice: ")

        if choice == '1':
            add_data()
        elif choice == '2':
            path = input("Enter CSV file path: ")
            load_from_csv(path)
        elif choice == '3':
            path = input("Enter JSON file path: ")
            load_from_json(path)
        elif choice == '4':
            generate_pdf("Student Report")
        elif choice == '5':
            generate_pdf("Company Report")
        elif choice == '6':
            print("Exiting...")
            break
        else:
            print("❌ Invalid choice!")


# ---------------------- RUN ----------------------
if __name__ == "__main__":
    menu()
