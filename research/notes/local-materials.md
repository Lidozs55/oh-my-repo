# 本地初始材料精读笔记

- 分析对象：`repo-refactor/`（SKILL.md + 5 个 references）、`repo-steward/`（SKILL.md + 7 个 references + README + scripts 扫描）、`discussion.txt`（28 行中文讨论）
- 用途：为「提高 AI 编程代码质量 / 指导 AI 优化低质量代码」大型中文 Skill 的构建提供结构规范与知识点素材
- 日期：2026-10-11

---

## A. Skill 工程结构规范

### A.1 repo-refactor 的组织方式

**Frontmatter（仅 2 个字段）**
- 只有 `name` + `description`，无其他元数据字段。
- `description` 约 250 词英文长段，单段不换行，结构为三段式：
  1. 一句话定义能力域（"Deep refactoring, rewriting, and optimization of everything inside a repository - ..."）；
  2. 触发条件密集列举（"Use whenever the user asks to refactor, rewrite, clean up..., mentions tech debt, code rot, legacy code, migration, modernization..., even if the word 'refactor' never appears"）——把用户可能的各种说法都塞进描述以提升自动触发命中率；
  3. 与兄弟 skill 的分工/反触发（"For behavior-preserving hygiene passes ... prefer repo-steward; this skill is for 'get better' redesign..."）——description 同时承担路由裁决功能。

**SKILL.md 正文结构（99 行，H2 分节，无 H3）**
1. `# 标题` + 一段「论点式」开篇：先断言问题本质（"agents fail most often, and the root cause is the harness, not the model"），再给出全 skill 的骨架概念（rulebook / judge / queue / gate / rollback 五要素）——主文件负责心智模型，不负责细节。
2. `## Step one, always: pick the aggression level`：L1-L4 四级表格（级别 | 名称 | 一句话定义 | 可观测行为 | 契约），紧跟 5 条 leveling 规则（用户显式指定 > 项目阶段推断 > L4 必须显式签核 > 不确定时带推荐地问 > 特定域先读对应参考）。
3. `## Step two: pick the scale`：轻量路径 vs 完整工作流的触发条件清单，明确「阈值是估计不是法律」、允许中途升级、不允许中途降级。
4. `## Lightweight path: the micro-loop`：用代码块给出编号步骤（0-4），把 git 检查、爆炸半径、judge 基线、微循环、终检写成可照抄的操作序列。
5. `## Three-domain routing`：表格路由（变更对象 | 安全网 | 详细指导文件），代码/文档/产品逻辑三个域各配不同安全网。
6. `## Red lines`：7 条编号红线，每条加粗开头短语（"Judge before blade"、"Archaeology before deleting"...），凌驾于所有流程之上。
7. `## Completion standard`：按级别分层的验收标准（含 no-op 检测、行为增量日志、新验收标准）+ 报告格式约束（禁止生成 REFACTOR_REPORT.md）。
8. `## Division of labor with other skills`：与 repo-steward、browser-use 的分工及 tie-breaker 判据。
9. `## Reference files`：结尾表格（File | When to read），每个参考文件对应明确读取时机——这是渐进式披露的路由表。

**references/ 拆分（5 个文件，36-98 行）**
| 文件 | 行数 | 主题 | 与主文件关系 |
|---|---|---|---|
| aggression-levels.md | 98 | L1-L4 每级的 Allowed/Forbidden/Safety net/Acceptance/Commit discipline/User prompt signals 六段式 | 主文件定级，本文件给执行细则 |
| code-refactor.md | 73 | 代码域：安全网构建（测试分诊/特征测试/奇偶校验 harness/canary 验证）、迁移模式选择表、执行循环、反作弊、考古协议 | 主文件路由到代码域时的展开 |
| docs-refactor.md | 36 | 文档域：Diátaxis 四类型、一事一主、7 步工作流、文档级 L1-L4 含义、反模式 | 最短的域参考 |
| product-logic.md | 52 | 产品操作逻辑域：journey 三件套、L4 验收操作化、按阶段迁移策略 | 主文件路由到交互逻辑时的展开 |
| workflow-large.md | 76 | 大重构 Phase 0-7 全流程，每阶段结尾 = 证据工件 + 门禁 | 完整工作流的执行手册 |

- 每个 reference 文件第一行都是「Read this when...」触发条件，与主文件的路由表一一对应。
- 拆分维度不是「章节」而是「决策分支」：主文件走到哪个决策点（定级后/选规模后/路由到某域后），才加载对应文件。

**附属文件**：无 scripts、无 README、无 LICENSE——纯方法论 skill，全部靠提示词约束。

### A.2 repo-steward 的组织方式

**Frontmatter（仅 2 个字段）**
- `name` + `description`。description 明显短于 repo-refactor（约 90 词），结构为两段式：
  1. 一句话定义 + 场景列举（"Keep software repositories lean, coherent, and current while coding, refactoring, reviewing, or cleaning up. Use for repository hygiene audits, code-structure cleanup, oversized-file or god-module investigation, documentation organization and drift prevention, AI-output cleanup, legacy repository rehabilitation, and pre-commit or pre-PR quality gates."）；
  2. 核心政策直接进描述（"Prefer deleting, consolidating, or reusing over adding..."）——把 skill 的「宪法」压缩进 description，保证即使只读元数据也知道立场。

**SKILL.md 正文结构（105 行）**
1. `# 标题` + 一句论点（"Reduce repository entropy without replacing one kind of mess with another"）+ 一句目标定义（最小一致仓库，而非更多结构）。
2. `## Core principles`：10 条编号原则，每条一句话，是全 skill 的价值判断基线。
3. `## Route to focused guidance`：按「症状 → 参考文件」的 bullet 路由（7 条，每条以用户可见症状开头，如 "Oversized files, god modules, duplication..."）。
4. `## Standard operating sequence`：Quick/Full 两档深度的表格 + 9 步标准序列（读本地规则 → 定边界 → 先侦查后编辑 → 定义可观测成功 → 最小一致变更 → 查熵 → 验证 → 检查 diff → 紧凑报告）。
5. `## Deterministic helpers`：bash 代码块列出 5 个脚本调用方式 + "Use scripts as evidence collectors; do not let them replace engineering judgment" 定位声明。
6. `## Decision rules before adding things`：按被添加物类型（文件/抽象/文档/依赖/注释/报告）列出「添加前必答问题」。
7. `## Repository output policy`：禁止生成的产物清单（SUMMARY.md、ANALYSIS.md、FIX_REPORT.md 等）。
8. `## Cleanup safety`：Safe / Review / Protected 三级删除安全分类。
9. `## Completion standard`：两句话收尾。

**references/ 拆分（7 个文件，35-112 行）——按「症状/关切」拆，不按流程阶段拆**
| 文件 | 行数 | 主题 |
|---|---|---|
| repository-hygiene.md | 38 | 物理垃圾：临时文件、密钥、生成物、根目录混乱 |
| code-structure.md | 67 | 大文件/上帝模块/重复/深嵌套/过早抽象 |
| docs-maintenance.md | 112 | 文档角色表、漂移检测、临时文档退役（最长的参考） |
| output-hygiene.md | 37 | AI 产出治理：注释、散文、报告、最终回复格式 |
| change-gate.md | 66 | 提交/PR 前门禁：diff 焦点、验收证据、验证顺序、独立评审 |
| legacy-cleanup.md | 44 | 存量烂仓库的 4 阶段分期康复 |
| configuration.md | 35 | .repo-steward.toml 配置格式（阈值 + 文档归属映射） |

**scripts/ 角色（6 个 Python 文件 + 1 test 文件）**
- `repo_scan.py`（按 RISKY_NAMES/RISKY_SUFFIXES/JUNK_SUFFIXES/JUNK_PARTS 扫描垃圾与密钥）、`file_metrics.py`（行数统计与阈值分级）、`docs_inventory.py`（文档与链接清单）、`docs_drift.py`（按配置映射检查未提交/更新提交的漂移候选）、`diff_guard.py`（staged/unstaged diff 检查）、`common.py`（git 调用、配置加载公共函数）。
- 全部仅用 Python 标准库；输出 JSON 证据，不做破坏性决策；tests/ 有单元测试。
- SKILL.md 与参考文件中反复标注脚本的能力边界（"name, path, and size signals, not proof of provenance"）。

**附属文件（完整独立仓库形态）**：README.md（54 行：四类熵、安装、工作流索引、脚本说明、设计立场、测试、许可证）、LICENSE（MIT）、assets/repo-steward.toml（配置模板）、agents/openai.yaml（ agent 接口元数据）、.github/workflows/ci.yml、.gitignore——这是一个「发布级」skill 的完整工程形态。

### A.3 两个 Skill 的设计哲学差异

