import json
import random
import os
from datetime import datetime, timedelta

random.seed(999) # Entirely different seed and data pool for evaluation

def random_date(year=2024):
    start_date = datetime(year, 1, 1)
    return (start_date + timedelta(days=random.randint(0, 365))).strftime("%Y-%m-%d")

vendors = ["NovaTech", "SynthCorp", "Omni Consumer", "Garrick Industries", "Spacely Sprockets", "Cogswell Cogs", "Tyrell Corp", "Sirius Cybernetics", "Weyland-Yutani", "Buy n Large"]
currencies = ["USD", "EUR", "GBP", "INR", "CAD"]
items_pool = [("Microchip", 5.0), ("Capacitor", 1.5), ("Sensor Array", 85.0), ("Fiber Optic Cable", 12.0), ("Audit Service", 200.0), ("Software License", 350.0)]

def generate_eval_invoice(idx):
    vendor = random.choice(vendors)
    inv_num = f"INV-EVAL-{random.randint(100, 999)}"
    date_str = random_date()
    
    missing_optional = random.choice([True, False])
    has_due = not missing_optional
    due_date = random_date(2025) if has_due else None
    
    currency = random.choice(currencies)
    
    num_items = random.randint(1, 4)
    line_items = []
    subtotal = 0.0
    
    for _ in range(num_items):
        item_name, base_price = random.choice(items_pool)
        qty = random.randint(1, 5)
        u_price = base_price + random.randint(0, 10)
        line_items.append({
            "description": f"{item_name} Rev_{random.randint(1,5)}",
            "quantity": qty,
            "unit_price": float(round(u_price, 2))
        })
        subtotal += qty * u_price
        
    subtotal = float(round(subtotal, 2))
    
    has_tax = not missing_optional
    tax = float(round(subtotal * 0.1, 2)) if has_tax else None
    total = float(round(subtotal + (tax if tax else 0.0), 2))
    
    expected_json = {
        "vendor": vendor,
        "invoice_number": inv_num,
        "date": date_str,
        "due_date": due_date,
        "currency": currency,
        "subtotal": subtotal,
        "tax": tax,
        "total": total,
        "line_items": line_items
    }
    
    raw_text = f"PROVIDER: {vendor} | BILLING DOC: {inv_num} | ISSUED: {date_str}\n"
    if has_due: raw_text += f"EXPECTED PAYMENT DATE: {due_date}\n"
    raw_text += f"CURRENCY DOMAIN: {currency}\n"
    for item in line_items:
        raw_text += f"{item['quantity']}x {item['description']} @ {item['unit_price']}/ea\n"
    raw_text += f"BASE COST: {subtotal}\n"
    if has_tax: raw_text += f"APPLIED TAX: {tax}\n"
    raw_text += f"FINAL AMOUNT: {total}"
    
    return raw_text, expected_json

def generate_eval_po(idx):
    buyer = random.choice(vendors)
    supplier = random.choice(vendors[::-1])
    po_num = f"PO-EVAL-{random.randint(100, 999)}"
    date_str = random_date()
    
    missing_optional = random.choice([True, False])
    has_delivery = not missing_optional
    del_date = random_date(2025) if has_delivery else None
    
    currency = random.choice(currencies)
    
    num_items = random.randint(1, 4)
    items = []
    total = 0.0
    
    for _ in range(num_items):
        item_name, base_price = random.choice(items_pool)
        qty = random.randint(10, 50)
        u_price = base_price + random.randint(0, 5)
        items.append({
            "item_name": f"Bulk {item_name}",
            "quantity": qty,
            "unit_price": float(round(u_price, 2))
        })
        total += qty * u_price
        
    total = float(round(total, 2))
    
    expected_json = {
        "buyer": buyer,
        "supplier": supplier,
        "po_number": po_num,
        "date": date_str,
        "delivery_date": del_date,
        "currency": currency,
        "total": total,
        "items": items
    }
    
    raw_text = f"PURCHASE REQUISITION: {po_num}\nISSUED BY: {buyer}\nVENDOR: {supplier}\nDATE OF ORIGIN: {date_str}\n"
    if has_delivery: raw_text += f"MUST DELIVER BY: {del_date}\n"
    raw_text += f"TRADE CURRENCY: {currency}\n"
    for item in items:
        raw_text += f"* {item['item_name']} (Quantity: {item['quantity']}, Rate: {item['unit_price']})\n"
    raw_text += f"GROSS REQUIREMENT: {total}"

    return raw_text, expected_json

def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    test_docs = []
    ground_truth = []
    
    # Generate 12 invoices and 8 POs
    for i in range(12):
        raw_text, json_obj = generate_eval_invoice(i)
        doc_id = f"eval_inv_{i+1}"
        test_docs.append(f"====== DOCUMENT: {doc_id} ======\n{raw_text}\n===============================================\n")
        ground_truth.append({"doc_id": doc_id, "expected": json_obj})
        
    for i in range(8):
        raw_text, json_obj = generate_eval_po(i)
        doc_id = f"eval_po_{i+1}"
        test_docs.append(f"====== DOCUMENT: {doc_id} ======\n{raw_text}\n===============================================\n")
        ground_truth.append({"doc_id": doc_id, "expected": json_obj})

    with open("test_documents.txt", "w") as f:
        f.write("\n".join(test_docs))
        
    with open("ground_truth.json", "w") as f:
        json.dump(ground_truth, f, indent=4)

    print("Generated 20 evaluation documents successfully.")

if __name__ == "__main__":
    main()
