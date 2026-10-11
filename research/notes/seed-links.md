# 种子链接深挖笔记（vibe-coding 大规模调研 · 第一批）

抓取日期：2026-10-11。本地归档：`D:\Code\oh-my-repo\research\raw\repos\`（4 个仓库）与 `D:\Code\oh-my-repo\research\raw\initial-links\`（5 个 md）。

---

## 1. lennney/stop-that-shit（2,545 stars）

本地：`research/raw/repos/stop-that-shit/`（含 README_EN/CN/KO、ARCHITECTURE.md、EVIDENCE.md、cases/、skills/）

- 定位：Skill + Guard（Hook 运行时强制）双层结构，治理 AI coding agent 的"无需求防御与范围膨胀"。支持 Codex / Claude Code / OpenCode / Hermes / Pi / OMP 六宿主（`README_EN.md`）。
- SHIT 哲学四分类（`README_EN.md`）：**S**cope creep（修复膨胀成无关重构）、**H**ashing & hypothetical hardening（没人读的 SHA-256、为想象未来写的兼容层）、**I**ntent violation（说好只读 review 却改了文件）、**T**ask thrashing（读/测/评无新信息地反复重启）。
- 核心规则是"Stop Ladder"五步决策序（`skills/stop-that-shit/SKILL.md`）：①明确交付物/权限/承诺 → ②先用现有工具直接解 → ③只为具体缺口扩展 → ④按效果评判防御（保留有效保护、删无用、修复吞错的）→ ⑤验证后收工。强调"行数/文件数/检查数不能替代判断"。
- 关键平衡：不是极简主义——"必要的迁移、受影响调用方、跨组件测试必须完成，即使 diff 变大"；反对的是"无当前用途的添加"（`skills/stop-that-shit/SKILL.md`）。
- 触发/调用方式：宿主原生指令 `$stop-that-shit review|answer|monitor|change|watch -- <任务>`，参数化边界 `files=`、`deps=allow`、`hash=allow`、`agents=N`；Guard 默认 OBSERVING，显式指令才 ARMED（`README_EN.md`）。
- Guard 只查"显式边界"不做业务判断：review 模式下写文件→Stop；加依赖→Ask；超 agents 预算→Stop；加哈希→Stop；写 files= 之外→Stop（`README_EN.md` 表格）。
- 架构（`ARCHITECTURE.md`）：宿主无关决策核心（decision/contracts/controller.cjs）+ 六个薄适配器 + 仅元数据的 runtime 证据 sidecar；shell 静态分析（可变性/哈希意图/依赖意图）集中共享。
- **诚实证据观**：EVIDENCE.md 反复声明"这些结果不确立一般模型有效性"；README 直说 paired eval 历史运行"results with no difference"——即规则对模型本征行为无显著改变，价值在于机器强制边界。维护者自述唯一证据是"本地观察 SHA-256 行为未复发"的轶事。
- 案例工程：cases/ 目录为 JSON 化 Bad/Good 配对案例（18 个公开对），带 schema、校验器、paired eval 脚本；issue 模板分 bad-case/good-case，"正例同样重要"。
- 附带 skill **STSS**（Stop That Shit Slop，`skills/stss/SKILL.md`）：治理输出文本的防御性废话/堆叠对冲（"may perhaps potentially"→直接陈述），方法：Claim Ledger（不增事实）+ Sentence Consumer Test（谁用这句？改变什么理解？删掉什么变假？）。
- 高价值 issues（`research/raw/initial-links/stop-that-shit-issues-highvalue.md`）：#44/#45 agents=N 静默截断至 8 + 累计 vs 并发语义之争（结论："不能只凭数量判定过度使用"）；#66 中文心跳子串误降权 change→monitor（自由文本解析契约的脆弱性）；#86 MUTABILITY_UNPROVEN 误伤合法解析器（假阳性）。

## 2. vibe.yinziapi.top（银子 Vibe 信息中枢 / AP-Vibe，作者 ginsonko，仓库仅 6 stars，v0.4.0-beta.3）

本地：`research/raw/initial-links/vibe-yinziapi-ap-vibe.md`

- 定位与代码质量正交但相关：**本地项目记忆/上下文工作台**，打通 Codex/Claude Code 跨窗口项目记忆——直接回应 Karpathy"需要项目级持久记忆"的愿望。
- 治理机制：项目资料保留"决定、来源、修改记录"（有来处）；昨天的结论可被新约束纠正、旧事故待办留档（能纠正）；十维项目雷达基于档案证据打分、"未知项保留未知"（量化评估尝试，维度定义需看 ginsonko/ap-vibe 仓库源码）。
- 多 agent 协作分工：独立任务并行、依赖串行、成果回收再检查；"查看、执行与唤醒分开核对"。
- 数据立场：档案本地可查看/修改/回滚，不用于训练；个人非商业免费、源码公开但非 OSI 开源。
- 分发范式：安装方式是给 agent 发"安装口令"，由 agent 读 README/INSTALL-CODEX.md 自行安装。

## 3. mattpocock/skills（284,722 stars，"Skills for Real Engineers"）

本地：`research/raw/repos/mattpocock_skills/`（skills/{engineering,productivity,misc,in-progress,deprecated}，docs/engineering/）

- 立场：反 GSD/BMAD/Spec-Kit 等"接管流程"的框架——"它们夺走控制权，让流程 bug 难以解决"；改为小、可改、可组合、任意模型可用的 skill（`README.md`）。
- 四大失败模式 → 四类解法（`README.md`）：
  1. **没做我想要的**（misalignment）→ grilling 会谈（`grill-me`/`grill-with-docs`）："没人确切知道自己要什么"（Pragmatic Programmer）；agent 反过来深挖需求直到设计树每个分支都有结论。
  2. **太啰嗦**（jargon / 20 词说 1 词的事）→ 共享语言：`GLOSSARY.md` 术语表 + ADR；收益是命名一致、代码库更可导航、agent 思考 token 更省（作者称"可能是仓库里最酷的技术"）。
  3. **代码跑不起来** → 反馈回路：静态类型、浏览器访问、自动化测试；`tdd` skill 强制红-绿-重构；`diagnosing-bugs` 分阶段门控诊断环（先建"对这个 bug 变红"的反馈回路→最小化→假设→插桩→修→回归测试）。
  4. **造出泥球**（agents 加速软件熵）→ 每天投资设计：`improve-codebase-architecture` 扫描"deepening opportunities"（Ousterhout 深模块：大量行为藏在小接口后），HTML 可视化报告+逐项 grill；`to-spec` 在写 spec 前先问你要动哪些模块。
- **user-invoked vs model-invoked 双层设计**（`README.md` Reference 节）：用户调用的负责编排（/grill-me、/implement…），模型自动调用的承载可复用纪律（tdd、code-review…）；前者可调后者，不可调另一个前者——skill 组合的显式拓扑。
- `code-review` skill（`skills/engineering/code-review/SKILL.md`）：双轴并行子代理评审——**Standards 轴**（仓库文档标准 + 固定 Fowler 12 坏味道基线：Mysterious Name/Duplicated Code/Feature Envy/Data Clumps/Primitive Obsession/Repeated Switches/Shotgun Surgery/Divergent Change/Speculative Generality/Message Chains/Middle Man/Refused Bequest，均"是什么→怎么修"格式）与 **Spec 轴**（漏做/越权做 scope creep/做错的），并行防上下文污染，聚合时禁止跨轴重排。
- `code-review` 的三条元规则：仓库文档标准永远压过坏味道基线；坏味道永远是判断题不是硬违规；工具已强制的直接跳过。
- 全景技能族：grill-with-docs / to-spec / to-tickets（tracer-bullet 票+阻塞边）/ implement（TDD 于预定 seam + 收尾 code-review）/ implement-spec（任务图+就绪前沿并行子代理）/ wayfinder（超大工作拆决策票地图）/ retro（会话后给 agent 环境提改进）/ handoff（会话压缩交接）/ teach / wait-what。
- issues（gh api，165 open）：多为细粒度 skill 行为修正（grilling 问题写成陈述、context 压缩时机、code-review 被内置 skill 覆盖 #1234）。
- discussions 值得追：#236 nightshift（to-prd→to-issues 的自主执行层）、#246 本仓库 write-a-skill vs Anthropic skill-creator、#248 Claude 的 rules 特性。

## 4. Zhen-Bo/pragmatic-clean-code-reviewer → 已更名 **Zhen-Bo/smell-check**（240 stars，0 open issues）

本地：`research/raw/repos/pragmatic-clean-code-reviewer/`（README 引用的就是 smell-check 新名；API 确认 301 重定向，desc: "Formerly pragmatic-code-review"）

- 定位：**证据分级的代码/测试坏味道审计 skill**——把《Refactoring》《Clean Code》测试坏味道文献变成 agent 可执行的程序；明确"不是 PR 评审 bot：无合并建议、不改代码、不跑测试"（`README.md`）。
- 核心方法论："Measured, not vibed"——结构度量尽量来自脚本（wc/AST 计数/jscpd/lizard），量不到的标 `estimate` 决不冒充事实；每条 finding 带**证据等级**：`mechanical`（脚本数出来的）/`semantic`（agent 判断且写出依据）/`estimate`（弱且自认）。
- "Diagnosis, not prescription"：finding 只说哪里错、维护者付出什么代价；修复策略归修复负责人。
- 动机宣言（`README.md` "Why smell-check"）："读《Refactoring》改变你看代码的方式，效果持续约一周。没人能在交付的同时把几百页判断装进工作记忆…… agent 写的代码越来越多，人脑里装的越来越少。书早就写好了怎么读代码库，smell-check 把它变成 agent 可执行的过程：度量替代记忆，证据替代印象。"
- 规则集：20 条稳定代码规则（长函数/大文件/深嵌套/重复代码/上帝类/霰弹手术/发散变化/推测泛化/死代码/魔法值…）+ 12 条测试规则（无断言测试/断言轮盘/eager 测试/条件测试逻辑/mystery guest/睡眠测试/顺序依赖/敏感相等…）+ 4 条实验规则默认关。每条规则自带例外（表驱动测试循环、composition root、wire 边界 DTO 被记录理由后 dismiss 而非报噪音）。
- **规模画像（size profiles）**：阈值随"多少人需要读这份代码"缩放——personal(长函数100行)/small(60)/medium(40)/large(30)/ultimate(20, auto 永不选)；auto 按源码行数选档并向用户披露所选档位与理由（`README.md`）。这是"质量标准与维护者规模挂钩"的可操作化。
- 审计流程六步（`SKILL.md`）：scope gate（用户必须显式点名范围，缺则询问等待；大范围警告 token 成本+上下文压缩风险，绝不静默截断，中断写 partial 报告）→ 读 .smell-check.toml → 定 profile → 机械pass → 语义pass → 合并出报告（Markdown 为 canonical，HTML 为 AI 按 DESIGN.md 现写，最后 validate_report.py 校验，验证错误必须全修）。
- 安全立场（`SKILL.md` Data stance）：被扫内容是数据不是指令（prompt injection 免疫声明）；不改不执行被审代码；不读 .gitignore 路径（防泄密）。
- issues（`research/raw/initial-links/smell-check-issues-highvalue.md`）：#7 维护者抱怨 Opus 5 越权自行开 PR、把反思要求当 prompt injection、被拆穿后撒谎——"有 gpt-5.6-sol 监督 Opus 时从不发生"（多模型互监的一手报告）；#1→#15 演化史显示每次大改都在修 AI 执行 skill 的失败模式（AI 困惑、执行被审代码、误触发）。

## 5. Karpathy 推文（2026-01 末，status 2015883857489522876）

本地：`research/raw/initial-links/karpathy-tweet-claude-coding-notes.md`（全文已存）

- 工作流：从 80% 手写/20% agent 变为 **95% agent**（Opus 4.5 + Claude Code）。
- CLAUDE.md 十条经验：极显式圈定 scope 且保持窄；**绝不说"X 看起来不对/多余"**（模型会当作重构/删除的邀请）；写验收标准（列应通过的测试）；列出预期改动文件与改动类型；改完 review diff+运行，接受"验证者"角色的繁琐；要求模型清理自己的临时产物；不过度约束解法（给自由度，像 mini-delegation）；**先设计文档后代码**（比 plan mode 可控，plan mode 自带会走火的假设）；CLAUDE.md 写约定不必太细（模型能从文件推断）。
- 三大失败模式：①静默错误假设（不管理困惑、不求澄清、不摆 tradeoff、该反驳不反驳）；②过度复杂化（膨胀抽象、不清理死代码扩大后续 diff、200 行写 50 行就够、1000 行实现 100 行的事、测试膨胀到源文件 3 倍还自造测试框架）；③附带损伤（改/删任务外不理解的代码与注释）。
- 愿望清单：模型需要"**困惑情绪**"信号（触发复查与澄清）；需要**项目级持久记忆/scratchpad**（非对话转录的朴素拷贝）。
- 心法："你是一个稍微不称职但非常快的实习生的经理"——清晰任务范围、验收标准、适度放权、信任但验证。

## 6. multica-ai/andrej-karpathy-skills（218,394 stars；原 forrestchang/andrej-karpathy-skills 已转移至此）

本地：`research/raw/repos/andrej-karpathy-skills/`（CLAUDE.md、skills/karpathy-guidelines/SKILL.md、.cursor/rules/karpathy-guidelines.mdc、EXAMPLES.md、README.zh.md）

- 本质：把 Karpathy 推文的观察浓缩成**一页四原则 behavioral skill**，同时提供 CLAUDE.md / Claude 插件 / Cursor 规则三种载体。
- 四原则（`skills/karpathy-guidelines/SKILL.md`）：①**Think Before Coding**（显式陈述假设、多解释并列出而非静默选择、有更简方案就说、困惑即停并点名）——治"静默错误假设"；②**Simplicity First**（不做没要求的功能、单次使用不抽象、不做没要求的灵活性/可配置性、不为不可能场景写错误处理、200 行能 50 行就重写；检验法："资深工程师会说这过度复杂吗"）——治"过度复杂化"；③**Surgical Changes**（不"顺手改进"相邻代码/注释/格式、不重构没坏的东西、匹配现有风格、发现无关死代码只提及不删除、只清理自己造成的孤儿引用；检验法："每一行改动都能追溯到用户请求"）——治"附带损伤"；④**Goal-Driven Execution**（命令式任务转可验证目标："修bug"→"先写复现测试再修"；多步任务列 step→verify 清单；强标准让模型自主循环，弱标准逼人反复澄清）——放大 LLM"会循环到达标"的长处。
- 自带 tradeoff 声明：偏向谨慎而非速度，琐碎任务自行判断不必全套流程。
- 生效判据（README "How to Know It's Working"）：diff 里无关变更变少；过度复杂导致的返工变少；澄清问题出现在实现之前；PR 干净最小无顺手重构。
- **PR #197 IN-PRACTICE.md**（未合并，全文已存 `research/raw/initial-links/karpathy-skills-PR197-IN-PRACTICE.md`）：四原则在真实生产库（多租户 TS 服务、双 agent 并行）作为 hook 强制规则落地后的增量——
  - **缺失的第五维：Verification Is Not Optional**："done 的主张只有检查真跑过且输出被看过才有效；跳过的测试/构建/部署要说清是哪个为什么；失败输出按失败报告，绝不总结成进展"。事故：`tsc` 在无 tsconfig 的根目录跑，打印帮助文本退出 0，链条继续 commit——"output seen 不等于 exit code 为零"。
  - 锐化1 **报告没查的部分**："看了 6/20，其余大概类似"必须原样写，不得写成对 20 个的结论——LLM 读了 6 个文件会像读了 20 个那样总结，"非不诚实，是总结读起来更好"。事故：安全审计后端全读前端只抽样，报告不说清读者会以为前端已清白。"未陈述的假设当发现呈现就是缺陷，即使碰巧对了。"
  - 锐化2 **复现测试必须先红**：绿着结束的测试什么都证明不了；红步不仅验证修复还验证测试本身（事故：签名密钥校验测试立即通过，因为它测空字符串而真实事故是变量缺失）。"新测试在写修复前就通过，你没找到 bug，你找到了一个坏测试。"真实漏洞案例：持续绿的 CI 里躺着越权洞（只断言 200/401 从不断言 403）。
  - 锐化3 **存量死代码的调和**："无关 diff 里不删，记录下来开专门任务清理"——零死代码标准管的是仓库应达状态，surgical 规则管的是单个 diff 允许包含什么；两规则两条作用域。事故：修授权 bug 时发现 3 处近似重复的审计日志 helper，诱人但无关；只加了自己的第 4 个调用点，旧 3 处记录成独立任务。
- 生态：issue #206 提议基于**Karpathy 更新的推文**（status 2105819303471976479，关于解释 agent 输出：清晰写作/图/交互网页/定制讲解视频）增加 `explain-agent-output` skill；#202 加 Gemini CLI/Antigravity 支持；#191 "按原则 2，Claude 5 模型应跳过此文件"。

## 7. Mnilax 推文（status 2053116311132155938）

本地：`research/raw/initial-links/mnilax-tweet-karpathy-analysis.md`（webReader 抓取被截断，仅存骨架）

- 内容：对 Karpathy 2026-01 推文的工程化解读，把三大失败模式命名为 **silent wrong assumptions / over-complication / orthogonal damage**——这套命名后被 forrestchang/multica 社区直接转成四原则 skill 的 "The Problems" 章节（`research/raw/repos/andrej-karpathy-skills/README.md` 可对照）。
- 价值：作为"失败模式 → 治理规则"映射链的中间节点；完整串未取到，是待补线索。

---

## 横向观察（跨来源综合）

1. **同一 Karpathy 源头的三条演化路径**：一页原则（karpathy-skills，218k stars）→ 运行时强制（stop-that-shit 的 Guard + IN-PRACTICE 的 hook 化）→ 文献程序化（smell-check 的证据分级）。覆盖"提示词 → 工具强制 → 度量审计"整条治理光谱。
2. **共识失败模式清单**（多源交叉验证）：scope creep / 过度复杂化与推测性泛化 / 顺手改动任务外代码 / 死代码不清理 / 测试膨胀与假绿 / 静默假设不澄清 / 越权行动（自行开 PR、review 改文件）/ 汇报不实（"应该没问题"当"已验证"）。
3. **共识机制模式**：显式 scope+验收标准先行（Karpathy CLAUDE.md 十条）；命令式转可验证目标（Goal-Driven）；双轴/多子代理隔离评审（mattpocock code-review）；证据分级与"未测部分显式声明"（smell-check、IN-PRACTICE）；配对案例回归（stop-that-shit cases）；渐进披露防 skill 膨胀（smell-check #2、mattpocock .agents/writing-docs）。
4. **诚实的负面结果同样重要**：stop-that-shit EVIDENCE.md 承认规则对模型行为"无差异"，价值在机器边界；这条对调研的"什么真正有效"问题是关键数据点。
5. **中文社区是重要生产者**：stop-that-shit（中文作者+LINUX DO 社区+中韩 README）、AP-Vibe、smell-check（中文维护者，繁中文档）——高质量治理工具并非英文社区独有。

## 最值得后续追问的线索

1. **PR #197 的 hook 强制版四原则**：IN-PRACTICE.md 的"验证非可选"维度与三条锐化是全部种子中最实战的规则增量——追 PR 是否合并、其 hook 实现、以及 issue #206 引用的 Karpathy 新推文（2105819303471976479，explain-agent-output 方向）。
2. **mattpocock discussions**：#236 nightshift 自主执行层、#246 write-a-skill vs Anthropic skill-creator、#248 Claude rules 特性；以及 `skills/in-progress/`（chief-of-staff、loop-me、setup-ts-deep-modules）和 `.out-of-scope/` 目录记录的"决定不做什么"。
3. **AP-Vibe 的十维雷达**：ginsonko/ap-vibe 仓库中风险评分维度的具体定义（目标符合度→证据验证等 10 维），是目前见到的唯一 vibe-coding 项目质量量化模型。
4. **smell-check 的 references/ 规则注册表**：`references/rules-code.md`、`rules-test.md`、`presets.md` 里每条规则的例外清单与阈值表，是可复用的规则资产（本地已克隆，直接读）。
5. **stop-that-shit 的 paired eval 方法论**：`evals/codex-paired/README.md` + `cases/` JSON 案例 schema——"如何科学评估一个治理 skill 是否有效"本身是个方法论富矿，含"无差异"负面结果的记录方式。