| 维度 | repo-refactor | repo-steward |
|---|---|---|
| 定位 | "get better"：重设计、重写、迁移 | "get clean"：保行为的熵清理 |
| 风险姿态 | 激进但分级：L1-L4 给自由度，级越高自由越大、验收越严 | 保守：默认删/合并/复用优先于新增，处处防过度工程 |
| 核心机制 | harness 五件套（规则书/裁判/队列/门禁/回滚）+ 分级 + 分域 | 原则清单 + 症状路由 + 决策问句 + 删除安全分级 |
| 确定性来源 | 纯方法论（git、测试、parity 脚本由 AI 现场构建） | 自带确定性脚本作为证据收集器 |
| 门禁 | 显式人类门禁（"human approval = start the next phase"） | 较弱：change-gate 是检查单，不是阶段门 |
| 行文风格 | 长句、密集、断言式、表格多、含轶事证据（Knight Capital、576 行规则书、16000 编译错误） | 短句、清单式、克制、几乎无轶事 |
| 与对方关系 | 描述里声明把保行为清理让给 steward | 覆盖 steward 自己的边界，不做大重构 |

### A.4 值得借鉴的优点与应避免的缺点

**优点（仿照构建新 Skill 时照搬）**
1. description 三段式写法：能力定义 + 触发说法密集列举（含 "even if the word X never appears"）+ 与兄弟 skill 的分工裁决——这是自动触发的关键面。
2. 主文件 = 决策路由 + 不变量（红线/原则），参考文件 = 决策分支细节；每个参考文件首行写触发条件；主文件结尾放「File | When to read」路由表——渐进式披露的标准范式。
3. 用表格承载决策信息（级别表、路由表、模式选择表、两档深度表），用编号红线/原则承载价值观，用代码块承载可照抄的操作序列——三种信息三种形态。
4. 长度控制：主文件约 100 行，参考文件 35-112 行；单文件单主题，可独立阅读。
5. 验收与反作弊面向 agent 特有失败模式（四种作弊模式、no-op 检测、judiciary canary 验证）——新 Skill 的「AI 代码质量」主题尤其需要这类内容。
6. 把「不做」写成显式规则：不生成一次性报告、不混入功能、不过度清理、不机械拆文件——负面清单比正面清单更能约束 agent。
7. 脚本定位声明（"evidence collectors, not engineering judgment"）与能力边界标注——带脚本 skill 的必备写法。
8. 跨 skill 显式分工 + tie-breaker 判据，避免两个 skill 抢同一任务。

**缺点（新 Skill 应避免）**
1. repo-refactor 的 description 过长（约 250 词），每次会话常驻成本高——中文大 Skill 若 references 更多，应考虑把部分触发词移到主文件正文。
2. repo-refactor 行文长句嵌套深（单句常 40+ 词），对非英语母语模型和中文使用者不友好——中文 Skill 应短句化。
3. 同一规则在多处重复（微循环在 SKILL.md 与 code-refactor.md 各一遍；反作弊出现 3 处）——有利于各文件独立成立，但推高总 token；需权衡「重要的事说三遍」与上下文成本。
4. 大量依赖专家术语（Fowler、Strangler Fig、Diátaxis、Expand-Contract、PEP 387、SemVer）无内嵌解释——中文 Skill 面向更广受众，术语需配一句话解释或中文对译。
5. docs-maintenance.md 112 行且混合工作流+角色表+脚本边界说明，是 repo-steward 中最「重」的文件——单参考文件超过 ~110 行时宜再拆。
6. repo-refactor 无任何脚本/可执行工件，方法论正确性无法机器校验；repo-steward 有脚本但 CI/测试较薄——新 Skill 若能配确定性检查脚本应配，并配测试。

---

## B. 知识点清单

（仅罗列，不整合、不取舍。来源为文件路径或 discussion.txt:行号）

### B.1 repo-refactor/SKILL.md

- [来源: repo-refactor/SKILL.md] 重构是 agent 最常失败的任务类型之一，根因是 harness（执行装置）而非模型本身
- [来源: repo-refactor/SKILL.md] 好的重构 harness 五组件：rulebook（规则书）、judge（裁判）、queue（队列）、gate（门禁）、rollback（回滚）
- [来源: repo-refactor/SKILL.md] 激进程度分级 L1 保守：严格 Fowler 重构，行为保持的结构改进，零变化（bug 也算行为）
- [来源: repo-refactor/SKILL.md] L2 标准：内部清理与局部改进，公共面不变（公共契约冻结、内部自由）
- [来源: repo-refactor/SKILL.md] L3 大胆：边界重设计，受控变更逐条记录，通过 Expand-Contract 改契约
- [来源: repo-refactor/SKILL.md] L4 自由：产品质量优先重设计，任何变化都允许，旧契约可整体抛弃
- [来源: repo-refactor/SKILL.md] 定级规则：用户显式表态（"keep it safe"/"go wild"）直接服从
- [来源: repo-refactor/SKILL.md] 无显式表态时先判断项目阶段：无外部消费者+无持久化 schema+无 API 消费者 = 开发期，默认 L2-L3 且可建议直接放弃兼容；已发布有用户则从 L1-L2 起
- [来源: repo-refactor/SKILL.md] monorepo 中按包/组件分别定级；跨组件共享代码遵循最严格的适用级别
- [来源: repo-refactor/SKILL.md] 大爆炸式全局重设计（L4）永远是需用户签核的显式选择，绝不作为默认——怪异的旧代码携带隐性知识，重写有真实成本
- [来源: repo-refactor/SKILL.md] 「不重构 / 只做最小修复」是合法结论，应在定级评估后诚实提出
- [来源: repo-refactor/SKILL.md] 不确定且选择会实质改变行为/兼容性/范围时，带着推荐去问用户
- [来源: repo-refactor/SKILL.md] 文档或产品逻辑目标的级别含义不同——决定之前（而非之后）先读对应参考文件的级别章节
- [来源: repo-refactor/SKILL.md] 规模选择：轻量路径 = 单模块、预计 ≤5 文件、不动公共契约、用户要快清
- [来源: repo-refactor/SKILL.md] 完整工作流触发条件（任一）：跨 ≥3 模块或 >10 文件；触碰公共 API/CLI/配置格式/持久化 schema；文档系统级重构；产品操作逻辑变更；遗留现代化或语言/框架迁移；用户明说大重构
- [来源: repo-refactor/SKILL.md] 阈值是估计不是法律；中途发现爆炸半径超轻量标准可立即升级为完整工作流；中途降级不存在——要么做完要么显式中止
- [来源: repo-refactor/SKILL.md] 微循环第 0 步：工作树必须干净（或先与用户确认现有变更）；确认在分支上
- [来源: repo-refactor/SKILL.md] 非 git 仓库是风险乘数：建议先 git init 或文件快照；否则只能在 ≤L2 下以更小步进行并明告无逐步回滚
- [来源: repo-refactor/SKILL.md] 爆炸半径报告：受影响文件数 + 风险层级（低=单叶子模块无契约；中=多模块或共享助手；高=任何契约/schema/用户旅程被触碰）
- [来源: repo-refactor/SKILL.md] 就地建裁判：找仓库现有测试/lint/构建命令，先跑一遍记录基线（含既有失败）；没裁判绝不动代码——先写钉住当前行为的特征测试
- [来源: repo-refactor/SKILL.md] 微循环：a.一句话陈述本步意图（提取 X/内联 Y/移动 Z）→ b.应用变更 → c.跑裁判 → d.绿=原子提交（"refactor:" 前缀）/红=git 回滚本步、拆更小、重试
- [来源: repo-refactor/SKILL.md] 全部步骤后跑一次宽验证（全量测试或更宽构建）并对照第 2 步基线报告
- [来源: repo-refactor/SKILL.md] 三域路由：代码域安全网=测试/lint/构建/奇偶 diff；文档域=类型审计+规范属主+链接命令抽查；产品操作逻辑域=旅程清单+当前行为快照+行为增量日志
- [来源: repo-refactor/SKILL.md] 混合变更：选主要目标对应的参考；对其余两域至少读其安全网章节
- [来源: repo-refactor/SKILL.md] 红线 1：裁判先于刀刃，且裁判必须被验证——在原代码上通过（或仅以基线记录的既有方式失败），且蓄意破坏其所覆盖内容时会变红；"绿"永远指相对基线无新失败，而非"全部通过"
- [来源: repo-refactor/SKILL.md] 绝不修改既有测试来变绿；≤L2 时既有失败只记录不修复；未经验证的裁判不是裁判
- [来源: repo-refactor/SKILL.md] 红线 2：绿则原子提交、红则立即回滚；git 检查点是唯一保险，"工作树随时可 reset"是勇气来源
- [来源: repo-refactor/SKILL.md] 红线 3：绝不混合重构与功能工作（≤L2 严格禁止；L3/L4 行为变更与结构迁移也分开提交以便评审）
- [来源: repo-refactor/SKILL.md] 红线 4：删不懂代码前先考古：git blame、邻近注释、相关测试；丑陋的一行可能编码了数周调试
- [来源: repo-refactor/SKILL.md] 红线 5：测试变更必须接受对抗性评审；绝不为实现改断言——断言真错就先证明再改；警惕四种作弊模式：把被测代码拷进测试、测试提前返回、无论结果都打印成功的脚本、掏空断言
- [来源: repo-refactor/SKILL.md] 红线 6：不可逆/破坏性动作的用户门禁：删除公共资产、触碰持久化 schema、删数据、移除有外部消费者的接口
- [来源: repo-refactor/SKILL.md] 红线 7：收缩（Contract）必须显式：要么完成（验证零引用）要么列为显式 TODO；跳过收缩比不重构更糟——遗留兼容层/开关都是带利息的债
- [来源: repo-refactor/SKILL.md] 完成标准：≤L1 全裁判相对基线绿；L2 公共面裁判绿 + no-op 检测（diff 反映预期结构变更而非化妆性搅动）
- [来源: repo-refactor/SKILL.md] ≥L3 额外产出行为增量日志：每条受控行为变更一行 `旧行为 → 新行为 | 原因 | 爆炸半径`；L4 还须定义并通过新验收标准（产品质量如何度量）
- [来源: repo-refactor/SKILL.md] 紧凑报告：改了什么、如何验证、剩余风险、显式 TODO；不生成 REFACTOR_REPORT.md 之类一次性报告文件（除非用户要求或仓库惯例）
- [来源: repo-refactor/SKILL.md] 与 repo-steward 分工：只原地删除/合并冗余产物用 steward；一旦跨调用者重构（提取/移动/重命名/重划边界）就是 refactor，用本 skill；两者可先后串联
- [来源: repo-refactor/SKILL.md] browser-use 技能用于产品操作逻辑的"当前行为快照"，实地录下现有流程

