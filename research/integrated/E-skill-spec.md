# 知识域 E 整合：Agent Skill 的工程规范与写作标准

> 阶段 3 整合产物。用途：直接指导「提高 AI 编程代码质量」大型中文 Skill（主入口 + 若干子 Skill）的构建。
> 每条带来源标记。整合日期：2026-10-11。

**来源标记**
- `[06-A.1]` / `[06-A.2]` / `[06-A.3]` / `[06-A.4]` = 06-local-materials.md Part A（repo-refactor / repo-steward 结构分析 / 哲学对比 / 优缺点）
- `[05-spec]` = 05-history-ecosystem-followup.md §skills-ecosystem-agentskills-io-spec（agentskills.io 规范）
- `[05-bp]` = 同上 §skills-ecosystem-anthropic-best-practices（Anthropic 官方写作最佳实践）
- `[05-mnilax]` = 同上 §followup-mnilax-12-rules（规则措辞有效性的量化实验）
- `[05-ste]` = 同上 §followup-karpathy-explain-llm-output（受控语言与信息保真的权衡）
- `[05-speckit]` = 同上 §spec-kit 模板机制（命令流水线组织）
- `[01-pccr]` / `[01-sts]` / `[01-sp]` / `[01-cpo]` / `[01-mp]` / `[01-aks]` = 01-repos-deep.md 六仓库（pragmatic-clean-code-reviewer / stop-that-shit / superpowers / claude-plugins-official / mattpocock_skills / andrej-karpathy-skills）
- `[04-hooks]` / `[04-konishi]` / `[04-steer]` / `[04-cursor]` / `[04-guard]` = 04-smells-and-tools.md tools 部（Claude Code hooks 官方参考 / Konishi 指南 / Anthropic steering 博客 / Cursor rules / 本地 guardrail 仓库横评）

---

## 1. 统一规范

### 1.1 目录与文件构成

- 一个 skill = 一个目录，最少包含一个 `SKILL.md`；SKILL.md = YAML frontmatter + Markdown 正文，缺一不可 `[05-spec]`。
- 可选标准目录：`references/`（按需阅读的补充文档）、`scripts/`（可执行代码）、`assets/`（模板/图像/数据文件）；目录内其余文件与目录也允许 `[05-spec]`。
- 引用 skill 内其他文件时用相对 skill 根目录的相对路径；引用链保持一层深（从 SKILL.md 直接可达），禁止深嵌套引用链 `[05-spec]`。
- 发布级完整形态可加 README、LICENSE、配置模板、CI、测试（repo-steward 范例）`[06-A.2]`；纯方法论 skill 可以零附属文件（repo-refactor 范例）`[06-A.1]`——两种形态都合法，按是否需要机器可校验决定。

### 1.2 frontmatter 字段与限制

| 字段 | 必填 | 限制 | 说明 |
|---|---|---|---|
| `name` | 是 | 1-64 字符；仅 unicode 小写字母数字与连字符；不得以连字符开头/结尾；不得连续连字符；**必须与父目录名一致** | `[05-spec]` |
| `description` | 是 | 1-1024 字符 | 同时描述做什么与何时使用；含具体触发关键词 `[05-spec]` |
| `license` | 否 | 保持简短（许可证名或文件名） | `[05-spec]` |
| `compatibility` | 否 | 1-500 字符；仅在有特定环境要求时提供 | `[05-spec]` |
| `metadata` | 否 | 字符串键值 map；键名需独特防冲突 | `[05-spec]` |
| `allowed-tools` | 否 | 空格分隔工具列表；实验性，各宿主支持不一 | `[05-spec]` |
| `disable-model-invocation` | 宿主扩展 | `true` = 仅用户可显式调用（编排层 skill 用） | mattpocock 用此区分 user-invoked / model-invoked `[01-mp]` |

- **实践共识：frontmatter 保持干净**，仅在真正需要时加可选字段 `[05-bp]`；两个本地范例均只用 `name` + `description` 两字段 `[06-A.1][06-A.2]`。
- 正文（frontmatter 之后）无格式限制，推荐小节：分步指令、输入输出示例、常见边界情况 `[05-spec]`。

### 1.3 description 触发写法（自动触发的唯一杠杆）

