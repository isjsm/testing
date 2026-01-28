import requests
import re
import time
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import track

console = Console()

def print_banner():
    banner = """
    [bold cyan]
     _    _ _____  _      _____                                 
    | |  | |  __ \| |    / ____|                                
    | |  | | |__) | |   | (___   ___ __ _ _ __  _ __   ___ _ __ 
    | |  | |  _  /| |    \___ \ / __/ _` | '_ \| '_ \ / _ \ '__|
    | |__| | | \ \| |________) | (_| (_| | | | | | | |  __/ |   
     \____/|_|  \_\______|_____/ \___\__,_|_| |_|_| |_|\___|_|   
    [/bold cyan]
    [bold yellow]--- Advanced Mass Scanner & Logger v2.0 ---[/bold yellow]
    """
    console.print(Panel(banner, subtitle="Developed for Moath", expand=False))

def extract_links(url):
    """استخراج جميع الروابط من صفحة واحدة"""
    try:
        response = requests.get(url, timeout=5)
        # البحث عن أي نص يبدأ بـ http أو https
        links = re.findall(r'(https?://[^\s<>"]+|www\.[^\s<>"]+)', response.text)
        return list(set(links)) # إزالة التكرار
    except:
        return []

def scan_url(url):
    try:
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        start_time = time.time()
        response = requests.get(url, timeout=5)
        end_time = time.time()
        
        status = response.status_code
        speed = round(end_time - start_time, 3)
        color = "green" if status == 200 else "yellow" if status in [301, 302] else "red"
        
        result = [url, f"[{color}]{status}[/{color}]", f"{speed}s"]
        
        # حفظ في الملف
        with open("results.txt", "a") as f:
            f.write(f"URL: {url} | Status: {status} | Time: {speed}s\n")
            
        return result
    except:
        return [url, "[bold red]ERROR[/bold red]", "-"]

def main():
    print_banner()
    
    target = console.input("[bold white]Enter Target URL to scrape & scan: [/bold white]")
    
    with console.status("[bold green]Extracting links..."):
        found_links = extract_links(target)
    
    if not found_links:
        console.print("[red]No links found or target unreachable![/red]")
        return

    console.print(f"[bold blue]Found {len(found_links)} links. Starting Mass Scan...[/bold blue]\n")

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Detected URL", style="dim", width=50)
    table.add_column("Status")
    table.add_column("Speed")

    # مسح محتوى ملف النتائج القديم
    with open("results.txt", "w") as f:
        f.write(f"--- Scan Results for {target} ---\n")

    for link in track(found_links, description="Processing..."):
        res = scan_url(link)
        table.add_row(*res)

    console.print("\n", table)
    console.print(Panel(f"[bold green]Scan Completed![/bold green]\nResults saved to: [yellow]results.txt[/yellow]"))

if __name__ == "__main__":
    main()
