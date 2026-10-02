# main.py
import os
from sanitizer.io_manager import process_leads, export_cleaned_leads, export_batches
from sanitizer.exceptions import SanitizerError

def main():
    print("Starting Cold Outreach Sanitizer...")
    
    input_file = os.path.join("data", "raw", "leads_dump.csv")
    output_folder = os.path.join("data", "processed")
    cleaned_output_file = os.path.join(output_folder, "cleaned_leads.csv")
    
    try:
        # Step 1: Process and clean (drops unwanted/banned/invalid emails)
        clean_leads = process_leads(input_file)
        
        if not clean_leads:
            print("No valid leads found to export.")
            return
            
        # Step 2: Save remaining cleaned leads to a dedicated new file
        export_cleaned_leads(clean_leads, cleaned_output_file)
        
        # Step 3: Batch and export
        # Split into batches (e.g., 3 for local testing, 50 for production)
        export_batches(clean_leads, output_folder, batch_size=3) 
        
        print(f"\nSuccess! Cleaned leads saved to '{cleaned_output_file}'.")
        print(f"Batches exported to '{output_folder}'.")
        print("Check 'sanitizer.log' to see which bad emails were dropped.")
        
    except SanitizerError as e:
        print(f"\nSYSTEM HALTED: {e}")
    except Exception as e:
        print(f"\nUNEXPECTED FATAL ERROR: {e}")

if __name__ == "__main__":
    main()
