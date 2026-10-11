# 知识域 B 整合：约束 AI 行为的工程机制 / 护栏 / 工具

> 阶段 3 整合产物。输入：04-smells-and-tools、01-repos-deep、05-history-ecosystem-followup、02-community-discussions。
> 整合规则：同机制合并、五层分类、统一强制性等级、裁决矛盾、剔除纯安装说明与重复内容。
> 日期：2026-10-11。

---

## 0. 强制性等级表（跨来源共识排序）

多来源对"强制性"有不同表述，合并为统一六级表（L0 最高）。每级定义：**该层失效不依赖模型是否"愿意"遵守**。

| 等级 | 名称 | 机制本质 | 失效条件 | 来源表述 |
|---|---|---|---|---|
| L0 | 进程/物理级 | OS 沙箱（Seatbelt/Landlock）、网络隔离、容器无凭据 | 内核级突破 | Codex sandboxing 文档："进程层面强制"；adzicg Docker 实践（02） |
| L1 | 组织管理级 | managed settings / allowManagedHooksOnly，用户不可覆盖 | 管理员失职 | Claude Code hooks 官方参考（04）；Konishi 反模式 7（04） |
| L2 | 会话工具级阻断 | PreToolUse exit 2 / permissionDecision=deny / 权限系统 deny / CI 拒绝合并 / git pre-commit 拒绝 | hook 超时（不阻断）、compaction 后被降权、fail-open 配置错误 | 官方 exit 2（04）；Konishi "hook is a guarantee"（04）；yurukusa "物理上阻止动作"（02）；durban01（02） |
| L3 | 确定性反馈环 | lint/测试/扫描在环内自动运行、PostToolUse block 回喂、converge 收敛报告 | 模型收到反馈仍不修（可再迭代）；不阻止坏代码产生 | spec-kit "机器强制互补"（04）；Biome 泛化结论（04）；Anthropic steering（04） |
| L4 | 流程门 | SDD 阶段门、宪法 GATE、人审批准点、checklist STOP | 依赖 agent 遵循命令流程 + 人在环 | spec-kit 评估"过程性门禁（probabilistic + 人工审批）"（04）；OpenSpec"人在实现前审批 plan"（04） |
| L5 | 概率性指令 | CLAUDE.md / AGENTS.md / rules / Skill 正文 | 长会话退化、注意力稀释、token 压力、prompt injection | Anthropic steering "指令是错误的工具"（04）；官方 advisory ~80%（05-Mnilax 转）；issue #2544 全链证据（02） |

**排序裁决依据**：Anthropic steering 博客（确定性→hooks、事实→CLAUDE.md）与 Konishi 金句（"A system prompt is a request. A hook is a guarantee."）给出 L2 vs L5 的二分；Codex sandboxing 补上 L0（"行为约束最终要落到进程边界而非措辞"）；spec-kit 自我评估确认 L4 是 probabilistic；context engineering 论文补上 L5 退化的物理原因（context rot）。社区 issue #2544/#27242 提供了 L2 与 L5 的实测失效证据（见各条目"局限"）。

**使用原则（多来源一致）**：一个约束放哪层，取决于"它绝对不能发生吗"——绝对不能→L0-L2；发生了要立刻被纠正→L3；流程性把关→L4；只是偏好与事实→L5。判断类内容永远无法上 L2（见待裁决 1）。

---

## 一、强制层（确定性执行）

### B1. OS 沙箱与网络隔离（L0）

- **原理**：agent 的行为约束最终要落到进程边界而非措辞。OS 级隔离（macOS Seatbelt / Linux Landlock 系统调用）限制模型可访问的文件、可无审批运行的命令与网络。
- **能解决**：①slopsquatting 供应链投毒的第一道确定性防线——网络默认禁时"包都装不下来，幻觉包无法伤害你"；②数据外泄；③破坏性命令波及工作区之外。
- **落地**：Codex 沙箱三档默认只读→需要时 workspace-write（网络默认禁）→显式 danger-full-access；approval policy（untrusted/on-failure/on-request/never）决定何时升级到人确认。Claude Code 侧：`docker sandbox run claude` 或项目全容器化（开发者与 CC 的接口=文件系统；容器无 git 凭据——能读历史能本地 git mv 但不能 push，必须人工 review 后外提）。
- **局限**：降低迭代速度（配 CI/环境拉起耗时）；沙箱内无法访问真实依赖源；"not a sandbox"是多数 hook 工具的诚实边界——hook 拦截≠沙箱。
- **来源**：04-codex-sandboxing；02-hn-claude-code-dumbed-down（lukev/chasd00）；02-hn-ask-llm-coding-established-codebase（adzicg Docker 实践，miohtama 称"最好指南"）。

### B2. Hooks 事件系统（Claude Code / Kiro 同构）（L2，含 L3 通道）

- **原理**：事件→matcher→动作。把"代码质量约束"从概率性提示升级为确定性执行的标准通道。事件覆盖会话级（SessionStart/End、PreCompact/PostCompact）、每轮（UserPromptSubmit、Stop）、agent 循环（PreToolUse 可阻断 / PostToolUse / PermissionDenied 等）。Kiro 同构：PostFileSave/PreToolUse/Stop + Command（确定性）或 Agent prompt 注入（概率性）双动作。
- **阻断语义（核心）**：退出码 **2=阻断**，stderr 作为原因反馈给模型；exit 1 不阻断（最常见 bug）。PreToolUse 细粒度 JSON：`hookSpecificOutput.permissionDecision = allow/deny/ask/defer` + `updatedInput`（可改写工具参数）；PostToolUse 用 `decision:"block"` 回溯打断（工具已执行，stderr 迫使模型修正）。`onFailure:"block"`（v2.1.295+）使钩子自身失败/超时/非法输出时也阻断。
- **能解决**：可执行的规则类约束——"禁止 amend 已 push 的 commit"、"强制 conventional commits"、"cat/head 强制换 Read 工具"、"review 模式禁止写"、"每轮重注入硬约束"、PostToolUse 触发 lint/format/test。
- **落地（合并 Konishi 六配方）**：
  1. 写后自动格式化：PostToolUse 匹配 `Write|Edit`，按扩展名跑 ruff/prettier/gofmt，**恒 exit 0**（"formatting is a convenience, not a gate"）；
  2. 审计日志：PostToolUse（matcher `*`，`async:true`）jq 落 JSONL，不占关键路径；
  3. Turn guard：Stop 门，有未提交变更 block 一次，marker 文件防死循环；
  4. SessionStart 注入 git branch/最近 commit/status（stdout 直进上下文）；
  5. PreCompact 快照草稿（防 compaction 丢失）；
  6. UserPromptSubmit 策略拦截（部署冻结期等）。
  Kiro 形态：`.kiro/hooks/` JSON，PostFileSave 匹配 `\.(ts|tsx)$` 跑 `npx eslint --fix`。
