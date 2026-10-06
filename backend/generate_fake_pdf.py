from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

def create_fake_contract(filename="sample_contract.pdf"):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    
    # Title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "MASTER SERVICES AGREEMENT")
    
    # Body
    c.setFont("Helvetica", 12)
    text = [
        "This Master Services Agreement (\"Agreement\") is entered into on October 6, 2026,",
        "by and between Acme Corp (\"Client\") and Northwind Engineering (\"Provider\").",
        "",
        "1. SERVICES TO BE PERFORMED",
        "Provider agrees to perform the software engineering services as outlined in the",
        "attached Statement of Work (SOW). The Provider will use commercially reasonable",
        "efforts to meet any delivery dates set forth in the SOW.",
        "",
        "2. PAYMENT TERMS",
        "Client agrees to pay Provider at the rate of $150 per hour for services rendered.",
        "Invoices shall be submitted monthly and are payable within Net 30 days.",
        "",
        "3. CONFIDENTIALITY",
        "Both parties agree to keep all proprietary information completely confidential",
        "and will not disclose such information to any third parties without prior written consent.",
        "",
        "4. TERMINATION",
        "Either party may terminate this Agreement with 30 days written notice.",
        "",
        "Signed,",
        "John Doe, CEO of Acme Corp",
        "Jane Smith, CTO of Northwind Engineering"
    ]
    
    y = height - 100
    for line in text:
        c.drawString(50, y, line)
        y -= 20
        
    c.showPage()
    
    # Add a second page just to test page numbers
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, height - 50, "APPENDIX A: STATEMENT OF WORK (SOW)")
    c.setFont("Helvetica", 12)
    
    sow_text = [
        "Project Name: Project SuperDocs",
        "Start Date: October 15, 2026",
        "End Date: December 31, 2026",
        "",
        "Scope of Work:",
        "- Develop backend Ingestion and Parsing pipeline using FastAPI.",
        "- Implement LangGraph background worker.",
        "- Provide comprehensive testing for PDF extraction."
    ]
    
    y = height - 100
    for line in sow_text:
        c.drawString(50, y, line)
        y -= 20
        
    c.showPage()
    c.save()
    print(f"Generated {filename}")

if __name__ == "__main__":
    create_fake_contract()