- **两要素**：skill 做什么（能力）+ 何时使用（具体场景与触发条件）——缺一即失效 `[05-bp]`。
- agent 决定是否用 skill 只读 name + description；**skill 未按预期触发时修 description，不修正文** `[05-bp]`。
- 模型倾向**欠触发**（under-trigger），所以要推触发词：把用户可能的各种说法密集写进描述，含 "even if the word X never appears" / "even if they don't explicitly ask for X" 句式 `[05-bp][06-A.1]`。
- 实操清单：用第三人称（"Creates" 而非 "Create"）；用用户会用的关键词；避免 "helps with"/"assists in" 虚词；包含具体名词；具体到能与相邻 skill 区分 `[05-bp]`。
- **三段式结构**（repo-refactor 范例）：① 一句话能力定义；② 触发说法密集列举；③ 与兄弟 skill 的分工/反触发——description 同时承担路由裁决功能 `[06-A.1]`。
- 变体（repo-steward 范例）：两段式 = 定义 + 场景列举 + **核心政策一句话直接进描述**（保证只读元数据也知道立场）`[06-A.2]`。
- 常见失败模式：description 只说 skill 包含什么（"includes scripts for..."）而不说何时用 `[05-bp]`。
- "One skill, one purpose"：合并多职责会使 description 变模糊、损害两者可发现性，应拆分 `[05-bp]`。
- 发布前用真实 agent 实例测试触发；可用 should-trigger / should-not-trigger（含 near-miss 近邻误触例）eval 迭代 description `[05-bp]`。

### 1.4 长度红线

| 层级 | 红线 | 来源 |
|---|---|---|
| SKILL.md 正文 | 规范建议 <500 行；Anthropic 目标 <5k token 且 <500 行 | `[05-spec][05-bp]` |
| 主文件实测最佳实践 | 本地范例 99 / 105 行（路由器型主文件） | `[06-A.1][06-A.2]` |
| 单个 reference 文件 | 范例区间 35-112 行；超过 ~110 行且混多主题时应再拆 | `[06-A.1][06-A.2][06-A.4]` |
| 相邻参照：CLAUDE.md / 规则文件 | <200 行共识；超过后遵守率急剧下降 | `[04-steer][05-mnilax]` |

- 本域裁决（见 §6）：500 行是规范硬上限，5k token 是预算口径；路由型主文件目标 **100-150 行**；参考文件 50-110 行。
- 中文注意：等量信息中文 token 数与英文不同，行数红线比 token 红线更易控；但 L1 description 按 1024 字符硬限执行 `[05-spec]`。

### 1.5 渐进式披露三级（progressive disclosure）

1. **Level 1 Metadata（常驻，约 100 token）**：启动时为所有 skill 加载 name + description——"这是向 agent 营销 skill 的唯一机会"，所以触发词必须在这里 `[05-spec][05-bp]`。
2. **Level 2 Instructions（激活时加载，<5k token / <500 行）**：完整 SKILL.md 正文一次性载入；因此较长的内容应拆为被引用文件 `[05-spec][05-bp]`。
3. **Level 3 Resources（按需）**：references/、scripts/、assets/ 仅在需要时加载 `[05-spec][05-bp]`；**脚本是 deepest disclosure——代码执行不进入上下文**，能用脚本确定性解决的问题就不要用散文指示模型 `[05-bp]`。

- 拆分的正确维度**不是「章节」而是「决策分支」**：主文件走到哪个决策点（定级后 / 选规模后 / 路由到某域后）才加载对应文件 `[06-A.1]`。
- repo-steward 变体：按「症状/关切」拆（用户可见症状 = 触发时刻）`[06-A.2]`——两种拆法统一于"需要该文件的时刻"（moments 原则 `[05-bp]`）。
- 必须常驻的信息不得放 references（Cursor 规则同结论：@file 引用不内联展开，始终需要的内容写进正文）`[04-cursor]`。

### 1.6 references/ 组织