- **局限**：①超时的 PreToolUse **不阻断**（"别指望卡死的钩子充当门禁"）；②compaction 后 hooks 输出被模型当作低于其压缩摘要的优先级（#27242）；③"hook 每轮重注入的项目硬约束也不绑定——信息 present 且 available，存在不等于被遵守"（#2544 petrinhu 8 小时会话数据点）；④钩子以完整 shell 权限运行——审查第三方钩子如同审查 postinstall，updatedInput 改写型是高风险代码；⑤慢钩子拖累每步——同步 gate 要快、限时；⑥deny 返回 ≠ 宿主真的没执行（stop-that-shit 的 `hostEffect: unobserved` 诚实设计）。
- **反模式清单（Konishi 七条合并）**：exit 1 代替 exit 2；无终止条件的 Stop 钩子死循环；matcher `mcp__memory` 是精确匹配（全服务器要 `mcp__memory__.*`）；期望 hook 的 allow 松动权限 deny；忽略配置层级 Managed > Local > Project > Plugin > User。
- **来源**：04-hooks-claude-code-reference；04-hooks-community-guide-konishi；04-kiro-hooks；02-gh-claudemd-rules-ignored（yurukusa 三个 PreToolUse 实例、Milofax "workaround 是 Hooks"）；02-gh-compaction-no-review（ThatDragonOverThere 复合故障链）。

### B3. 权限系统与组织管理配置（L1/L2）

- **原理**：工具级 allow/deny/ask 规则（如 `Bash(rm *)`），独立于提示词。官方明言：硬性 allow/deny 应交给权限系统而非钩子（钩子的 `if` 字段只是 best-effort 过滤）。
- **能解决**：危险命令/危险路径的组织级不可覆盖管控；`allowManagedHooksOnly` + managed settings 实现组织级护栏（员工无法删除）。
- **落地**：`.claude/settings.json`（project，可入库共享）→ local(.local) → managed（最高）。权限 deny 优先于 hook allow。
- **局限**：粗粒度（路径/命令模式级），无法表达"语义上危险的命令"（如 flag 重排隐藏的 `git reset --hard`）——那要靠语义解析型工具（B5）。
- **来源**：04-hooks-claude-code-reference；04-hooks-community-guide-konishi。

### B4. CI 门禁与 Git hooks（L2，compaction 无法影响的最后防线）

- **原理**：在模型上下文之外运行，不受 compaction/注意力退化影响。CodeRabbit 对策："用 policy-as-code 强制风格——CI 强制 formatter、linter、style guide 在 review 前消灭整类 AI 问题"。
- **能解决**：全库漂移（`vibecheck --min-score 60` 门禁）；变更行级门禁（`--fail-on`/`--max-warnings` 配 `--staged` 或 GitHub Action 只扫 PR 变更文件）；SAST 安全门禁（Veracode：结构化 review 后失败率 45%→<10%）；认知复杂度预算门禁（SonarQube/Codacy/Semgrep）；diff 模式与全库门禁分工——`--diff`/`--staged` 用于 PR 行级、`--min-score` 用于全库（diff 模式禁用评分：只扫变更行却除以 1 KLOC 会伪装成全库分数）。
- **落地**：pre-commit 官方配方或 `.git/hooks/pre-commit` 里 `npx vibecheck --staged .`（配 husky）；GitHub Action 输出 SARIF 进 Security tab；`biome ci` 只查不改。**必须同时拦截 `--no-verify`/`--no-gpg-sign` 绕过**（agent-guard 的反绕过设计）。
- **局限**：反馈延迟（不在 agent 循环内，模型不自修——人修或下一轮修）；CI 只见代码不见意图；扫描器读不了的文件绝不报 clean（vibecheck exit 2 点名路径）。
- **来源**：04-code-smells-vibecheck-rules；04-biome-cli-agent-safe-flags；05-vibe-history-coderabbit（对策 2）；05-followup-veracode；04-local-repos-guardrail-mechanisms（agent-guard）。

### B5. 独立护栏工具（契约式 Guard / 策略引擎 / 语义拦截）（L2）

社区四个 serious 项目 + 横向三条趋同观察：

