# vibe-quality

治理 AI 生成代码与低质量代码的中文 Skill：主入口（路由表 + 红线）带 6 个子技能文件与 2 个脚本（扫描与自测，零第三方依赖），把代码体检、独立评审、行为保持重构、质量工作流、护栏治理变成带证据、可追溯的流程。

## 目录结构

```
vibe-quality/
├── SKILL.md                # 主入口：路由表 + 红线
├── references/
│   ├── audit.md            # 代码体检：带证据的问题清单
│   ├── smells.md           # 55 条 AI 代码坏味道目录
│   ├── simplify.md         # 行为保持的简化与重构
│   ├── workflow.md         # 质量优先工作流（三档流程）
│   ├── review.md           # 独立评审与四值判定
│   └── guardrails.md       # hooks / CI / 规则文件护栏
├── scripts/
│   ├── quality_scan.py     # 机械证据收集器（仅标准库）
│   └── selftest.py         # 脚本一键自测
└── bin/
    └── cli.js              # npm 安装器（npx vibe-quality）
```

## 安装

方式一，npm 安装器（发布到 npm 后可用）：

```bash
# 在项目根目录执行，装到项目级 .agents/skills/
npx vibe-quality

# 装到用户级，所有项目可用
npx vibe-quality --global

# 装到指定目录
npx vibe-quality --dir /path/to/skills
```

方式二，skills CLI（装到 Claude Code、Cursor 等 75+ agent）：

```bash
# 从 npm registry 的 tarball 安装（版本号随发布更新）
npx skills add https://registry.npmjs.org/vibe-quality/-/vibe-quality-1.0.0.tgz

# 或从 GitHub 仓库安装（若已推送）
npx skills add Lidozs55/oh-my-repo --skill vibe-quality
```

方式三，手动复制：把整个 `vibe-quality/` 目录复制到任一位置（目录名不可改，须与 frontmatter `name` 一致）：

- 用户级：`~/.agents/skills/vibe-quality/`
- 项目级：项目下 `.agents/skills/` 或 `.zcode/skills/` 里

## 怎么用（触发说法示例）

- 「帮我体检一下这坨 AI 生成的代码」
- 「这段代码太膨胀了，重构清理一下，但别改行为」
- 「评审一下 agent 刚写的这个 diff，测试是不是假绿」

## 脚本自测

```bash
python scripts/selftest.py        # 或在包目录内 npm test
```

## 许可

MIT，见 LICENSE。
