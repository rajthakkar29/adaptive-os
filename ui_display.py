from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

def show_status(mode, risk, tier, folder_locked):

    table = Table(show_header=True, header_style="bold cyan")

    table.add_column("System Mode")
    table.add_column("Risk Score")
    table.add_column("Security Tier")
    table.add_column("Folder State")

    tier_color = {
        "Green": "green",
        "Yellow": "yellow",
        "Red": "red"
    }

    folder_state = "Locked" if folder_locked else "Unlocked"

    table.add_row(
        mode,
        f"{risk:.3f}",
        f"[{tier_color[tier]}]{tier}[/{tier_color[tier]}]",
        folder_state
    )

    console.clear()
    console.print(Panel(table, title="Context-Based Security Monitor"))