MALICIOUS_PORTS = {

    22: "Known SSH Brute Force Activity",

    445: "SMB Exploitation Risk",

    3389: "RDP Attack Risk",

    80: "Web Attack Activity",

    443: "Encrypted Traffic Investigation"
}


def get_threat_intel(port):

    return MALICIOUS_PORTS.get(
        port,
        "No Intelligence Found"
    )