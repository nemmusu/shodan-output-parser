# Shodan Wrapper and Results Filter

This repository contains a script to download search results from Shodan and filter specific fields from the results. The script extracts and simplifies the output, keeping only essential information. Additionally, it allows you to save the results in a JSON file and print detailed entries. The full JSON result from Shodan is always downloaded and saved locally in a GZIP compressed format.

## Requirements
- Shodan API key
- Python 3.x
- Shodan CLI

## Installation

1. Install the Shodan CLI if you haven't already:

    ```sh
    pip install shodan
    ```

2. Clone this repository:

    ```sh
    git clone https://github.com/nemmusu/shodan-wrapper.git
    cd shodan-wrapper
    ```

## Usage

### Downloading and Filtering Shodan Results

The main script `shodan_wrapper.py` wraps the Shodan download command and filters the results based on specified fields.

#### Command Line Arguments

- `filename`: Name of the file to save the search results (file .json.gz)
- `search_query`: Search query (e.g., "org: organization", "ip: 8.8.8.8" or "ip: 8.8.0.0-8.8.255.255, "hostname: example.com")
- `--limit`: Maximum number of results to download (optional)
- `-j, --json`: Save the results in a JSON file (optional)
- `-v, --verbose`: Print detailed extracted entries (optional)

### Example

```sh
python shodan_wrapper.py results "org: yourorganization" --limit 100 -j -v
```

## Screenshots

Help:

![help](https://github.com/nemmusu/shodan-output-parser/blob/main/doc/img/help.png)

JSON output:
![json](https://github.com/nemmusu/shodan-output-parser/blob/main/doc/img/json_file.png)

Log file:
![log](https://github.com/nemmusu/shodan-output-parser/blob/main/doc/img/log_file.png)

Verbose:
![verbose](https://github.com/nemmusu/shodan-output-parser/blob/main/doc/img/verbose.png)