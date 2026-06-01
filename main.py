import argparse
import os

def load_wordlist(path):
    with open(path, "r") as f:
        return [line.strip() for line in f if line.strip()]

def check_url(url):
    # silent curl, only return HTTP status code
    cmd = f'curl -o /dev/null -s -w "%{{http_code}}" {url}'

    result = os.popen(cmd).read().strip()

    if result != "000":
        print(f"[FOUND] {url} -> HTTP {result}")
    else:
        print(f"[NOT FOUND] {url}")

def main():
    parser = argparse.ArgumentParser(description="Subdomain enum using curl")

    parser.add_argument(
        "-d",
        "--domain",
        required=True,
        help="Target domain (e.g. example.com)"
    )

    parser.add_argument(
        "-w",
        "--wordlist",
        required=True,
        help="Path to wordlist file"
    )

    parser.add_argument(
        "-p",
        "--prefix",
        action="store_true",
        help="Search extensions like .txt .html .php"
    )

    args = parser.parse_args()
    wordlist = load_wordlist(args.wordlist)

    for word in wordlist:

        # Extension mode
        if args.prefix:
            extensions = [".txt", ".html", ".php"]

            for ext in extensions:
                url = f"http://{args.domain}/{word}{ext}"
                check_url(url)

        # Subdomain mode
        else:
            url = f"http://{args.domain}/{word}"
            check_url(url)

if __name__ == "__main__":
    main()