1. **stop-that-shit（契约式 Guard）**：Skill（建议层）+ Guard（机器强制层）双形态，同一首行指令（`$stop-that-shit change -- ...`）设置契约（模式 change/review/answer/monitor、`files=`、`deps=allow`、`hash=allow`、`agents=N`）。克制 SHIT 四症状：Scope creep / Hypothetical hardening / Intent violation / Task thrashing。armed 时五项硬决策仅基于可观察事实：review 模式写入→Stop、`files=` 外写入→Stop、未授权依赖新增→Ask、超 `agents=N`→Stop、无 `hash=allow` 的高置信哈希→Stop。delegation ledger 并发安全记账（确认完成才释放容量）。默认 `OBSERVING/unconfirmed` 观察模式，须显式 arm；未武装不得宣称拦截。
2. **gryph（YAML 策略引擎 + 审计）**：hooks 进 Claude Code/Cursor/Windsurf/Gemini CLI/OpenCode；YAML 规则对动作 block/warn/guide 三档；所有事件落本地 SQLite 审计库（`gryph logs` 查 agent 读过/跑过/改过什么），纯本地无遥测。
3. **claude-code-safety-net（破坏性命令语义拦截）**：PreToolUse 解析命令**实际语义**（包一层或重排旗标藏不住）；拦 `git reset --hard` 与 SSH key/.env 访问；**fail-open 声明**："A broken config file never blocks anything"；诚实边界 "not a sandbox"。
4. **agent-guard（秘密防泄漏）**：拦 .env 读取、掩码 secret 输出、gitleaks 扫过才许进 Git；**拒绝 agent 用 `--no-verify` 绕过钩子**。
5. **横向趋同（三条）**：①语义解析而非纯正则（safety-net 解析语义、agent-guard 拦绕过旗标、stop-that-shit 未知工具保守阻断 "block unknown mutability rather than guessing"）；②审计成标配（SQLite/JSONL，可回溯）；③每个项目写明"不是什么"——**边界诚实本身是机制设计的一部分**。
- **局限**：静态分析假阳性（#86：MUTABILITY_UNPROVEN 一刀切阻断合法解析器）；自由文本解析行为契约脆弱（#66：Codex 心跳含中文"只观察"被误判降级）；累计 vs 并发限额语义争议（#44 静默截断至 8）；**护栏本身也要有测试集**（stop-that-shit 的 18 组 Bad/Good 判例做行为回归）。
- **裁决（fail-open vs fail-closed）**：分用途——**安全拦截型 hook 必须 fail-closed**（配 `onFailure:"block"`），否则失败的钩子静默放行一切；**审计/格式化型可 fail-open**（safety-net 声明、stop-that-shit 审计写失败不改控制决策）。两者都是诚实设计，但不能混用。
- **来源**：04-local-repos-guardrail-mechanisms；01-stop-that-shit 全节（ARCHITECTURE/EVIDENCE/hooks.json）；02-stop-that-shit-issues-highvalue。

---

## 二、反馈层（确定性反馈环）

### B6. Linter / Formatter 自动化（L3，"保存即 lint"）

- **原理**：静态检查融入 AI 工作流的最常见形态是 agent 保存/编辑文件后自动触发。Cursor 官方最佳实践与 Anthropic steering 同一共识：**规则文件不要重复 linter 能做的事**（style guide 交给 linter）；"真正的杠杆在'谁在何时以何种权限调用它们'（hooks 自动调用 vs CI 拒绝），而非工具本身"。
- **能解决**：格式漂移（CodeRabbit：AI PR 格式问题 2.66 倍）、命名不一致、可机械修复的坏味道——在 review 前消灭整类问题，省下人审带宽。
- **落地（agent 安全标志合并）**：①错误容忍——`--skip-parse-errors`、`--format-with-errors=true`（agent 常写半成品代码，中间态文件不应让整个 lint 崩溃）；②修复分级——`--write/--fix` 默认只应用 safe fixes，`--unsafe` 需显式传入（防 agent 应用破坏性修复）；③非交互——`biome ci` 只查不改；④可审计抑制——`biome lint --suppress --reason=STRING`；⑤增量接口——`--changed/--since/--staged` + `--stdin-file-path` 供 PostToolUse 对刚写文件即时反馈。PostToolUse 自动格式化配方见 B2。
- **局限**：只覆盖机械可判定的规则；不覆盖架构/逻辑/安全语义；速度敏感（同步 gate 每步都跑，须快+限时）。
- **来源**：04-biome-cli-agent-safe-flags；04-cursor-rules（最佳实践 4）；04-kiro-hooks；05-vibe-history-coderabbit。

### B7. 测试与验证纪律（L3，含 L4 判定门）

- **原理**：测试是"可以任意次重跑的确定性期望"（martinmilo），给 agent 一致反馈水平（mattpocock 失败模式 #3 的解法）。验证纪律的核心是**证据先于断言**：模型自述成功不算证据，VCS diff/测试输出才算。
- **能解决**：AI 代码的逻辑/正确性问题（CodeRabbit：逻辑错误多 75%、修复最贵）；"看起来像成功"的最贵失败（Mnilax 规则 12：迁移静默跳过 14% 记录，11 天后才发现）；测试自欺（12 个全过的 auth 测试，生产 auth 却坏——函数返回常量）。
- **落地（多来源铁律合并）**：
  1. **superpowers TDD**："NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST"——先写测试看它失败再实现；写码在测试前？删掉重来（不保留做参考）。Verify RED/Verify GREEN 强制（GREEN 须跑**项目整套测试**，不止单文件）。
  2. **superpowers verification-before-completion**："NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE"。Gate Function 五步：IDENTIFY（什么命令能证明）→RUN（新鲜完整执行）→READ（完整输出+退出码）→VERIFY→THEN claim。红旗词："should/probably/seems to"。常见对照："agent 完成"需要 VCS diff 显示变更（agent 报告 success 不算）。
  3. **第五维（IN-PRACTICE PR #197）**："Verification Is Not Optional"——exit 0 ≠ output seen（tsc 在无 tsconfig 的根目录打印帮助文本、退出 0、链条继续 commit 的事故）；报告你没查的部分（"看了 6/20，其余大概类似"必须原样写）；**复现测试必须先红**（"如果你的新测试在写修复之前就通过——你没有发现一个 bug，你发现了一个坏测试"）。
  4. **proof_pack 机械判定（code-modernization）**：三档 PROVEN / NOT PROVEN / PARTLY PROVEN，"判定由固定规则计算，绝不是模型的意见"。六检查：Tests ran（计数必须来自脚本自己解析的结果文件，只敲进 test-runs.json 的计数封顶为 "gap"）、Rules traced、Same behavior、Fresh inputs、Canary（故意单行破坏，其结果文件显示测试变红——笔记里的 "Canary:" 行是主张不是证据）、Source untouched。"手工敲的基线什么也证明不了"。
  5. **spec-kit converge**：implement→converge 循环 until Converged；三值裁决 verified/partial/failed——**missing verification 不算修复**。
- **局限**：LLM 生成的测试可能同义反复或镜像实现（断言用代码自己的方式重算期望值→永真）；tmarlice 实测"除了 1==1 什么都没测"；Qodo：用 AI 写测试的信心 61% vs 不用的 27%（采用者信心翻倍但质量取决于示例与上下文）；流程成本——superpowers 慢的批量投诉（#743：trivial 任务也 35 分钟、快速吃光额度）。
- **来源**：01-superpowers（test-driven-development / verification-before-completion / writing-good-tests）；02-karpathy-skills-PR197；01-claude-plugins-official（proof_pack/baseline_diff）；04-speckit-sdd；02-hn-good-code-agents（martinmilo/tmarlice）；05-code-smells-qodo。

