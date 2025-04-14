#!/usr/bin/env python3
"""
Status Checker for Content Generator
Runs periodic checks every 5 minutes to monitor the content generator's progress
"""

import sys
import time
from pathlib import Path
import subprocess
import psutil
from datetime import datetime
import colorama
from colorama import Fore, Style

# Initialize colorama
colorama.init()

class StatusChecker:
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.output_dir = self.base_dir / "content_generator" / "output" / "app3"
        self.log_file = self.output_dir / "content_generator.log"
        self.last_file_count = 0
        self.last_log_size = 0
        self.start_time = datetime.now()
        self.process = None
        self.expected_files = [
            'output_blog.md',
            'output_show_notes.md',
            'output_newsletter.md',
            'output_social_posts.md',
            'output_bio.md',
            'output_ad_copy.md',
            'output_reputation.md',
            'output_website.md'
        ]

    def print_status(self, message: str, color: str = Fore.WHITE):
        """Print a colored status message with timestamp."""
        now = datetime.now()
        duration = now - self.start_time
        print(f"{color}[{duration.total_seconds():.1f}s] {message}{Style.RESET_ALL}")

    def start_generator(self):
        """Start the content generator process."""
        cmd = [
            sys.executable,
            "-m",
            "content_generator.content_generator",
            "--transcript",
            "input/transcript_chunks.md",
            "--style",
            "input/style-profile.md"
        ]
        
        self.print_status("Starting Content Generator...", Fore.CYAN)
        self.process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return self.process.pid

    def check_process_status(self, pid):
        """Check if the process is still running."""
        try:
            process = psutil.Process(pid)
            if process.status() == psutil.STATUS_ZOMBIE:
                return False, "Process is zombie"
            return True, f"Process is {process.status()}"
        except psutil.NoSuchProcess:
            return False, "Process not found"

    def check_file_progress(self):
        """Check progress of generated files."""
        current_files = list(self.output_dir.glob('*.md'))
        new_count = len(current_files)
        
        if new_count > self.last_file_count:
            new_files = [f.name for f in current_files if f.name not in self.expected_files]
            self.print_status(f"New files generated: {', '.join(new_files)}", Fore.GREEN)
            self.last_file_count = new_count
            
        return new_count, len(self.expected_files)

    def check_log_progress(self):
        """Check for new log entries and errors."""
        if not self.log_file.exists():
            return "No log file found"
            
        current_size = self.log_file.stat().st_size
        if current_size > self.last_log_size:
            with open(self.log_file, 'r') as f:
                f.seek(self.last_log_size)
                new_logs = f.read()
                
                errors = [line for line in new_logs.splitlines() if 'ERROR' in line]
                if errors:
                    return f"Found {len(errors)} new errors"
                    
                self.last_log_size = current_size
                return f"Log size increased by {current_size - self.last_log_size} bytes"
        return "No new log entries"

    def run_periodic_check(self, pid):
        """Run a single status check."""
        print("\n" + "="*50)
        now = datetime.now().strftime("%H:%M:%S")
        self.print_status(f"Status Check at {now}", Fore.CYAN)
        print("-"*50)
        
        # Check process
        is_running, status = self.check_process_status(pid)
        if not is_running:
            self.print_status(f"WARNING: {status}", Fore.RED)
            return False
        self.print_status(f"Process Status: {status}", Fore.GREEN)
        
        # Check files
        current, total = self.check_file_progress()
        self.print_status(f"File Progress: {current}/{total} files generated", Fore.CYAN)
        
        # Check logs
        log_status = self.check_log_progress()
        self.print_status(f"Log Status: {log_status}", Fore.CYAN)
        
        return True

    def run(self):
        """Main run loop."""
        # Create output directory
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Start the generator
        pid = self.start_generator()
        self.print_status(f"Content Generator started with PID: {pid}", Fore.GREEN)
        
        try:
            while True:
                if not self.run_periodic_check(pid):
                    self.print_status("Content Generator appears to have stopped. Investigation needed.", Fore.RED)
                    break
                    
                # Wait 5 minutes before next check
                self.print_status("Next check in 5 minutes...\n", Fore.YELLOW)
                time.sleep(300)  # 5 minutes
                
        except KeyboardInterrupt:
            self.print_status("\nMonitoring interrupted by user", Fore.YELLOW)
            if self.process:
                self.process.terminate()
            return 1
            
        return 0

def main():
    """Main entry point."""
    checker = StatusChecker()
    return checker.run()

if __name__ == "__main__":
    sys.exit(main())
