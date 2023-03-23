# Define input parameters
param(
    [Parameter(Mandatory=$true)]
    [string]$UserName,

    [Parameter(Mandatory=$true)]
    [string]$EmailAddress,

    [Parameter(Mandatory=$true)]
    [string]$Department,

    [Parameter(Mandatory=$true)]
    [string]$JobTitle,

    [Parameter(Mandatory=$true)]
    [SecureString]$Password
)

# Validate input parameters
if (-not ($UserName -and $EmailAddress -and $Department -and $JobTitle -and $Password)) {
    throw "Missing required input parameter(s)"
}

# Check if user already exists in Active Directory
$user = Get-ADUser -Filter {samAccountName -eq $UserName} -ErrorAction SilentlyContinue
if ($user) {
    Write-Host "User $UserName already exists in Active Directory"
    return
}

# Generate secure password
$securePassword = ConvertTo-SecureString -String $Password -AsPlainText -Force

# Create new user account in Active Directory
New-ADUser -Name $UserName -SamAccountName $UserName -UserPrincipalName "$UserName@yourdomain.com" -EmailAddress $EmailAddress -Department $Department -Title $JobTitle -AccountPassword $securePassword -Enabled $true

# Add user to appropriate groups based on department and job title
$groupNames = @()
if ($Department -eq "Sales") {
    $groupNames += "Sales Group"
} elseif ($Department -eq "Marketing") {
    $groupNames += "Marketing Group"
}

if ($JobTitle -eq "Manager") {
    $groupNames += "Managers Group"
}

foreach ($groupName in $groupNames) {
    Add-ADGroupMember -Identity $groupName -Members $UserName
}

# Email the user their password
$smtpServer = "smtp.yourdomain.com"
$fromAddress = "admin@yourdomain.com"
$toAddress = $EmailAddress
$subject = "Your new user account information"
$body = "Dear $UserName,<br><br>Your new user account has been created. Your temporary password is: $Password.<br><br>Please log in to the system and change your password as soon as possible.<br><br>Best regards,<br>The Admin Team"

$smtp = New-Object Net.Mail.SmtpClient($smtpServer)
$msg = New-Object Net.Mail.MailMessage($fromAddress, $toAddress, $subject, $body)
$msg.IsBodyHtml = $true
$smtp.Send($msg)

# Log all actions to a centralized log file
$logFilePath = "C:\Logs\AccountCreation.log"
$logMessage = "$(Get-Date) - User account $UserName created by $($env:USERNAME)"
Add-Content -Path $logFilePath -Value $logMessage

Write-Host "User account $UserName has been created successfully"