### B8. 静态度量与 slop 扫描（L3 → CI 门禁升 L2）

- **原理**：AI 代码的结构性劣化可测、可归因、可由门禁压低（CIQ 与 arXiv 2511.15817 互证）。vibecheck 自称 "ESLint for AI slop"：40 条捕获 AI 生成代码坏味道的规则（安全 6/错误处理 7/代码质量 9/AI 痕迹 14/框架 4），纯正则、零配置本地跑。
- **能解决**：AI 特有痕迹（幻觉 import、犹疑注释、桩函数、复述式注释——ESLint 抓不到）；错误处理缺口（CodeRabbit：AI PR 近 2 倍）；安全漏洞（Veracode Top CWE：XSS 33.5%/路径遍历 24.5%/OS 注入 20.1%/SQL 注入 18.1%/硬编码凭证 13.4%——checklist 可直接对齐这 5 类）；认知复杂度恶化（CIQ：AI 辅助代码认知/圈复杂度比值上升，重复度 +81%）。
- **落地**：
  - CIQ 五条：认知复杂度预算纳入评审门禁；嵌套上限/卫语句约定；重复超阈值强制抽公共库 + 给 agent"先查现有工具再写"指令；生成前 prompt 显式要求最小复杂度实现、生成后跑复杂度扫描再合并；监控重复度/认知圈比值仪表盘。
  - vibecheck：slop score 按类别拆分（每 KLOC 严重度加权，单规则每 KLOC 上限 20 分防单规则主导）；分级锚定真实语料四分位而非学校量表；校准曲线可复现（`scripts/calibrate.ts`）；baseline 指纹不含行号（可在文件内移动存活）；抑制必须带理由且计数上报。**设计启示可迁移**：任何 AI-slop 度量都要防"分数描述你的视图而非代码库"（写 baseline 曾把分数直接送满 100 而代码未变）。
  - Veracode：prompt 明确要求安全写法失败率 31.5%→24.3%（-7pp，低成本杠杆，固化进 Skill 措辞有量化收益）。
- **局限**：正则无 AST 的误报/漏报；度量代理指标可被优化目标污染（jadarma 对 Copilot 研究的批判同样适用于自我度量）；mnilax 教训——依赖可能不存在的工具的规则（"always use eslint"）在工具不在时静默失效，措辞应能力无关（"match the codebase's enforced style"）。
- **来源**：04-code-smells-vibecheck-rules；05-followup-ciq-imitation-game；05-followup-veracode；05-vibe-history-jadarma（方法论警惕）。

### B9. 依赖幻觉防御（包幻觉，L0-L2-L3 纵深）

- **原理**：包幻觉是结构性风险而非偶发 bug——商业模型平均 5.2%、开源 21.7% 的建议包为幻觉（USENIX'25，57.6 万样本）；幻觉率与 HumanEval 分数负相关；编码模型"没有为安全代码优化"（Pareto 前沿稀疏）。slopsquatting：攻击者抢注幻觉包名投毒。
- **能解决**：新增依赖成为显式事件而非静默发生；阻断规则文件注入攻击的下游（PackHallu：进化优化的注入文本可诱导依赖替换，跨模型强迁移）。
- **落地（论文清单 + 机制映射）**：①沙箱默认断网（L0，B1）；②PreToolUse 拦截包管理器安装命令、PostToolUse 扫 manifest diff（L2，B2）；③lockfile 优先/新依赖白名单校验（对照官方 registry 元数据、provenance）/CI 扫 manifest diff（L2，B4）；④确定性 PyPI/npm 存在性检查 + slopsquatting 风险分类器（两层检测器，L3）；⑤vibecheck 的 `no-hallucinated-import-js/py` 规则。**依赖变更必须有机字符串级校验，不能依赖"模型读了好规则就会听话"**（PackHallu 防御推论 2）。
- **局限**：白名单维护成本；私有源/镜像的误报；规则文件本身是攻击面（见 B13）。
- **来源**：04-code-smells-arxiv-package-hallucination；04-pkg-hallucination-importing-phantoms；04-pkg-hallucination-rule-file-injection；05-vibe-history-arxiv-abstracts（论文 3）。

---

## 三、流程层（SDD 与计划门）

### B10. Spec-Driven Development 三实现（L4）

- **原理**：先定义 what/why 再决定 how；需求只存在于聊天历史中导致不可靠（OpenSpec 立项动机）。用 Markdown 工件持久化，可人审、可 diff。
- **三实现合并对照**：

| 维度 | spec-kit（GitHub） | OpenSpec | Kiro |
|---|---|---|---|
| 重量 | 彻底但重（刚性阶段门） | 刻意轻（"no rigid phase gates"） | IDE 级，三工件 |
| 宪法 | constitution 每项目一次，聚焦代码质量/测试/可维护性；**Constitution Check 是 GATE**（Phase 0 前必须过、Phase 1 后复查；违宪未论证则 ERROR） | 无 | 无 |
| 人工门 | implement 前 checklist 门（有未勾选项→STOP 询问用户）；clarify 苏格拉底补问 | **人在写码前 review proposal**（杠杆最大的人工门） | 每阶段多个人工审批门（approval gates） |
| 收敛 | implement→converge until "Converged"；三值裁决 | expanded profile 加 /opsx:verify | property-based testing（IDE-only） |
| 防腐烂 | 工件在 .specify/ 入库 | **归档时合并回主 spec**（每变更一目录+归档合并） | tasks.md 实时状态更新 |
| 对治 over-complication | **Complexity Tracking 表**：仅当宪法检查存在需论证的违宪项才填——Violation/Why Needed/Simpler Alternative Rejected Because 三列强制为复杂度辩护 | — | — |
| 任务格式 | 五要素 `- [ ] [TaskID] [P?] [Story?] Description with file path`；字段约束逐字引用不得留给实现裁量 | tasks.md 清单 | 依赖图分 waves 并行 |
- **spec-kit 模板机制补充**：extensions.yml 前置/后置 hook——mandatory hook 必须 EXECUTE_COMMAND 真实调用并等待完成，optional 只提示；YAML 解析失败不得静默跳过。checklist 理念："Checklists are UNIT TESTS FOR REQUIREMENTS WRITING"——验证需求写作质量而非实现；`[x]` 意为评审者认定需求质量满足，生成命令禁止自勾。NEEDS CLARIFICATION 上限 3 条（scope > 安全/隐私 > UX > 技术细节），其余做有依据猜测记入 Assumptions。
- **局限**：本质是 probabilistic + 人工审批（依赖 agent 遵循命令流程）——与 hooks 的机器强制互补而非替代；重量争议见待裁决 3（mattpocock 明确反对 GSD/BMAD/Spec-Kit 式接管流程；superpowers #743 慢的批量投诉）。
- **来源**：04-speckit-sdd；04-openspec；04-kiro-specs；05-vibe-history-speckit；05-05-第三部分 spec-kit 模板机制全节。

