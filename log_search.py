import sys, re, csv, operator, os

# Get CLI args: [1] is the log source, [2] is the destination folder
log_file, out_dir = sys.argv[1], sys.argv[2]
os.makedirs(out_dir, exist_ok=True) 

# Standard dicts: we'll handle missing keys on the fly during the loop
errors_dict, users_dict = {}, {}

# Regex: captures the error message and the user in parentheses
err_pat = r'ERROR ([\w ]*) \(([^)]+)\)'
inf_pat = r'INFO .* \(([^)]+)\)'

with open(log_file) as f:
    for line in f:
        # Check for ERROR logs; update error tally and user stats
        err_match = re.search(err_pat, line)
        if err_match:
            msg, user = err_match.group(1), err_match.group(2)
            errors_dict[msg] = errors_dict.get(msg, 0) + 1
            users_dict.setdefault(user, {"INFO": 0, "ERROR": 0})["ERROR"] += 1
        else:
            # If not an error, check for INFO logs to log user activity
            inf_match = re.search(inf_pat, line)
            if inf_match:
                user = inf_match.group(1)
                users_dict.setdefault(user, {"INFO": 0, "ERROR": 0})["INFO"] += 1

# Sort errors by count (descending) and users by name (alphabetical)
err_sorted = sorted(errors_dict.items(), key=operator.itemgetter(1), reverse=True)
usr_sorted = sorted(users_dict.items())

# Export Error Report: ranking of the most common ways the system died
with open(os.path.join(out_dir, 'errors.csv'), 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Error', 'Count'])
    writer.writerows(err_sorted)

# Export User Report: breakdown of INFO vs ERROR counts per user
with open(os.path.join(out_dir, 'users.csv'), 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Username', 'INFO', 'ERROR'])
    for user, counts in usr_sorted:
        writer.writerow([user, counts['INFO'], counts['ERROR']])