### B.2 repo-refactor/references/aggression-levels.md

- [来源: repo-refactor/references/aggression-levels.md] 核心原则：激进越高自由越大但验收越严——授权不是放任（delegation is not abdication）
- [来源: repo-refactor/references/aggression-levels.md] 公共面定义：你被允许改变的边界之外的所有消费者能观察到的一切——库的导出 API、应用的入口及其 I/O（CLI 参数/输出/退出码、配置文件、持久化 schema、网络 API、机器可读日志）；边界模糊时按更宽的面当作公共
- [来源: repo-refactor/references/aggression-levels.md] L1 精髓：bug 也是行为，修 bug 就是违规；bug 单独记录、在自己的变更中处理
- [来源: repo-refactor/references/aggression-levels.md] L1 允许：提取/内联函数与变量、移动、重命名、去重、简化条件与控制流、消除魔数、条件转多态等 Fowler 手法；有基准证据的语义保持性能优化
- [来源: repo-refactor/references/aggression-levels.md] L1 禁止：任何可观测行为变化——输出、返回值、日志、错误文案；接口语义（签名可变、语义不可变）
- [来源: repo-refactor/references/aggression-levels.md] L1 安全网：特征测试钉住当前行为，期望值来自真实运行结果（绝不靠猜填），基线含既有 bug，基线单独提交
- [来源: repo-refactor/references/aggression-levels.md] L1 提交纪律：每个原子手法一个 "refactor:" 提交，消息注明所用手法；用户信号词："keep it safe"/"pure refactor"
- [来源: repo-refactor/references/aggression-levels.md] L2 安全网双层裁判：公共面测试（终审，贯穿到底）+ 实现耦合测试（改写为可同时对旧/新实现运行的可移植断言）
- [来源: repo-refactor/references/aggression-levels.md] L2 提交纪律：死代码删除单独提交并在消息中附考古证据（如 "last touched 2023-x, no callers, grep-verified"）
- [来源: repo-refactor/references/aggression-levels.md] L3 核心：契约可变，但变化是受控过程；用 Expand-Contract 模式（Expand → Migrate → Contract 三段独立提交）
- [来源: repo-refactor/references/aggression-levels.md] L3 Migrate 阶段：把 grep 出的调用者清单当隐式契约，逐个迁移逐个验证；"剩余调用者数"是进度指标；每步保持可编译可测试
- [来源: repo-refactor/references/aggression-levels.md] L3 禁止跳过 Contract；Knight Capital 事故由遗留过期开关引起（兼容层是带利息的债的实例）
- [来源: repo-refactor/references/aggression-levels.md] L3 验收：新契约裁判绿 + 完整行为增量日志 + 迁移指南（新旧映射表，可自动化时写 codemod）+ Contract 完成或显式追踪
- [来源: repo-refactor/references/aggression-levels.md] L4 前提条件（全部满足）：开发期或用户显式授权；新验收标准已定义（每条核心旅程有可验证标准，否则"质量优先"退化为"我感觉更好"）；先做弃置式试点（试点只产出规则修订与设计修正，试点代码扔掉）
- [来源: repo-refactor/references/aggression-levels.md] L4 仍禁止：把"我感觉更好"当验收；功能无声消失——即使整体弃兼容也要留 changelog 和一行迁移说明（SemVer 0.x 允许破坏但不允许静默破坏）；无门禁的不可逆动作
- [来源: repo-refactor/references/aggression-levels.md] 门禁的含义："人类批准 = 开始下一阶段"，而不是每步都问
- [来源: repo-refactor/references/aggression-levels.md] L4 安全网：面向新契约建裁判（先为新旅程写验收测试）；旧代码作为参考实现（奇偶 diff 非空不再是失败——差异是重设计的产出，逐条记入行为增量日志）
- [来源: repo-refactor/references/aggression-levels.md] L4 提交纪律：分阶段大提交 + 每阶段 tag/分支支持整阶段回滚；每个阶段边界是安全停靠点
- [来源: repo-refactor/references/aggression-levels.md] 定级自检：用户口中的"重构"常是 L3/L4 重设计——先对齐级别，避免挂 L1 之名行 L4 之事
- [来源: repo-refactor/references/aggression-levels.md] 反向自检：已发布产品上的"顺带小改动"常是伪装的契约变更——变更清单一出现公共面条目就升级流程或缩小变更
- [来源: repo-refactor/references/aggression-levels.md] 单任务可分块定级："核心模块 L1、外围工具 L4"，把每块的级别写进任务卡

### B.3 repo-refactor/references/code-refactor.md

- [来源: repo-refactor/references/code-refactor.md] 测试分诊：公共面测试（走公共接口/CLI/端到端）= 原样终审；实现耦合测试（mock 内部结构、测私有函数）= 改写为可移植断言，只断言可观测行为、绝不断言内部形状
- [来源: repo-refactor/references/code-refactor.md] 特征测试四规则：期望值来自真实运行输出；基线含既有 bug（钉住"是什么"而非"应该是什么"）；基线单独提交后才能改结构；重构后 diff 非空 → 有意变更（更新基线+记日志+必要时确认）vs 无意变更（回滚）
- [来源: repo-refactor/references/code-refactor.md] 没有测试框架也能建裁判：一次性奇偶脚本（代表性输入跑目标函数、打印输出、前后 diff）就是合法特征基线且零依赖；给仓库加测试框架本身就是仓库变更，需用户同意
- [来源: repo-refactor/references/code-refactor.md] 代码无法隔离执行（网络/DB/时间/硬件依赖）时：在最近可行接缝测试（CLI 入口、公共 API、模块边界）；没有接缝就把"造接缝"作为第一步重构（提取薄封装），或用 Sprout/Wrap（只加新码不碰旧码），或降低激进级别
- [来源: repo-refactor/references/code-refactor.md] 奇偶 harness：挑约 7 个代表性输入场景，新旧实现输出逐项 diff；diff 前先归一化（剥时间戳/路径/id、排序无序集合、规范化 NaN/Infinity）；裁判突报大量失败时先怀疑比较器再怀疑代码
- [来源: repo-refactor/references/code-refactor.md] 裁判金丝雀验证：新裁判必须在原代码上绿、在你蓄意破坏一处时红；未验证裁判的绿灯不可信
- [来源: repo-refactor/references/code-refactor.md] 迁移模式选择表：原地增量微循环（同语言纯重构默认项，先做前置清理降噪）；Branch-by-Abstraction（替换被多处引用的实现：建抽象→逐调用者迁移→切换→删旧+抽象，剩余调用者数=进度）；Expand-Contract（不兼容接口/数据变更，三段独立提交，数据迁移用校验和比对）；Strangler Fig（整体替换子系统/服务，先立 facade/路由，新旧共存切片切换，适合有真实流量的系统）；并行新码库+切换（整体搬迁如语言迁移，配奇偶 harness；JS→TS 这类增量超集迁移不值得并行码库）
- [来源: repo-refactor/references/code-refactor.md] 每种模式下：切换/删旧点之前建回滚分支；"不迁移"永远是合法结论
- [来源: repo-refactor/references/code-refactor.md] 裁判定价：秒级裁判（lint/类型检查/单测）每轮跑；分钟级裁判（全量构建/集成测试）分批跑
- [来源: repo-refactor/references/code-refactor.md] Pattern-first 原则：同类错误第 2 次出现 = 规则有罪 → 修规则书 → 重新生成整批受影响文件；绝不违反规则对单文件手工打补丁
- [来源: repo-refactor/references/code-refactor.md] 分歧型近似重复不是重复代码：合并前先在真实输入上 diff 行为；相同→≤L2 随意合并；分歧→统一即行为变更（≤L2 保留两份或参数化，≥L3 记日志或问用户哪个是正典）
- [来源: repo-refactor/references/code-refactor.md] No-op 检测：收尾时问"这个 diff 产生了什么可验证的变化"；纯清理批次要显式声明是纯清理
- [来源: repo-refactor/references/code-refactor.md] 四种 agent 作弊模式（均来自实战观察）：把被测代码拷进测试以"去依赖"；让测试提前返回；生成无论结果都打印 "Test passed!" 的脚本；掏空断言换取表面绿灯
- [来源: repo-refactor/references/code-refactor.md] 禁止 "0→80% 覆盖率"大跃进（诱发作弊）；用种子样例加测试，每条可单独验证；第二视角（新会话/独立子 agent）复审所有测试 diff 是硬要求
- [来源: repo-refactor/references/code-refactor.md] 删码考古协议：git blame 看最后修改时间与提交信息；读邻近注释与相关测试；grep 所有引用（含字符串/反射/配置里的动态引用）；仍不确定→保留并注释或问用户；绝不在不确定时删迁移/锁文件/fixture/用户数据
- [来源: repo-refactor/references/code-refactor.md] 上下文与并行：计划/队列持久化到磁盘每轮重读；机械批量变更派给子 agent 且只带回结论；并行甜点区很低：实现 agent ≤2 个（token 成本 3-10 倍）；评审者最受益于更强模型/独立上下文；探索性重写实验放独立 worktree
- [来源: repo-refactor/references/code-refactor.md] 完成清单：公共面裁判全绿、无未解释 diff；no-op 检测通过；所有测试变更经对抗评审；死码删除附考古证据；Contract 完成或追踪；≥L3 行为增量日志完整；L4 新验收标准逐条通过