### B11. 计划写作与执行台账（L4）

- **原理**：计划是"实现者无法独自做出的决定之集合"（superpowers writing-plans）；执行期的裁决必须留下台账——"没有台账的偏离是秘密做的决定"（executing-plans）。
- **能解决**：spec 与实现漂移；压缩后丢失进度（"会话记忆活不过压缩——进度记在台账文件不只是 todos"）；执行者私改决定。
- **落地**：计划文档头必含 Global Constraints（spec 的项目级要求逐条一行）与 Review Focus（spec 隐含但无测试行使的五个最可能咬人的输入类）；任务结构 Files/Interfaces（Consumes/Produces 精确签名——"每个任务的实现者只看得到自己的任务"）；内联执行四停条件（不可逆操作/安全敏感/规范外副作用/计划破到全是猜）+ Ruling 台账行 `<决定了什么>—<为什么>—<错了的代价>`；终审是整次运行买的唯一新上下文（最强模型 subagent，不许自己读 diff 顶替）；发现分级：Critical/Important 进修复遍（每修按 TDD），Minor 记台账永不进修复遍。
- **裁决（完整代码计划 vs 契约式计划，superpowers #895 之争）**：**按 executor 能力分层**。弱 implementer（haiku 级）用完整代码计划（obra 立场：让弱模型能抄写）；强模型（Opus/GPT-5.x 级）用"契约+验收+nuance 注释+仅 tricky bits 伪代码"（GiveMe-A-Name 中间层，AGENTIF 研究支持：过度指定妨碍判断）；计划含可运行内容（迁移 SQL 等）时冻结计划+对 shipped 代码做 delta review（hbiagi 资金敏感案例的教训：计划 46 小时从 171KB 涨到 1.2MB，editor 子代理占 61% 成本）。m13v 的反向风险要写进规则：抽象化验收使背离"安静地作为满足的验收清单溜过"——验收必须是测试不是意图陈述。superpowers v6.4.2 的实际修复（"一个 step 给出确切签名、文件与 spec 的值，implementer 写主体"）正是这个中间层。
- **局限**：流程成本高（#743）；上下文更少的 subagent 反而表现更好的反直觉证据（envictor）；spec 冻结时 spec-driven 不 work（dudeinhawaii）——spec 必须可随走随更新。
- **来源**：01-superpowers（writing-plans/executing-plans/requesting-code-review）；02-gh-superpowers-plans-overspecify（全文）；02-gh-superpowers-slowness。

### B12. 需求拷问（grilling / clarify / 多模型拷问 plan）（L4）

- **原理**：软件最常见的失败是错位（misalignment）——你以为 dev 懂了，看到成品才发现完全理解错了（mattpocock 引 Pragmatic Programmer）。对 agent 一样：unknown unknowns 无法 spec，只能被"拷问"暴露。
- **能解决**：silent wrong assumptions（Karpathy 三大失败模式之首）；模型替你做错误假设并一路狂奔。
- **落地**：①grilling 设计树 + frontier 轮询——每轮问出整个前沿（所有前置已定、现在就能问的问题），每题给推荐答案，用户回答重塑树，**前沿为空才结束**；分工铁律"找事实是你的工作，永远不是用户的"（环境事实派 sub-agent 查，不问用户）；②让 agent 在写 spec 前拷问你 + **再让不同模型拷问 plan**（piscaries：一次就抓住通用评审漏掉的设计问题）；③初始 prompt 末尾 "ask me up to 5 questions"（Harper Reed/danphilibin 复证："magic ticket"）；④spec-kit [NEEDS CLARIFICATION] 三条件下才标记 + 上限 3 条；⑤团队规则："先 chat 模式谈透、达成一致再切 agent 模式"（Alan01252，Antigravity 默认范式）。
- **局限**：问题质量依赖模型对领域的理解；"有问题就问否则就做"很少真的产生提问——要主动问 "do you have any questions?"（bogtog）；grilling 本身花时间（对 trivial 任务过度）。
- **来源**：01-mattpocock_skills（grilling/grill-with-docs）；02-hn-good-code-agents（piscaries/runjake）；02-hn-harper-reed-llm-codegen-workflow；05-spec-kit 模板机制；02-hn-ask-getting-better-at-ai-coding。

---

## 四、规则层（概率性指令）

### B13. 规则文件（AGENTS.md / CLAUDE.md / cursor rules）（L5）

