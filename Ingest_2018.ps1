# --- Ingest_2018.ps1 ---
param([int]$Year = 2018)

Write-Host "=== Processing Chase statements for $Year ==="

$scriptDir  = Split-Path -Parent $MyInvocation.MyCommand.Definition
$historyDir = Join-Path $scriptDir "Chase_history"
$pythonExe  = "python"
$scriptPath = Join-Path $scriptDir "statement_to_excel.py"

$pdfFiles = Get-ChildItem -Path $historyDir -Filter "$Year*.pdf" | Sort-Object Name
if (-not $pdfFiles) {
    Write-Host "No PDF files found for $Year in $historyDir"
    exit
}

foreach ($pdf in $pdfFiles) {
    Write-Host "-> Processing $($pdf.Name)..."

    $args = @(
        $pdf.FullName,
        "--rules", "category_rules.txt",
        "--dashboard", "Chase_Budget_Dashboard.xlsx",
        "--debug"
    )

    & $pythonExe $scriptPath @args
    if ($LASTEXITCODE -ne 0) {
        Write-Host "WARNING: Error processing $($pdf.Name)"
    } else {
        Write-Host "Done $($pdf.Name)"
    }
}

Write-Host "=== Completed processing for $Year ==="
