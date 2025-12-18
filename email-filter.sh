#!/bin/sh

# 这里设置你的旧邮箱（错误的那个）
WRONG_EMAIL="4300917@qq.com"

# 这里设置你的新邮箱（正确的那个）
NEW_NAME="DawnTilDusk"
NEW_EMAIL="430066917@qq.com"

if [ "$GIT_COMMITTER_EMAIL" = "$WRONG_EMAIL" ]
then
    export GIT_COMMITTER_NAME="$NEW_NAME"
    export GIT_COMMITTER_EMAIL="$NEW_EMAIL"
fi
if [ "$GIT_AUTHOR_EMAIL" = "$WRONG_EMAIL" ]
then
    export GIT_AUTHOR_NAME="$NEW_NAME"
    export GIT_AUTHOR_EMAIL="$NEW_EMAIL"
fi