### B.4 repo-refactor/references/docs-refactor.md

- [来源: repo-refactor/references/docs-refactor.md] 文档重构无业界现成实践（现有 skill 只覆盖代码），其安全网为原创设计
- [来源: repo-refactor/references/docs-refactor.md] 原则 1 一事一主（one fact, one canonical owner）：每个持久事实只在一个地方权威记录，其余链接或一句话摘要；重复事实是漂移之源——改一处漏三处
- [来源: repo-refactor/references/docs-refactor.md] 原则 2 每页一类型（Diátaxis 四分）：tutorial（跟做）/how-to（解决任务）/reference（查事实）/explanation（理解为什么）；混型页→拆；判定方法：问读者拿这页做什么
- [来源: repo-refactor/references/docs-refactor.md] 原则 3 文档与代码同一 PR：契约/命令/架构变更伴随更新文档，分离是漂移的开始
- [来源: repo-refactor/references/docs-refactor.md] 原则 4 死文档：删除或封存——Google 关停某 wiki 时 90% 文档数月无人访问；无主文档是负债不是资产；删除遵循 repo-steward 的安全分类（迁移/法律/发布元数据受保护）
- [来源: repo-refactor/references/docs-refactor.md] 原则 5 宁少勿多：默认目标是"最小一致文档集"而非"更完整的文档体系"；新建文档前先问哪个既有正典文档应该拥有这个事实
- [来源: repo-refactor/references/docs-refactor.md] 文档重构七步工作流：清单（路径/类型/承载事实/属主/新鲜度）→ 类型审计（混型与无型标记，决定拆/并/删/重写）→ 重复事实映射（选定唯一正典属主）→ 设计新结构 + 新旧路径映射表 → 迁移（git mv 保历史；内容重组与位置移动分开提交；每次移动后跑链接检查）→ 漂移修复（逐条执行命令验证、编译/运行示例、对齐版本号/路径/参数名）→ 验收
- [来源: repo-refactor/references/docs-refactor.md] 文档验收安全网：无死链（含抽查外链）；命令抽查通过；无孤儿页（没有任何页面链入）；无重复正典事实；每页有类型和属主；README 与 docs 索引 ≤2 跳到达核心内容
- [来源: repo-refactor/references/docs-refactor.md] 文档域级别含义：L1 修错字/统一术语/规范格式（零内容变化）；L2 重组目录/合并重复/删死文档（事实集不变，每个事实仍可找到且更易找到）；L3 文档架构重设计 + 与代码变更耦合的契约文档更新（产出新旧映射表，被删/并文档说明"内容去了哪"）；L4 推倒重来（先定义新受众与旅程：谁、来做什么、期望多快找到；按旅程验收；旧文档归档而非蒸发）
- [来源: repo-refactor/references/docs-refactor.md] 文档反模式：生成没人要的一次性 SUMMARY/ANALYSIS/报告；搭空目录树和索引页"显得成体系"；仅为统一语气/格式重写整页（文档版 no-op 重构）；把教程写成参考手册（类型错配是最常见质量问题）
- [来源: repo-refactor/references/docs-refactor.md] AI 生成文档噪声典型：复述代码的段落、"In this document, we will..." 开场 boilerplate、无信息量小节标题——重写时优先删除

### B.5 repo-refactor/references/product-logic.md

- [来源: repo-refactor/references/product-logic.md] 产品操作逻辑重构的特殊性：其"行为"就是产品本身，安全网不是测试而是旅程（journeys）；此域同样无业界 agent 实践，旅程式安全网为原创设计
- [来源: repo-refactor/references/product-logic.md] 旅程三件套之 1 旅程清单：枚举用户完成任务的所有路径（注册/初始化、核心工作流、错误恢复、升级/迁移）；来源：代码入口（路由表/命令注册）、既有 how-to 文档、issue/工单里的真实抱怨；每条旅程记录：入口 → 步骤序列 → 出口（成功/失败形态）
- [来源: repo-refactor/references/product-logic.md] 旅程三件套之 2 当前行为快照（产品逻辑版的特征测试）：实地录下当前行为而非凭记忆描述——Web UI 用 browser-use 走一遍（截图+步骤记录）；CLI 用脚本录真实会话（命令序列+输出）；API 取代表性请求/响应样本
- [来源: repo-refactor/references/product-logic.md] 快照两用途：(a) ≤L3 的回归基线；(b) 任何级别下都是"现状证据"——新设计必须逐条交代每条旧旅程的去向
- [来源: repo-refactor/references/product-logic.md] 旅程三件套之 3 行为变更表（≥L3 强制）：每行 `旧行为（附快照证据）→ 新行为 | 原因 | 爆炸半径（哪些用户/哪条旅程）`；L4 还记录删除项及理由
- [来源: repo-refactor/references/product-logic.md] L4 "产品质量优先"操作化为可验证新验收标准，每条核心旅程至少回答：完成性（N 步内完成？给出目标 N）；可恢复性（中途失败从哪恢复？丢不丢数据？）；可理解性（错误信息是否说"什么坏了+怎么办"？）；可发现性（新用户不看文档能否猜到下一步？用 browser-use 冒烟验证）；一致性（相似操作在不同入口行为是否相同？）
- [来源: repo-refactor/references/product-logic.md] 新验收标准必须在写代码之前定义（设计阶段），在最后阶段核验
- [来源: repo-refactor/references/product-logic.md] 按项目阶段的迁移策略：开发期（无外部消费者）→ 直接切换+changelog+一行迁移说明，整体弃兼容是推荐动作，唯一要求是不静默破坏；有用户 → 破坏性变更是过程不是事件——新旧映射表+迁移指南（可自动化时写 codemod）、高风险旅程用双入口过渡或灰度（feature flag 且登记过期时间）、先发弃用警告（PEP 387 惯例：移除前保留 ≥2 个次版本）
- [来源: repo-refactor/references/product-logic.md] 数据操作：任何破坏用户数据的操作（改存储格式、删字段）无条件用户门禁 + 回滚路径（备份/导出）
- [来源: repo-refactor/references/product-logic.md] 交互流变更必须同 PR 更新：CLI 帮助文本与补全、UI 文案、错误信息、相关 how-to 文档、示例代码；"交互改了文档没改"是最常见漂移
- [来源: repo-refactor/references/product-logic.md] 行为增量日志是迁移指南的原材料：表写完，指南基本只剩排版
- [来源: repo-refactor/references/product-logic.md] 配置格式变更是持久化契约：走 code-refactor.md 的 Expand-Contract
- [来源: repo-refactor/references/product-logic.md] 验收清单：全旅程覆盖（每条旧旅程在新世界有明确处置：保留/简化/合并/删除，删除有理由）；≤L3 快照复录比对（每个差异出现在行为增量日志）；L4 新验收标准逐条通过附证据；迁移指南/changelog 与日志一致；错误路径不是事后补——每条核心旅程至少验证一个失败场景

### B.6 repo-refactor/references/workflow-large.md

