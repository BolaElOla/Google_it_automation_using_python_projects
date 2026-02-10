import re,csv,sys,os

def contains_domain(address, domain):
    # Regex to check if the email ends with the specific domain
    domain_pattern = r"[\w\._]+@" + domain + r'$'
    if re.match(domain_pattern, address):
        return True
    return False

def replace_domain(address, old_domain, new_domain):
    # Swaps the old domain for the new one if a match is found
    if contains_domain(address, old_domain):
        address = re.sub(old_domain, new_domain, address)
    return address

def main():
    # Basic check to ensure you provided enough arguments (Input, Output, OldDomain, NewDomain)
    if len(sys.argv) < 5:
        print("Usage: python script.py <input_csv> <output_csv> <old_domain> <new_domain>")
        sys.exit(1)

    csv_file_loc = sys.argv[1]
    v2_csv_file_loc = sys.argv[2]
    old_domain = sys.argv[3]
    new_domain = sys.argv[4]

    # Check if input file exists so we don't crash and burn
    if not os.path.exists(csv_file_loc):
        print(f"Error: The file '{csv_file_loc}' implies it exists... but it doesn't.")
        sys.exit(1)

    with open(csv_file_loc, newline='') as old:
        reader = csv.DictReader(old)
        with open(v2_csv_file_loc, 'w', newline='') as new:
            writer = csv.DictWriter(new, fieldnames=reader.fieldnames)
            writer.writeheader()
            for row in reader:
                # Watch out: ' Email Address' has a space in your original code, keep it matching your CSV header!
                row[' Email Address'] = replace_domain(row[' Email Address'], old_domain, new_domain)
                writer.writerow(row)

if __name__ == "__main__":
    main()