#!/bin/bash

# 确保脚本在遇到错误时停止
set -e

# 获取脚本所在的绝对路径
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
FILTER_SCRIPT="$SCRIPT_DIR/email-filter.sh"

echo "=========================================="
echo "正在准备修复 Git 邮箱历史..."
echo "规则脚本: $FILTER_SCRIPT"
echo "=========================================="

if [ ! -f "$FILTER_SCRIPT" ]; then
    echo "错误: 未找到 email-filter.sh 文件！"
    echo "请确保该文件与本脚本在同一目录下。"
    exit 1
fi

# 确保规则脚本有执行权限
chmod +x "$FILTER_SCRIPT"

echo "开始执行历史重写（这可能需要几分钟）..."

# 使用 git filter-branch 执行重写
# 注意：我们使用 source (.) 来在当前 shell 上下文中执行规则脚本
git filter-branch --force --env-filter ". \"$FILTER_SCRIPT\"" --tag-name-filter cat -- --all

echo "=========================================="
echo "✅ 历史重写成功！"
echo "请使用 'git log' 检查提交记录是否已修正。"
echo "确认无误后，运行以下命令强制推送到远程："
echo "git push --force --all"
echo "=========================================="
