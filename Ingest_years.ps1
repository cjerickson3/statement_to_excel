param(
    [Parameter(Position = 0, Mandatory = $true)]
    [int]$Year,

    [switch]$dbg
)

# Core settings
$script    = "statement_to_excel.py"
$dashboard = "Chase_Budget_Dashboard.xlsx"
$rules = "category_rules.csv"
$pdfFolder = "Chase_history"

Write-Host "=== Ingesting Chase PDFs for $Year ==="

# Gather all PDFs matching the year
$Years = "2018", "2019", "2020", "2021", "2022", "2023", "2024", "2025"
Write-Host $Years
foreach ($Year in $Years) {
$files = Get-ChildItem $pdfFolder -Filter "$Year*.pdf" | Sort-Object Name

if (-not $files) {
    Write-Host "No PDF statements found for $Year in $pdfFolder"
    exit
}

foreach ($file in $files) {
    Write-Host ""
    Write-Host "→ Processing $($file.Name)"

    # Build arguments for statement_to_excel.py
    $args = @(
        $file.FullName,
        "--dashboard", $dashboard,
        "--rules", $rules
    )

    if ($dbg) {
        $args += "--debug"
    }

    python $script @args
}}

Write-Host ""
Write-Host "=== Completed ingest for $Year ==="
