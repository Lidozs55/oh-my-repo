# vibe-coding 调研与 Skill 构建交付索引

日期：2026-10-11。本目录是「大规模调研 vibe-coding 资源并从零构建质量治理 Skill」任务的全部产物索引。

## 一、原始材料留档（阶段 1 产物）

`research/raw/` 共 6224 个文件：

- `raw/repos/`（17 个仓库克隆，均已去 .git）：stop-that-shit、pragmatic-clean-code-reviewer（smell-check）、superpowers、claude-plugins-official、anthropic-skills、mattpocock_skills、andrej-karpathy-skills、spec-kit、ap-vibe、awesome-claude-code、awesome-claude-skills、awesome-vibe-coding、agent-guard、claude-code-safety-net、gryph、move-code-quality-skill、trailofbits-skills-partial
- `raw/articles/`（约 120 篇，每篇头部含来源 URL 与抓取日期）：vibe coding 溯源与批评（Karpathy 推文、Wikipedia、Simon Willison×3、arXiv×5、媒体报道等）、AI 代码坏味道实证（GitClear、DORA、SO Survey、Qodo、USENIX 包幻觉等）、经典方法论（Fowler、Clean Code、PragProg、APSD、Google eng-practices、strangler fig 等）、followup 补档（跨模型评审实验、Veracode、CIQ、Mnilax 12 规则等）
- `raw/discussions/`（20 个讨论串）：HN×10、GitHub issues×5、Reddit、Cursor 论坛×2、掘金×2
- `raw/initial-links/`（6 个）：任务种子链接的抓取（含 issue 深挖）
- `raw/tools/`（16 篇）：hooks 官方参考、Spec Kit、OpenSpec、Kiro、AGENTS.md、codex-sandbox、cursor-rules、context engineering、biome、guardrails.ai、konishi 指南等

`research/notes/`（9 份检索笔记）：各路检索 agent 的提炼笔记（local-materials、seed-links、vibe-history、skills-ecosystem、ai-code-smells、guardrails-mechanisms、community-voices、methodology、followups）。

## 二、知识点清单（阶段 2 产物）

`research/knowledge/` 共 4243 行、约 3300 条带溯源的知识点：

- `01-repos-deep.md`（513 行）：17 个仓库中 26 个 skill/文件的精细提取
- `02-community-discussions.md`（987 行）：26 个讨论串约 900 条，含立场与赞数标注
- `03-methodology.md`（975 行）：26 个方法论来源 746 条
- `04-smells-and-tools.md`（670 行）：32 个来源 457+ 条
- `05-history-ecosystem-followup.md`（672 行）：31 个来源约 478 条
- `06-local-materials.md`（426 行）：本地两个 Skill 结构分析 + discussion.txt 逐行拆解 261 条

## 三、整合结果（阶段 3 产物）

`research/integrated/` 共 1498 行：

- `00-ADJUDICATIONS.md`：主 agent 对 25 项待裁决矛盾的最终裁决（24 条编号裁决 + Skill 世界观）
- `A-code-smells.md`（471 行）：62 条坏味道 11 分类 + 25 条量化数据（带方法学注记）
- `B-guardrails.md`（248 行）：强制性等级表 L0-L5 + 五层 18 条机制
- `C-methodology.md`（262 行）：review 母表 48 条 9 维度 + 重构纪律 + 手法梯队 + 验证方法
- `D-workflow.md`（205 行）：生命周期工作流 + 上下文管理 + 行为约束 + 多 agent 模式
- `E-skill-spec.md`（260 行）：Skill 写作统一规范 + 架构推荐 + 22 条反模式

## 四、最终 Skill（阶段 4/5 产物）

`vibe-quality/`（见其 README.md）：主入口 SKILL.md（105 行路由器+10 条红线+三场景动线）+ 6 个子技能（smells 坏味道目录 55 条 / audit 审计流程 / review 评审母表 8 维 38 条 / simplify 行为保持重构 14 手法 / workflow 三档流程 / guardrails 护栏与配方）+ 2 个零依赖脚本（quality_scan.py 扫描器 + selftest.py 自测 27 项）。经 3 轮审查-修复（规范一致性、内容质量、文档洁净度、反照抄、脚本复测）与最终验收，全中文、无源材料照抄。

## 脉络

初始材料（discussion.txt + links.txt + 两个本地 Skill）→ 8+2 路并行检索归档 → 8 路知识点提取 → 5 域整合 → 25 项矛盾裁决 → 7 路并行构建 → 3 轮审查修复 → 验收交付。
