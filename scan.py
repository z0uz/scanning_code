import subprocess
import sys
import shutil

def check_install_amass():
    """
    Check if amass is installed. If not, install it using the appropriate package manager.
    """
    if shutil.which("amass") is None:
        print("amass is not installed. Installing...")
        # Modify the following command based on your system's package manager (e.g., apt, yum, brew)
        subprocess.run(["apt", "install", "amass"])  # Example for Debian-based systems (Ubuntu)
        # If you're using macOS, you might use brew for installation
        # subprocess.run(["brew", "install", "amass"])
        # You may need to adjust this command based on your system's package manager
        print("amass has been installed successfully.")
    else:
        print("amass is already installed.")

def recon_recommendations(target_ip, basic_ports="21,22,25,53,80,110,135,139,143,443,445,1433,1521,3306,3389,5432,5900,8080,8443,9100", full_ports="1-10000"):
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
    subprocess.run(f"cat amass.txt | awk '{{print $2}}' | sort -u", shell=True)
    print()

    # Perform DNS enumeration
    print("[+] Performing DNS enumeration:")
    subprocess.run(f"dnsrecon -d {target_ip} -t axfr", shell=True)
    print()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python scanning.py <target_ip>")
        sys.exit(1)

    target_ip = sys.argv[1]
    check_install_amass()  # Check and install amass if necessary
    recon_recommendations(target_ip)