- 每个 reference 文件第一行写「Read this when...」触发条件，与主文件路由表一一对应 `[06-A.1]`。
- 单文件单主题、可独立阅读（不依赖主文件在场也能懂）`[06-A.1][06-A.4]`。
- 文件越小越省上下文；保持各 reference 聚焦 `[05-spec]`。
- 注册表模式（大型规则集范例）：pragmatic-clean-code-reviewer 把规则按族拆为 rules-code.md（20+3 条）/ rules-test.md（12+1 条），配 measurement.md（怎么测）、presets.md（阈值）、finding-schema.md（输出格式）、principles-glossary.md（可选引用源）——**"数什么"与"切点在哪"分离，规则条目与阈值表分离** `[01-pccr]`。
- 范例参考文件命名：按域/决策点命名（code-refactor.md、docs-refactor.md、aggression-levels.md、workflow-large.md `[06-A.1]`）或按症状命名（repository-hygiene.md、code-structure.md、change-gate.md `[06-A.2]`）。

### 1.7 scripts/ 组织与定位声明

- 脚本要求：自包含或清楚记录依赖；校验输入、检查错误条件、以清晰信息失败；优雅处理边界；长时操作分阶段输出；可用库但要锁定版本 `[05-spec][05-bp]`。
- 本地范例工程形态：全部仅用 Python 标准库；输出 JSON 证据、不做破坏性决策；配单元测试；SKILL.md 中放「脚本调用方式 + 定位声明」一节 `[06-A.2]`。
- **定位声明是必备写法**："Use scripts as evidence collectors; do not let them replace engineering judgment"（证据收集器，不是工程判断）`[06-A.2]`；并反复标注能力边界（如 "name, path, and size signals, not proof of provenance"）`[06-A.2]`。
- 诚实边界声明同样适用于 skill 本身：写明「不是什么」（stop-that-shit："not a sandbox"；skill 未武装 Guard 时不得宣称拦截）`[01-sts][04-guard]`。

### 1.8 hooks 与 skill 的配合（确定性 vs 概率性分工）

- 分工铁律："A system prompt is a request. A hook is a guarantee."——skill 正文是概率性建议；必须确定性发生的约束交给 hooks / 权限系统 / CI `[04-konishi][04-steer]`。
- 经验法则：确定性行为 → hooks；事实 → CLAUDE.md/rules；流程 → skills；隔离旁路 → subagents `[04-steer]`。
- compaction 行为差异（写 skill 时要假设的退化条件）：skills 正文仅在调用时加载、compaction 后共享预算最旧先丢；hooks 完全绕过 compaction `[04-steer]`——**长会话中 skill 指令会退化，红线类内容要么在每次路由时重读、要么配置为 hook**。
- 双形态模式（stop-that-shit 范例）：同一指令（`$stop-that-shit change -- ...` 首行契约）在仅装 Skill 时是提示，装 Guard 后变成 PreToolUse 机器边界——语义判断（Stop Ladder）住 SKILL.md，硬策略（五项可观察事实）住 Guard，**更新 Skill 不改变 Guard 策略** `[01-sts][04-guard]`。
- 大型质量 Skill 的落地建议：skill 内提供「可选 hooks 配方」参考文件（交宿主执行，如 PostToolUse 自动格式化、PreToolUse 拦危险命令），配方注明"格式化是便利不是门禁"级别差异 `[04-konishi]`；不要在散文里承诺强制行为 `[04-steer]`。
- 护栏本身也要有测试集（stop-that-shit 18 组 Bad/Good 判例做行为回归）`[04-guard]`——配 scripts/hooks 的 skill 应同样自测。

---

## 2. 大型多子 Skill 架构推荐

### 2.1 三种组织模式对比

| 模式 | 范例 | 结构 | 优点 | 代价 |
|---|---|---|---|---|
| A. 单 skill + references/ 拆分 | repo-refactor（1+5）`[06-A.1]`、repo-steward（1+7+scripts）`[06-A.2]`、pccr 注册表 `[01-pccr]` | 一个 SKILL.md 主入口，细节全在 references | L1 只占一条 description（~100 token）；触发决策单一；安装简单 | 全部触发时刻挤一个 description；正文必须承担全部路由 |
| B. 多 skill 目录 | mattpocock（user-invoked 编排层 + model-invoked 纪律层，`disable-model-invocation: true`）`[01-mp]`、stop-that-shit（stop-that-shit + stss 两 skill）`[01-sts]`、claude-plugins-official（plugin = agents/commands/skills 多件套）`[01-cpo]` | 每个子域独立 skill 目录 | 每个触发时刻（moment）独立、description 聚焦 `[05-bp]`；按"谁能调用"分层 `[01-mp]` | N 条 description 常驻 L1（N × ~100 token）；须显式写分工与 tie-breaker 防抢任务 `[06-A.4]` |
| C. skill 间互链 | superpowers（executing-plans 正文显式引用 verification-before-completion、systematic-debugging 等）`[01-sp]`、mattpocock grill-with-docs（全文 = 调 Skill 工具两次：grilling + domain-modeling）`[01-mp]` | 独立 skill 在正文按名引用兄弟 skill | 组合复用；无文件包含依赖 | 链接仅是提示，需被链 skill 的 description 也能独立触发 |

