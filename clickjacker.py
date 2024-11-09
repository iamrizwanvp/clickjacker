import requests
import argparse
from colorama import Fore, Style, init

# Initialize colorama for Windows compatibility
init()

def check_clickjacking(subdomain):
    try:
        response = requests.get(subdomain, timeout=5)
        headers = response.headers

        # Set default color and message for protected subdomains
        color = Fore.WHITE
        protection_status = f"{subdomain} - Protected"

        # Check for X-Frame-Options and Content-Security-Policy headers
        if 'X-Frame-Options' in headers:
            protection_status += f" (X-Frame-Options: {headers['X-Frame-Options']})"
        elif 'Content-Security-Policy' in headers and "frame-ancestors" in headers['Content-Security-Policy']:
            protection_status += f" (Content-Security-Policy: {headers['Content-Security-Policy']})"
        else:
            # Vulnerable to clickjacking
            color = Fore.RED
            protection_status = f"{subdomain} - Vulnerable to Clickjacking!"

        # Display results in a "box"
        print(f"{color}{'='*40}")
        print(protection_status)
        print(f"{'='*40}{Style.RESET_ALL}\n")

    except requests.RequestException as e:
        print(f"{Fore.WHITE}{'='*40}")
        print(f"{subdomain} - Error: {e}")
        print(f"{'='*40}{Style.RESET_ALL}\n")

def main(input_file):
    try:
        with open(input_file, 'r') as file:
            subdomains = file.read().splitlines()
        
        for subdomain in subdomains:
            if not subdomain.startswith('http'):
                subdomain = 'http://' + subdomain  # Default to HTTP if scheme is missing
            check_clickjacking(subdomain)
    
    except FileNotFoundError:
        print("Error: File not found. Please check the file path.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Clickjacking vulnerability checker")
    parser.add_argument("-i", "--input", help="Path to file with list of live subdomains", required=True)
    args = parser.parse_args()
    
    main(args.input)

