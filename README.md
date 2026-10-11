# oh-my-repo

vibe-coding 调研工作区：大规模调研档案 + 从调研中从零构建的中文代码质量 Skill [vibe-quality](https://www.npmjs.com/package/vibe-quality)。

## 目录结构

| 目录/文件 | 内容 | 是否入库 |
|---|---|---|
| `vibe-quality/` | 最终 Skill：主入口 SKILL.md + 6 个子技能 + 扫描/自测脚本，npm 包根 | 是 |
| `research/SUMMARY.md` | 全部调研与交付产物的索引 | 是 |
| `research/notes/` | 各路检索的提炼笔记（9 份） | 是 |
| `research/knowledge/` | 带溯源的知识点清单（6 份，约 3300 条） | 是 |
| `research/integrated/` | 五域整合结果 + 主 agent 裁决记录 | 是 |
| `research/raw/` | 原始下载留档：17 个仓库克隆、约 120 篇文章、20 个讨论串（6200+ 文件） | 否（仅本地留档，见 .gitignore） |
| `repo-refactor/`、`repo-steward/` | 任务初始参考 Skill（repo-steward 为 MIT） | 是 |
| `discussion.txt`、`links.txt` | 任务初始讨论与种子链接 | 是 |

## 快速开始

```bash
# 安装 skill 到当前项目（发布后可用）
npx vibe-quality

# 本仓库内直接安装到用户级
node vibe-quality/bin/cli.js --global

# 脚本自测
python vibe-quality/scripts/selftest.py
```

用法与触发说法见 [vibe-quality/README.md](vibe-quality/README.md)；调研脉络见 [research/SUMMARY.md](research/SUMMARY.md)。

## 说明

- `research/raw/` 收录的是第三方公开内容（仓库快照、文章、讨论），仅作本地调研留档，避免再分发，故不入库；如需重建可按各文件头部记录的来源 URL 重新抓取。
- vibe-quality 的内容基于调研再创作，不包含源材料的原文搬运；引用的量化数据均带方法学限定。