- 命令流水线变体（spec-kit）：`/speckit-*` 多命令 = 多入口 skill 链，一次调用一个、人在中间审阅——"constitution 每项目一次；specify→plan→tasks→implement→converge 每功能一轮" `[05-speckit]`。适合「流程分阶段 + 人工门禁」型内容，不适合常驻路由型内容。

### 2.2 推荐架构（针对「提高 AI 编程代码质量」大型中文 Skill）

**推荐：模式 A 为主体（主入口 Skill + references 决策分支 + scripts 证据收集器），仅对触发时刻显著不同的子域升格为兄弟 Skill（模式 C 互链）。**

理由：① 单条 L1 description 常驻成本最低，触发裁决最简单 `[05-spec]`；② 本地两个成熟范例（99/105 行主文件）证明该模式承载大型方法论可行 `[06-A.1][06-A.2]`；③ 注册表模式已在最大型范例（pccr，33 条规则 + 4 个协议文件）验证 `[01-pccr]`；④ 「审计 / 修复 / 评审」是不同触发时刻（moments `[05-bp]`），若主 agent 要求独立子 Skill，按 §2.6 升格判据处理。

目录树示例：

```
ai-code-quality/                     # 目录名 == frontmatter name（[05-spec]）
├── SKILL.md                         # 主入口，目标 100-150 行（见 §2.3）
├── references/                      # 按"需要该文件的决策时刻"拆（[06-A.1][05-bp]）
│   ├── scope-and-profile.md         # 定范围/定严格档（每次任务开始时读）
│   ├── smell-catalog-code.md        # 代码坏味道注册表（审计/评审代码域时读）
│   ├── smell-catalog-test.md        # 测试坏味道注册表（涉测试时读）
│   ├── quality-gates.md             # 裁判/基线/金丝雀/完成前验证（动手改与宣称完成前读）
│   ├── refactor-plays.md            # 修复模式选择表（决定怎么修时读）
│   ├── review-workflow.md           # 独立评审/跨模型评审流程（评审时读）
│   ├── anti-cheat.md                # agent 作弊模式与对抗性评审（涉测试变更时读）
│   └── hooks-recipes.md             # 可选确定性钩子配方（宿主支持时读）
├── scripts/                         # stdlib-only 证据收集器（[06-A.2]）
│   ├── scan_metrics.py              # 行数/嵌套/参数等机械测量，输出 JSON
│   └── tests/test_scan_metrics.py   # 脚本单元测试
└── assets/
    └── quality-config.toml          # 可选阈值配置模板（零配置可用）
```

### 2.3 主入口 SKILL.md 职责（七件套，均来自本地范例验证）

1. `# 标题` + **论点式开篇**：先断言问题本质，再给出全 skill 骨架概念（心智模型），不写细节 `[06-A.1][06-A.2]`。
2. **第一决策：定档/定级表**（如 L1-L4 表或 Quick/Full 两档表，列：级别 | 一句话定义 | 可观测行为 | 契约）+ 定档规则（用户显式指定 > 项目阶段推断 > 不确定带推荐地问）`[06-A.1][06-A.2]`。
3. **路由节**：按症状 → 参考文件，或按决策点 → 参考文件（写法见 §2.5）`[06-A.1][06-A.2]`。
4. **编号红线/核心原则**：每条一句话、加粗开头短语，凌驾于流程之上（价值观层）`[06-A.1][06-A.2]`。
5. **标准操作序列**：编号步骤，可照抄（代码块承载）`[06-A.1][06-A.2]`。
6. **脚本定位声明**（若带 scripts）：调用方式 + "evidence collectors, not judgment" `[06-A.2]`。
7. **完成标准 + 产出政策 + 与兄弟 skill 分工**：含负面清单（禁止生成一次性报告文件）与 tie-breaker 判据 `[06-A.1][06-A.2][06-A.4]`；结尾是参考文件路由表 `[06-A.1]`。

