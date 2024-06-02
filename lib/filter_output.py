import gzip
import sys
import json

def extract_data(file_path):
    extracted_data = []
    try:
        with gzip.open(file_path, 'rb') as f:
            first_line = f.readline().decode('utf-8').strip()
            while not first_line:
                first_line = f.readline().decode('utf-8').strip()
            for line in f:
                line = line.decode('utf-8')
                line = line.strip()
                if not line:
                    continue
                entry = json.loads(line)
                extracted_entry = {
                    'ip_str': entry.get('ip_str', ''),
                    'port': entry.get('port', ''),
                    'transport': entry.get('transport', ''),
                    'product': entry.get('product', ''),
                    'version': entry.get('version',''),
                    'os': entry.get('os',''),
                    'org': entry.get('org', ''),
                    'hostnames': entry.get('hostnames', []),
                    'vulns': []
                }
                if 'vulns' in entry:
                    for vuln, details in entry['vulns'].items():
                        if 'CVE' in vuln and 'verified' in details:
                            extracted_entry['vulns'].append({vuln : f'verified: {details["verified"]}'})
                extracted_data.append(extracted_entry)
    except gzip.BadGzipFile as e:
        print("Errore durante la lettura del file:", e)
        sys.exit(1)
    return extracted_data

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py file.json.gz")
        sys.exit(1)
    file_path = sys.argv[1]
    extracted_data = extract_data(file_path)
    for entry in extracted_data:
        print(entry)