- **原理**：被读入上下文的"概率性指令"。AGENTS.md 是开放标准（"a README for agents"，6 万+项目，Linux Foundation 下治理）；monorepo 可嵌套，**"The closest AGENTS.md to the edited file wins"**；一份文件通用 Codex/Jules/Cursor/Amp/Aider/Gemini CLI/Zed 等。Cursor 四级注入：Always / Auto Attached（globs）/ Agent Requested（按 description 自选）/ Manual；规则内 @ 引用不内联展开（须始终在场的内容写进正文）。
- **有效性量化（Mnilax，50 任务 × 30 库 × 6 周）**：失误率 无规则 ~41% → 4 规则 11% → 12 规则 3%；合规率几乎零额外注意力成本（78%→76%）。**负面结果同样量化**：18 条时合规率 76%→52%（200 行天花板真实存在，超过后模型模式匹配到"规则存在"而不真读）；"Be careful/think hard" 类不可测试规则合规率跌至 ~30%；示例子代价比规则高（3 示例 ≈ 10 条规则的上下文成本且过拟合）；"act as senior" 无效（"Claude already thinks it's senior"）。
- **无效性量化（反面证据链）**：①Anthropic 官方：CLAUDE.md 是 advisory，~80% 遵循率、超 200 行急剧下降；②issue #2544（45 reactions，20+ 重复 issue 链）：跨仓库持续忽略强制规则，"表现得好像 CLAUDE.md 只是可选建议"，7 个月无官方回应；道歉完整但次日重犯；③**63% 量化研究（rulereceipt，559 个公开规则文件）**：63% 的内容根本不是指令（目录/参考表/架构笔记/风格指南）；剩余 8,101 条真规则中 **35% 具体到可被 matcher/hook 执行、65% 是判断类**——多数人猜的比例正好相反；"三分之二的内容无论写得多好都无法表达为 blocking hook——这是格式的属性不是纪律问题"；④静态 linter（soul-sol，396 个 CLAUDE.md）：**约四分之三文件静态检查挑不出毛病——文件基本没问题，失败在于运行时没有任何东西强制执行**；⑤机制：规则注入在 HEAD 位置，对话变长时注意力权重最低（Lost in the Middle）；compaction 后被降权或遗忘；两条信息冲突时它会两条都忽略。
- **注入攻击面（PackHallu，arXiv 2610.09264）**：规则文件本身是 prompt injection 攻击面——进化优化的注入文本可诱导依赖替换，跨模型/跨框架强迁移。**从网上复制的规则文件应视为不可信输入**。
- **▶ 矛盾裁决：规则文件有用 vs 无用**——两边证据都成立但谈论的是不同子集。裁决三条：
  1. **规则文件有效，但仅限"少而硬"**：≤12 条、每条是可测试的祈使句（"state assumptions explicitly" 而非 "think hard"）、每条回答"这防止什么失误"（行为契约不是愿望清单）；<200 行（超 12 条注意力崩塌有量化数据）；针对自己真实犯过的错保留 6 条好过 12 条里 6 条用不上。
  2. **可执行子集（35%）必须 hook 化**：durban01 两堆分法——"完成任务前跑测试/永不碰 .env/不 force push main/commit 格式"根本不该是指令，应是 hooks；判断类（命名/架构/何时提问）留在 CLAUDE.md，会随上下文退化且无解。63% 的非指令内容并非无用（导航/上下文有价值）但**不应承担强制职责**——它解决的是"模型不知道"，不是"模型不做"。
  3. **运行时零强制是格式属性**：soul-sol 的静态结论终结了"把文件写更好"的幻想——四分之三文件本来就没问题；继续打磨措辞（全大写/感叹号/red）无收益，投入应转向强制层。
- **落地**：内容=项目概览、构建/测试命令、代码风格、测试说明、安全注意（"像对新同事交代的事"）；列出测试命令则 agent 会自动尝试运行并修复（行为杠杆也是风险面）；只在 agent 重复犯错时才加规则（Cursor 最佳实践 5）；规则进 git、随模式演进更新、定期删除失效规则（steering："append-only 规则腐烂"——规模化后每个团队追加指令而没有任何东西被删除）；来源可信（注入风险）；能力无关措辞。
- **局限**：~80% 遵循率上限；长会话/compaction 退化无解；判断类 65% 无法上 L2（待裁决 1）；注入攻击面。
- **来源**：04-agents-md-spec；04-cursor-rules；04-steering-claude-code-blog；05-followup-mnilax-12-rules；02-gh-claudemd-rules-ignored（全文：mhofer1976/junaidtitan/tonydzi/rulereceipt/soul-sol/durban01/petrinhu）；02-karpathy-tweet-claude-coding-notes。

### B14. 行为纪律 Skill（四原则 + 验证第五维）（L5，流程化封装）

- **原理**：把失败模式→治理规则的映射链封装成 Skill。Karpathy 三大失败模式（silent wrong assumptions / over-complication / orthogonal damage）→ forrestchang 四原则 skill（12 万 star，2026 最快增长单文件仓库）→ IN-PRACTICE 增补第五维。
- **四原则**：①Think Before Coding（不假设、不藏困惑、呈现 tradeoff）；②Simplicity First（最少代码、零投机——"好代码是简单地解决今天问题的代码，不是过早解决明天问题的代码"）；③Surgical Changes（每行改动可追溯到用户请求；匹配既有风格；存量死代码两条作用域规则）；④Goal-Driven Execution（定义成功标准并循环到验证——"别告诉它做什么，给它成功标准看它跑"）。
- **第五维（生产库落地增量）**：Verification Is Not Optional（见 B7.3）；三个锐化：报告实际查的+明说没查的；复现测试必须先红；存量死代码作用域调和（"零死代码规则设定的是仓库应达状态，本规则防的是无关 diff 里长出第二个无人 review 的改动"）。
- **Mnilax 补充 8 规则（2026 生态新失败模式）**：Use the model only for judgment calls（路由/重试/确定性变换用普通代码）；Token budgets are not advisory；Surface conflicts, don't average them（"同时满足两条规则的折中代码是最差的代码"）；Read before you write（"看起来正交"是代码库里最危险的话）；Tests verify intent, not just behavior；Checkpoint after every significant step；Match conventions even if you disagree；Fail loud。
- **机制分工（steering 经验法则）**：确定性行为→hooks；事实→CLAUDE.md/rules；流程→skills；隔离旁路→subagents。compaction 行为差异：Rules 重新注入（持续生效）；Skills 正文仅调用时加载；Subagents 完全隔离；**Hooks 完全绕过 compaction**。指令遵守边际递减——指令越多遵守越松。
- **局限**：同为 L5 概率性（遵守依赖模型）；steering 分工表是设计指引非保证；skill 触发依赖 description 质量（"修 description 而不是正文"）。
- **来源**：01-andrej-karpathy-skills（全节）；02-karpathy-tweet-claude-coding-notes；02-karpathy-skills-PR197-IN-PRACTICE；05-followup-mnilax-12-rules；04-steering-claude-code-blog；04-skills-ecosystem-anthropic-best-practices。

