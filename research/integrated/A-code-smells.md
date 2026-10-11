# 知识域 A（整合版）：AI 生成代码的坏味道 / 质量问题清单及实证数据

> 阶段 3 整合产物。输入：knowledge/01（六仓库）、02（社区讨论）、03（方法论）、04（坏味道与工具）、05（历史生态追查）。
> 整合规则：同类合并（保留最准确名称+定义+代码级表现，来源 2-4 个）；矛盾裁决（见文末）；移除纯历史八卦、产品 UX 抱怨、重复新闻叙事与方法学可疑数据（见 0.4 移除说明）。
> 原始条目约 200 条（smell-check 36 + Fowler/refactoring.guru 22 + APSD 红旗 11 + vibecheck 40 + 各类 checklist/研究报告/社区痛点约 90）→ 合并为 **62 条**，按 11 类组织。

## 0. 使用前提

### 0.1 坏味道的定位
- 坏味道 = 「有已知清理手法的可维护性警告」，**不是 bug 的证明**；工具测数字，判断含义与例外靠 LLM/人（smell-check 总则）。本清单用于诊断（发现+证据），修复策略另属修复负责人。
- 数值阈值随规模档案变化（smell-check presets：long-function 20–100 行、deep-nesting 1–6 层、large-file 200–1000 行等），本文件只定义「数什么」，切点由使用者按项目规模定。

### 0.2 AI 代码坏味道的四条总体机制（成因总纲）
1. **放大器 / 向平均水平回归**：LLM 从人类代码的缺陷分布中学习，模仿大众写法而非最佳写法；「没有 AI 独有的 issue 类型——人类与 AI 犯同类错误，AI 只是更频繁、更大规模」（CodeRabbit）；DORA 2025 同称 AI 放大组织既有优劣势（CIQ、CodeRabbit、DORA）。
2. **概率偏置 → 样板偏好**：语言模型偏好高概率输出——生成刻板样板（getter/文档注释/通用模式）比生成应用特定实现更「合适」，于是后者系统性不足（HN duskwuff 机制分析）。
3. **请求间无记忆 → 重复生成相似解**：不同请求对同一问题反复生成相似代码块（如相同的 409 重试块），而非抽公共库（CIQ 机制）；上下文缺失是信任第一杀手（Qodo：65% 重构场景错过相关上下文）。
4. **失败模式是「貌似合理」而非「困惑」**：命名惯用、风格统一、细看才知错；人类评审直觉靠「困惑信号」触发，AI 代码 uniformly confident，注意力被均匀分布而本不该均匀（continuumcode；条目 62）。

### 0.3 概念辨析（Skill 中勿混用）
- 「LLM code smells」（SpecDetect4LLM 系列论文）指**调用 LLM 的应用代码**的坏味道（LLM 推理集成不良实践），**不是**「LLM 生成的代码」的坏味道。前者实证：692 个开源项目 73.5% 受影响（precision 91.3%）/ 前期 200 项目 60.5%。
- 系统级元坏味道（Clean Code 六症状）：Rigidity 僵化 / Fragility 脆弱 / Immobility 固化 / Needless Complexity 无谓复杂 / Needless Repetition 无谓重复 / Opacity 不透明——是下层具体条目的上层表现，不作单独条目。
- 质量维度框架（ap-vibe 十维）：intent/logic/completeness/reliability/security/performance/maintainability/compatibility/usability/validation——可作为 Skill 的评估输出结构参考，非坏味道本身。

### 0.4 移除说明（整合规则 3 的执行）
- 移除：造词史/年度词/Torvalds/rsync 事件/Lovable 商业互怼/Claude Code 泄漏源码争论等**过程叙事**（仅保留其可量化部分）；Cursor 视图/diff 显示/compaction/封号/superpowers 慢等**产品 UX 抱怨**（非代码质量）；hooks/规则文件配置细节（属其他知识域）；掘金 AI 助手文的推广性数据（标注需回溯原始论文，弃用）。
- 降级为低置信度：Yegge 5x/25x 生产力倍率、Anthropic「90% 代码 AI 写」（口径不明，见量化节 G 组）。

---

## 一、冗余与重复类（AI 高发区 #1）

**1. 重复代码（token 克隆 / copy-paste）** [SC code.duplicate-code; Fowler Duplicate Code]
- 定义：近似相同的 token 序列出现在多处，改一处漏其余。
- 典型表现：同一 409 重试块、同一校验逻辑在多文件各有一份；5+ 行重复块堆积。
- 成因：AI 请求间无记忆，反复生成相似解而非抽公共库；vibe coding 下复制粘贴首次超过移动/重构成为主导变更形式。
- 检测：jscpd 等克隆工具（`--min-lines 5 --min-tokens 50` 量级）；**无工具不得编造克隆百分比**；重复度/KLOC 趋势监控。
- 来源：smell-check、Fowler、GitClear、CIQ。

**2. 重复知识（同规则多处表达 / 信息泄漏）** [SC code.duplicated-knowledge; APSD Information Leakage]
- 定义：同一条业务规则/设计决策被编码在多处（即使文本不同）；改规则需协同编辑。与 1 的区分：这是「共享含义」不是「相似形状」——偶然相似、必须分叉的代码应保持分离。
- 典型表现：train/test 数据构造各自内嵌同一文件格式知识；HTTP 接口暴露整个 `Map getParams()` 而非 `getParameter(name)`。
- 检测：变化耦合判断——同概念，改一处不改其余即为错。
- 来源：smell-check、APSD、PragProg（DRY 是知识单一权威，非文本去重）。

**3. 错过复用（就地复制而非调用既有实现）** [SC code.missed-reuse(experimental); CCON "Duplicated instead of reused"]
- 定义：repo 已有合适的 helper/类型/模块，附近又新写一份。
- 典型表现：既有同功能函数旁又写一个（import 顺序导致 6 个月的 source of truth 被覆盖——Mnilax 规则 8 事故）；monorepo 共享包被多个 worker 各自重复实现（HN established-codebase 楼主自述）。
- 成因：多文件 agent 编辑从不搜索既有 seam；「写前不读」。
- 检测：新逻辑匹配到同职责、接口兼容的既有符号，**须引用具体既有符号路径作证据**。
- 来源：smell-check、continuumcode、Mnilax、HN。

**4. 补丁堆积（特例堆叠）** [SC code.patch-accumulation(experimental)]
- 定义：单元靠堆特例生长——额外 flag、函数末尾补丁、每次事故「再来一个 if」——而非围绕真实规则重设计。
- 典型表现：`if special_customer` / `if legacy_path` 式分支主导的长函数，分支间无公共结构，注释指向过去的救火。
- 成因：AI 连续窄修复的典型累积形态（AI 行为特有高发）。
- 来源：smell-check、CodeRabbit（控制流缺陷 +75% 的一部分）。

