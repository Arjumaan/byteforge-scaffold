#!/usr/bin/env python3
"""
ByteForge CLI - The Command Line Interface for the ByteForge Security Platform.
Usage:
  python byteforge.py scan -u https://example.com -t nuclei
  python byteforge.py targets
  python byteforge.py report -id 1
"""
import argparse
import asyncio
import sys
import os
import json
from datetime import datetime

import argparse
import asyncio
import sys
import os
import json
from datetime import datetime

# Change CWD to backend so valid relative paths (like ./byteforge.db) work correctly
BACKEND_DIR = os.path.join(os.getcwd(), 'backend')
if os.path.exists(BACKEND_DIR):
    os.chdir(BACKEND_DIR)
    sys.path.append(os.getcwd()) # Add new CWD (backend) to path
else:
    # If we are already inside backend or similar, handle it
    sys.path.append(os.getcwd())

from app.db import engine, init_db # Import init_db to ensure tables exist if fresh run
from app.models import Target, Job, Finding
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession

# Import service runners
from app.services.nuclei_runner import run_nuclei
from app.services.crawl import run_crawl
from app.services.recon import run_subdomain_enum

# ANSI Colors
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_banner():
    print(rf"""{Colors.BLUE}
    ____        __       ______                       _____            ______     __    __
   / __ )__  __/ /____  / ____/___  _________ _____  / ___/_________ / __/ __/___/ /___/ /
  / __  / / / / __/ _ \/ /_  / __ \/ ___/ __ `/ _ \ \__ \/ ___/ __ `/ /_/ /_/ __  / __  / 
 / /_/ / /_/ / /_/  __/ __/ / /_/ / /  / /_/ /  __/___/ / /__/ /_/ / __/ __/ /_/ / /_/ /  
/_____/\__, /\__/\___/_/    \____/_/   \__, /\___//____/\___/\__,_/_/ /_/  \__,_/\__,_/   
      /____/                          /____/                                              
{Colors.ENDC}
{Colors.BOLD}ByteForge Scaffold CLI v1.0.0 - Enterprise Security Suite{Colors.BOLD}{Colors.ENDC}
    """)

async def list_targets():
    async with AsyncSession(engine) as session:
        result = await session.execute(select(Target))
        targets = result.scalars().all()
        
        print(f"\n{Colors.HEADER}=== Registered Targets ==={Colors.ENDC}")
        print(f"{'ID':<5} {'NAME':<30} {'SCOPE':<20} {'DATE':<20}")
        print("-" * 75)
        for t in targets:
            # We need to manually decrypt if strictly required, but for list view raw might be safer or decrypt explicitly
            # Note: t.decrypt_fields() is synchronous but uses cpu-bound crypto, safe enough here
            try:
                t.decrypt_fields()
            except:
                pass # Already decrypted or plain
                
            created_str = t.created_at.strftime('%Y-%m-%d') if t.created_at else "N/A"
            print(f"{t.id:<5} {t.name:<30} {t.scope:<20} {created_str}")
        print("")
    
    await engine.dispose()

async def add_target(url, scope):
    if not url.startswith("http"):
        url = "https://" + url
        
    async with AsyncSession(engine) as session:
        target = Target(name=url, scope=scope)
        target.encrypt_fields()
        session.add(target)
        await session.commit()
        await session.refresh(target)
        
        target.decrypt_fields()
        print(f"{Colors.GREEN}[+] Target added successfully: {target.name} (ID: {target.id}){Colors.ENDC}")
        await engine.dispose()
        return target.id

