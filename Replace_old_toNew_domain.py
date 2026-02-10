import re , csv

def contains_domain(address, domain):
  domain_pattern= r"[\w\._]+@"+domain+r'$'
  if re.match(domain_pattern,address):
    return True
  return False

def replace_domain(address, old_domain, new_domain):
  if contains_domain(address,old_domain):
    address =re.sub(old_domain,new_domain,address)
  return address

def main():
    old_domain, new_domain = 'abc.edu', 'xyz.edu' 
    csv_file_loc="/home/student/data/user_emails.csv"
    v2_csv_file_loc="/home/student/data/v2_user_emails.csv"

    with open(csv_file_loc,newline='') as old:
      reader=csv.DictReader(old)
      with open(v2_csv_file_loc,'w',newline='') as new:
        writer=csv.DictWriter(new, fieldnames=reader.fieldnames)
        writer.writeheader()
        for row in reader:
            row[' Email Address'] = replace_domain(row[' Email Address'], old_domain, new_domain)
            writer.writerow(row)
main()

