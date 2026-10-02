# sanitizer/io_manager.py
import csv
import logging
import os
from typing import List, Dict
from .core import clean_name, is_valid_email
from .exceptions import MissingFileError

# Configure the production logger
logging.basicConfig(
    filename='sanitizer.log', 
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def process_leads(input_path: str) -> List[Dict]:
    """Reads the raw CSV, cleans the data, and returns a list of valid leads."""
    if not os.path.exists(input_path):
        raise MissingFileError(f"Cannot find input file: {input_path}")

    valid_leads = []
    
    with open(input_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row_num, row in enumerate(reader, start=2): # Start at 2 because row 1 is headers
            raw_email = row.get("email", "")
            raw_first_name = row.get("first_name", "")
            raw_company = row.get("company", "")
            
            if not is_valid_email(raw_email):
                logging.warning(f"Row {row_num}: Invalid or banned email skipped -> {raw_email}")
                continue
                
            clean_lead = {
                "first_name": clean_name(raw_first_name),
                "email": raw_email.strip().lower(),
                "company": raw_company.strip().title()
            }
            valid_leads.append(clean_lead)
            
    logging.info(f"Processed {len(valid_leads)} valid leads out of total.")
    return valid_leads

def export_cleaned_leads(leads: List[Dict], output_path: str) -> None:
    """Exports all valid, cleaned leads into a single new CSV file."""
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    fieldnames = list(leads[0].keys()) if leads else ["first_name", "email", "company"]
    with open(output_path, mode='w', encoding='utf-8', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(leads)

    logging.info(f"Saved {len(leads)} cleaned leads to {output_path}")
    print(f"Exported cleaned leads file: {output_path} ({len(leads)} leads)")

def export_batches(leads: List[Dict], output_dir: str, batch_size: int = 50) -> None:
    """Splits the valid leads into chunks and writes them to separate CSV files."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir) # Create the processed folder if it doesn't exist

    # The Chunking Logic: slices the list from 'i' to 'i + batch_size'
    for i in range(0, len(leads), batch_size):
        batch = leads[i:i + batch_size]
        batch_num = (i // batch_size) + 1
        
        file_path = os.path.join(output_dir, f"campaign_batch_{batch_num}.csv")
        
        with open(file_path, mode='w', encoding='utf-8', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=["first_name", "email", "company"])
            writer.writeheader()
            writer.writerows(batch)
            
        print(f"Exported {file_path} ({len(batch)} leads)")
