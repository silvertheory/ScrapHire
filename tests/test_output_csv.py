import os
from pathlib import Path
import subprocess
import sys


def test_scraper_creates_csv():
    """
    Portfolio test: verifies the scraper runs and creates the expected CSV output.
    """

    project_root = Path(__file__).resolve().parents[1]
    script_path = project_root / "src" / "scrapehire.py"
    output_csv = project_root / "data" / "scrapehire_jobs.csv"

    # Remove old output if it exists so the test is deterministic
    if output_csv.exists():
        output_csv.unlink()

    # Run the scraper as a subprocess using the current Python interpreter
    result = subprocess.run(
        [sys.executable, str(script_path)],
        cwd=str(project_root),
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"Scraper failed:\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
    assert output_csv.exists(), "Expected output CSV was not created in data/."
    assert output_csv.stat().st_size > 0, "Output CSV exists but is empty."