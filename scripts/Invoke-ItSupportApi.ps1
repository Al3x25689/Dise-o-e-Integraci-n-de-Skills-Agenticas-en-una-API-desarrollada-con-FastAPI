[CmdletBinding(DefaultParameterSetName = 'Get')]
param(
    [Parameter(Mandatory, ParameterSetName = 'Get')]
    [ValidateSet('/health', '/tickets/categories', '/tickets/priorities')]
    [string]$Path,

    [Parameter(Mandatory, ParameterSetName = 'Analyze')]
    [hashtable]$Ticket,

    [ValidateRange(1, 65535)]
    [int]$Port = 8000
)

$ErrorActionPreference = 'Stop'
$python = Join-Path (Split-Path -Parent $PSScriptRoot) '.venv\Scripts\python.exe'
$client = Join-Path $PSScriptRoot 'it_support_client.py'
if ($PSCmdlet.ParameterSetName -eq 'Analyze') {
    $json = ConvertTo-Json -InputObject $Ticket -Compress
    $encoded = [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($json))
    $result = $encoded | & $python $client analyze --port $Port
}
else {
    $operation = ($Path -split '/')[-1].ToLowerInvariant()
    $result = & $python $client $operation --port $Port
}

if ($LASTEXITCODE -ne 0) {
    throw "Error del cliente de IT Support API (codigo $LASTEXITCODE)."
}
ConvertFrom-Json -InputObject $result
