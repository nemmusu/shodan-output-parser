import argparse
import subprocess
from lib import filter_output
import json

def shodan_download(filename, search_query, limit=None):
    command = ['shodan', 'download']
    if limit is not None:
        command.append('--limit')
        command.append(str(limit))
    command.append(filename)
    command.append(search_query)
    subprocess.run(command)

def main():
    parser = argparse.ArgumentParser(description="Wrapper for the Shodan download command")
    parser.add_argument('filename', help='Name of the file to save the search results (file .json.gz)')
    parser.add_argument('search_query', help='Search query (e.g., "org: organization", "ip: 7.7.7.7", "hostname: example.com")')
    parser.add_argument('--limit', type=int, help='Maximum number of results to download')
    parser.add_argument('-j', '--json', action='store_true', help='Save the results in a JSON file')
    parser.add_argument('-v', '--verbose', action='store_true', help='Print detailed extracted entries')
    args = parser.parse_args()
    shodan_filename = f"download/{args.filename}"
    shodan_filename_ext = f"download/{args.filename}.json.gz"
    args.filename = f"output/{args.filename}"
    shodan_download(shodan_filename, args.search_query, args.limit)
    extracted_data = filter_output.extract_data(shodan_filename_ext)
    with open(args.filename + "_details.log", 'w') as f:
        for entry in extracted_data:
            f.write("IP: {}\n".format(entry['ip_str']))
            f.write("Port: {}\n".format(entry['port']))
            f.write("Protocol: {}\n".format(entry['transport']))
            try:
                if entry["product"]:
                    try:
                        if entry["version"]:
                            f.write("Version: {} {}\n".format(entry['product'], entry['version']))
                    except KeyError:
                        f.write("Product: {}\n".format(entry['product']))
            except KeyError:
                    pass
            try:
                if entry["os"]:
                    f.write("OS: {}\n".format(entry['os']))
            except KeyError:
                pass
            f.write("Organization: {}\n".format(entry['org']))
            f.write("Hostnames:\n")
            for hostname in entry['hostnames']:
                f.write("- {}\n".format(hostname))
            if entry['vulns']:
                f.write("Vulnerabilities:\n")
                for vuln_dict in entry['vulns']:
                    for vuln, details in vuln_dict.items():
                        f.write("- {} > {}\n".format(vuln, details))
            f.write("\n")
    if args.verbose:
        for entry in extracted_data:
            print("IP:", entry['ip_str'])
            print("Port:", entry['port'])
            print("Protocol: {}".format(entry['transport']))
            try:
                if entry["product"]:
                    try:
                        if entry["version"]:
                            print("Version: {} {}".format(entry['product'], entry['version']))
                    except KeyError:
                        print("Product: {}".format(entry['product']))
            except KeyError:
                    pass
            try:
                if entry["os"]:
                    print("OS: {}".format(entry['os']))
            except KeyError:
                pass
            print("Organization:", entry['org'])
            print("Hostnames:")
            for hostname in entry['hostnames']:
                print("-", hostname)
            if entry['vulns']:
                print("Vulnerabilities:")
                for vuln_dict in entry['vulns']:
                    for vuln, details in vuln_dict.items():
                        print("-", vuln, ">", details)
            print()
    if args.json:
        with open(args.filename + "_filtered.json", 'w') as f:
            json.dump(extracted_data, f, indent=2)

if __name__ == "__main__":
    main()