**5. 重复 switch（同一判别多链复现）** [SC code.repeated-switches; Fowler Switch Statements]
- 定义：对同一 type/status 的相同判别复制到多个 switch/match/if-else 链；新增变体要逐链猎取。
- 例外：系统边界处的单个穷尽 switch。
- 来源：smell-check、Fowler、Clean Code（多态优先于条件链）。

## 二、规模与复杂度类（膨胀类）

**6. 过长函数（god function）** [SC code.long-function; Fowler Long Method; VBC no-god-function]
- 定义：一个函数体做太多事，读者无法在脑中装下整条路径。
- 典型表现：80+ 行（vibecheck 阈值）或超规模档案阈值（20–100 行）；名字需要 "and" 才诚实；高低抽象层混杂。
- 检测：机械可数（非空非注释行；一行多语句计 1）。
- 来源：smell-check、Fowler、vibecheck。

**7. 过大文件 / 单文件巨石** [SC code.large-file; Reddit 年度痛点帖]
- 定义：单文件大到导航/评审/归属成本上升。
- 典型表现：AI 默认把你要的东西写进单个超长文件 → 难懂难调；撞上下文窗口后生成极慢（改一行重生成整段）；后期拆分/重构常出错或丢功能，进入「AI 修不了、我也修不了」的死胡同。
- 例外：生成代码、纯数据表/快照 fixture、vendored 第三方拷贝。
- 来源：smell-check、Reddit r/ChatGPTCoding 年度帖（痛点②⑤⑥⑦）。

**8. 过深嵌套（认知复杂度的主要载体）** [SC code.deep-nesting; VBC no-deep-nesting; CIQ]
- 定义：控制结构堆叠到看不清 happy path。
- 典型表现：4+ 层嵌套不改用早返回；嵌套、递归、混合运算符推高认知复杂度（Sonar 认知复杂度指标——度量「人脑的痛感」，与可维护性强相关）。
- 数据：vibecheck 31 仓库扫描中 46% 的发现是深嵌套（单规则占比过高，评分须设每规则上限）；CIQ：AI 代码条件 +7%、循环 +4%，认知/圈复杂度比值上升。
- 检测：峰值深度机械可数；认知复杂度工具（SonarQube/Codacy/Semgrep）。
- 来源：smell-check、vibecheck、CIQ。

**9. 上帝类（多变更理由中枢）** [SC code.god-class; Fowler Large Class]
- 定义：一个类型拥有许多不相关变更理由，"do-everything" 中枢，内聚低。与 7 区分：大小主因报 large-file，多职责主因报 god-class。
- 来源：smell-check、Fowler。

**10. 过长参数列表** [SC code.long-parameter-list; Fowler]
- 定义：调用方要提供太多独立实参，调用点易错难扩展。检测机械：所有声明值参数计 1（解构算 1，排除 receiver）。
- 来源：smell-check、Fowler、Clean Code（参数尽量 ≤3）。

## 三、数据与状态类

**11. 基本类型偏执** [SC code.primitive-obsession; Fowler]
- 定义：领域概念（id、money、email、status、单位）用裸 string/number/bool 携带，校验/格式化规则散落重复。
- 来源：smell-check、Fowler、Clean Code（值对象优先）。

**12. 数据泥团** [SC code.data-clumps; Fowler]
- 定义：同一小组值总一起出现在参数/字段/返回元组中——一个没有名字的概念（3+ 值或带不变式的 2 值跨多签名出现）。
- 来源：smell-check、Fowler。

**13. 魔法值** [SC code.magic-values; CC]
- 定义：裸字面量携带策略含义（超时、限额、状态、乘数）。例外：数学恒等值、故意具体的测试数据。
- 来源：smell-check、Clean Code。

**14. 全局数据 / 共享可变状态** [SC code.global-data; PragProg Tip 47/57]
- 定义：进程级可变状态让远处代码互相干扰，写入顺序成为契约的一部分；「共享状态就是错误状态」。
- 来源：smell-check、PragProg。

**15. 纯数据类 / 贫血实体（规则外泄）** [Fowler Data Class; cleanarch 常见坑]
- 定义：只有字段没有行为的类，业务规则散落到各 service——分层只是「多了几步的文件夹」。
- 典型表现：Order 只是 public setter 口袋，不变量全在 OrderService。
- 来源：Fowler/refactoring.guru、NDepend clean architecture 文。

## 四、抽象与耦合类

**16. 投机泛化 / 过度抽象（YAGNI 违例）** [SC code.speculative-generality; G Over-engineering; KP over-complication; STS]
- 定义：为想象中的未来而存在的抽象、参数、扩展点——无人使用或仅单一实现。
- 典型表现：单一折扣计算写成策略类+Enum+Protocol+dataclass 30+ 行 setup（Karpathy 例，4 行函数够用）；空接口层级、从不改变行为的 config flag；1000 行实现 100 行的事；「AI 在你合理地**不想要**最佳实践的地方强行套用最佳实践」（HN Iulioh）。
- 成因：模型默认套用训练语料中的设计模式与「最佳实践」（「训练集的默认运行模式是加尽可能多的 bloat 和抽象」——HN andai）；时间维度错配——好代码是简单解决今天的问题，不是过早解决明天的问题。
- 检测：未用类型参数、单实现钩子；自问「资深工程师会说这过度复杂吗」。
- 来源：smell-check、Google looking-for、Karpathy、stop-that-shit、HN。
- 附：过度指定指令同样妨害判断（AGENTIF 研究 + superpowers #895 讨论）——给 agent 的 spec 指定意图与约束优于指定实现。

**17. 浅模块 / 直通方法（含碎片化）** [APSD Shallow Module + Pass-Through Method; SC code.middle-man; Fowler Middle Man/Lazy Class; CIQ]
- 定义：接口复杂度与其功能不相称；多数方法只转发到另一类型；每层应有不同抽象，直通方法说明相邻两层抽象相同。
- 典型表现：Java IO 式三对象链（前两个从不直接使用）；AI 代码「文件更小、类/函数更多更细，但整体认知复杂度仍升」——碎片化+平庸化（CIQ）。
- 来源：APSD、smell-check、Fowler、CIQ。

**18. 依恋别人家的数据（Feature Envy）** [SC code.feature-envy; Fowler]
- 定义：函数更多伸手进别的类型的数据而非处理自己的状态。检测：权衡外部字段/getter 使用 vs 自身状态（数据所有权问题，非窄接口协作）。
- 来源：smell-check、Fowler。

