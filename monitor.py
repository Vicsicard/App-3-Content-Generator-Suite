#!/usr/bin/env python3
"""
Simple Monitor Script for Content Generator Suite
"""

import sys
import time
from pathlib import Path
import subprocess
import colorama
from colorama import Fore, Style

# Initialize colorama
colorama.init()

def print_status(message: str, color: str = Fore.WHITE):
    """Print a colored status message."""
    print(f"{color}{message}{Style.RESET_ALL}")

def main():
    """Main monitoring function."""
    # Define paths
    base_dir = Path(__file__).parent
    output_dir = base_dir / "content_generator" / "output" / "app3"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Start content generator
    cmd = [
        sys.executable,
        "-m",
        "content_generator.content_generator",
        "--transcript",
        "input/transcript_chunks.md",
        "--style",
        "input/style-profile.md"
    ]
    
    print_status("Starting Content Generator...", Fore.CYAN)
    print_status(f"Output directory: {output_dir}", Fore.CYAN)
    print_status(f"Command: {' '.join(cmd)}\n", Fore.CYAN)
    
    # Run the process
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    try:
        while True:
            # Check if process has finished
            if process.poll() is not None:
                break
                
            # Check for new output
            output = process.stdout.readline()
            if output:
                print_status(output.strip(), Fore.WHITE)
                
            error = process.stderr.readline()
            if error:
                print_status(f"ERROR: {error.strip()}", Fore.RED)
            
            time.sleep(0.1)
            
        # Get any remaining output
        stdout, stderr = process.communicate()
        if stdout:
            print_status(stdout.strip(), Fore.WHITE)
        if stderr:
            print_status(f"ERROR: {stderr.strip()}", Fore.RED)
            
        # Print final status
        if process.returncode == 0:
            print_status("\nContent generation completed successfully!", Fore.GREEN)
        else:
            print_status(f"\nContent generation failed with code {process.returncode}", Fore.RED)
            
    except KeyboardInterrupt:
        print_status("\nMonitoring interrupted by user", Fore.YELLOW)
        process.terminate()
        return 1
        
    return process.returncode

if __name__ == "__main__":
    sys.exit(main())
