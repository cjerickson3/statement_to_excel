import subprocess
import re
import os
from pathlib import Path

def redact_chase_statement(text):
    """
    Redact personal information from Chase bank statement text.
    Customize the patterns below based on what you see in your statements.
    """
    
    # Redact account numbers (various formats)
    # Chase accounts are typically 9-12 digits
    text = re.sub(r'\b\d{9,12}\b', 'XXXXX' + r'\g<0>'[-4:] if len(r'\g<0>') >= 4 else 'XXXXX', text)
    text = re.sub(r'Account\s*(?:Number|#)?\s*:?\s*\d+', 'Account Number: XXXXXXXXX', text, flags=re.IGNORECASE)
    
    # Redact routing numbers (9 digits)
    text = re.sub(r'Routing\s*(?:Number|#)?\s*:?\s*\d{9}', 'Routing Number: XXXXXXXXX', text, flags=re.IGNORECASE)
    
    # Redact names - you'll need to customize this with your actual name
    # Example: text = re.sub(r'John Doe', 'CUSTOMER NAME', text, flags=re.IGNORECASE)
    YOUR_NAME = "YOUR_NAME_HERE"  # Replace with your actual name
    text = re.sub(re.escape(YOUR_NAME), 'CUSTOMER NAME', text, flags=re.IGNORECASE)
    
    # Redact addresses - customize with your actual address
    # Example: text = re.sub(r'123 Main St.*?\d{5}', 'CUSTOMER ADDRESS', text, flags=re.IGNORECASE)
    YOUR_ADDRESS_PATTERN = r"YOUR_ADDRESS_PATTERN_HERE"  # Replace with pattern matching your address
    # text = re.sub(YOUR_ADDRESS_PATTERN, 'CUSTOMER ADDRESS', text, flags=re.IGNORECASE | re.DOTALL)
    
    # Redact phone numbers
    text = re.sub(r'\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b', 'XXX-XXX-XXXX', text)
    
    # Redact email addresses
    text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', 'XXXXX@XXXXX.com', text)
    
    # Redact SSN or tax ID (if present)
    text = re.sub(r'\b\d{3}-\d{2}-\d{4}\b', 'XXX-XX-XXXX', text)
    
    return text

def process_pdf_to_redacted_text(pdf_path, output_dir=None):
    """
    Convert PDF to text using pdftotext and redact personal information.
    
    Args:
        pdf_path: Path to the PDF file
        output_dir: Directory to save redacted text files (default: same as PDF)
    """
    pdf_path = Path(pdf_path)
    
    if not pdf_path.exists():
        print(f"Error: PDF file not found: {pdf_path}")
        return None
    
    # Set output directory
    if output_dir is None:
        output_dir = pdf_path.parent
    else:
        output_dir = Path(output_dir)
        output_dir.mkdir(exist_ok=True)
    
    # Create temporary file for pdftotext output
    temp_txt = output_dir / f"{pdf_path.stem}_temp.txt"
    final_txt = output_dir / f"{pdf_path.stem}_redacted.txt"
    
    try:
        # Run pdftotext
        print(f"Processing: {pdf_path.name}")
        subprocess.run(['pdftotext', '-layout', str(pdf_path), str(temp_txt)], 
                      check=True, capture_output=True)
        
        # Read the text
        with open(temp_txt, 'r', encoding='utf-8', errors='ignore') as f:
            text = f.read()
        
        # Redact personal information
        redacted_text = redact_chase_statement(text)
        
        # Save redacted version
        with open(final_txt, 'w', encoding='utf-8') as f:
            f.write(redacted_text)
        
        # Remove temporary file
        temp_txt.unlink()
        
        print(f"✓ Saved redacted text to: {final_txt}")
        return final_txt
        
    except subprocess.CalledProcessError as e:
        print(f"Error running pdftotext: {e}")
        return None
    except Exception as e:
        print(f"Error processing {pdf_path.name}: {e}")
        return None

def batch_process_pdfs(pdf_directory, output_dir=None):
    """
    Process all PDF files in a directory.
    
    Args:
        pdf_directory: Directory containing PDF files
        output_dir: Directory to save redacted text files (default: same as PDFs)
    """
    pdf_dir = Path(pdf_directory)
    pdf_files = list(pdf_dir.glob("*.pdf"))
    
    if not pdf_files:
        print(f"No PDF files found in {pdf_directory}")
        return
    
    print(f"Found {len(pdf_files)} PDF files")
    print("-" * 50)
    
    for pdf_file in pdf_files:
        process_pdf_to_redacted_text(pdf_file, output_dir)
    
    print("-" * 50)
    print(f"Processing complete!")

# Example usage
if __name__ == "__main__":
    # Option 1: Process a single PDF
    # process_pdf_to_redacted_text("statement_jan_2024.pdf")
    
    # Option 2: Process all PDFs in a directory
    # batch_process_pdfs("./chase_statements", output_dir="./redacted_statements")
    
    # Customize these paths for your setup
    PDF_DIRECTORY = "./chase_pdfs"  # Change to your PDF directory
    OUTPUT_DIRECTORY = "./redacted_texts"  # Change to where you want output
    
    batch_process_pdfs(PDF_DIRECTORY, OUTPUT_DIRECTORY)