**19. 消息链 / 火车残骸** [SC code.message-chains; Fowler; PragProg Tip 46]
- 定义：调用点走过一长串中间对象（`a.b().c().d()`），调用方对对象图知道太多。例外：设计为单表达式的 fluent DSL。
- 来源：smell-check、Fowler、PragProg（LoD：「访问一个东西尽量别超过一个点」）。

**20. 霰弹式修改（Shotgun Surgery）** [SC code.shotgun-surgery; Fowler]
- 定义：一个概念性变更被迫在散落多文件做许多小编辑，漏一处就行为漂移。检测：git 历史的重复并行编辑作证据。
- 来源：smell-check、Fowler。

**21. 发散式变化（Divergent Change）** [SC code.divergent-change; Fowler]
- 定义：一个模块因许多不相关理由被改（持久化+UI+计费规则同文件）。与 9 区分：「现在多职责」报 god-class，「随时间多变更轴」报本条。
- 来源：smell-check、Fowler。

**22. 时序分解（Temporal Decomposition）** [APSD 红旗]
- 定义：按执行顺序组织模块，导致同一知识被多处使用（train creator / training / test creator / evaluation 四模块都懂同一数据格式）。与 2 互为因果：一个看知识耦合、一个看结构形态。
- 来源：APSD。

**23. 契约漂移（跨文件不一致假设）** [SC code.contract-drift(experimental)]
- 定义：契约两侧（producer/consumer、schema/handler、client/server DTO、route/handler 参数）在字段名、可空性、单位或错误形状上跨文件分叉。
- 成因：AI 跨文件编辑无全局视图。检测：成对引用两侧对照。
- 来源：smell-check（experimental）。

> 其他低频 Fowler 坏味道（保留名录、不展开）：Refused Bequest、Temporary Field、Inappropriate Intimacy、Alternative Classes with Different Interfaces、Parallel Inheritance Hierarchies、Incomplete Library Class、「用注释掩盖本应重构的代码」。来源：refactoring.guru / mattpocock 12 条基线。

## 五、防御与过度工程类

**24. 假设性加固（无效防御）** [STS H; KP]
- 定义：没有落地目的的「以防万一」机制——没人读的校验和、为想象未来准备的兼容层。判据：保护必须检测问题并导向拒绝/恢复/诊断；**机制名字和行数不决定保护是否有用**。
- 典型表现：导出文件顺手附 `.sha256` 而发布流程不消费 digest（若消费则必须保留）。
- 来源：stop-that-shit（SHIT 之 H）、Karpathy。

**25. 不必要的重依赖** [VC 性能检查 1; GitHub 官方 review 第 4 步]
- 定义：内置方法/标准库够用时引入完整工具库或新包。
- 成因：训练数据里出现过（vibecoder）；新包还可能是幻觉包（→ 条目 50）。
- 来源：vibecoder checklist、GitHub copilot review 教程、Veracode。

**26. 配置参数外推（把复杂度推给用户）** [APSD]
- 定义：该内部决策的导出成参数让调用方指定；借口是「用户更懂自己的领域」，实质常是逃避处理重要问题。自问：「调用方能选出比我算出的更好的值吗？」不可避免时给好默认值。
- 来源：APSD（含 Clean Code「防止过度可配置化」）。

## 六、命名与可读性类

**27. 命名坏味道（误导 / 含糊 / 不一致三子型）** [SC code.misleading-naming; APSD Vague Name + Hard to pick name; VC; CR]
- 误导：名字暗示错误行为——`validateUser` 实际查支付状态（vibecoder）；隐藏副作用的名称。只有不匹配会改变维护者决策时才标记。
- 含糊：给变量/方法找不到简单名字，说明设计可能不干净（APSD「Hard to pick name」）。
- 不一致：同一概念多词并存、与 repo 术语错配、泛化标识符——CodeRabbit：命名不一致近 2 倍（AI 缺 repo 惯例上下文，趋向通用默认名）。
- 来源：smell-check、APSD、vibecoder、CodeRabbit。

**28. 复述式注释** [VBC 4 条规则; APSD comment that repeats code; G]
- 定义：注释解释代码在做什么而非为什么存在。
- 典型表现：`// initialize the counter`；旁白式 `// This function handles...`；编号步骤注释 `// Step 1:`；ASCII 分割线 `// ========`。
- 来源：vibecheck、APSD、Google（多数注释应承载代码无法承载的推理）。

**29. 犹疑 / 免责注释** [VBC no-hedging-comments]
- 定义：暴露未验证不确定性的注释。典型表现：`// should work`、`// might not be the best approach`、`# might not be ideal`。
- 定性：AI 特有 tell——出现即提示该处未经核实。
- 来源：vibecheck。

**30. 自信的错误注释 / 解释** [VC 注释准确性; CCON Confident wrong explanation; HN]
- 定义：注释/文档/总结自信地描述错误的行为或理由。
- 典型表现：「返回用户全名」的注释挂在返回 ID 的函数上（比没有注释更糟）；对「为什么能工作」plain wrong 即使结果对（HN gabriela_c）；啰嗦超长注释是 Claude 系特有（HN mkozlows）——错误注释会误导未来读它的 agent（HN jazzypants 因此重写）。
- 检测：每条 JSDoc/行内解释对照代码实际行为读（vibecoder）；从解释中抽查事实性 claim（continuumcode 七步之 6）。
- 来源：vibecoder、continuumcode、HN。

**31. 占位与残留（生成不完整痕迹）** [VBC 6 条规则; VC 质量检查 1]
- 典型表现：`TODO: implement` / `FIXME: add` 占位；`throw "not implemented"` / `NotImplementedError` 桩进生产；被 import 但从未调用的函数/类型（含定义后从未引用的 `Protocol` 类）；console.log/print 遗留；`// Generated by ChatGPT` 式署名注释；`from module import *`。
- 定性：AI 生成不完整的直接指纹（vibecoder：「死代码是维护负担和未来 review 的困惑源」）。
- 来源：vibecheck、vibecoder。

**32. 与既有约定 / 风格漂移** [MN 规则 11; CR 格式 2.66x; KP Surgical Changes; G Consistency]
- 定义：改动不匹配 repo 既有模式——命名、架构、格式、错误处理惯例。
- 典型表现：用自定义 error 类的库中出现新代码抛裸 Error；向 class 组件库引入 hooks 破坏测试模式（Mnilax 事故）；修 bug 顺手改引号风格、加类型注解、重排空白（Karpathy 反例）；「AI 不能完美遵守 repo 惯例，命名/架构/格式趋向通用默认」（CodeRabbit）。
- 判据：conformance > taste；真觉得有害就提出来，不要静默分叉（Mnilax）。
- 来源：CodeRabbit、Mnilax、Karpathy、Google。

## 七、错误处理类（AI 高发区 #2）

