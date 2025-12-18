# 获取当前脚本所在目录的绝对路径
$ScriptDir = $PSScriptRoot
$FilterScript = "$ScriptDir\email-filter.sh"

# 将 Windows 路径转换为 Git Bash 兼容的路径格式 (例如 C:\Users -> /c/Users)
$GitPath = $FilterScript -replace '\\', '/'
$GitPath = $GitPath -replace '^([a-zA-Z]):', '/$1'

Write-Host "=========================================="
Write-Host "正在准备修复 Git 邮箱历史..."
Write-Host "脚本路径: $GitPath"
Write-Host "=========================================="

# 检查 git 是否可用
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Error "未找到 git 命令，请确保已安装 Git。"
    exit 1
}

# 执行 git filter-branch
# 注意：使用双引号包裹路径以防止空格问题
$EnvFilter = ". ""$GitPath"""

Write-Host "开始执行重写（这可能需要几分钟，取决于仓库大小）..."
git filter-branch --force --env-filter $EnvFilter --tag-name-filter cat -- --all

if ($LASTEXITCODE -eq 0) {
    Write-Host "=========================================="
    Write-Host "✅ 历史重写成功！"
    Write-Host "请使用 'git log' 检查提交记录是否已修正。"
    Write-Host "确认无误后，运行以下命令强制推送到远程："
    Write-Host "git push --force --all"
    Write-Host "=========================================="
} else {
    Write-Host "❌ 重写失败，请检查上方错误信息。"
}