- [来源: repo-refactor/references/workflow-large.md] 大重构每阶段结尾 = 证据工件 + 门禁；轻量场景跑完汇报即可，重大事项（设计批准、契约切换、删旧路径）须用户点头才开下一阶段——"人类批准 = 开始下一阶段"
- [来源: repo-refactor/references/workflow-large.md] 计划必须持久化到磁盘（如 docs/refactor-plan.md 或仓库惯例位置）：长任务中上下文会退化，每轮重读计划文件而非相信会话记忆；每轮从磁盘重建进度（在队列文件里勾掉已完成项）；任务天然可中断可续跑
- [来源: repo-refactor/references/workflow-large.md] 门禁范围规则："重大工作" = 对有外部消费者仓库的任何 L3+、任何 L4、或预期爆炸半径 >10 文件；用户已显式授权 L4 时 Phase 0 任务卡与 Phase 3 设计评审仍需门禁（可合并为一次批准）；拿不准时呈交工件并继续非破坏性工作，不要闲着
- [来源: repo-refactor/references/workflow-large.md] 工件纪律：只有计划、队列、规则书（以及计划 fan-out 时）是磁盘文件；其余工件（任务卡、侦查报告、终报）在对话中汇报——控制仓库内一次性文件
- [来源: repo-refactor/references/workflow-large.md] Phase 0 定级与边界：确定激进级别（可分块授予）、变更边界、项目阶段（外部消费者？持久化 schema？API 消费者？）、约束（时间/兼容/性能）；可行性检查——"不重构/只最小修/分期推迟"是合法结论；仓库根若有遗留计划文档先读（可能是上次中断的任务）；工件=任务卡（级别×边界×验收标准×回滚策略），门禁=用户确认
- [来源: repo-refactor/references/workflow-large.md] Phase 1 侦查：用确定性脚本（grep/AST 工具，不靠记忆）生成文件粒度与包/模块粒度依赖图——曾因漏掉包级循环导致 16000 个编译错误；爆炸半径（依赖与被依赖、受影响文件数、风险层级）；测试资产盘点（哪些测公共面、哪些耦合实现、缺口在哪）；涉文档做类型审计、涉产品逻辑做旅程清单
- [来源: repo-refactor/references/workflow-large.md] Phase 2 裁判与安全网：测试分诊；无测试区先建特征测试或奇偶 harness（约 7 个代表性场景）；金丝雀验证（原码绿、蓄意破坏红）；记录基线状态（含已在失败的检查，避免事后归因错误）
- [来源: repo-refactor/references/workflow-large.md] Phase 3 设计与规则：写规则书（迁移/重构规则集，存仓库如 PORTING.md）——两个执行单元可能回答不同的每个决定都写进去、只决定一次；每条规则一句话 + 一个正例一个反例；百万行生产移植的全部"提示词"就是一份 576 行规则书
- [来源: repo-refactor/references/workflow-large.md] Phase 3 目标设计：新结构/契约/旅程草图 + 显式验收标准（L4 尤其必须先定新标准）；门禁=用户批准设计（重大工作强制）
- [来源: repo-refactor/references/workflow-large.md] Phase 3 试点：在 2-3 个代表性文件上跑全流程，唯一产出是规则修订与设计修正，试点代码丢弃；机械迁移可试"双翻译对比"（一次按规则翻译、一次不知情的自由翻译，diff 暴露规则缺口）——曾在一个案例里于 3 个文件上抓到会污染 1448 个文件的缺陷
- [来源: repo-refactor/references/workflow-large.md] Phase 4 迁移计划：按 code-refactor.md 选择表选模式；队列落盘——待办单元（文件/调用者/旅程）列进队列文件，"完成"= 变更后的文件存在于磁盘；每轮从磁盘重建剩余队列，不依赖会话状态；规划提交/PR 序列（批量、顺序、依赖）与回滚点（阶段级 tag/分支）；门禁=用户批准计划
- [来源: repo-refactor/references/workflow-large.md] Phase 5 执行循环：一次一单元→编辑→跑廉价裁判（秒级：lint/类型检查/相关测试）→绿提交/红回滚拆小
- [来源: repo-refactor/references/workflow-large.md] 反抽风护栏：一个单元最多尝试 3 次后视为规则问题；禁止占位实现（过不了裁判的桩是红单元不是完成）；新建任何助手前先 grep 是否已有；不确定的边缘情况打 `TODO(refactor):` 标记而非猜测
- [来源: repo-refactor/references/workflow-large.md] Phase 5 规则修订纪律：每条规则修订附一行理由；门禁运行中，规则修订在下个门禁批量报告而非静默应用
- [来源: repo-refactor/references/workflow-large.md] Phase 6 收缩与同步：删除旧路径/兼容 shim/双写，完成须验证零引用零调用；给 feature flag 和兼容层登记过期机制（属主+移除条件/日期），不许永生开关；文档同步（契约/命令/架构变更与代码同 PR）；发布行为增量日志与迁移指南；门禁=零引用验证通过
- [来源: repo-refactor/references/workflow-large.md] Phase 7 验证与交付：对抗性评审——独立视角（新会话/独立子 agent/另一模型）复审关键 diff 与所有测试变更，分歧逐条解决；全量裁判+基线比对；no-op 检测；紧凑报告（变更/验证/剩余风险/显式 TODO）；提议把计划/队列/规则书归档（如 ADR）或删除——它们是工作状态不是交付物
- [来源: repo-refactor/references/workflow-large.md] 中断恢复：队列文件+计划文档=全部状态；恢复=重读两者+与 git log 对账；不存在"恢复会话"这回事；发现上次遗留的计划文档先对账再决定继续或归档

### B.7 repo-steward/SKILL.md

- [来源: repo-steward/SKILL.md] 总目标：不是"更多结构"，而是保行为、意图、可维护性的最小一致仓库；减少仓库熵且不用一种混乱换另一种混乱
- [来源: repo-steward/SKILL.md] 核心原则：删/合并/复用优先于新增（文件、抽象、依赖、注释、报告、文档）
- [来源: repo-steward/SKILL.md] 核心原则：指标与阈值只是调查信号，绝不是自动裁决
- [来源: repo-steward/SKILL.md] 核心原则：重构前先保行为——用测试、可复现命令或显式观察到的行为建立基线
- [来源: repo-steward/SKILL.md] 核心原则：变更保持在任务边界内，不机会主义地重写无关代码/文档
- [来源: repo-steward/SKILL.md] 核心原则：既有正典文档能拥有该事实时不创建新文档；一个持久事实一个正典属主，其他文档链接或简短摘要
- [来源: repo-steward/SKILL.md] 核心原则：解释为什么而非是什么；避免复述代码的注释与散文
- [来源: repo-steward/SKILL.md] 核心原则：无压力不抽象——需有重复行为、多实现、稳定边界或已证实的复杂度才建抽象
- [来源: repo-steward/SKILL.md] 核心原则：不仅为满足行数阈值拆内聚文件
- [来源: repo-steward/SKILL.md] 核心原则：不确定文件、来源不明的生成物、迁移、fixture、锁文件、用户数据，未确认角色前绝不删除
- [来源: repo-steward/SKILL.md] 两档巡查深度：Quick（实质性/跨切编辑后交付前，或专项卫生检查：相关检查+变更代码结构+每个新文件+受影响正典文档）；Full（里程碑收尾、广域清理、PR 批次收尾、显式审计：另加契约、依赖方向、配置、文档一致性；广域/高风险尽量用独立评审）
- [来源: repo-steward/SKILL.md] 标准序列第 1 步：先读本地规则——AGENTS.md、CONTRIBUTING.md、manifest、CI、formatter/linter 配置、相关文档
- [来源: repo-steward/SKILL.md] 标准序列第 3 步：编辑前先侦查——搜索既有工具函数、正典文档、相似模块、既有命名；先从仓库证据解决实质性歧义；只有未决备选会实质改变行为/兼容/范围时才问，否则用既有低影响默认值；有更简单方案满足同样要求时推荐它
- [来源: repo-steward/SKILL.md] 标准序列第 4 步：用 change-gate 的 acceptance-evidence 定义可观测成功；非平凡多步工作把关键实现步骤与对应验证配对进工作计划；从仓库规则/manifest/CI 发现权威测试/类型检查/构建命令；跑最窄的有用基线检查并记录既有失败或不可用项
- [来源: repo-steward/SKILL.md] 标准序列第 5 步：做最小一致变更，遵循周围风格与惯例；不为假想需求加选项、扩展点、配置、回退路径；保留由真实输入、信任边界或受支持契约正当化的错误处理
- [来源: repo-steward/SKILL.md] 标准序列第 6 步：查熵——这次变更是否引入了不必要的文件、概念、依赖、注释、文档或重复事实
- [来源: repo-steward/SKILL.md] 标准序列第 8 步：检查 diff——移除意外搅动、临时工件、调试输出、无关格式化、过时文档、被本次变更废弃的代码
- [来源: repo-steward/SKILL.md] 标准序列第 9 步：紧凑报告——改了什么、验证了什么、剩余风险；除非被要求不生成第二份实施报告
- [来源: repo-steward/SKILL.md] 脚本定位：作为证据收集器使用，不让它们替代工程判断；全部仅用 Python 标准库
- [来源: repo-steward/SKILL.md] 添加前决策问句：文件——有独立职责或生命周期吗；抽象——有真实重复行为/多实现/付得起间接成本 的稳定边界吗；文档——哪个既有正典文档应拥有此事实；依赖——标准库或既有依赖够用吗；注释——解释意图/不变量/非显然约束/惊人权衡吗；报告——用户要持久报告还是紧凑回复就够；答案弱就不加
- [来源: repo-steward/SKILL.md] 仓库产出政策：不创建 SUMMARY.md、ANALYSIS.md、IMPLEMENTATION_NOTES.md、FIX_REPORT.md、REFACTOR_REPORT.md 等一次性工件（除非用户显式要求或仓库惯例要求）
- [来源: repo-steward/SKILL.md] 仓库产出政策：不留临时脚本、拷贝的日志、生成截图、调试转储、基准输出、编辑器备份、临时导出物；任务只需小修补时不为规范化风格整文件重写
- [来源: repo-steward/SKILL.md] 清理安全三级分类：Safe（编辑器备份、已知缓存、可复现生成物、已确认正典属主的重复临时报告）可自动删；Review（旧脚本、归档计划、fixture、快照、生成代码、vendored 内容、本地配置）与 Protected（迁移、锁文件、法律文件、发布元数据、用户数据、需轮换的密钥、未知再生路径的工件）须用户授权
- [来源: repo-steward/SKILL.md] 完成标准：一次成功的治理让仓库更易导航、维护更便宜，且没有用更多文件或更多散文掩盖复杂度