### 2.4 子文件（references）职责四规则

- 首行「Read this when: ...」触发条件，与主文件路由表一一对应 `[06-A.1]`。
- 单文件单主题、可独立阅读；50-110 行，超 110 行或混主题即再拆 `[06-A.1][06-A.4]`。
- 承载一类决策分支的细节（该分支的表、清单、操作序列、例外），不复述主文件全部红线——只按需引用触发词（如"宣称完成前重读主文件完成标准"）`[06-A.1]`。
- 规则集类文件采用注册表条目格式：每条含 symptom / detectors / exceptions / refactoring（+related），阈值与规则分离（阈值进配置或 presets 类文件）`[01-pccr]`。

### 2.5 路由表写法（三种并存，按信息形态选）

```markdown
<!-- 形态 1：决策点路由（repo-refactor 式）——用于流程型分支 -->
## 三域路由
| 变更对象 | 安全网 | 详细指导 |
|---|---|---|
| 代码 | 测试/lint/构建 | references/smell-catalog-code.md |
| 测试 | 断言位点/真实依赖 | references/smell-catalog-test.md |

<!-- 形态 2：症状路由（repo-steward 式）——用于用户可见问题 -->
## 按症状路由
- 嵌套过深、函数过长、上帝模块、重复 → references/smell-catalog-code.md
- 空断言测试、过度 mock、flaky → references/smell-catalog-test.md

<!-- 形态 3：结尾总路由表（必备）-->
## 参考文件
| 文件 | 何时读 |
|---|---|
| references/quality-gates.md | 动手修改前建裁判；宣称完成前 |
| references/anti-cheat.md | 任何测试被新增或修改时 |
```

来源：形态 1/3 `[06-A.1]`，形态 2 `[06-A.2]`，注册表按需加载 `[01-pccr]`。

### 2.6 升格判据：reference 何时升为独立子 Skill

满足任一条即升格为兄弟 Skill（模式 B/C）：
1. **触发时刻不同**（audit 时 / 修复时 / 评审时是不同 moment `[05-bp]`），且该域在主 skill 未激活时也需被独立触发；
2. 用户会显式点名调用（→ 考虑 `disable-model-invocation: true` 编排层 `[01-mp]`）；
3. 需要独立的双形态（skill + guard/hooks）`[01-sts]`。

升格后必做：新 skill 的 description 写三段式（定义 + 触发 + **与主 skill 的分工与反触发**）`[06-A.1]`；主 skill 的「Division of labor」节加 tie-breaker 判据 `[06-A.1][06-A.4]`；互链只按 skill 名在正文引用，不做文件包含 `[01-sp]`；编排层可调用纪律层、纪律层不得互调编排层 `[01-mp]`。

---

## 3. 行文风格