---

## 五、上下文层

### B15. Compaction 与护栏外置（L5 的物理成因 → 强制层外置的依据）

- **原理**：context rot——token 越多召回越差；注意力预算有限。**长会话质量下降是"规则失效"的物理原因——护栏必须放在上下文之外（hooks/权限/CI），compaction 后仍生效**（context engineering 推论 1）。规则在 compaction 后重新注入故持续生效；CLAUDE.md 类 HEAD 注入则被稀释（Lost in the Middle）。
- **能解决**：长会话退化；"AI 上下文一长忘记设计决策、改 A 坏 B"。
- **落地**：①PreCompact hook 快照（草稿/对话导出 markdown，Konishi 配方 5、yurukusa 脚本）；②状态外置（见 B16）；③compaction 调优（保留摘要+最近 5 个访问文件；先最大化召回再提精度）；④**架构级 workaround（bestiaya）**：不再依赖 transcript 可回看——job 状态放上下文窗口外的 markdown 文件，决策落地即写；下一个会话读文件而非历史——"不恢复压缩前上下文，而是消除对它的依赖"（实测 93K 字符状态、接管时实读 53K）。
- **局限**：CC 的 compaction 后历史不可回看是产品缺陷（#27242，89 reactions：无法审计压缩后推理、plan mode 探索对话孤儿化、transcript mode 硬编码 hidePastThinking）；压缩后 hooks 输出也被模型降权（复合故障）。
- **来源**：04-context-engineering-anthropic；04-hooks-community-guide-konishi；02-gh-compaction-no-review（全文）；02-gh-claudemd-rules-ignored（mhofer1976/junaidtitan）。

### B16. 持久记忆与状态外置（L5 增强但跨会话存活）

- **原理**：结构化笔记持久化在上下文窗口之外（todo list、NOTES.md），事后重载——"persistent memory with minimal overhead"（Claude-plays-Pokémon 证明数千步/上下文重置后保持连贯）。
- **能解决**：会话/窗口切换丢上下文；重复劳动与结论丢失；跨会话多步工作流断裂（2026 生态新问题，Mnilax）；重复代码（不同请求间无记忆→同一问题反复生成相似解——CIQ 对重复 +81% 的机制解释）。
- **落地**：①执行台账（B11）本身就是记忆外置；②feedback memories——把用户纠正（"don't do X"/"always use Y"）提取写入 CC 原生记忆，经 SessionStart/PreCompact/Stop hooks 自动重注入（cozempic v1.4.1：修不了 HEAD 位置问题但让纠正活过压缩、每轮重读）；③ap-vibe 项目档案：方案为什么改/文件在哪/待办有哪些按项目保存（"昨天否掉的版本，今天不用再吵"），十维雷达评分**非 null 分必须带 reason + evidence_refs**（有分数必须给理由+证据引用，ContractError 强制）；④GLOSSARY.md 共享语言（agent 被空投进项目自己猜行话→20 个词说 1 个词的事；逐会话复利 + agent 思考 token 更少）；⑤Karpathy 愿望：内置 scratchpad 承载跨会话增长的项目上下文。
- **局限**：记忆交接的信任问题——持久记忆中的安全规则 dispatch 时不绑定（petrinhu：对话中提起能正确复述，给 subagent 布置任务时指示了较弱缓解）；记忆本身可被污染；token 成本（53K 字符的接管读取）。
- **来源**：04-context-engineering-anthropic；02-gh-claudemd-rules-ignored（junaidtitan/petrinhu）；02-gh-compaction-no-review（bestiaya）；05-05-第四部分 ap-vibe 十维；01-mattpocock_skills（domain-modeling）；02-karpathy-tweet（愿望 2）。

### B17. 子代理隔离与跨模型评审（L4/L5 混合）

- **原理**：专职子代理在干净上下文里做深工作，只回传 1000-2000 token 摘要；复杂研究任务显著优于单代理。评审同理：评审者拿到的是精心裁剪的上下文——**绝不是你的会话历史**（superpowers requesting-code-review）。
- **能解决**：自我确认偏置（"don't have Claude review its own code"）；同作者同盲区（"终审评审者是整次运行买的唯一新上下文"）；主上下文污染。
- **跨模型评审的量化（arXiv 2607.21656，116 道 LiveCodeBench 难题）**：**有用配对是不对称的——用 Claude 审 Codex 71.6%→89.7%（p=.001）；Codex 自评 Codex 84.5%（弱于跨模型）；但 Codex 审 Claude 91.4%→82.8%（不升反降，p=.046）**；Claude 自评强草稿无效（91.4% 不变）。分层选择：弱草稿→自评/跨模型，强草稿→跳过。评审条件：只看题面+diff、不跑测试也能大幅提升。**纠偏**：工具 neal 的默认方向（Claude 写 Codex 审）恰是论文负收益方向——Skill 中必须写明方向。
- **其他评审实践合并**：多 agent 投票（claude-plugins code-review：5 个并行 Sonnet 独立评审 + Haiku 打 0-100 置信度 + **过滤 <80 分**——误报清单含"linter/typechecker 会抓的"）；多模型争论（"多个模型对一处变更争论产生的洞察远好于单模型评审"，truverif.ai）；gpt-5.6 监督 Opus 的一手报告（smell-check #7：配额耗尽单用 Opus 才出事）；多视角 hitlist（jkingsman：Opus/GPT5.4/Gemini 各写再汇总）。
- **局限**：上下文更少的 subagent 表现更好但评审深度受限；评审成本（每任务新评审者）；AI 评审自动化与人审的关系见待裁决 2。
- **来源**：04-context-engineering-anthropic；05-followup-cross-model-review-evidence（全文）；01-superpowers（requesting-code-review/code-reviewer）；01-claude-plugins-official（code-review）；02-hn-good-code-agents（verdverm/runjake/vivekpolavarapu）；02-smell-check-issues-highvalue。

### B18. 渐进披露与按需检索（L5 的上下文经济学）