async def run_scan(target_identifier, scan_type):
    """
    Run a scan. target_identifier can be ID or URL.
    """
    target_id = None
    target_url = None

    async with AsyncSession(engine) as session:
        # Resolve target
        if target_identifier.isdigit():
            target = await session.get(Target, int(target_identifier))
            if target:
                target.decrypt_fields()
                target_id = target.id
                target_url = target.name
        else:
            # Search by name (needs decryption to match strictly, or just assume input matches decrypted)
            # This is complex with encryption. For CLI simplicity, we prioritize ID or exact encrypted match?
            # Creating a fresh target for ad-hoc scan is easier
            print(f"{Colors.WARNING}[!] 'scan' by URL via CLI temporarily creates a target or requires ID.{Colors.ENDC}")
            # Try to add it temporarily or find it? Let's just create it to be helpful.
            # But the user might want to scan an EXISTING target.
            # Simplified: Require ID or assume user knows what they are doing.
            target_url = target_identifier
            if not target_url.startswith("http"): target_url = "https://" + target_url
            # We assume ID 1 for ad-hoc if not found, or create new.
            # Let's search all and match (slow but functional for CLI)
            result = await session.execute(select(Target))
            all_targets = result.scalars().all()
            for t in all_targets:
                t.decrypt_fields()
                if t.name == target_url:
                    target_id = t.id
                    break
            
            if not target_id:
                print(f"{Colors.BLUE}[*] Target Not Found. Creating new target: {target_url}{Colors.ENDC}")
                new_t = Target(name=target_url, scope="ad-hoc")
                new_t.encrypt_fields()
                session.add(new_t)
                await session.commit()
                await session.refresh(new_t)
                target_id = new_t.id

    print(f"{Colors.BLUE}[*] Initializing {scan_type.upper()} scan for {target_url} (ID: {target_id})...{Colors.ENDC}")
    
    # Run the scan
    results = None
    if scan_type == 'nuclei':
        results = run_nuclei(target_id, target_url)
    elif scan_type == 'crawl':
        results = run_crawl(target_id, target_url)
    elif scan_type == 'recon':
        results = run_subdomain_enum(target_id, target_url)
    elif scan_type == 'full_scan':
        print(f"{Colors.BLUE}[*] Phase 1: Recon (Subdomain Enumeration){Colors.ENDC}")
        r1 = run_subdomain_enum(target_id, target_url)
        
        print(f"{Colors.BLUE}[*] Phase 2: Crawl (Spidering){Colors.ENDC}")
        r2 = run_crawl(target_id, target_url)
        
        print(f"{Colors.BLUE}[*] Phase 3: Nuclei (Vulnerability Scanning){Colors.ENDC}")
        r3 = run_nuclei(target_id, target_url)
        
        results = {
            "summary": "Full Scan Completed",
            "findings_count": r3.get('findings_count', 0),
            "recon": r1,
            "crawl": r2,
            "nuclei": r3
        }
    else:
        print(f"{Colors.FAIL}[!] Unknown scan type: {scan_type}{Colors.ENDC}")
        return

    print(f"{Colors.GREEN}[+] Scan Completed!{Colors.ENDC}")
    # Pretty print summary if possible
    print(json.dumps(results, indent=2, default=str)) # default=str handles datetime
    await engine.dispose()

def main():
    print_banner()
    parser = argparse.ArgumentParser(description="ByteForge CLI Security Tool")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # 'targets' command
    subparsers.add_parser("targets", help="List all registered targets")

    # 'add' command
    add_parser = subparsers.add_parser("add", help="Add a new target")
    add_parser.add_argument("-u", "--url", required=True, help="Target URL (e.g., https://example.com)")
    add_parser.add_argument("-s", "--scope", default="public", help="Scope (public, private, internal)")

    # 'scan' command
    scan_parser = subparsers.add_parser("scan", help="Run a security scan")
    scan_parser.add_argument("-t", "--target", required=True, help="Target URL or ID")
    scan_parser.add_argument("--type", choices=['nuclei', 'crawl', 'recon', 'full_scan'], default='nuclei', help="Type of scan")

    args = parser.parse_args()

    if args.command == "targets":
        asyncio.run(list_targets())
    elif args.command == "add":
        asyncio.run(add_target(args.url, args.scope))
    elif args.command == "scan":
        asyncio.run(run_scan(args.target, args.type))
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
