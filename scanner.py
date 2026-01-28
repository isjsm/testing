import requests
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import track
import time

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
    [bold yellow]--- Professional URL Scanner v1.0 ---[/bold yellow]
    """
    console.print(Panel(banner, subtitle="Created by Your Name", expand=False))

def scan_url(url):
    try:
        # إضافة http إذا لم تكن موجودة
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
            
        start_time = time.time()
        response = requests.get(url, timeout=10)
        end_time = time.time()
        
        status = response.status_code
        speed = round(end_time - start_time, 3)
        server = response.headers.get('Server', 'Unknown')
        
        # تحديد اللون حسب الحالة
        color = "green" if status == 200 else "yellow" if status in [301, 302] else "red"
        
        return [url, f"[{color}]{status}[/{color}]", f"{speed}s", server]
    except Exception as e:
        return [url, "[bold red]FAILED[/bold red]", "-", str(e)[:20]]

def main():
    print_banner()
    
    # طلب الروابط من المستخدم
    urls_input = console.input("[bold white]Enter URLs (separated by space): [/bold white]")
    urls = urls_input.split()

    table = Table(title="Scan Results", show_header=True, header_style="bold magenta")
    table.add_column("URL", style="dim")
    table.add_column("Status")
    table.add_column("Response Time")
    table.add_column("Server")

    if not urls:
        console.print("[red]No URLs provided![/red]")
        return

    # محاكاة فحص احترافي مع شريط تقدم
    for url in track(urls, description="Scanning..."):
        result = scan_url(url)
        table.add_row(*result)

    console.print("\n", table)

if __name__ == "__main__":
    main()