- **原理**：不预载，保留轻量引用（路径/查询/链接）运行时取；"找到最大化期望结果可能性的最小高信号 token 集合"。Skill 三级披露：Metadata（~100 token 常驻）→ Instructions（<5k token 激活时）→ Resources（按需）；脚本是最高披露层——**代码执行不进入上下文，"能用脚本确定性解决的问题就不要用散文指示模型"**。
- **能解决**：context rot；根 CLAUDE.md 成本最高（"每一行无论相关与否都耗 token"）；References 高密度 cheat sheet 比散文有效（匹配训练分布）。
- **落地**：混合策略（CLAUDE.md 预载 + 按需检索，"do the simplest thing that works"）；Cursor @ 引用不内联展开；SKILL.md <500 行、引用链一层深；手动选上下文已失效（54% 仍错过相关性 → 工具自主选 33% → 跨会话持久 16%——Qodo：上下文越自动化越持久越可信）；`.ai-context` 文件夹（架构/标准/常见模式）提问前先喂。
- **局限**：检索质量依赖元数据（目录结构/命名）；Qodo 上下文缺口数据（重构 65% 最高）说明纯检索不够——学习型仓库级上下文引擎是其方向，但对个人 Skill 而言落地形态就是分层加载纪律。
- **来源**：04-context-engineering-anthropic；04-skills-ecosystem-agentskills-io-spec；04-skills-ecosystem-anthropic-best-practices；04-cursor-rules；05-code-smells-qodo；02-hn-ask-llm-coding-established-codebase（adzicg）。

---

## 六、已裁决矛盾（本次整合拍板，≤3）

1. **规则文件有用 vs 无用**：两派证据各谈一个子集。裁决——规则文件有效但**少而硬**（≤12 条可测试祈使句、<200 行、每条对应真实失误）；可执行子集（35%）**必须 hook 化**（运行时零强制是格式属性，不是纪律问题——soul-sol 四分之三文件静态无毛病）；63% 非指令内容承担导航职责而非强制职责。证据链：Mnilax 量化收益（41%→3%）× issue #2544 运行时失效 × rulereceipt 63%/35% × soul-sol 静态结论。
2. **hooks fail-open vs fail-closed**：分用途裁决——安全拦截型必须 fail-closed（`onFailure:"block"`，否则失败的钩子静默放行一切）；审计/格式化型可 fail-open（safety-net 与 stop-that-shit 的声明均属此类）。配套裁决：deny 返回 ≠ 宿主未执行（hostEffect: unobserved），任何"已拦截"的宣称必须区分这两层。
3. **完整代码计划 vs 契约式计划（superpowers #895）**：按 executor 能力分层——弱模型完整代码计划，强模型契约+验收+关键伪代码；计划含可运行内容时冻结+delta review；抽象化验收需防"背离安静溜过"（验收必须是测试不是意图陈述）。依据：obra/GiveMe-A-Name 双方朝中间会合 + AGENTIF 研究 + superpowers v6.4.2 实际修复方向。
   （附带小裁决：跨模型评审方向必须写明"用 Claude 审 Codex"，neal 类工具默认方向是量化负收益方向。）

---

## 七、待裁决矛盾（需主 agent 拍板）

1. **65% 判断类规则没有确定性强制通道**：rulereceipt 证明三分之二规则内容"无论写得多好都无法表达为 blocking hook"；事后检查只能让模型判——而模型判官会过度报告（对含 1 个真问题的会话报 10 个违规；加 "never came up" 第四判定后 10→4），"检查器的失效模式永远是过度报告——报两次假的人们就不再读了"。且 petrinhu 的 8 小时会话数据点显示**hook 每轮重注入也不绑定**（信息存在且可用 ≠ 被遵守）。即：L2 对判断类约束有天花板。**待裁决**：中文 Skill 对判断类规则（命名/架构/何时提问）是接受 L5 退化并辅以高频人审，还是引入"独立评审 agent + never-came-up 四值判定"作为折中？这决定 Skill 的骨架形态。
2. **AI 评审在环自动化 vs 生成-评审分离铁律**：支持自动化——Qodo 数据（有 AI 评审在环质量改善 81% vs 55%；即便交付没提速质量收益也翻倍；80% 的 PR 无人类评论）； verdverm 用便宜模型审大厂模型、gabriela_c 多轮 GitHub-PR 式 review 后再发 agent 修。反对——thelostdragon 铁律"不能让 AI 同时做代码生成和代码评审/测试，绝不双 AI"；superpowers "agent reports success 不算证据"；esalman 事故（Copilot 篡改测试让 edge case 通过）；sfjailbird 循环质疑"用 LLM 生成测试确保 LLM 代码能工作？等一下……"。两派都有一手证据。**待裁决**：Skill 默认推荐哪档（AI 审 + 人抽查 / 人审 + AI 辅助 / 按风险分级），以及"跨模型+人工验证 review"是否作为强制条款。
3. **SDD 应为默认路径还是重路径**：支持重流程——spec-kit 141k star、converge 收敛、宪法 GATE、OpenSpec"人在实现前审批是杠杆最大的人工门"；HN 多人复证 spec 先行决定质量（runjake/jv22222/dudeinhawaii）。反对——mattpocock 立场声明明确反对 GSD/BMAD/Spec-Kit 式接管流程（拿走控制权、过程 bug 难解）；superpowers #743 批量投诉（trivial 任务 35 分钟、额度吃光、"裸 claude code 2 分钟搞定"）；Mnilax 指出 Simplicity First 在原型期过度开火；speed/质量按项目分级（Yegge：原型放任、生产盯紧）。**待裁决**：中文 Skill 是否把 SDD 作为默认工作流（重），还是默认轻流程 + 按风险升级到 SDD（分级），或提供两档显式选择？影响 Skill 的篇幅与门槛。
4. **护栏生态的宿主锁定问题**：最强强制机制（hooks/managed settings）是 Claude Code/Codex 私有语义；AGENTS.md 开放标准只覆盖 L5。中文 Skill 若要跨工具（含国产 agent）有效，L2 层几乎无法统一表达——stop-that-shit 的"宿主无关内核 + 六薄适配器"是唯一先例但工程成本高。**待裁决**：Skill 按 Claude Code 系编写并声明边界，还是投入适配器层？
