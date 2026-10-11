# 主题四笔记：约束 AI 编程行为的工程机制（guardrails）与工具

日期: 2026-10-11
原始材料: `research/raw/tools/`（12 篇归档）+ `research/raw/repos/`（本地挖掘 8 仓库）

一句话总纲（多方共识）: **"A system prompt is a request. A hook is a guarantee."** 强制性来自"约束住在上下文之外"——OS 沙箱 > 权限系统 > 钩子(exit 2) > CI 门禁 > 人工审批门 > lint 反馈环 > 流程 Skill > 规则文件/提示词（概率性，长会话必退化）。

---

## 1. OS 沙箱与权限最小化 —— 强制性: ★★★★★（物理层）
- 原理: 进程级隔离（macOS Seatbelt / Linux Landlock 类），限制文件访问、可执行命令、网络。不依赖模型听话。
- Codex: 默认沙箱跑本地任务；read-only / workspace-write（网络默认禁）/ danger-full-access 三档 + 审批策略（untrusted/on-failure/on-request/never）。
- 网络默认禁同时防依赖幻觉（slopsquatting）与数据外泄。
- 落地: agent 默认只读；写仅限工作区；装包/联网/出工作区 = 显式升级事件。
- 来源: https://developers.openai.com/codex/sandbox

## 2. 工具调用钩子（PreToolUse/PostToolUse 硬门）—— 强制性: ★★★★★（代码层）
- 原理: 宿主在工具调用前后执行本地程序；**exit 2 = 阻断**（stderr 回喂模型当理由），JSON 可精控 allow/deny/ask/defer、改写 updatedInput、PostToolUse block 回溯打断迫使模型改。onFailure:"block" 防钩子静默失效。
- Claude Code 事件面: PreToolUse/PostToolUse/PostToolUseFailure/Stop/UserPromptSubmit/PreCompact/SubagentStart...；Kiro 同构（PostFileSave/PreToolUse/Stop + Command/Agent 两类动作）。
- 反模式: exit 1 不拦、慢同步钩子、无终止条件的 Stop 循环、第三方钩子= postinstall 级风险。
- 落地: 破坏命令拦截（safety-net 语义解析命令，包一层/换旗标没用）；策略引擎（gryph: YAML 规则 block/warn/guide + SQLite 全量审计）；契约式（stop-that-shit: `$stop-that-shit review -- ...` 首行指令设契约，review=只读，Guard 机器强制）。
- 来源: https://code.claude.com/docs/en/hooks ; https://kiro.dev/docs/hooks/ ; https://hidekazu-konishi.com/entry/claude_code_hooks_complete_guide.html ; repos/{stop-that-shit, gryph, claude-code-safety-net, agent-guard}

## 3. 静态检查自动反馈环 —— 强制性: ★★★★（自动执行，但"便利非门禁"到"CI 拒绝"可调）
- 原理: lint/format 不指望模型记得跑，由钩子/CI 确定性执行。Biome/Ruff 无专门 agentic 模式，靠安全标志组合: safe-fix 默认/--unsafe 显式、--skip-parse-errors 容忍 agent 半成品、stdin/staged/changed 增量接口。
- 社区配方: PostToolUse 匹配 Write|Edit → 按扩展名跑 ruff/prettier/gofmt，exit 0（"formatting is a convenience, not a gate"）；Kiro: PostFileSave → `npx eslint --fix`。
- CI/pre-commit 是第二道: AI 未过 lint/测试的代码直接拒绝合并——真正的"拒绝"住在仓库层。
- Cursor 官方实践明确: **style 规则别写进规则文件，交给 linter**。
- 来源: https://biomejs.dev/reference/cli/ ; konishi 指南; https://cursor.com/docs/context/rules

## 4. 验证纪律（TDD + 完成前验证）—— 强制性: ★★★（提示性 Skill；挂上 Stop 钩子/CI 后升 ★★★★）
- 原理: 把"完成的定义"从模型自述改为外部证据。
- superpowers 两条铁律: "NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST"（没看到测试失败=不知道它测什么；先写码就删掉重来）；"NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE"（Gate: 识别证明命令→新鲜执行→读全输出→核对→才许 claim；"agent reports success"不算证据，diff 才算）。
- Spec Kit 同构: 验证三值裁决 verified/partial/failed，**missing verification 不算修复**；converge 循环直到 Converged。
- 配套钩子: Stop 钩子查未提交变更（带 marker 防死循环）。
- 来源: repos/superpowers ; https://github.com/github/spec-kit ; karpathy-skills PR197 IN-PRACTICE（rule file 见 raw/initial-links/）

## 5. 规格驱动开发（SDD）与阶段门 —— 强制性: ★★★（人工审批门 + 工件持久化）
- 原理: 需求不再只活在聊天历史；spec/design/tasks 变成可 review、可 diff 的 Markdown 工件，"先 what/why 后 how"。
- Spec Kit: constitution（项目原则一次成文）→ specify→plan→tasks→implement→converge，可选 checklist/一致性分析做质量门。Kiro: requirements(EARS 式验收标准)/design/tasks 三工件 + 每阶段 approval gates + 任务依赖图 wave 并行。OpenSpec: 更轻，propose（人审后再写码）→apply→archive（归档时合并回主 spec，防规格腐烂），刻意"no rigid phase gates"。
- 落地: 评审点放在**实现之前**是杠杆最大的人工门；convergence 循环替代"一次生成"。
- 来源: https://github.com/github/spec-kit ; https://kiro.dev/docs/specs/ ; https://github.com/Fission-AI/OpenSpec

