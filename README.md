# DawnTilDusk.github.io 站点说明

本仓库用于发布 GitHub Pages 网站，发布目录为 `docs/`。

注意事项：
- 仅 `docs/` 下的内容会被发布到网站。
- 非网站项目（如 RL、pong 等）请不要存放在本仓库中，以避免混淆与增大仓库体积。
- 自动发布已通过 GitHub Actions 配置（`.github/workflows/pages.yml`）。当 `docs/` 有变更并推送到 `main` 分支时会自动部署。

推荐的工作流（方案B）：
1. 在工作区根目录（非本仓库）开发源码：`satire-runner/`、`satire-man/`。
2. 运行根目录的 `deploy.ps1` 脚本，将上述源码同步复制到本仓库的 `docs/`，并自动提交推送。
3. 等待 GitHub Actions 发布完成后访问：
   - 主页：https://DawnTilDusk.github.io/
   - 示例页面：https://DawnTilDusk.github.io/satire-runner/

维护建议：
- 若需添加新的公开页面或项目，请在工作区根目录创建对应目录并通过部署脚本同步到 `docs/`。
- 如需在本仓库忽略某些非 `docs/` 内容，可在未来添加 `.gitignore` 进行限制（当前不做强限制，按需再配置）。