import json
import random

# 1. Configuration
input_file = "optimized_records.json"  # Your source file
output_file = "optimized_records_sample.json"     # Where the sample will be saved
sample_size = 90

def generate_random_sample():
    try:
        # 2. Load the data
        with open(input_file, "r", encoding='utf-8') as f:
            all_records = json.load(f)
        
        # 3. Handle cases where the data is smaller than the requested sample size
        actual_sample_size = min(len(all_records), sample_size)
        
        print(f"Total records found: {len(all_records)}")
        print(f"Generating a sample of {actual_sample_size} records...")

        # 4. Pick random samples
        sampled_records = random.sample(all_records, actual_sample_size)

        # 5. Save the sample
        with open(output_file, "w", encoding='utf-8') as f:
            json.dump(sampled_records, f, indent=4, ensure_ascii=False)
            
        print(f"Success! Sample saved to '{output_file}'")

    except FileNotFoundError:
        print(f"Error: Could not find '{input_file}'")
    except json.JSONDecodeError:
        print(f"Error: '{input_file}' is not a valid JSON file.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    generate_random_sample()