## 6. 规则文件治理（AGENTS.md/CLAUDE.md/Cursor rules）—— 强制性: ★★（概率性）
- 原理: 常驻上下文的事实与约束。AGENTS.md 已是 Linux Foundation 旗下开放标准（60k+ 项目），"最近的文件优先"，60+ 工具兼容。
- 腐烂问题（Anthropic 官方承认）: "every team appends their own instructions and nothing gets deleted"；每行无论相关与否都耗 token；指令越多遵守越松。共识: CLAUDE.md <200 行、单规则 <500 行、linter 能管的不写、只在重复犯错处加规则、进 git 随演进删改。
- 注入风险: 规则文件=不可信输入（PackHallu 实验证明可经规则文件注入实施包替换攻击，跨模型可迁移）。
- 来源: https://agents.md/ ; https://claude.com/blog/steering-claude-code-skills-hooks-rules-subagents-and-more ; https://cursor.com/docs/context/rules ; https://arxiv.org/abs/2610.09264

## 7. 上下文工程（长会话质量维持）—— 强制性: ★★（纪律性）
- 原理: context rot 使长会话规则失效；对策是"最小高信号 token"+ 外置状态。
- 四件套: compaction（压缩重启+保留摘要/最近文件）、structured notes/agentic memory（NOTES.md 外置记忆，跨上下文重置延续）、subagent 隔离（脏上下文不进主线程，只回 1-2k token 摘要）、just-in-time 检索（存引用不存内容）。
- 关键推论: **凡是要在 compaction 后仍生效的约束，必须放在上下文之外**（hooks/权限/CI）——这正是"机制 vs 提示"的分界线。
- right altitude: 从最小提示开始，按观察到的失败追加指令（而非预防性堆规则）。
- 来源: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents

## 8. 供应链与安全护栏（secrets/依赖幻觉）—— 强制性: ★★★★（钩子+CI 双层）
- 依赖幻觉（slopsquatting）: 实证研究确认幻觉率随模型/语言/任务措辞变化，与 HumanEval 负相关，"models are not being optimized for secure code"；幻觉包名被抢注即攻击窗口。对策: lockfile 优先、新依赖=显式审批事件（白名单/registry 元数据校验）、沙箱断网、PreToolUse 拦包管理器命令、CI 扫 manifest diff。
- Secrets: agent-guard 拦 .env 读取、gitleaks 扫暂存、**拒绝 agent 用 --no-verify 绕过**；GitHub Push Protection 等 hosted 层兜底。
- 治理层: managed settings（组织级不可覆盖钩子/权限）= 企业 guardrail 的最终形态。
- 来源: https://arxiv.org/abs/2501.19012 ; repos/agent-guard ; hooks 文档

## 9. 通用输入/输出护栏框架 —— 强制性: ★★★★（代码层，但非编码场景主流）
- guardrails.ai: Input/Output Guards + 可组合验证器 Hub + 结构化输出生成；面向通用 LLM 应用。编码 agent 生态实际走 CLI hooks + 本地策略引擎路线，不用 hosted 框架。
- 来源: https://www.guardrailsai.com/docs

## 10. 反过度工程契约（stop-that-shit 的独特贡献）—— 强制性: ★★（Skill）/ ★★★★★（Guard 联动）
- SHIT 分类: Scope creep / Hypothetical hardening / Intent violation / Task thrashing。
- Stop Ladder: ①理解责任与边界→②直接方案优先（项目内/标准库/已装依赖）→③只为关闭具体缺口扩展→④按效果评判防御（检测什么、改变什么；保留有效防护，删冗余，修复吞错误的防护）→⑤验证后收工（复用仍有效的证据）。
- 工程细节值得学: 默认 unconfirmed 观察模式（须显式 arm 才拦，防误伤）；delegation ledger（子代理槽位并发账本）；未知工具保守阻断；**护栏自带 18 组 Bad/Good 判例回归测试**；同一指令"Skill=提示 / Guard=机器边界"双形态。
- 来源: repos/stop-that-shit

---

## 强制性排序共识（多来源交叉验证）
1. OS 沙箱（物理隔离） 2. 宿主权限系统 3. Hooks exit-2 阻断（onFailure:block） 4. CI/pre-commit 拒绝 5. 人工审批门（SDD 阶段门） 6. lint/format 自动反馈环（改行为不拦路径） 7. 流程 Skill/TDD 纪律 8. 规则文件/系统提示（概率性，长会话与注入下退化）
所有来源共同点: 确定性约束必须住在上下文之外；提示词只配做"请求"。

## 最值得吸收进中文 Skill 的机制（候选）
1. **验证证据门**: verification-before-completion 的 Gate Function + 三值裁决（"agent 自述成功"不算证据）——纯提示层即可落地，见效最快。
2. **Stop Ladder 反过度工程梯**: 直接方案→具体缺口→按效果评判防御——直接对治 AI 过度防御/范围蔓延，是"提高代码质量"的差异化内容。
3. **"Skill 提示 + 钩子强制"双层打包**: Skill 正文写判断标准，附带可安装的 hooks.json/PostToolUse lint 配方，声明哪些约束必须下放到钩子/CI（并诚实标注"Skill-only 不保证行为"——stop-that-shit 式边界声明）。

## 待追问线索
- Spec Kit 的 constitution/clarify 命令的具体提示词模板（需克隆 spec-kit 读 templates/commands）。
- 跨模型交叉 review（cross-model review）实践未找到扎实来源，需专门检索（如 "LLM cross review code quality" / Cursor bugbot 类产品）。
- diet1031/claude-code-infrastructure-showcase 的"钩子驱动 Skill 智能选择"机制；以及 awesome-claude-code 中 compass（cost-tiered subagents + guardrail hooks）值得深挖。
