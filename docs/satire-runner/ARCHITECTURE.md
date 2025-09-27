# Satire Runner 项目架构说明

本说明文档概述 satire-runner 的目录结构、核心模块、状态机、渲染层、数据与控制流，以及本地预览与部署要点。内容与代码内的中文注释相互印证，便于维护与扩展。

## 目录结构

```
satire-runner/
├── index.html       # 单页入口，包含样式、Phaser 配置与全部游戏逻辑
├── you.png          # 玩家贴图
└── .vercel/         # （可选）Vercel 配置目录
```

项目采用“单文件 + 少量静态资源”的结构，便于快速预览与部署为静态站点。

## 核心模块与职责

- Phaser 场景（preload/create/update）
  - preload：加载 you.png 等资源。
  - create：初始化玩家/地面/HUD/输入绑定与图层（含 CSS 障碍容器），并根据 STATE.phase 控制生成器开关。
  - update：驱动游戏循环（移动、碰撞检测、分数与演出效果更新）。

- 生成器（仅在 STATE.phase === 'play' 生效）
  - spawnObstacle：Canvas 物理障碍。
  - spawnItem：加分/减分或效果道具。
  - spawnCssObstacle：CSS 文本型下落障碍（DOM 元素），营造“文本雨”。

- 碰撞检测与结算
  - checkCssCollisions：玩家与 DOM 障碍的近似矩形碰撞，更新 GPA 等指标。

- 演出与 UI
  - HUD 与提示：顶部提示文本，flashHUD 提供反馈闪烁。
  - 叠层：showOverlay 提供通用覆盖层（标题+副标题+关键词按钮）。
  - 结局对话：showEndingDialogue 保留大字标题，其余内容改为逐句点击推进，风格与开场一致。
  - 开场：showIntro 三段点击推进，gateTransition“大门打开”后进入可玩阶段。

- 重置与重开
  - resetGame：清理 CSS 障碍与图层、重置 STATE（GPA=2.0 等）、重新启动场景。
  - 关键词按钮：在结局对话最后出现，用于重开（“复读”“进组”）。

- 作弊与特殊流程
  - activateCheat（FREEDOM）：锁定 GPA=4.0 并提示后续难度（试玩阶段可选择不启用）。

## 状态机（STATE）

主要字段：
- phase：intro → play → success/fail（或 easter）
- gpa：绩点，影响玩家发光/变暗与结局触发
- elapsed/avoidedCount/cheatActive：计时、避障计数与作弊标记

结局触发条件：
- gpa < 1.0 → 失败（北京退学，关键词“复读”）
- gpa > 4.0 → 成功（新的内卷牢笼，关键词“进组”）
- gpa < 1.5 → 玩家整体变暗
- gpa > 3.5 → 玩家发光（模糊光晕）

## 渲染层与图层组织

- Canvas（Phaser）：玩家实体、地面与运动、HUD 文本、开场与结局演出。
- CSS Layer（DOM）：文字型下落障碍，绝对定位于游戏容器上方，独立于 Canvas 渲染；与玩家做近似矩形碰撞。

## 数据与控制流（简要）

1. 首次进入 → showIntro 三段对话 → gateTransition 转场 → STATE.phase=play
2. play 阶段：生成器按定时/随机产生 Canvas 与 CSS 障碍、物品；update 驱动移动与碰撞
3. GPA/计数根据碰撞与道具调整；达到阈值 → 进入 success/fail → showEndingDialogue 展示结局对话
4. 结局对话点击推进到最后一条，出现关键词按钮 → 点击触发 resetGame 重开

## 本地预览与部署

- 本地开发：
  - `npx --yes serve -l 5500 satire-runner`
  - 访问 `http://localhost:5500/`

- 线上托管（任一静态主机）：
  - Vercel / Cloudflare Pages / Netlify / GitHub Pages / Gitee Pages
  - 站点根指向 `satire-runner/` 目录即可。

## 修改建议与扩展方向

- 将 CSS 障碍的碰撞改为更精确的字形边界或 SVG 路径（目前为近似矩形）。
- 引入资源管理与多场景（例如单独的 IntroScene 和 PlayScene），减少单文件体积与耦合。
- 增加音效与自适应移动端触控手势。
- 提供国际化（i18n）文案文件，便于多语言。

如需更细致的内联注释，可参考 index.html 内的“项目架构总览”与各函数中文注释，并提出你希望重点解释的模块，我会进一步补充。