**33. 吞错（静默失败）** [VBC 6 条规则; AS; STS; MN 规则 12]
- 定义：异常被捕获后既不处理、不上抛、也不导致可见失败。
- 典型表现：空 catch 块；`except: pass` / bare `except:`；catch 只 `console.error` 不 rethrow；`.then()` 链无 `.catch()`；`except X:` 只打日志就继续。
- 高危实例：计费 try-catch 吞错 → 支付失败被当成功 → 给失败付款用户发订阅，真金白银亏损（aislopfix 六个月修复业务中最危险类目之一）。
- 来源：vibecheck、aislopfix、stop-that-shit、Mnilax。

**34. 含糊报错** [VBC no-vague-error; CC]
- 典型表现：`throw new Error("Something went wrong")` 弝含糊异常与含糊 `Promise.reject`；抛出的异常不带上下文（Clean Code）。
- 来源：vibecheck、Clean Code。

**35. 错误路径覆盖缺口（happy path 偏好）** [CR ~2x; VC 逻辑检查 2; CCON 七步之 5]
- 定义：try-catch 只处理预期错误类型、静默吞掉意外；或整段路径无 null 检查/early return/护栏。
- 成因：「agent 写 happy path 很好、错误处理不一致」（continuumcode）；CodeRabbit：错误处理与异常路径缺口近 2 倍，与真实世界宕机紧密相关；后台任务「捕获即忽略」意味着任务无声停止。
- 检测：专门看被调用方失败时会发生什么——错误被吞、被包装、被记录还是被返回。
- 来源：CodeRabbit、vibecoder、continuumcode。

**36. 失败被读成成功 / 假完成** [STS; MN 规则 12; PR197 第五维; SUP]
- 定义：把失败读成空结果继续；跳过检查仍宣称完成。
- 典型表现：catch 后返回空集合让上游以为成功；跳过 14% 记录的「迁移完成」11 天后报表才发现（Mnilax 事故）；`npm run lint && tsc --noEmit | head -5 && git commit`——tsc 在无 tsconfig 的目录打印帮助文本、exit 0、链条继续 commit（exit 0 ≠ output seen，PR197 事故）；报告读了 6/20 个文件却总结成 20 个的结论。
- 判据：「最贵的失败是看起来像成功的失败」；没有新鲜验证证据不得宣称完成；checked 与 assumed 必须区分汇报。
- 来源：stop-that-shit、Mnilax、karpathy-skills PR#197、superpowers verification-before-completion。

**37. 可定义掉的错误 / 过度防御式异常** [APSD Define Errors Out of Existence]
- 定义：可通过重定义语义消除的错误条件却抛异常（unset「不存在则抛」vs「确保不再存在」）；异常代码比主逻辑还大、很少被执行故难测试易藏 bug。
- 来源：APSD、MITRIX（Phase 1 清理含「补/修基础错误处理」）。

## 八、测试类（AI 高发区 #3）

**38. 无效断言 / 同义反复测试** [SC test.assertion-free; SUP 镜像断言; MP Tautological; HN]
- 定义：测试构造上就不可能失败，或根本不断言。
- 典型表现：测试体零断言位点；`const expected = buildQuery({...}); expect(buildQuery({...})).toBe(expected)` 永真；「LLM 生成的测试除了 1==1 什么都没测」（HN tmarice）；change detector——只有有意决策（常量值、私有结构）能让它挂。
- 检测：期望值必须来自独立事实源（字面量/手算 fixture/spec）；心内 Mutation Check——错常量/错分支/空返回等现实变异至少一个测试应失败。
- 来源：smell-check、superpowers、mattpocock、HN。

**39. 测试不编码意图（全过但测错东西）** [MN 规则 9; PR197 锐化 2; SUP TDD]
- 定义：测试通过证明不了行为正确——未先看过失败的测试什么也证明不了。
- 典型表现：12 个 auth 测试全过而生产 auth 函数返回常量（Mnilax 事故）；持续绿的越权洞——endpoint 只断 200/401 从不断言 403（PR197 事故）；「如果你的新测试在写修复之前就通过——你没有发现一个 bug，你发现了一个坏测试」。
- 判据：写不出「业务逻辑变了就会挂」的测试 = 函数是错的；复现测试必须先红后绿。
- 来源：Mnilax、PR197、superpowers TDD（「没有失败的测试就没有生产代码」）。

**40. 弱化 / 篡改测试** [CCON Weakened test; GH 官方 review 第 5 步; HN]
- 定义：为让代码通过而放松断言、删除或跳过测试，而不是修复。
- 典型表现：实现与测试同 commit 改动、断言变松；Copilot 篡改测试让 edge case 通过（HN esalman 事故）；「测试被删除或跳过而不是被修复」是 AI 特有威胁（GitHub 官方 review 指南点名）。
- 检测：测试文件单独 diff；断言数量应「变多」而非「横移」；自己跑测试而不接受声明。
- 来源：continuumcode、GitHub copilot 教程、HN。

**41. 过度 mock** [SC test.over-mocking; SUP; MP]
- 定义：替身替换几乎全部协作者、断言只落在 mock 调用历史上——真实输出、解析和错误路径未被证明。
- 典型表现：`expect(mock).toHaveBeenCalledTimes(3)` 测的是 mock 配置不是被测代码；部分 mock 在下游读被省略字段时静默失败（测试过、集成坏）；按真实结构完整镜像 mock。
- 原则：mock 挣不到断言；在正确的层 mock（慢/外部操作），保持测试依赖的东西为真。
- 来源：smell-check、superpowers、mattpocock。

**42. 测试膨胀** [KP 失败模式 2; PR197]
- 典型表现：Claude 生成测试文件行数是源文件 3 倍，甚至自带自造的测试「框架」。
- 来源：Karpathy 2026-01 推文、PR197。

**43. 实现耦合测试** [MP Implementation-coupled; SUP]
- 定义：mock 内部协作者、测私有方法、经侧信道验证（查数据库而非用接口）——重构后测试挂但行为没变。
- 原则：测试住在公共 seam 上，验证行为而非实现细节；好的测试读起来像规格。
- 来源：mattpocock、superpowers。

**44. 经典测试坏味道组（继承自人类）** [SC test 规则 12 条]
- 一组收录：断言轮盘（多断言无结构，失败说不清）、急切测试（一测多行为）、条件测试逻辑（if/循环可能跳过断言）、神秘访客（隐藏外部依赖）、泛化 fixture（大世界只用一片）、被忽略测试（skip 无理由无期限）、昏睡测试（固定 sleep 而非条件等待）、顺序依赖测试、敏感相等（`str(obj)` 比对）、晦涩测试（`test1`/`works`）、非确定性 flaky（活时钟/未播种随机/真实网络）。
- 检测：skip 标记与硬等待可 grep；断言位点与 gate 节点可脚本数。
- 来源：smell-check rules-test（12 stable）。