### B.8 repo-steward/references/repository-hygiene.md

- [来源: repo-steward/references/repository-hygiene.md] 物理侦查：分别列出已跟踪文件与未忽略的未跟踪文件（git ls-files --others --exclude-standard）；staging 前也检查新文件与 diff；被忽略的生成文件与已提交的生成文件是两回事
- [来源: repo-steward/references/repository-hygiene.md] 检查生成物是否有文档化的再生路径；把源控的 fixture/快照与意外产物分开
- [来源: repo-steward/references/repository-hygiene.md] git 仓库中扫描脚本只枚举已跟踪文件；干净的扫描结果≠完整覆盖，未跟踪文件须单独检查；repo_scan.py 只提供名称/路径/尺寸信号，不是来源证明或可安全删除的证明
- [来源: repo-steward/references/repository-hygiene.md] 值得检查的信号：*.log/*.tmp/*.bak/*.orig/交换文件/编辑器自动保存；.env/凭据式命名/私钥/token 转储；node_modules/.venv/target/dist/build/覆盖率输出/缓存；大体积二进制；根目录无关脚本；源缺失的生成资产；所有权重叠的重复配置
- [来源: repo-steward/references/repository-hygiene.md] 不要过度清理：不因体积大就删锁文件、迁移、fixture、快照、vendored 资产、生成源码、模型文件、notebook、二进制——先确认是否是有意的仓库输入
- [来源: repo-steward/references/repository-hygiene.md] 不对布局已一致的仓库强推通用 src/ 布局
- [来源: repo-steward/references/repository-hygiene.md] 修复顺序：删明确意外的垃圾 → 只为真生成/本地产物收紧 ignore 规则 → 只在新位置能澄清所有权时移动错位文件 → 找到正典属主后合并重复 → 只在不显然且持久时文档化再生方式 → 重跑扫描并检查 diff

### B.9 repo-steward/references/code-structure.md

- [来源: repo-steward/references/code-structure.md] 从职责出发而非行数：一个 900 行但语法内聚的解析器可能比五个靠间接层连接的 180 行文件更健康；行数只是检查的由头，不是拆分的理由
- [来源: repo-steward/references/code-structure.md] 结构调查清单：单模块多职责；函数混杂编排/I-O/校验/策略/格式化；可分叉的重复逻辑；依赖环或跨意图边界的 import；utils/helpers/common 模块堆积无关行为；多概念阶段导致的长函数；隐式编码状态机的深层条件；单实现无边界压力的抽象；只为改名的包装函数；对同一数据的重复校验/推导（含 schema 校验器已保证的手写检查）；掩盖破损不变量的静默内部回退/吞错（在信任边界校验，内部保证用类型或断言表达）；仅为避免更新旧调用者的并行替代实现/兼容参数（真实受支持契约才保留兼容）
- [来源: repo-steward/references/code-structure.md] 状态/契约/依赖方向：识别状态、事件、配置、派生数据的权威属主；派生与失效机制清晰的缓存/投影是合法的；多个可写权威才是问题；改冻结契约前查仓库声明的 schema/API/协议兼容规则与审批/版本/迁移流程——不把清理静默变成破坏性变更；新目录要被架构测试/导入规则覆盖，无自动化时抽查代表性别跨边界 import
- [来源: repo-steward/references/code-structure.md] 移除能力时，在受支持兼容政策内一并移除废弃配置键与消费者；新配置键必须有读取者且有文档化默认值或显式必填校验
- [来源: repo-steward/references/code-structure.md] 基线优先：无基线的重构使"清理"与意外行为变化无法区分
- [来源: repo-steward/references/code-structure.md] 首选重构顺序：1 删有据死代码与重复；2 提取具名局部函数（澄清阶段且不造跨文件间接）；3 职责/生命周期可独立理解时才分模块；4 真实边界需要时才引接口/trait/protocol；5 两个以上调用者证明稳定共享后才移动共享代码；6 每个一致步骤后重跑聚焦测试
- [来源: repo-steward/references/code-structure.md] 结构前提使能行为变更时：把移动/重构与行为变更拆成可评审的步骤，适当时分开提交；拆模块时让测试对齐新职责边界，内聚工作流保留共享集成覆盖
- [来源: repo-steward/references/code-structure.md] 反过度工程门：同时满足——仅一个实现、包装不增加不变量或边界、调用点更难追踪、仅靠假想未来需求辩护——则拒绝该抽象
- [来源: repo-steward/references/code-structure.md] 拒绝增加导航成本却不降低概念负载的机械拆分
- [来源: repo-steward/references/code-structure.md] 尺寸信号（调查信号非失败，仓库惯例覆盖之）：源文件约 600+ 非空行→查职责；约 1000+ 非空行→高优先调查；函数约 80+ 行→查阶段与嵌套

### B.10 repo-steward/references/docs-maintenance.md

- [来源: repo-steward/references/docs-maintenance.md] 原则：一个持久事实一个正典属主；同一安装命令/架构规则/配置真相不复制进多份长寿命文档，选一个属主，其余链接或简短摘要
- [来源: repo-steward/references/docs-maintenance.md] 默认文档角色表：README.md=项目目的/快速开始/主入口（非完整架构）；AGENTS.md=给 agent/贡献者的指令、命令、约束、仓库惯例（非 README 副本）；docs/architecture.md=当前系统结构/边界/数据流/不变量（非历史讨论）；docs/decisions/*.md=重要决策的为什么（追加历史而非改写）；docs/development.md=持久本地开发/测试/调试/发布流程；CHANGELOG/发布说明=时间序用户可见变更史；docs/plans/=临时计划（完成后归档或删除，不许冒充当前架构）
- [来源: repo-steward/references/docs-maintenance.md] 仓库已有清晰角色分工时不强推该布局，保留一致的本地惯例
- [来源: repo-steward/references/docs-maintenance.md] 文档盘点：识别持久文档/临时计划/生成文档/重复指南/归属不清文件；对每个持久文档确定：目标读者、正典拥有的事实、能使这些事实失效的源文件/配置、是否被其他文档重复
- [来源: repo-steward/references/docs-maintenance.md] 变更面确定：代码/配置变更后列出可能变化的事实——命令与 flag、包名与路径、环境变量、公共 API、配置 schema、模块边界、持久化行为、部署/发布流程、用户可见行为；只读拥有这些事实的文档，不反射式打开每个文档
- [来源: repo-steward/references/docs-maintenance.md] 用可执行证据对照文档而非散文：manifest/脚本对命令；router/CLI 声明对接口；schema/迁移对持久化；CI workflow 对验证/发布；代码边界对架构声明
- [来源: repo-steward/references/docs-maintenance.md] Git 新近度是漂移信号不是证明：源文件比文档新意味着"检查此文档"，不是"重写此文档"
- [来源: repo-steward/references/docs-maintenance.md] 最小补丁：修正过时事实而不机会主义重写；保留未受影响的措辞与结构；两文档重复同一事实时：选正典属主→完整细节留在那→别处换短摘要或链接→验证链接与锚点
- [来源: repo-steward/references/docs-maintenance.md] 临时文档退役：无持久价值→删；历史推理有价值→归档；只把持久结论提升进正典文档；绝不让已完成的计划充当第二份当前真相
- [来源: repo-steward/references/docs-maintenance.md] 验证清单：链接与引用路径（含源码注释中的文档/章节引用）；可廉价运行的命令；改名符号与配置键；受 API 变更影响的示例；持久文档间重复事实；过时的"planned/TODO/future/not implemented"表述
- [来源: repo-steward/references/docs-maintenance.md] 进度页与已完成清单项要对照测试或观察到的行为核验，而非凭记忆；有意义的设计偏差记录进仓库既有决策机制；系统变了才更新当前设计文档，保留历史决策；新持久文档加入既有索引，不为这次巡查新建索引
- [来源: repo-steward/references/docs-maintenance.md] 脚本边界：docs_inventory.py 只查本地链接文件存在性，不查章节锚点与源码注释引用；docs_drift.py 只标记有未提交变更或更新 git 提交的已映射已跟踪源文件，不覆盖未跟踪源也不证明事实正确性
- [来源: repo-steward/references/docs-maintenance.md] 只有反复漂移的仓库才建 .repo-steward.toml 做 docs→sources 映射；小仓库不加机器辅助漂移检查
- [来源: repo-steward/references/docs-maintenance.md] 文档反模式：因 agent 产出了就提交的 SUMMARY/ANALYSIS/任务报告；README 重复详细开发文档；不标注"提案"却描述意图而非现状的架构文档；各自漂移的重复命令片段；混合入职/设计史/API 参考/运维的巨型"大而全"文档；不验证内容只更新时间戳

### B.11 repo-steward/references/output-hygiene.md

- [来源: repo-steward/references/output-hygiene.md] 值得保留的注释：非显然不变量；奇怪变通为何存在；兼容约束；性能/安全权衡；代码本身揭示不了的协议/算法意图
- [来源: repo-steward/references/output-hygiene.md] 应删注释：复述下一行、重复名字、解释普通语法的叙述式注释
- [来源: repo-steward/references/output-hygiene.md] 文档散文：偏好具体陈述、命令、文件名、行为；避免仪式性小节、营销语言、重复总结、无仓库特定价值的通用"最佳实践"散文；短解释不扩写成分类学，除非该分类帮助真实决策
- [来源: repo-steward/references/output-hygiene.md] agent 产出默认不持久化报告：发现放对话里，除非用户要持久工件或仓库惯例要求；创建 Markdown 前先问是否已有文档拥有该内容，有则更新它
- [来源: repo-steward/references/output-hygiene.md] 最终回复默认结构：1 改了什么；2 做了什么验证；3 未解决风险或有意推迟的工作；避免复述每条命令、重复任务本身、给简单变更写长复盘

### B.12 repo-steward/references/change-gate.md

- [来源: repo-steward/references/change-gate.md] diff 焦点五问：每个变更 hunk 服务于请求任务或必要前提吗；格式化/生成输出碰到无关文件了吗；清理静默改变行为了吗；变更引入临时报告/日志/截图/转储/本地配置了吗；改名留下失效引用了吗
- [来源: repo-steward/references/change-gate.md] 本次变更废弃的 import/变量/助手/引用，验证无消费者后一并移除；约定范围外的既有死代码只报告不删（显式清理任务可含，但须守清理安全规则）
- [来源: repo-steward/references/change-gate.md] 仓库含无关工作时用显式 staging 而非无差别 git add .
- [来源: repo-steward/references/change-gate.md] 验收证据：实现前把请求结果转成可观测检查——bug 修复：先用聚焦测试/命令复现失败再验修复；校验变更：无效输入被拒+有效输入仍通过；重构：建立前后行为等价，而非仅文件更小或无关套件绿；文档变更：对照权威源核验受影响事实+检查变更链接，代码测试通过不能证明散文正确
- [来源: repo-steward/references/change-gate.md] 既有检查能证明结果就用既有的；不能就加聚焦覆盖；检查失败后调查、做范围内修正、重跑；不为通过而弱化判据；验证不可用或需用户决策时，报告具体限制而非宣称完成
- [来源: repo-steward/references/change-gate.md] 验证顺序：1 只对受影响文件做 format/check（如支持）；2 聚焦单测/回归测试；3 相关组件的 typecheck/lint/build；4 范围需要时更宽项目检查；5 工具改完文件后检查最终 diff
- [来源: repo-steward/references/change-gate.md] 没跑过的检查不得宣称通过；基线检查失败时先区分既有失败与回归再继续依赖它的清理；范围内回归修掉并重跑，无关失败如实报告不宣称干净门禁
- [来源: repo-steward/references/change-gate.md] 广域/高风险的完整巡查尽量请只读独立评审者；供给：约定范围、基线提交/tag、当前 diff、新文件、相关仓库规则、验证结果；评审受影响文件及其调用者，而非仅变更行
- [来源: repo-steward/references/change-gate.md] 评审发现格式：`file:line [blocking|important|suggestion] problem; suggested repair`；不为填满分类编造发现；范围内 blocking/important 确认后在关门前解决并重跑受影响验证与修复评审；修复需破坏性动作/契约变更/范围扩张时报 blocked 而非擅自继续；非阻塞建议放既有 issue/backlog 或最终回复，不开新报告文件
- [来源: repo-steward/references/change-gate.md] 独立评审明显有益但不可得时：做显式第二遍自查，且不得把自查描述为独立评审
- [来源: repo-steward/references/change-gate.md] 文档影响：diff 改变任何持久事实（命令/配置/API/路径/架构/部署/schema/用户可见行为）时才查文档；不因源文件变了就更新文档
- [来源: repo-steward/references/change-gate.md] 高置信度 blocking 发现：diff 中出现密钥/私钥材料；合并冲突标记；意外调试转储或本地环境文件；变更引入的破损测试；无源变更或解释的生成物搅动
- [来源: repo-steward/references/change-gate.md] 大 diff、大文件、TODO、文档新近度是评审信号不是自动 blocker；新 TODO/FIXME/HACK 对照变更基线按上下文评审，数量既不证明债也不证明该删有用的标记；尊重仓库既有债务基线政策，不引入第二套基线系统

### B.13 repo-steward/references/legacy-cleanup.md

- [来源: repo-steward/references/legacy-cleanup.md] 存量乱仓库不搞一遍式 mega-refactor
- [来源: repo-steward/references/legacy-cleanup.md] Phase 1 调查取证：仓库垃圾与生成物；大多职责模块；重复逻辑；过时重复文档；仅当依赖工作在范围内才看过时依赖；失败或缺失的验证路径；反复一起改的热点；产出短优先级计划，避免生成永久审计文档
- [来源: repo-steward/references/legacy-cleanup.md] Phase 2 稳定：结构清理前识别关键行为；无测试会使清理不安全处补聚焦回归覆盖；只文档化验证变更所需的非显然执行步骤
- [来源: repo-steward/references/legacy-cleanup.md] Phase 3 按一致切片清理，优先序：明显意外产物 → 有据死代码 → 重复事实/文档 → 带测试的局部结构重构 → 模块边界变更 → 仍正当才做更大架构工作；每片离开时仓库保持有效可评审
- [来源: repo-steward/references/legacy-cleanup.md] Phase 4 防复发：只给可重复的高信号检查加自动化（密钥扫描、格式/lint/测试门禁、生成文件检查、选定文档漂移映射）；不把每个清理观察都变成新 CI 规则

### B.14 repo-steward/references/configuration.md

- [来源: repo-steward/references/configuration.md] 零配置即可工作；仅当仓库特定映射或阈值改善信号时才加 .repo-steward.toml；从 assets/repo-steward.toml 模板起步
- [来源: repo-steward/references/configuration.md] 阈值只是警告级别；metrics 输出的 high 严重度=高优先调查，不是门禁失败；改阈值前先按仓库文件尺寸分布与源/测试/文档职责校准；仓库特定设置保留在此既有格式中
- [来源: repo-steward/references/configuration.md] ignore 规则须给可追溯理由（TOML 注释或仓库既有记录）；区分有意排除的生成/vendored 内容与临时债务；临时豁免要有属主或追踪 issue + 复审条件；不用新增 ignore 规则掩盖新引入的问题
- [来源: repo-steward/references/configuration.md] 文档归属映射：source glob 让文档在匹配的已跟踪源文件有未提交变更或 git 历史更新时成为评审候选；不把每个源文件映射到每个文档——宽映射让漂移检查噪声化失效

### B.15 repo-steward README.md 与 scripts/

- [来源: repo-steward/README.md] 仓库熵的四种形态：文件系统熵（生成垃圾/缓存/密钥/意外二进制/临时报告）；代码熵（上帝模块/职责不清/重复/错误抽象）；文档熵（重复事实/过时命令/架构漂移/永生计划）；agent 熵（冗长注释/多余 Markdown 工件/无关 diff/过度工程）
- [来源: repo-steward/README.md] 治理总则：删、合并、复用优先于增
- [来源: repo-steward/README.md] 捆绑 Python 脚本仅标准库，只收集证据不做破坏性决策；从 skill 目录运行并传目标仓库路径
- [来源: repo-steward/README.md] git 扫描只覆盖已跟踪文件，未跟踪文件单独检查；diff_guard.py 默认查未暂存、--staged 查已暂存；漂移检查用配置映射+git 历史给评审候选建议，不证明漂移
- [来源: repo-steward/README.md] 设计立场：偏好一致职责与正典所有权而非机械拆分或额外工件；与仓库既有 AGENTS.md、CI、linter、formatter、测试套件协作而非取代
- [来源: repo-steward/scripts/repo_scan.py] 脚本用 RISKY_NAMES（.env、id_rsa、credentials.json、secrets.json、token.txt 等）、RISKY_SUFFIXES（.pem/.key/.p12/.pfx）、JUNK_SUFFIXES（.log/.tmp/.bak/.orig/.swp/.swo）、JUNK_PARTS（node_modules/.venv/__pycache__ 等）四张硬编码表做确定性扫描——把人工判断规则固化为枚举表
- [来源: repo-steward/scripts/] 其余脚本分工：file_metrics.py=非空行计数与 warn/high 分级；docs_inventory.py=文档与本地链接存在性清单；docs_drift.py=按配置映射报未提交/更新提交的漂移候选；diff_guard.py=staged/unstaged diff 检查；common.py=git 调用/配置加载/忽略判断公共层；全部输出 JSON 证据
- [来源: repo-steward/tests/test_repo_steward.py] 发布级 skill 为脚本配单元测试（python -m unittest discover -s tests）

### B.16 discussion.txt（逐行）

- [来源: discussion.txt:1] AI 写代码快，但往往逻辑啰嗦、嵌套极深
- [来源: discussion.txt:1] Claude Code 官方插件 code-simplifier 专治 AI 代码的"防御过头"（过度防御式编程）和"波动拳"（发散膨胀的写法），让代码回归人类审美
- [来源: discussion.txt:2] 手动替代方案：让 AI 以《Clean Code》《Clean Architecture》《The Pragmatic Programmer》三本书的原则重新 review 代码
- [来源: discussion.txt:3] 给没有代码的 .dm 规则文件定义为"项目协作文件"；实战感受：让 AI 治理这类规则文件比让它写代码效果差太多，容易被气到
- [来源: discussion.txt:3] 很难保证 AI 按规则办事；想让它守规矩就要塞一堆规矩，越堆越多，也管不住它
- [来源: discussion.txt:4] 相同的 AI、不同的结果；AI 无法替代人类增长认知和能力
- [来源: discussion.txt:5] 长上下文容易忘东西；256K 才是舒适区间
- [来源: discussion.txt:5] 最好找一两个 agent 先把方案和细节全部敲定，再"按图索骥"照图施工
- [来源: discussion.txt:5] 一个 agent 从头跟到尾不存在；频繁 compact 也不行——compact 太多同样导致要求更慢、更烧钱
- [来源: discussion.txt:6] 不是上下文容量问题：每个任务控制在会话上下文窗口的 80% 以内
- [来源: discussion.txt:6] 主要问题是 AI 容易逮住一个文档就往里写东西；严格控制 AI 又可能导致规则文件挤占上下文
- [来源: discussion.txt:6] AI 从文本中理解逻辑链路的能力远低于从代码实现中获取信息
- [来源: discussion.txt:7] preview 版模型行为可能不受收敛、不受控；最好用 Claude 和 GPT（行为克制），Kimi 也行但太贵；DS、GLM 等对规则的敬畏意识差一点
- [来源: discussion.txt:7] 用国产模型时在铁律里加明显信号：称呼、emoji、特殊标志；称呼变了或不发 emoji 了，就再喂一轮（规则）
- [来源: discussion.txt:7] 被动约束用钩子：每 5-8 轮抽背——七条铁律随机抽一条问记不记得，不记得就重读
- [来源: discussion.txt:8] 出现奇怪问题直接问 AI，并附上"我是想解决问题"；它一般能自查出直接原因；不说这句它会不停道歉，之后接着再犯
- [来源: discussion.txt:9] 用 CODEX（GPT-6 出来后主用 6）；CODEX 工作很难追踪行为、阅读量过大；加识别符号方便观察 AI 行为是个思路
- [来源: discussion.txt:10] 项目 AGENTS.md 保持简洁，协作类文件入口用索引呈现
- [来源: discussion.txt:10] 失控点：AI 不会在 AGENTS.md 里乱写，但不能分辨项目文件层级，经常把信息写进高层文件；层级越深越乱，增加上下文负担且难保证来源唯一
- [来源: discussion.txt:10] 现在用 index 文件定义项目协作文件层级，再用写入规则约束，跑两天效果还行；这相当于一种编程，但 AI 读文字规则容易错漏和偏差
- [来源: discussion.txt:11] 钩子（hook）是拦截点/中断点：发送信息后、大模型准备发送信息前，满足条件一定触发的卡口（Codex 应该也有）
- [来源: discussion.txt:11] 钩子属应用层机制，不管上下文怎么稀释，满足条件就执行；可用钩子实现轮巡，或设触发词强制调用 skills
- [来源: discussion.txt:11] 强制性排序：钩子是目前大模型工具里强制性最高的；并驾齐驱的是挂代理；再次是容易被上下文稀释的 AGENTS.md；其他 skills 或 MCP 不具备太多强制性
- [来源: discussion.txt:12] agent 通病：改东西时总习惯插入来源或背景；有时为对齐格式丢掉原生美德
- [来源: discussion.txt:12] 把 AI 丢进整洁度 60 分的文件里，它尽管有 80 分的书写能力，也只会发挥 60 分——需要定期清理
- [来源: discussion.txt:13] 可把项目传 GitHub，让网页端 GPT-6 Pro 读后给计划书；提示词 1"大扫除"：只做清理不加功能，找死代码、重复逻辑，先列清单
- [来源: discussion.txt:13] 提示词 2"严格限制范围"：只读指定 xxx 模块，别扫整个仓库单文件；超过 800 行先出拆分方案，不动代码
- [来源: discussion.txt:13] 提示词 3"把规则当代码管"：读仓库 AGENTS.md/CLAUDE.md，找出代码里已不存在的旧规矩删掉；留下的每条补一句为什么；生成文档确认后让本地 agent 执行
- [来源: discussion.txt:14] 只有先把功能整理成严格文档，再根据文档完整重构，才能降低问题
- [来源: discussion.txt:15] AI 时代，给项目做减法往往更重要
- [来源: discussion.txt:16] （做减法/机构膨胀）就是大企业病的原理
- [来源: discussion.txt:17] 可以试 GitHub 项目 OpenSpec
- [来源: discussion.txt:18] 代码洁癖做法：每次跑完让 AI 删冗余代码、过时文档；文档只记录目前项目状态
- [来源: discussion.txt:19] 文件变大之前就弄（拆分/分章），否则后期更难维护，至少做分章
- [来源: discussion.txt:19] 减少规则仍需要自己限制或盯着 AI
- [来源: discussion.txt:19] 实际架构与已淘汰部分的文档最好分开
- [来源: discussion.txt:19] 修文件 3-4 次的教训：让 AI 自己记录，不是内容讲太长就是实现过程打转；最近一次用 Claude 子 agent 无视文件规则、按章节分批重整成功
- [来源: discussion.txt:20] 更倾向由开发者负责对话约束行为：先让 AI 分析项目架构并确认需求（plan 模式）→ 执行修改 → 让 AI 审核修改过程中因架构缺陷导致的临时性方案 → AI 审完自己再审是否存在临时方案、删死代码、写测试用例 → 人工复查与测试 → 提交
- [来源: discussion.txt:20] 人工约束能很大程度避免 AI 忽略约束；代价是每次对话都塞 md、token 花得多
- [来源: discussion.txt:21] 对话达到一定数量后，让 AI 生成对话记忆精简版，用 skill 交接对话，在新对话继续开发；新会话开全局记忆索引
- [来源: discussion.txt:21] 全局记忆做成"索引+记忆"两部分以减少 token 消耗；新会话会让 agent 重新耗 token 了解内容，但至少少犯错，规则也会重新捡起不至于忘
- [来源: discussion.txt:22] rule 设置了，听不听全由它：第一次会听，和人类一样，等你忘了，它也一起忘了
- [来源: discussion.txt:23] 让 AI 先写文档会写个超级复杂的文档，再让它照做，token 耗光也做不出来
- [来源: discussion.txt:24] 初始化设计非常重要；单靠万能规则、万能提示词不出问题才怪
- [来源: discussion.txt:24] AI 编程问题规避的最佳方案不是万能规则/万能提示词，而是搞懂模型特性和工具
- [来源: discussion.txt:24] 上下文不会管理、一上来猛堆提示词，后面注意力爆炸、灾难性遗忘
- [来源: discussion.txt:25] （对某方法/数据）有一定作用但具体多大不好说，列的数据基准不知道；日常开发错误率 43% 的话没人用 AI 编程——一个任务 43% 错误率，一个项目那么多任务，百分百不可能成功（对数据的怀疑）
- [来源: discussion.txt:26] 一直沿用的流程：1 写编码规范文档（风格、边界、红线）；2 写技术文档（基础技术栈、项目框架）；3 逐步列需求；4 要求 AI 阅读以上文档输出系统实现方案；5 依方案写系统详细设计、数据库设计、接口设计等文档，最后编码
- [来源: discussion.txt:26] 上述流程每一步都要重读最初的编码规范和技术文档；token 富余时可让多个 AI 交叉检验
- [来源: discussion.txt:27] 正常步骤被吹得神乎其神，既高估 AI 也低估自己对 AI 的理解
- [来源: discussion.txt:27] 标准流程：对齐需求 → 设计方案 → 完善方案 → 确认开发顺序 → 单步执行确认 → 自审报告
- [来源: discussion.txt:28] 一大堆抽象指令 AI 能遵守吗？能，但不完全能；性能不行的模型不太听话；聪明的模型会自言自语"哦，这违反了用户定下的 xxx 规则"而另想方案；有的模型更抽象也能执行
- [来源: discussion.txt:28] 模型训练语料里约束对应明确、练得好的模型比较听话
- [来源: discussion.txt:28] 有效果，但核心是更强的约束、边界；最好两层约束：第一层最外面的全局约束 + 具体项目第二层更详细约束
- [来源: discussion.txt:28] 指令也只是输入，和普通对话同一性质、同一优先级（并无特殊强制性）
