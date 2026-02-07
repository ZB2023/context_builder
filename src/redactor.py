import re


PATTERNS = {
    "API Key": re.compile(
        r'''(?:api[_-]?key|apikey|access[_-]?key)[\s]*[=:]\s*["']?([a-zA-Z0-9_\-]{16,})["']?''',
        re.IGNORECASE,
    ),
    "Secret": re.compile(
        r'''(?:secret|token|bearer)[\s]*[=:]\s*["']?([a-zA-Z0-9_\-]{16,})["']?''',
        re.IGNORECASE,
    ),
    "Password": re.compile(
        r'''(?:password|passwd|pwd)[\s]*[=:]\s*["']?([^\s"']{4,})["']?''',
        re.IGNORECASE,
    ),
    "Email": re.compile(
        r'[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}',
    ),
    "IPv4": re.compile(
        r'\b(?:\d{1,3}\.){3}\d{1,3}\b',
    ),
    "Private Key": re.compile(
        r'-----BEGIN\s+(?:RSA\s+)?PRIVATE\s+KEY-----',
    ),
    "AWS Key": re.compile(
        r'AKIA[0-9A-Z]{16}',
    ),
    "Connection String": re.compile(
        r'''(?:mongodb|postgres|mysql|redis)://[^\s"']+''',
        re.IGNORECASE,
    ),
}

REPLACEMENT = "***REDACTED***"


def redact_content(content, enabled_patterns=None):
    if enabled_patterns is None:
        enabled_patterns = list(PATTERNS.keys())

    redacted = content
    findings = []

    for name in enabled_patterns:
        pattern = PATTERNS.get(name)
        if pattern is None:
            continue

        matches = pattern.findall(redacted)
        if matches:
            findings.append({"pattern": name, "count": len(matches)})
            redacted = pattern.sub(REPLACEMENT, redacted)

    return redacted, findings


def redact_scan_result(scan_result, enabled_patterns=None):
    redacted_result = {
        "root": scan_result["root"],
        "structure": scan_result["structure"],
        "files": [],
        "skipped": scan_result["skipped"],
        "errors": scan_result["errors"],
    }

    total_findings = []

    for file_data in scan_result["files"]:
        redacted_content, findings = redact_content(
            file_data["content"], enabled_patterns
        )

        redacted_result["files"].append(
            {
                "path": file_data["path"],
                "encoding": file_data["encoding"],
                "content": redacted_content,
            }
        )

        if findings:
            total_findings.append(
                {"file": file_data["path"], "findings": findings}
            )

    return redacted_result, total_findings


def get_available_patterns():
    return list(PATTERNS.keys())