- **祈使句 + 可测试**：每条规则回答"这防止什么失误"；"be careful / think hard / really focus" 是纯噪音（实测合规率跌至 ~30%），换成具体祈使句（"state assumptions explicitly"）`[05-mnilax]`。
- **规则条数有预算意识**：实测 12 条以上合规率下降、200 行天花板真实存在（CLAUDE.md 场景数据，SKILL.md 参照适用）`[05-mnilax]`；主文件红线/原则控制在 ~10 条量级 `[06-A.2]`（repo-steward 10 条原则）。
- 示例不进规则正文：3 个示例 ≈ 10 条规则的上下文成本且过拟合 `[05-mnilax]`；正例/反例采用"每条规则一句话 + 一个正例一个反例"的紧凑形态（spec-kit 规则书写法）`[05-speckit]`。
- **高密度 cheat-sheet 优于散文**：匹配模型训练方式（训练数据就是 API 文档式高密度内容）`[05-bp]`；"目标清楚地说一次，让模型的训练补细节"——训练中已内化的信息无需复述 `[05-bp]`。
- 清晰度规则要**可数可查**（"clearly 是观点，规则可数"），但严控到死会丢信息（严格受控语言实测丢 46.8% 事实，宽松版丢 8.5%）——采用"可数规则 + 适度宽松" `[05-ste]`。
- **三种信息三种形态**：表格承载决策信息（级别表/路由表/模式选择表）；编号红线承载价值观；代码块承载可照抄操作序列 `[06-A.4]`。
- **负面清单优于正面清单**：把「不做」写成显式规则（不生成一次性报告、不混入功能、不过度清理）——比正面清单更能约束 agent `[06-A.4]`。
- 写全失败路径与边界情况（"If X fails, do Y"；缺失输入、畸形数据处理）——skill 不是工具清单，正文要解释工作流与编排 `[05-bp]`。
- 借口对照表 / 合理化防线表是高杠杆写法：列出 agent 常见自我合理化及反驳（superpowers TDD/验证/调试三 skill 均用此结构）`[01-sp]`。
- 中文行文要求：短句化（避免 40+ 词嵌套长句 `[06-A.4]`）；专家术语配一句话解释或中文对译 `[06-A.4]`。
- 诚实边界：能力边界、未验证事项、脚本局限显式写出（"evidence collectors, not judgment" `[06-A.2]`；"not a sandbox" `[04-guard]`；未武装不得宣称拦截 `[01-sts]`）。

---

## 4. 反模式清单（写作规范视角）

**description 类**
1. description 只说包含什么不说何时用 `[05-bp]`；2. 一个 skill 塞多职责使描述模糊 `[05-bp]`；3. description 过长（250 词级）推高每次会话常驻成本 `[06-A.4]`；4. 触发词缺失导致欠触发（修 description 而非正文）`[05-bp]`；5. 兄弟 skill 描述互不声明分工 → 两 skill 抢同一任务 `[06-A.4]`。

**结构类**
6. SKILL.md 超 500 行 / 5k token `[05-spec][05-bp]`；7. references 深嵌套引用链（>一层深）`[05-spec]`；8. 按章节而非决策分支拆文件 `[06-A.1]`；9. reference 首行无触发条件、与主文件路由表脱节 `[06-A.1]`；10. 单 reference 超 ~110 行且混多主题 `[06-A.4]`；11. 必须常驻的信息误放 references（引用不内联展开）`[04-cursor]`。

**行文类**
12. 不可测试的口号式规则（"be careful"）`[05-mnilax]`；13. 示例堆积进规则正文 `[05-mnilax]`；14. 规则总数失控（>12 条合规率降）`[05-mnilax]`；15. 嵌套长句、术语无解释 `[06-A.4]`；16. 同一规则无节制多处重复（独立成立 vs token 成本需权衡）`[06-A.4]`；17. 依赖可能不存在的工具的措辞（"always use eslint"→ 换能力无关措辞 "match the codebase's enforced style"）`[05-mnilax]`。

**机制类**
18. 用散文承诺强制行为（"系统提示是请求，钩子才是保证"）`[04-konishi][04-steer]`；19. 能用脚本确定性解决的问题写成散文指示 `[05-bp]`；20. 脚本无定位声明与边界标注、或让脚本做破坏性决策 `[06-A.2]`；21. 声称未验证的效果（skill 未实测触发、guard 未武装宣称拦截）`[05-bp][01-sts]`；22. 生成一次性 SUMMARY/ANALYSIS/报告类工件污染仓库 `[06-A.2]`。

---

## 5. 参考范例映射

| 规范要素 | 直接范例 |
|---|---|
| 主入口七件套 / references 单文件拆分 | repo-refactor、repo-steward `[06-A.1][06-A.2]` |
| description 三段式 + 分工反触发 | repo-refactor `[06-A.1]`；Anthropic dashboard 案例 `[05-bp]` |
| description 政策前置一句话 | repo-steward `[06-A.2]` |
| 注册表式 references（规则/阈值/格式/词汇表分离） | pragmatic-clean-code-reviewer `[01-pccr]` |
| 编排层/纪律层双层 skill（user-invoked 调 model-invoked） | mattpocock_skills `[01-mp]` |
| skill 间互链（正文按名引用兄弟 skill） | superpowers `[01-sp]` |
| 双形态：skill 建议层 + guard 机器层同指令 | stop-that-shit `[01-sts][04-guard]` |
| 命令流水线多入口 + 人工门禁 | spec-kit `/speckit-*` `[05-speckit]` |
| scripts 证据收集器 + stdlib + 测试 + 定位声明 | repo-steward `[06-A.2]` |
| 借口对照表 / 红旗清单写法 | superpowers TDD/验证/调试 `[01-sp]` |
| 简短原则清单（10 条式） | repo-steward Core principles `[06-A.2]`；karpathy 四原则 `[01-aks]` |
| 确定性/概率性分工配方 | Anthropic steering 博客、Konishi hooks 指南 `[04-steer][04-konishi]` |

