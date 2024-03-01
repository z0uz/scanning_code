This Python script performs reconnaissance tasks on a target IP address. Here's a summary of what it does:
Subdomain Enumeration: It uses the amass tool to enumerate subdomains associated with the target IP address.
DNS Enumeration: It uses the dnsrecon tool to perform DNS enumeration, checking for zone transfer and resolving DNS records.
Basic Scan: It performs a basic Nmap scan (nmap -p <ports> -sV) on the target IP address, where <ports> are specified as a default set of common ports.
Full Scan: It performs a comprehensive Nmap scan (nmap -p <ports> -sV -sC -A -Pn) on the target IP address, where <ports> cover a wide range of ports.
Recommended Recon Commands: It executes a series of recommended reconnaissance commands using Nmap scripts on ports 80 and 443, such as checking HTTP titles, SSL certificates, and more.
Enumerating Open Ports and Services: It uses Nmap to enumerate open ports and services on the target IP address.
Performing DNS Enumeration: It utilizes dnsrecon to perform additional DNS enumeration tasks.