## 九、安全类（AI 高发区 #4）

**45. 硬编码秘密与凭证暴露（含前端直连数据库）** [VBC no-hardcoded-secrets; VER CWE-798 13.4%; AS; VC]
- 典型表现：API key/token/密码进 config、seed data、测试 setup（AI 爱放示例凭据）；私钥/DB 凭证直接暴露在前端 JS bundle；全部请求从前端发往数据库、没有后端——等于把库公开（aislopfix 失败模式 #2）。
- 数据：硬编码凭证是 Veracode Top CWE 之一（13.4%）。
- 来源：vibecheck、Veracode、aislopfix、vibecoder。

**46. 注入与危险调用** [VBC 6 条; VER Top CWE; VC; CC]
- 典型表现：字符串拼接/f-string 拼 SQL；`eval()`/`exec()`/`new Function()`/`os.system()`/`subprocess(shell=True)`；`innerHTML`/`dangerouslySetInnerHTML`；生产 Flask `debug=True`。
- 数据（Veracode Top CWE）：XSS 33.5%、路径遍历 24.5%、OS 注入 20.1%、SQL 注入 18.1%。
- 成因：AI 明知参数化查询却不总用（vibecoder）；无显式 prompt 时复刻旧训练数据的遗留模式（CodeRabbit）。
- 来源：vibecheck、Veracode、vibecoder。

**47. 授权 / 数据作用域缺失（IDOR）** [AS 最普遍; VC 授权检查; Deng et al.; Lovable 事件]
- 定义：认证了用户但不查其对**具体资源**的权限；数据无行级作用域。
- 典型表现：换 URL 里的 id 就能取到别人的 order/profile——「所有项目都以同样方式建成这样」，原作者非技术背景时现代 LLM 依然会犯（aislopfix 失败模式 #1，最普遍）；RLS 策略存在但与应用逻辑不一致——Lovable 的 security scanner 只查 RLS 存在性不查正确性，制造虚假安全感。
- 数据：vibe-coded 应用审计 9,041 个应用 91% 含漏洞（Deng et al.）；Lovable 1,645 应用 170 个（~10.3%）任何人可读用户信息。
- 来源：aislopfix、vibecoder、Deng et al.、Lovable/Palmer 报告。

**48. 认证缺失** [VC 检查 4]
- 典型表现：新 API 路由先跑业务逻辑不查认证——「未认证调用会怎样」这个问题在 AI 代码里常常永远不会被提出来。
- 来源：vibecoder checklist。

**49. 错误信息泄漏** [VBC no-error-info-leak]
- 典型表现：`err.message`/`err.stack` 直接进 HTTP 响应。
- 来源：vibecheck。