---

## 6. 已裁决矛盾（本域裁决记录）

1. **description "pushy" vs 简洁** → 裁决：**密集但在界内**。触发词密集列举是必要的（欠触发是默认失败模式 `[05-bp]`），但受 1024 字符硬限 `[05-spec]` 与常驻成本约束 `[06-A.4]`：三段式保留 `[06-A.1]`，触发列举压缩到最高频用户说法，核心政策只留一句 `[06-A.2]`，其余移入主文件正文。
2. **SKILL.md <500 行 vs <5k token vs 越短越好** → 裁决：**三个口径分层**。500 行 = 规范硬上限 `[05-spec]`；5k token = 预算口径 `[05-bp]`；路由型主文件的工程目标是 100-150 行（本地范例 99/105 行 `[06-A.1][06-A.2]`），细节下放 references（50-110 行/文件）。
3. **拆分维度：流程阶段 vs 症状** → 裁决：统一为「**需要该文件的决策时刻**」（moments 原则 `[05-bp]`）。repo-refactor 按决策点（定级后/选域后）`[06-A.1]`、repo-steward 按症状 `[06-A.2]` 是同一原则的两种投影：症状本身就是用户侧的触发时刻。路由表两式并存（§2.5）。

---

## 待裁决矛盾（需主 agent 决策）

1. **「主入口+若干子 Skill」的实现形态**：内嵌 references（单 skill，本域推荐 §2.2）vs 独立子 skill 目录（多 skill，每条 description 常驻 ~100 token，N 个子 Skill = N 份 L1 成本 `[05-spec]`）。若目标宿主（ZCode）的 skill 发现机制/插件体系支持多 skill 且 L1 预算宽松，可对「审计/修复/评审」三个触发时刻各设独立子 skill 并互链 `[05-bp][01-sp]`；否则按 §2.2 单主入口。**取决于宿主机制与子 Skill 数量，主 agent 裁决。**
2. **description 与正文语言**：规范允许任意字符（1-1024）`[05-spec]`，但全部范例 description 为英文 `[06][01]`；中文 description 对中文用户触发的命中率无实测数据，用户混用英文术语（"refactor"、"review"）时的匹配行为未知。可选：中文为主 + 关键英文触发词混排。**需实测或由主 agent 定策略。**
3. **是否捆绑确定性 scripts（+测试）**：repo-refactor 纯方法论（无脚本，正确性无法机器校验）vs repo-steward 带脚本（维护成本 + 宿主 Python 依赖）`[06-A.3]`。本域倾向带最小 stdlib 脚本集（质量域的行数/嵌套/断言位点测量是高价值确定性证据 `[01-pccr]`），但脚本数量与测试深度需主 agent 按维护预算定。
4. **重复度上限**：「重要的事说三遍」（各文件独立成立 `[06-A.1]`）vs 总 token 最小化 `[06-A.4]`——红线/反作弊在主文件与相关 reference 中的重复次数无定量标准，建议 ≤2 处且措辞不同，主 agent 可按实测 token 预算调整。
5. **是否建触发 eval 集**：Anthropic 建议 should-trigger / should-not-trigger（含 near-miss）eval 迭代 description `[05-bp]`——成本 vs 触发质量，主 agent 决定是否投入。
6. **主文件规则总条数**：mnilax 的 12 条上限 / 200 行天花板数据来自 CLAUDE.md 场景 `[05-mnilax]`，对 SKILL.md 正文（激活才加载、非全时常驻）的适用性未验证——红线+原则合计条数上限（本域暂按 ~10-15 条工程估计）需主 agent 定。