**50. 幻觉依赖与供应链投毒（slopsquatting）** [Spracklen USENIX'25; Importing Phantoms; PackHallu; VBC]
- 定义：import 了 npm/PyPI 上不存在的包；攻击者抢注幻觉包名投毒；规则文件（AGENTS.md/cursorrules）被注入恶意提示诱导把合法依赖换成攻击者的包。
- 数据：商业模型幻觉率 ≥5.2%、开源 21.7%；205,474 个不重复幻觉包名；1/5 的 Python/JS 样本引用幻觉包（Veracode）；幻觉率与 HumanEval 分数负相关、代码质量与幻觉率前沿稀疏——「编码模型没有为安全代码优化」。
- 检测：新依赖对照 registry 存在性/白名单/lockfile；PreToolUse 拦截安装命令 + PostToolUse 扫 manifest diff。
- 来源：Spracklen et al.、Importing Phantoms（arXiv 2501.19012）、PackHallu（arXiv 2610.09264）、vibecheck。
- 关联：条目 57（幻觉 API 是正确性问题，本条是供应链问题）。

## 十、性能类

**51. N+1 / 循环内 I/O / 过度 I/O** [VC N+1; CR ~8x]
- 典型表现：循环内做数据库调用（「先循环再取数太好写了」——AI 稳定产出 N+1）；过多 I/O 操作。
- 数据：CodeRabbit——性能回归数量少但严重偏向 AI（过多 I/O 约 8 倍），AI 重清晰轻资源效率。
- 来源：vibecoder、CodeRabbit。

**52. 重复计算 / 缺缓存** [VC 检查 4]
- 典型表现：循环或高频函数内输入不变却重算昂贵操作（DB 查询/API 调用/复杂计算）；修复常是一行缓存，但要先看出模式。
- 来源：vibecoder。

**53. 缺失索引** [VC 检查 3]
- 典型表现：AI 引入按列过滤/排序的新查询时很少加索引；小数据集正常、负载下指数级劣化。
- 来源：vibecoder。

## 十一、AI 行为特有类（过程性 / 跨文件坏味道）

> 传统清单（Fowler/APSD/Clean Code）为人类代码设计；本类是 AI 失败模式专属——它们多数不落在单行代码上，而落在**过程与 diff 形状**上。

**54. 静默错误假设** [KP 失败模式 1; MN 规则 1; MP grilling]
- 定义：模型替你做错误假设并径直跑下去——不管理困惑、不求澄清、不指出不一致、不呈现 tradeoff、该顶回时不顶回。
- 典型表现：「导出用户数据」默默假设导出全部用户、文件位置、字段集合、CSV 列名。
- 对策映射：Think Before Coding / grilling（让 agent 就需求详尽提问）。
- 来源：Karpathy、Mnilax、mattpocock。

**55. 范围蔓延与正交伤害（scope creep / orthogonal damage）** [STS S; KP 失败模式 3; CCON; G]
- 定义：一个修复膨胀成不相关重构；任务外代码/注释被顺手改动。
- 典型表现：两文件任务动九个文件（看内容前先看文件清单——本身就是一条 finding）；修「空 email 崩溃」时顺手加 username 校验规则、改注释、重排格式；相邻代码「改进」、没坏的东西被重构。
- 判据：每一行改动都应能直接追溯到用户请求（Karpathy Surgical Changes）。
- 来源：stop-that-shit（SHIT 之 S）、Karpathy、continuumcode、Google。

**56. 静默删除护栏** [CCON Silent deletion]
- 定义：边界分支/守卫/护栏被悄悄删掉——「diff 读起来像简化、行为上是 bug」。
- 检测：先读删除行（最高产出、最常被跳过的检查）+ 被整个删除的文件。
- 来源：continuumcode。

**57. 幻觉 API / 过时 API / 幻觉 import** [CCON Invented API; VC 逻辑检查 1; VBC]
- 定义：调用一个「理应存在」却不存在的方法或包；或描述的是训练时的 API 而 API 已变。
- 定性：AI 逻辑 bug 最常见的单一来源（vibecoder——训练截止时间）；「不编译一眼可见」的只是少数，更多是编译、能跑、语义错。
- 检测：编译/运行（编译器常能抓）；外部 API 调用对照现行文档验证。
- 来源：continuumcode、vibecoder、vibecheck。

**58. 冲突平均** [MN 规则 7]
- 定义：代码库两种矛盾模式并存时，AI 写「同时满足两条的折中代码」——最差的代码。
- 典型事故：双错误处理器把错吞两遍。
- 对策：选其一（更新/更受测的），解释并标记另一待清理。
- 来源：Mnilax。

**59. 局部自洽、整体失序（缺设计意图面包屑）** [atmoio; MITX; QODO; HN krackers]
- 定义：每个改动单元孤立看良好、与 prompt 自洽，但对整体结构、邻接模式、全局架构「没有 respect」；AI 代码缺少人类开发者留下的「意图面包屑」（注释、命名约定、目录结构中的设计意图）。
- 典型表现：段落句法都对、整章在全书语境中不成立（atmoio 小说比喻）；文件循环 import、业务逻辑散落表示层、工具函数做不相关的事（MITRIX 典型病灶）；「AI 极擅长造零件，非常不擅长大局」（HN jrm4）。
- 成因：上下文窗口装不下非玩具项目（65% 重构场景 AI「错过相关上下文」——Qodo）；基准测试奖励短期正确性、不计长期 refactorability（HN krackers）。
- 来源：atmoio(HN)、MITRIX、Qodo、HN。

**60. 假完成 / 未验证宣称** [SUP; MN 规则 12; PR197 第五维; KP]
- 定义：以「should/probably/seems to」「tests pass」「this is now done」等意图性句子替代实际观察。
- 典型表现：未跑验证就表达满意；agent 报 success 而 VCS diff 无变更；宣称「构建成功」但只看了 linter。
- 判据（Gate Function 五步）：IDENTIFY 什么命令能证明 → RUN 新鲜完整执行 → READ 全输出+退出码 → VERIFY → THEN 宣称。跳过任何一步 = 撒谎，不是验证。
- 来源：superpowers、Mnilax、PR197、Karpathy（Goal-Driven Execution）。
- 注：与条目 36（代码级吞错）同根——一个在代码里、一个在汇报里。

**61. 指令遵循衰减（规则文件不可靠）** [GH #2544; MN; Anthropic steering; 社区审计]
- 定义：CLAUDE.md/AGENTS.md 等规则是概率性建议——长会话、compaction、规则冲突、token 压力下被静默忽略；追加指令对遵守率边际递减。
- 数据：社区审计 559 个公开规则文件——63% 内容不是指令，真规则中仅 ~35% 可机械 hook 化；396 个 CLAUDE.md 静态扫描约 3/4 挑不出毛病——「文件基本没问题，失败在运行时没有任何东西强制执行」；规则条数超限后合规率骤降（Mnilax：18 条时 76%→52%）。
- 推论（对 Skill 设计关键）：可执行规则下沉为 hooks/linter/CI（确定性，「A system prompt is a request. A hook is a guarantee.」）；判断类规则才留在提示层。
- 来源：gh-claudemd-rules-ignored（#2544 及审计评论）、Mnilax、Anthropic steering 博客。

**62. 看似合理（plausible）而非困惑（confused）** [CCON; HN zarzavat]
- 定义：AI 代码失败模式的元特性——错误包装在惯用命名与统一风格里，细看才知错；「错误只是更隐蔽：编译、能跑、但边界 case 错/有安全洞/埋技术债——review 负担一点没减轻」。
- 后果：人类评审直觉失灵（困惑信号缺失）；skim 过的 agent 产出就是没审过的产出。
- 来源：continuumcode、HN。

---

## 量化实证数据（每条带来源与方法学注记）

### A. 代码质量纵向（真实仓库大数据）

1. **GitClear 2025**（2.11 亿行变更，2020-01–2024-12，~72.9 万开发者；匿名私有仓库 + 25 个最大开源项目）：
   - 5 行以上重复代码块频率 2024 年增长 **8 倍**（同报告另有 4x 的趋势性口径；LeadDev 转述「重复率比两年前高 10 倍」——三者口径不同，引用须注明）。
   - copy/paste 行数历史首次超过 moved 行（占比 8.3%→12.3%）；「moved」（重构代理指标）占比从 2021 年 25% 跌至 2024 年底 <10%；报告标题即「Refactoring at 8% of Changed Lines」。
   - churn（新增后 3 个月内被更新/删除的代码）平均 4.1%，预计 2026 年翻倍；复制粘贴是 churn 的上游。
   - 方法学注记：时间跨度与真实仓库规模为其强度；但公司主营代码质量分析（间接商业动机）；原站抓取不完整（Cloudflare），部分数字来自二手转述。
2. **CIQ 内部对比**（2,200 万行级代码库，AI 辅助文件 vs 非 AI 文件）：重复度 8.5% vs 4.7%（**+81%**）；千行重复块 11.2 vs 5.2（**+115%**）；认知复杂度/圈复杂度比值上升；条件 +7%、循环 +4%；文件均 LOC 略降（「碎片化+平庸化」）。注记：单一企业内部数据、未见同行评审；机制解释（插值训练分布 + 请求间无记忆）合理。
3. **vibecheck 31 仓库扫描**（Cursor/Bolt/Lovable/Replit/v0 构建）：3,597 文件共 14,695 问题；46% 为深嵌套；Cursor 构建仓库平均 6.36 问题/文件。注记：**工具自家 README 营销数据**，规则集偏嵌套、校准语料仅 6 仓库——低置信度，仅作「AI 构建仓库的坏味道密度量级」参考。

### B. AI vs 人类 PR 对比

4. **CodeRabbit**（2025-12，470 个开源 GitHub PR：320 个 AI 署名 + 150 个人类；结构化 issue 分类法，率比统计）：
   - 总 issue 约 **1.7 倍**（每 PR 10.83 vs 6.45）；critical/major 发现 +1.4–1.7 倍；逻辑与正确性 **+75%**；可读性 **>3 倍**（全数据集最大差异）；错误处理缺口 **~2 倍**；安全最高 **2.74 倍**；过多 I/O 约 **8 倍**；并发与依赖正确性 ~2 倍；格式 **2.66 倍**；命名不一致 ~2 倍。
   - 关键定性：**没有任何 issue 类别是 AI 独有的**——人类与 AI 犯同类错误，AI 更频繁、更大规模。
   - 方法学注记：厂商报告（卖 AI 评审）；作者身份靠 AI 共同署名信号推断、无法确认纯人类组纯净；两组差异统计显著，完整方法学公开于报告末。
5. **GitHub 官方 Copilot 受控研究**（2024，宣称 200 人随机对照，实为 243 人 121/121、104/98 有效提交）：
   - 头条：Copilot 组 56% 更可能通过全部测试；可读性 +3.62%、可靠性 +2.94%、可维护性 +2.47%、简洁性 +4.16%；PR 接受 +5%。
   - **jadarma 方法学批判（引用此研究必须携带）**：①任务偏置——CRUD API 端点是 code-lab 级、认知无挑战的工作，由此推「AI 总体改进代码」不诚实；②**「code error」定义排除功能性错误**（只算命名/行长/重复/分支等可读性问题）——「那不是 error，那是 linter 警告」；③样本数对不上（百分比加总≠100，「多出的 40 个对照者去哪了」）；④参与者互评有风格偏置、主观度量黑箱；⑤对照组可能是被剥夺日常工具的戒断效应；⑥其自身数据（Copilot 组 commit 更多更小、变更行数更高、churn 上升）与 GitClear 互证反方向——moved 减少=更少重构、copy-paste 增加=更多重复。
   - 裁决：数字可引但必须带上述警示；与 GitClear 冲突时采信 GitClear。

### C. 安全

6. **Veracode 2025 GenAI Code Security Report**（100+ LLM × 15 语言，48,000+ 生成样本，SAST 按 CWE 分类）：
   - **45%** 的 AI 生成代码样本未通过至少一项安全测试；结构化 review 方法后可降到 **10% 以下**。
   - 模型差异约 4 倍：Claude 3.5 Sonnet 失败率最低 19%，Meta Code Llama 2 7B 最高 78.4%；「更大模型 ≠ 更安全」；代码专用微调反而更差（41.4% vs 基座 39.9%——过拟合旧模式）。
   - 语言：PHP 56.9% / C 52.4% / Java 47.7% vs JavaScript 34.1% / Python 31.7%（训练语料越老的语言风险越高）。
   - Top CWE：XSS 33.5%、路径遍历 24.5%、OS 注入 20.1%、SQL 注入 18.1%、硬编码凭证 13.4%。
   - 提示词效应：具体、设计良好的安全提示把失败率 31.5%→24.3%（-7pp）——prompt 是低成本质量杠杆；约 1/5 的 Python/JS 样本引用幻觉包。
   - 方法学注记：安全厂商（卖扫描），但样本量与 CWE 分解方法学公开，「45%→<10%」是其结构化 review 主张的核心量化依据。
7. **Tihanyi et al.**（FormAI-v2，331,000 个可编译 C 程序，ESBMC 形式化验证标注）：**≥62.07%** 生成程序有漏洞；FormAI 数据集（112k 个 GPT-3.5 程序）51.24%。注记：学术、形式化验证降假阳；仅 C 语言、零样本中性提示、2024-04 模型代。
8. **Deng, Fan, Meng**（arXiv 2606.23130，审计 9,041 个 vibe-coded 应用 + 200 个部署）：**91%** 含漏洞；归纳 8 种反复出现的 agent 失效模式。
9. **Lovable 事件**（2025-05，Matt Palmer 报告）：1,645 个 Lovable 生成应用中 **170 个（~10.3%）**「任何人可访问用户个人信息」；其 security scanner 只查 RLS 策略存在性、不查正确性。注记：单人测量、报告者为 Replit 员工（竞品）——数字被广泛引用但来源有利益背景，量级可信、精确值慎引。

### D. 幻觉与供应链

10. **Spracklen et al.**（USENIX Security 2025）：16 个流行 LLM × 2 个提示集，576,000 个代码样本；商业模型幻觉包率 **≥5.2%**、开源 **21.7%**；205,474 个不重复幻觉包名；定性为「持续且系统性的现象」。
11. **Importing Phantoms**（arXiv 2501.19012）：幻觉率取决于模型、语言、模型大小与任务措辞；与 HumanEval 分数负相关（可作风险启发式）；代码质量与幻觉率的 Pareto 前沿稀疏——「编码模型没有被优化来生成安全代码」。
12. **PackHallu**（arXiv 2610.09264）：规则文件（AGENTS.md/.cursorrules）是未充分检验的 prompt injection 攻击面；进化优化出的注入跨模型/跨框架高可迁移——从网上复制的规则文件应视为不可信输入。

### E. 生产力与感知落差

13. **METR RCT**（2025-07，16 名资深开源维护者、246 个真实维护任务、随机分配 AI 开/关；Cursor Pro + Claude 3.5/3.7）：
    - AI 使完成时间**增加 19%**；开发者事前预测提速 24%、事后仍自认提速 20%——**感知与实际约 40% 落差是其最稳健结论**。
    - 屏幕录制分析：主动编码/调试/阅读时间确实减少，但被「审查 AI 输出、写 prompt、等待生成、idle」淹没；未修改即接受的 AI 代码 <44%；review 占 AI 组 9% 时间。
    - 方法学注记：随机对照+屏幕录制，内部效度高；**外推限制**——平均 10 年库龄、>100 万行、隐性知识密集的仓库，Claude 3.5/3.7 时代工具（无 agent），作者自承「不适用于更简单的现实场景」；HN 批评者要求用新代模型重做。
14. **Stack Overflow 2025**（各题约 3.3 万受访者）：84% 使用/计划使用 AI（上年 76%）；**46% 主动不信任** AI 输出准确性 vs 33% 信任（仅 3% 高度信任）；10 年+ 经验者最不信任；**66% 最大挫败 = 「几乎对、但差一点」**；45% 认为调试 AI 代码更耗时；72%+5% 不做 vibe coding。
15. **Qodo State of AI Code Quality 2025**（609 名开发者，自我报告）：
    - 上下文缺失：65% 用 AI 重构者称助手「错过相关上下文」（按任务：重构 65% > 样板 64% > 编写/测试 ~60% > 评审 58%）；上下文类改进诉求 ~30% 超过「减少幻觉」24%。
    - 幻觉量级：25% 开发者估计每 5 条建议 1 条含事实错误（~20%）；四象限中「高幻觉+低信心」占 **76.4%**（红区主导）。
    - 评审杠杆：有 AI 评审在环的质量改善率 81% vs 无 55%；即便无提速，AI 评审团队质量收益也翻倍（36% vs 17%）。
    - 渗透率：65% 开发者称每次提交 ≥1/4 由 AI 生成或塑形，15% 称 >80%。
    - 方法学注记：厂商报告（卖 AI 测试/评审）；全部自我报告，与 CodeRabbit 实测数据构成「感知 vs 实测」张力（见待裁决 #5）。
16. **DORA 2024/2025**：AI 采用显著提升个人生产力、心流与满意度，但**降低交付稳定性与吞吐**（LeadDev 转引：AI 使用增 25% → 交付稳定性降 7.2%）；2025 定性：AI 是「放大器」，回报取决于底层组织系统。注记：大样本调查（n≈39,000 量级年度调查），因果为统计关联。
17. **Harness State of Software Delivery 2025**（转引）：与感知的生产力收益相反，多数开发者花**更多**时间调试 AI 生成代码、更多时间解决安全漏洞。注记：二手转引，仅作方向性佐证。

### F. 规则 / 工具遵循与治理（对 Skill 设计直接相关）

18. **Mnilax 自称数据**（50 个代表性任务 × 30 代码库 × 6 周）：无规则失误率 ~41% → Karpathy 4 规则 11% → 12 规则 3%；合规率 4→12 规则几乎不变（78%→76%）；**规则超过 12 条时合规率 76%→52%**（18 条实测）；「Be careful/think hard」类不可测试指令使合规率跌至 ~30%。注记：**单人 X 长文、无公开方法学**——低置信度；但「规则条数上限/注意力预算」结论与 Anthropic 官方（CLAUDE.md advisory、~80% 遵循率、>200 行急剧下降、边际递减）方向一致。
19. **社区审计数据**（gh #2544 评论区）：559 个公开规则文件中 63% 内容不是指令；8,101 条真规则中 ~35% 可 matcher/hook 执行、65% 是判断类；396 个 CLAUDE.md 静态扫描约 3/4 无可挑——「失败不在文件而在运行时无强制」。注记：社区研究者自制工具，方法学在 issue 内公开，样本为公开仓库非随机。
20. **Cross-Model LLM Code Review**（arXiv 2607.21656，116 道 LiveCodeBench 难题）：Claude 审 Codex 草稿 71.6%→**89.7%**（p_BH=.001）；**Codex 审 Claude 91.4%→82.8%（不升反降，p=.046）**；同模型自评对弱草稿有效（84.5%）、对强草稿无效。结论：交叉评审**不对称**——「用 Claude 审 Codex，别反过来」；社区工具 neal 的默认方向恰是负收益方向。注记：实验室题目、reviewer 只看题面+草稿不跑测试；单研究待复现。
21. **arXiv 2511.15817（PSC 因果分析）**：提示词设计与模型架构决定生成代码的味道倾向（Propensity Smelly Score 作结构质量信号）——结构质量劣化可测、可归因、可由提示词设计压低。

### G. 口径不明的高传播数字（降级为背景叙事，不作证据）

22. Yegge「chat 5x / agents 25x 生产力倍率」「agent fleets 2026」：单人博文推演，无方法学。
23. Anthropic CEO「Anthropic 70–90% 代码由 Claude 写」：访谈口径不明——HN gowld 质疑其按自动补全字符数计（多数相当于十年前的 tab 补全），与「agent 写大部分代码」是不同断言。
24. YC W25「25% 初创公司 95% 代码 AI 生成」：合伙人访谈口径（不含 import 库），非审计数据；Friedman 强调这些创始人全部技术过硬。
25. **Koren et al.《Vibe Coding Kills Open Source》**：经济学均衡模型外推而非直接测量；作者对媒体自认证据「大多是间接的（circumstantial）」。仅作生态背景，不入坏味道证据链。

---

## 已裁决矛盾（本域内已处理）

1. **「GitHub 官方研究：AI 代码质量更好」 vs 「GitClear/CodeRabbit/CIQ：更差」**——裁决：采信后者。GitHub 研究任务偏置（CRUD 端点）+「code error」定义排除功能性错误 + 样本数疑点（jadarma），使其测的接近「lint 通过率」而非质量；其自身副产物数据（churn 升、commit 更小）反与 GitClear 互证。引用 GitHub 数字时**强制附带方法学警示**（已写入量化节 B-5）。
2. **「AI 有没有独有坏味道」**——裁决：采信放大器论（CodeRabbit「无独有类型」+ CIQ「向平均水平回归」+ DORA「放大器」）。传统结构类坏味道（一~十类）AI 与人类同类、只是频率更高；AI **真正特有**的是幻觉类与过程类（幻觉 API/包、静默假设、局部自洽整体失序、假完成、指令遵循衰减），已单独归入第十一类。
3. **「烂代码也能做爆款（Claude Code 泄漏源码争论）」 vs 「代码质量决定长期演进」**——裁决：按时间尺度拆分（HN pron 框架）。短期产品成功不否定长期可维护性成本（tristramb：「烂代码的问题不是不能用，是变得无法修改」）；Skill 定位于长期可维护代码，一次性原型按 Karpathy/Willison 的边界豁免（低风险、无第三方依赖者）。
4. **GitClear 内部数字口径不一（4x/8x/10x）**——裁决：以「2024 年 5+ 行重复块频率增长 8 倍」为精确口径；4x 为趋势粗口径、10x 为 LeadDev 的「比两年前重复率」转述。引用时注明口径（已写入量化节 A-1）。

## 待裁决矛盾（需主 agent 拍板）

1. **自称/营销数据的取舍**：vibecheck 31 仓库扫描、Mnilax 41%→3%、Yegge 倍率、Anthropic 90%、YC 95% 均无公开方法学。本文件的处理：Yegge/Anthropic/YC 降级为背景叙事（G 组），vibecheck/Mnilax 标「低置信」收录（A-3、F-18）。主 agent 可决定更激进（全删）或更宽松（升为证据）。
2. **厂商报告（GitClear/CodeRabbit/Veracode/Qodo 均有商业动机）是否统一降权**：本文件逐条注记了利益背景，未做统一权重。Skill 引用时是否需要固定的「利益相关声明」措辞规范？
3. **METR「慢 19%」 vs 微软系等「快 26%」类正收益研究**：本文件按适用域并存（METR：资深开发者+百万行大库+Claude 3.5/3.7 无 agent 工具；正收益研究：入门/标准化任务）。Skill 立场是否规定：引用 METR 必须同时注明工具代际，否则有误导性？
4. **GitHub 官方研究的最终地位**：本文件裁决「带 jadarma 警示保留」（量化节 B-5）。若主 agent 认为其方法学缺陷致命，可改为彻底弃用——影响该条及其交叉引用。
5. **感知 vs 实测的基调**：Qodo「59% 开发者说 AI 提升了代码质量、78% 报告生产力收益」与 CodeRabbit 实测「AI PR issue 1.7 倍」、SO「66% 最大挫败=almost right」并存。本文件倾向实测优先（自我报告有幸存者偏差与利益脱敏问题），但 Skill 整体基调（乐观/中性/悲观）需主 agent 定，它决定引用哪些数据放在开头。
