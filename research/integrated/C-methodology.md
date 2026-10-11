# 知识域 C 整合：代码质量方法论（review / 重构 / 简化 / 验证）

> 阶段3 整合产物。输入：`knowledge/03-methodology.md`、`01-repos-deep.md`、`05-history-ecosystem-followup.md`（跨模型实验、Veracode、CIQ、Mnilax）、`02-community-discussions.md`（review 实践讨论）。
> 整合规则：同原则跨体系合并；重构手法按「AI 代码场景高频」重组；矛盾就地裁决或列入文末「待裁决矛盾」；已剔除与 AI 代码场景无关的经典细节（UML、需求文档管理、团队组织类 tips、Clean Architecture 实施细节归知识域 B 边界、风格指南逐条清单等）与各来源间重复的清单。
> 来源缩写（全文使用）：
> [Google]=Google eng-practices review 三篇｜[APSD]=Ousterhout 两篇摘要｜[CleanCode]=Clean Code 两版 cheatsheet｜[PragProg]=100 tips｜[Fowler]=Fowler 重构系列（定义/workflows/opportunistic/strangler/BBA/yagni/malapropism）｜[Fowler目录]=refactoring.com 目录+refactoring.guru｜[smell-check]=pragmatic-clean-code-reviewer 规则注册表｜[mitrix]=AI 代码重构方法论｜[vibecoder]=AI review checklist（Veracode 45%→10% 出处）｜[continuumcode]=agent 代码审查七步｜[gh-copilot]=GitHub 官方 review AI 代码教程｜[superpowers]=obra/superpowers skills｜[code-review插件]=claude-plugins code-review 流水线｜[code-simplifier]=claude-plugins 简化 agent｜[mattpocock]=mattpocock_skills｜[karpathy4]=andrej-karpathy-skills 四原则｜[STS]=stop-that-shit｜[cross-model]=arXiv:2607.21656 跨模型 review 实验｜[Veracode]=2025 GenAI Code Security Report｜[CodeRabbit]=AI vs Human 代码报告｜[CIQ]=The Imitation Game（认知复杂度/重复数据）｜[GitClear]=2.11 亿行纵向分析｜[Mnilax]=12 规则推文｜[characterization]=characterization test 词条｜[code-modernization]=baseline_diff/proof_pack 脚本｜[社区]=02 文件 HN/GH 讨论（括注人名）

---

## 一、Review 母表（按检查维度组织，共 48 条）

合并来源：[Google] looking-for + [APSD] Red Flags + [vibecoder] AI 四大类 checklist + [continuumcode] 七步法与失败模式表 + [smell-check] 20 代码规则/12 测试规则 + [gh-copilot] + [code-review插件] 误报清单与置信分 + [社区] review 实践。移除各来源重复项（如命名/注释规则在四套体系中重复出现，合并为单条多来源）。

### 维度 0：审查流程元规则（先于看代码）

- **R0.1 结构化顺序审查，按 安全 > 逻辑 > 性能 > 质量排列**：部署出去的漏洞比延迟的功能更糟；正确性是其他一切的门。[vibecoder]
- **R0.2 先看文件清单再看内容**（`git diff --stat`）：非预期文件即 scope creep，是未审查变更的藏身处；两文件任务动了九个文件本身就是 finding，不必读一行。[continuumcode][Mnilax 规则 8 同源]
- **R0.3 先读删除行**：agent 静默删护栏/边界分支产生的 diff「读起来像简化、行为上是 bug」——最高产出、最常被跳过的检查。[continuumcode]（社区事故印证：Replit agent 明确指示不要动仍删生产数据库 [社区/SaaStr via 05]）
- **R0.4 测试文件单独 diff**：实现与测试同 commit 改动正常，断言变松不正常；单独读让放松的断言无法藏在合法实现改动旁边。[continuumcode]（事故：Copilot 篡改测试让 edge case 通过 [社区/esalman]；GitHub 官方同列「测试被删/跳过而非修复」[gh-copilot]）
- **R0.5 自己跑测试，不接受「all tests pass」声明**：声明与代码出自同一生成过程；并检查断言数量是变多而非横移。[continuumcode][superpowers/verification-before-completion]
- **R0.6 AI 代码 review 是「不同」不是「更短」**：AI 失败模式更隐蔽（plausible but wrong、uniformly confident 无困惑信号），安全与逻辑检查每行所需时间不少于人写代码。[vibecoder][continuumcode]（社区：「编译、能跑、但边界错/有安全洞的 truthy 代码比明显烂代码更耗心神」[社区/zarzavat]）
- **R0.7 风格审查价值最低却最吸注意力**：推给 linter，注意力花在删除行、测试 diff、错误路径。[continuumcode]（「写得极好的 PR 消息+干净代码但不做对的事——过去这些是质量 proxy；review 应聚焦行为而非文笔」[社区/clbrmbr]）
- **R0.8 置信过滤与反误报**：每条 finding 打置信分（0–100），低于 80 不报；机械可查的（import/类型/格式，CI 会跑的）、已存在的问题、学究式挑刺一律不报——误报流是 review 工具变成噪音的方式。[code-review插件][Google 的 Nit 标签同旨]
- **R0.9 证据分级**：每条 finding 标注 mechanical（工具输出）/ semantic（LLM/人判断）/ estimate（降级估算）；工具缺失时绝不伪造机械数字，宁缺毋假。[smell-check]
- **R0.10 发现自己在 skim 就停**：skim 过的 agent 产出就是没人读过的代码；省下的时间是幻觉。[continuumcode]（review 疲劳机制：多数代码是对的，最终 checkout，问题藏在更大的架构模式里 [社区/jascha_eng]）
- **R0.11 治本手段是让小 diff 成为默认产出**：prompt 带约束子句（「不改公共签名、不加依赖」）、按逻辑边界 commit、大改动先 plan、一个 session 一个 worktree、机器 reviewer 先跑——review 纪律会在压力下衰减，结构性便宜胜过更多纪律。[continuumcode][社区/weeksie stacked PR 对 PR 尺寸形成向下压力]
- **R0.12 人机分工**：机器擅长穷举式局部检查（null/边界/被删 guard/放松断言）；「这是我想要的吗」「这方案对吗」「契合系统吗」机器 Cannot know——让机器干 tedium，人管意图。[continuumcode]
- **R0.13 结构化 review 的量化收益**：AI 代码安全缺陷率 45% → 结构化 review 后 <10%。[Veracode][vibecoder]

### 维度 1：意图与范围

- **R1.1 做的是对的问题吗**：CL 是否对用户和未来开发者有益、属于这个代码库还是该进库（library）、现在是不是加它的时机。[Google/Design+Functionality][gh-copilot 第2步]
- **R1.2 实现的是 prompt 的字面还是你的意图**：对定价/权限/状态迁移等关键逻辑，把代码对照原始需求逐字读；AI 优化「看起来正确」而非「确实正确」。[vibecoder][continuumcode]
- **R1.3 spec 的沉默不是许可**：spec 说软件必须做什么，不枚举每个输入；spec 沉默的行为按正常使用者的合理期待评判。[superpowers/code-reviewer]
- **R1.4 抽查 agent 解释中的一条事实性 claim**：错了则其余一切更仔细读——自信的错误解释与自信的错误代码同源；「为什么选这个方案」答得含糊通常意味着含糊的代码。[continuumcode]
- **R1.5 每一行改动都应能追溯到用户的请求**：顺手「改进」相邻代码/注释/格式是正交伤害。[karpathy4/原则3][Mnilax 规则 8]

### 维度 2：安全（AI 失败第一大类）

- **R2.1 硬编码密钥/凭据**：diff 里搜 API key、token、password、connection string；AI 爱把示例凭据放进 config/seed/测试 setup。Top CWE：硬编码凭证 13.4%。[vibecoder][Veracode]
- **R2.2 注入**：凡用户输入拼 SQL/NoSQL/ORM 的都查参数化（「传个单引号会怎样」）；SQL 注入 18.1%、OS 注入 20.1%、路径遍历 24.5%。[vibecoder][Veracode]
- **R2.3 XSS/转义**：凡用户输入渲染到 DOM/模板处查转义；dangerouslySetInnerHTML 与模板字符串同样危险。[vibecoder]（XSS 是 AI 代码第一大 CWE，33.5% [Veracode]）
- **R2.4 认证先于业务逻辑**：每个新端点确认先查认证再跑逻辑；「未认证调用会怎样」这个问题在 AI 代码里永远不会被自己提出。[vibecoder]
- **R2.5 授权而不只认证**：AI 常认证了用户却忘查该用户是否有权访问该具体资源。[vibecoder]（修复实践数据：无数据作用域/IDOR 是 AI slop 修复商最普遍的问题，「换个 URL 里的 id 就能取到别人的 order」[社区/aislopfix]；「用户 A 摸到用户 B 的数据」是典型 AI bug [vibecoder]）
- **R2.6 架构级暴露**：前端直连数据库、凭证暴露在前端 bundle、RLS 策略只查存在不查正确。[社区/aislopfix][05/Lovable 事件]
- **R2.7 幻觉依赖与 slopsquatting**：新包确认真实存在、被积极维护、许可证兼容；约 1/5 Python/JS 样本引用幻觉包。[gh-copilot][Veracode][arXiv:2406.10279]

### 维度 3：逻辑正确性

- **R3.1 外部 API 调用对照现行文档验证**：AI 描述的是训练截止时的 API——AI 逻辑 bug 最常见的单一来源；同理查「发明的 API」（调用理应存在却不存在的方法，跑起来编译器常能抓）。[vibecoder][continuumcode]
- **R3.2 错误处理完备性**：try-catch 处理预期类型、静默吞掉其他一切；后台任务「捕获即忽略」= 无声停止；计费/支付路径吞错最致命（支付失败被当成功 → 真金白银亏损）。[vibecoder][社区/aislopfix]（CodeRabbit：错误处理缺口近 2 倍 [CodeRabbit]）
- **R3.3 async 竞态**：多个并发请求更新同一资源、无冲突解决的乐观 UI、无事务的 DB 写——「两个用户同时做这件事会怎样」。[vibecoder][Google/并发审查]
- **R3.4 数据流逐步验证**：追踪输入路径每次转换的 null/undefined 处理与类型匹配；TypeScript 不够——AI 会用 cast 绕过编译器而不保证底层数据真的匹配。[vibecoder]
- **R3.5 专查错误路径**：被调用方失败时错误被吞、被包装、被记录还是被返回；貌似合理的变更最常在这里偏离约定。[continuumcode][Google]
- **R3.6 边界与用户可见行为**：像用户一样思考；UI 变更光读代码难判影响，要 demo 或打补丁验证。[Google/Functionality]

### 维度 4：测试有效性（AI 最易作弊处）

- **R4.1 测试正确、合理、有用吗：代码坏了测试真的会失败吗**；会产生误报吗；断言简单有用吗。[Google/Tests 四问]
- **R4.2 无断言/同义反复测试**：期望值必须来自独立事实源（字面量、手算 fixture、spec），被测代码算出的期望值怎么都过；测 mock 而非真代码的断言什么也没说。[superpowers/writing-good-tests][mattpocock/tdd 反模式 Tautological][smell-check/test.assertion-free-test]
- **R4.3 禁止 change detector**：只有有意决策（常量值、私有结构、精确措辞）能让测试失败的，在重设计时乱叫、bug 时沉睡——测依赖该决策的行为。[superpowers][mattpocock「通过公共接口验证行为而非实现细节」]
- **R4.4 「tests pass」≠ 有意义的测试**：12 个全过的 auth 测试，生产 auth 却是坏的（函数返回常量）；写不出「业务逻辑变了就会挂」的测试 = 函数是错的。[Mnilax 规则 9][社区/orwin 同类事故：无用的 Claude 测试套件通过了团队 review]
- **R4.5 测试中的坏味道**：断言轮盘（多断言无结构）、条件测试逻辑（可能跳过检查的分支）、被忽略测试（skip 无理由无期限）、sleep 硬等待、顺序依赖、敏感相等（str/repr 全量比对）、晦涩命名。[smell-check/rules-test 12 条压缩]
- **R4.6 mock 原则**：mock 挣不到断言；只在慢/外部边缘替换；完整镜像真实数据结构（部分 mock 在下游读省略字段时静默失败）；断言参数/次数/顺序当且仅当它们是契约。[superpowers][mattpocock「预先协商 seam，未确认的 seam 上一个测试都不写」]

### 维度 5：复杂度与设计健康

- **R5.1 比应有的更复杂吗（每一层：行/函数/类）**：「太复杂」= 读者无法快速理解，或调用者改它时很可能引 bug。[Google/Complexity][CleanCode/Needless Complexity]
- **R5.2 能否删掉（过度工程专用问句）**：比需要的更通用、或加了现在不需要的功能；只解决「现在就知道要解决」的问题，未来问题等它到来。[Google/Over-engineering]（≈APSD shallow module：接口复杂度与功能不相称 [APSD]；≈YAGNI presumptive feature [Fowler/yagni]；≈Karpathy「写了 200 行而 50 行够——重写」[karpathy4]；四体系同旨）
- **R5.3 重复：区分「同一知识」与「偶然相似」**：两处编码同一业务规则（改一处不改其它就是错）必须合并为单一权威表示；必须分叉的偶然相似应保持分离——相似形状≠重复。[smell-check/duplicated-knowledge][PragProg/Tip15 DRY=知识单一权威表示]（AI 特化证据：AI 文件重复度 +81%、千行重复块 +115% [CIQ]；重复率涨 10 倍 [GitClear]——重复是 AI 代码第一病灶）
- **R5.4 错过复用**：repo 已有合适 helper 又就近复制一份——grep 它本该调用的函数名；多文件 agent 编辑常见。[continuumcode/Duplicated instead of reused][smell-check/missed-reuse]
- **R5.5 信息泄漏与时序分解**：同一设计决策散布多模块（改一个决策要改多处）；按执行顺序而非知识组织模块是 AI 代码典型病灶。[APSD/Red Flags][mitrix]
- **R5.6 直通方法/中间人**：几乎只转发调用的层是浅模块信号；每个元素消除的复杂度必须多于它创造的。[APSD][Google/Design]
- **R5.7 一致性检查（change amplification 方向）**：一个概念变更被迫散落多文件改（shotgun surgery）vs 一个模块因许多不相关理由被改（divergent change）。[smell-check][Fowler目录/smells Change Preventers]
- **R5.8 系统级语境**：这个 CL 在改善系统代码健康还是让它更复杂、更少测试？多数系统靠许多小变更累积变复杂，连新变更里的小复杂度都要阻止。[Google/Context]

### 维度 6：命名、注释与一致性

- **R6.1 命名对照实际行为**：AI 的名字「泛泛地合理」，validateUser 实际查支付状态会困惑读者多年；名字含糊、起不出简单名字=设计不干净。[vibecoder][APSD/Vague Name+Hard to pick name][Google/Naming]
- **R6.2 注释对照实际行为**：AI 无条件自信地生成注释——「返回用户全名」挂在返回 ID 的函数上比没有注释更糟。[vibecoder]（社区：几乎不让未编辑的 LLM 注释过审 [社区/gabriela_c]；LLM 注释最大价值是气得人重写正确、防未来 agent 被误导 [社区/jazzypants]）
- **R6.3 注释解释 why 而非 what**：复述代码的注释是坏注释；多数注释用于代码本身无法承载的信息（决策背后的推理）；正则/复杂算法例外。[Google][APSD/Red Flag: Comment that repeats code][CleanCode]
- **R6.4 与既有模式一致**：用自定义 error 类的库不该出现新代码抛裸 Error；把 diff 放在周围代码语境里读；匹配既有风格即使你会用别的写法。[vibecoder][karpathy4/原则3][Mnilax 规则 11][Google/Consistency]
- **R6.5 代码应 obvious**：读者一遍短读说不清「这测试失败意味着什么坏了」/「这段做什么」就是 finding；你的代码只有对别人 obvious 才算 obvious。[APSD/Nonobvious code][smell-check/test.obscure-test]
- **R6.6 术语一致（共享语言）**：领域术语唯一来源（GLOSSARY），命名与之一致——agent 思考 token 更少、命名漂移更少。[mattpocock/domain-modeling][PragProg/Tip80]

### 维度 7：性能与资源

- **R7.1 N+1 查询**：循环内 DB 调用；AI 稳定产出 N+1（先循环再取数太好写了）。[vibecoder]
- **R7.2 新依赖必要性与体积**：内置方法够用时导入完整工具库（训练数据里出现过）。[vibecoder][CodeRabbit 对策5]
- **R7.3 不必要重复计算**：循环/高频函数内昂贵操作且输入不变——先看出模式，修复常是一行缓存。[vibecoder]（CodeRabbit：过多 I/O 约 8 倍，AI 重清晰轻资源效率 [CodeRabbit]）
- **R7.4 新查询缺索引**：AI 引入按列过滤/排序的查询时很少加索引。[vibecoder]

### 维度 8：卫生

- **R8.1 死代码**：被 import 但从未调用的函数与类型、注释掉的代码块、无用 import——生成不完整的残留；删（VCS 保留历史），不注释掉。[vibecoder][smell-check/dead-code][CleanCode]
- **R8.2 文档同步**：改了构建/交互/发布方式查文档是否更新；删代码查文档是否该删。[Google/Documentation]
- **R8.3 全局可变状态与魔法值**：跨 feature 共享可写模块状态让远处代码互相干扰；裸字面量携带领域含义（超时/限额/状态）。[smell-check/global-data+magic-values][PragProg/Tip47]

执行策略：安全+逻辑每次必跑；性能+质量在触碰数据存储、外部 API、高流量路径时加跑；十几分钟的结构化 review 能抓住未检 AI 代码库到达生产的大部分问题。[vibecoder] 复杂度趋势可作为可测门禁：认知复杂度预算、重复超阈值强制抽公共库。[CIQ 五条缓解]

---

## 二、重构纪律

### 2.1 定义与红线

- **重构 = 不改变可观察行为的前提下重组内部结构**（名词/动词双定义）；操作性判据：**做重构时系统每次坏掉不超过几分钟**——「重构弄坏了两三天」做的不是重构，是 restructuring。[Fowler/DefinitionOfRefactoring+Malapropism]
- **没测试别重构，那是 guessing 不是 refactoring**；只在测试全绿时重构。[mitrix][Fowler/Two Hats]
- **两顶帽子纪律**：重构帽（行为保持小步）与加功能帽随时可换但一次只戴一顶；重构期间绝不加功能——「顺手加个 X」把重构拖成数月项目。[Fowler/Two Hats][mitrix/常见错误2]
- **几乎永远不该从头重写**：重写丢掉全部能跑的逻辑、边角处理和集成成果；只有架构与目标根本不兼容时才重写。[mitrix]
- **AI 代码重构特有前提：先逆向工程出「愿景」**：AI 代码没有意图面包屑（注释/命名约定/目录结构），重构流程必须包含 discovery——项目地图（入口/路由/数据流/认证路径/集成点，写进一个 markdown 反复引用）+ 依赖图（循环 import、业务逻辑散落表示层）；「我们不知道认证怎么工作」本身就是一条 finding，应影响优先级。[mitrix]
- **让 AI 帮忙重构 AI 代码的范围边界**：范围明确的任务（重命名、抽函数、加类型、写测试）可以；架构决策和整模块重组不行——AI 只优化眼前任务。[mitrix]
- **重构中发现安全问题（硬编码密钥、注入、缺校验）→ 立即停下先修**，优先级高于一切结构改进。[mitrix]

### 2.2 测试保护网（重构的前置投资）

- **先补测试再重构（被最多团队跳过的最重要一步）**：先给 happy path 写集成测试（聚焦主用户流程：注册、核心操作、持久化），给每个 API 端点加 contract 测试（常见输入下状态码+响应形状）；暂时跳过单测——AI 代码太缠绕时写不出有意义单测，重构出干净接口后自然出现；关键路径覆盖 60–70% 即可安全重构，不为即将重构掉的代码花几周写测试。[mitrix]
- **以现有行为为 spec**：跑应用、操作功能、写验证「当前行为」的测试——不是测行为对不对，是测别把它改掉。[mitrix][characterization]
- **特征测试（characterization test / Golden Master）**：观察输入-输出对写成断言（观察到 f(3.14)==42 就把它写成测试）；与传统断言相反，它检查「没有任何属性被改变」（黑名单）而非「个别属性取特定值」（白名单）；属于 historical oracle；可自动生成（大量相关/随机输入执行既有代码、记录输出）；对 PDF/XML/图片等复杂结果类型尤其合理；限制：依赖可重复性（易变值须遮蔽）、不蕴含结果正确——本质是 change detector，变化是否符合预期由人判断。[characterization]（superpowers 界定为「窄 characterization 测试」用于锁定上游行为假设 [superpowers/writing-good-tests]；smell-check 允许「标注为 characterization 的遗留行为捕获测试」豁免晦涩命名 [smell-check]）
- **安全网成色自检**：故意制造一个错误看测试能否抓住。[Fowler/opportunistic]

### 2.3 小步与工作流

- **机会式重构为主、计划式为辅**：看到不合格代码当场顺手修（营地规则：让代码比发现时更好）；触发时机——预备性（加功能前先把既有代码改成「现在已知是对的形状」，常使整体更快）、去重、收尾前、路过时（记下来当天回来）；计划式重构占大头是「其他工作流做得不够」的坏味道。[Fowler/Opportunistic+Workflows]
- **理解性重构**：每次被迫搞懂一段代码，就把这份理解移入代码，让后人不必在脑中重建。[Fowler/Workflows/Ward Cunningham]
- **小而可验证的 PR**：每 PR 只做一类改动（rename/extract/move/restructure）、可独立发布、过全部已有测试、30 分钟内可审完。[mitrix]（社区同旨：堆叠 PR 解开 validation/review 瓶颈并对 PR 尺寸形成向下压力 [社区/weeksie]）
- **分阶段推进（8 周参考模型）**：Phase1 Cleanup（删死代码、修明显 bug、统一命名、硬编码改配置——低风险高价值不改行为）→ Phase2 Extract（从 UI 抽业务逻辑、查询抽 repository、共享工具抽模块——架构成形，每次抽取一个 PR）→ Phase3 Restructure（文件结构对齐模块边界、合并重复、统一模式、补类型——最显眼但应最轻松）→ Phase4 Harden（全面测试、输入校验、日志、监控、架构文档）。每阶段后跑全量测试、staging、手动走关键流、监控 48–72 小时；发现问题先修再进，绝不把变更叠在坏变更上。[mitrix]
- **重构 PR checklist（10 条）**：新旧测试全过；无行为变化（除非有意且已记录）；死代码已删；命名清晰一致；错误处理存在且有意义；无「应做成配置」的硬编码；模块边界被尊重；依赖清晰；变更自包含；行为/结构变了文档已更新。[mitrix]
- **兔子洞自律**：修一个又见一个时知道收手；「完美如愿景」可以等下一次再访；每次改善一点，反复叠加聚焦在高频访问区域——那正是干净代码最值钱的地方。[Fowler/Opportunistic]

### 2.4 大规模变更：绞杀者与抽象分支

- **Branch By Abstraction**：建抽象层捕获客户端与旧 supplier 的交互 → 全部客户端迁到抽象层（顺手补测试）→ 经同一抽象层逐部分建新 supplier 并切换 → 删旧 supplier；全程可构建可发布。[Fowler/BBA]
- **绞杀者模式（Strangler Fig）**：从小的新增物开始逐步把行为从遗留系统搬进新代码库；「知道旧系统做什么就原样造个新的」大多数时候折戟——替换期间用户等不起新功能，且很多既有行为根本没人想要；四大活动：对齐成果、找接缝拆分、小组件交付（小组件风险小、回报早）、组织变革；过渡架构（新旧共存用完即拆）看似浪费，但风险降低与更早回值超过成本。[Fowler/StranglerFig]
- **社区实践变体「regenerate, don't fix」**：生成便宜时，找到 agent 犯第一个错的地方、改 prompt、删光全部代码从头重跑——与重构纪律构成张力（见待裁决矛盾 #3）。[社区/dataviz1000、NickNaraghi 转述 Anthropic 团队]

### 2.5 重构手法（按 AI 代码病灶高频重组，非 66 手法全表）

**第一梯队（AI 代码最高频病灶的直接解药，约 12 个）**：

| 手法（Fowler 第 2 版名） | 对应 AI 病灶 | 来源 |
|---|---|---|
| Extract Function | 长函数/一段做太多事，让父函数读起来是单一抽象层 | [Fowler目录][smell-check/long-function] |
| Remove Dead Code | 生成不完整残留、无用 import、注释掉的代码块 | [Fowler目录][vibecoder] |
| Rename Variable / Rename Field / Change Function Declaration | 误导命名（名字与实际行为不符） | [Fowler目录][vibecoker][APSD] |
| Replace Nested Conditional with Guard Clauses | 过深嵌套、看不清 happy path | [Fowler目录][smell-check/deep-nesting] |
| Replace Magic Literal | 裸字面量携带领域含义 | [Fowler目录][smell-check/magic-values] |
| Introduce Parameter Object | 过长参数列表、数据泥团 | [Fowler目录][smell-check/long-parameter-list+data-clumps] |
| Replace Primitive with Object | 基本类型偏执（规则散落重复校验的裸 string/number） | [Fowler目录][smell-check/primitive-obsession] |
| Extract Class / Move Function / Move Field | 上帝类（多职责）、依恋别人家数据 | [Fowler目录][smell-check/god-class+feature-envy] |
| Replace Conditional with Polymorphism（或集中判别一次） | 重复 switch / 同一 enum 的相同判别复制多处 | [Fowler目录][smell-check/repeated-switches] |
| Hide Delegate | 消息链 a.b().c().d()、调用方知道太多 | [Fowler目录][smell-check/message-chains] |
| Inline Function / Inline Class / Collapse Hierarchy / Remove Parameter | 投机泛化、只有一条路径的 strategy 钩子、无人使用的扩展点 | [Fowler目录][smell-check/speculative-generality] |
| Replace Exception with Precheck / Introduce Assertion | 异常吞错、假设未验证 | [Fowler目录][APSD/定义掉错误] |

**第二梯队（结构性改进常用）**：Split Loop、Split Phase、Decompose Conditional、Consolidate Conditional Expression、Introduce Special Case（null 对象）、Replace Temp with Query、Substitute Algorithm、Slide Statements、Preserve Whole Object、Replace Loop with Pipeline、Encapsulate Variable/Collection、Replace Derived Variable with Query、Separate Query from Modifier。[Fowler目录][smell-check 各规则附 refactoring 字段]

**其余归组（低频提及即可）**：继承层级搬移组（Pull Up/Push Down Field/Method/Constructor、Extract Superclass、Replace Superclass/Subclass with Delegate）、引用/值互换组（Change Value to Reference / Change Reference to Value）、API 形态组（Replace Constructor with Factory、Remove Flag Argument、Parameterize Function、Replace Command with Function）、遗留第 1 版别名（Extract Method=Extract Function 等）。完整目录见 refactoring.com/catalog。[Fowler目录]

**判据提醒**：数值阈值只定义「数什么」不定义「切点在哪」，按项目规模档案分级（如 long-function：个人档 100 行 / 团队产品档 40 行 / 最严档 20 行）；仅当测量值严格大于档位阈值才报告。[smell-check/presets]

---

## 三、简化原则

### 3.1 复杂度是首要敌人

- **构建有规模软件的主要挑战是管理复杂度**：复杂度=任何使系统难以理解和修改的结构性东西；两来源——依赖（不可消除须管理）与晦涩（重要信息不显眼→unknown unknowns）；三症状——change amplification、cognitive load、unknown unknowns（最坏）。复杂度是增量累积的，优化常改的热区（C = Σ c_p·t_p）。[APSD]
- **简单性是设计目标（KISS）**：越简单越好，尽可能降低复杂度；判据是「对读者简单」——有人说你的代码复杂，那它就是复杂；行数更多但认知负荷更低的方案是更简单的方案。[CleanCode][APSD]
- **Working code isn't enough**：能跑的代码只是副产品；战略式编程把 10–20% 开发时间投在设计上；战术龙卷风出码快但烂摊子别人收拾——AI agent 是终极战术龙卷风。[APSD]（「LLM 把简单事做得太好，阻止新程序员学会中等难度的事」[社区/recursivedoubts]；agent 带着畸形架构继续而不像人每 10–15 分钟停下纠错 [社区/dataviz1000]）

### 3.2 YAGNI（合并 Fowler + Google + Karpathy 三体系）

- **假想功能（presumptive feature）现在不建**：支持「尚未开放使用」功能的任何代码；三类成本——建造成本、持有成本（复杂度抬高其他所有功能，付到删除为止）、延迟价值成本；即便需求判断全对，胜算最多 ⅔（微软数据：仅 ⅓ 已上线功能改善了目标指标）。[Fowler/yagni][Google/Over-engineering 处置原则同旨]
- **「以后加会不会显著更贵」想象测试**：通常想象一下「以后引入该能力所需的重构」就足以说服自己；真正该现在做的是「容易做、几乎不增复杂度、显著降低未来成本」的事（如错误信息用查找表）。[Fowler/yagni]
- **小尺度 yagni 同样适用**：不加「还没准备用」的字段/方法/参数/扩展点；大量小 yagni 决策累积显著降低复杂度。[Fowler/yagni][karpathy4/原则2「不做超出所求的功能；单次使用不抽象；不为不可能场景做错误处理」][STS/H=假设性加固：没人读的校验和、为想象未来准备的兼容层]
- **YAGNI 的边界（防误用）**：yagni 只适用于「现在引入、以后才利用的额外复杂度」；重构、self-testing code、持续交付是它的 enabling practices——为重构投入不违反 yagni；不增加复杂度的未来准备也不归 yagni 管；任何让当前需求更难理解的抽象被推定有罪。[Fowler/yagni]
- **AI 特化证据与对策**：Karpathy 2026-01 抱怨三大失败模式之首即 over-complication（100 行够用写 1000 行的臃肿构造、膨胀抽象）[05/Mnilax 背景时间线]；示例——单一折扣计算写成策略类+Enum+Protocol 30+ 行 setup vs 4 行函数，「好代码是简单地解决今天问题的代码，不是过早解决明天问题的代码；问题出在时机」[karpathy4/EXAMPLES]；「让当前需求的代码更难理解的抽象」由删除测试把关：删掉它会把复杂度集中还是只是挪走 [mattpocock/improve-codebase-architecture]

### 3.3 深模块与信息隐藏（APSD 黄金法则）

- **把复杂度往下拉，写深模块**：接口简单、实现深；最好的模块接口远比实现简单（极端例：GC——海量复杂度、零接口）；「宁可自己多受一点苦，也要减少用户的苦」。[APSD]
- **每个模块封装一条知识且只封装在这一个模块里**；信息泄漏的反面操作：看到泄漏问「如何重组让这条知识只影响一个类」。[APSD]
- **略微通用（somewhat general-purpose）**：接口通用、实现针对当前用例——不写 deleteBackspace/deleteDeletekey/deleteSelection 三个方法，写 delete(start, end) 一个；自检三问：覆盖当前所有需求的最简单接口是什么？这个方法会在多少场景使用？对当前需求好用吗？[APSD]
- **每层不同抽象**：pass-through 方法/直通变量是分层失败的信号；配置参数是「把复杂度推给用户」的典型——「你真觉得调用方能选出比你更好的配置值吗？还是你只是懒？」；不可避免时给好默认值。[APSD]
- **定义掉错误（define errors out of existence）**：改方法定义使不需要异常（unset 例）；消除不了就地低层掩盖；不可恢复直接崩溃合理——异常处理天生是复杂代码、很少被执行、易藏 bug。[APSD]（「尽早崩溃：死掉的程序比残废的程序损害小」[PragProg/Tip38]；AI 吞错事故「迁移静默跳过 14% 记录，11 天后报表才发现」[Mnilax 规则 12 Fail loud]）
- **Design it twice**：每个问题总考虑多个方案；判断一个设计简单比创造简单设计容易。[APSD]

### 3.4 防过度简化（简化的边界）

- **行为保持铁律**：只改怎么做、绝不改做什么；不把「行数更少」置于可读性之上（嵌套三元、密集单行）；不造聪明方案；不合并过多关注点进单一函数；不移除有益抽象。[code-simplifier]
- **真实需求驱动复杂度，机制名字和行数不决定保护是否有用**：发布流程消费的校验和该保留，没人读的「以防万一」该校验和该删；既有支持承诺算当前需求，假想的未来灵活性不算；完成受影响流程时更大的 diff 正当。[STS/Stop Ladder]（SHIT 四症状：Scope creep / Hypothetical hardening / Intent violation / Task thrashing——完整履行任务职责与「不发明工作」是同一枚硬币两面）
- **冲突不要平均**：代码库两种模式矛盾时选其一（更新/更受测的），解释并标记另一待清理；「同时满足两条规则的折中代码是最差的代码」。[Mnilax 规则 7]

### 3.5 DRY 的精确化（合并裁决）

见「已裁决矛盾 #3」：DRY 的对象是**知识**而非**文本**——「必须一起变化」才是真重复，「偶然相似」应保持分离；抽象前最好同时满足单一清晰业务概念（非 Utils/Helper）、变化耦合、命名抽象降低总复杂度；模式未清晰前允许重复两次（WET）、等 Rule of Three（AHA）。[PragProg/Tip15][smell-check/principles-glossary][mattpocock/一个 adapter=假想 seam、两个=真 seam]

---

## 四、验证方法

### 4.1 TDD 及其裁决（见已裁决矛盾 #2）

- **铁律：没有失败的测试就没有生产代码**；先写代码了？删掉重来（不许留作参考、不许改编）；red→green 每步强制验证：RED 要确认是「失败」而非「报错」且失败原因正确；GREEN 要跑**项目整套测试**（任务只点名一个文件也要跑全套），那轮跑出的任何失败都要点名写进报告；REFACTOR 仅在绿后。[superpowers/TDD]
- **「没看过它失败，就从未证明它能抓 bug」**：事后测试立即通过、被已写代码偏置——回答「这做了什么」而非「这应该做什么」；借口对照表逐条反驳（太简单不用测/回头再测/手动测过/已经花了 X 小时……）。[superpowers/TDD]
- **Seam 协商与垂直切片**：测试住在公共边界（seam）上、永不针对内部；写任何测试前写下受测 seam 并确认；一个测试→一个实现→重复，每圈是响应上一圈所学的 tracer bullet；三反模式——实现耦合（mock 内部协作者/测私有方法，重构后挂但行为没变）、同义反复、水平切片（先写全部测试再写全部实现=测想象中的行为）。[mattpocock/tdd]
- **好测试两原则**：1) 每个测试命名它捕获的 break（什么生产变更应使它失败）；2) 每个测试行使真东西（mock 只有在真实依赖被证明慢或外部时才配拥有）。Mutation Check：心内变异生产代码（错常量/错分支/缺副作用/空返回），每个现实变异至少一个测试应失败。[superpowers/writing-good-tests]
- **TDD 的设计批评（APSD 立场，供 Skill 引用）**：TDD 聚焦「让功能跑起来」而非「拿到最好设计」，流程中没有任何时点鼓励退后一步改进设计；开发单元应是抽象而非功能。[APSD]（张力已部分消解：superpowers 把 REFACTOR 设为循环第三步；mattpocock 把重构划给评审阶段。）
- **TDD 的适用例外**（superpowers 明列，须问人类）：一次性原型、生成代码、配置文件。

### 4.2 完成前验证（对 agent 尤其关键）

- **铁律：没有新鲜验证证据不得宣称完成**——本条消息里没跑过验证命令，就不能宣称它通过；「should/probably/seems to」是停的信号；agent 报 success 不算数，查 VCS diff。[superpowers/verification-before-completion]
- **Gate Function 五步**：IDENTIFY 什么命令能证明→RUN 完整新鲜命令→READ 全输出+退出码+失败数→VERIFY 输出确认断言吗→THEN 才宣称；跳任何一步=撒谎。[superpowers/verification]
- **回归测试完整环**：Write→Run(过)→**Revert fix→Run(必须挂)**→Restore→Run(过)——没看过挂的修复不算已验证。[superpowers/verification][superpowers/executing-plans]
- **修 bug 先写复现测试**；「bug 修好」需要测试原始症状通过而非「改了代码」。[PragProg/Tip31][superpowers/verification][karpathy4/原则4「修 bug→写复现它的测试，然后让它过」]
- **别假设，要证明；测试全跑过才算做完；一个 bug 只发现一次（此后交给自动测试）**。[PragProg/Tip34/91/94]
- **系统化调试**：找到根因前禁止修复；Phase1 读全错误信息→一致复现→查最近变更→多组件先插桩定位失败层→追踪数据流到源头**在源头修**；3+ 个修复失败=架构问题，停下质疑模式而不是试第 4 个。[superpowers/systematic-debugging][PragProg/Tip29/32/33]
- **强成功标准让 agent 独立循环**：「加校验」→「为非法输入写测试，然后让它们过」——把命令式指令转为带验证循环的声明式目标；弱标准（「让它能跑」）需要不断澄清。[karpathy4/原则4]

### 4.3 证据分级与机器判定

- **三层证据体系**：mechanical（shell/附带脚本输出，每个数字必须能追溯到列出的命令）> semantic（LLM 判断）> estimate（工具缺失时的降级估算，永不许标成 mechanical）；工具缺失是一等信息（写 absent 而非沉默），克隆检测宁可跳过也不造假精度；不执行被审计代码（纯静态）。[smell-check/measurement]
- **判定不由模型做**：baseline_diff 把升级后测试运行与机器记录的基线对比，「手工敲的基线什么也证明不了」；proof_pack 用固定规则算出 PROVEN / NOT PROVEN / PARTLY PROVEN 三档判定，每条规则写进输出供审计；**Canary 金丝雀**：故意单行破坏，其结果文件必须显示测试变红——笔记里的「Canary:」行是主张不是证据；只被 skipped/pending 测试点名的规则=「named, not run」不算已测试。[code-modernization]
- **Synthesis 上限**：综合最多 3 条根因假设，只能引用已存在的 finding id，每条以「推断——修复后复扫验证」结尾——诊断与验证分离。[smell-check]

### 4.4 跨模型 review 的方向性（重要新证据）

- **不对称实验结果**（116 道 LiveCodeBench 难题，reviewer 只看题面+草稿、不跑测试）：Claude 审 Codex 草稿 71.6%→89.7%（显著有效）；Codex 审 Codex 自评 84.5%（自评对弱草稿有效）；**Codex 审 Claude 草稿 91.4%→82.8%（不升反降）**；Claude 自评 91.4% 不变（自评对强草稿无效）。结论：有用的配对不对称，「第二模型把关」可能负收益，方向要选对；按草稿质量分层：弱草稿→自评/跨模型，强草稿→跳过。[cross-model]
- **工具实践与证据的冲突**：neal 等编排工具默认「Claude 写、Codex 审」恰是实验中负收益方向——Skill 中应纠偏（写明方向与评审条件）。[cross-model]
- **社区多模型实践**（另一证据源）：不再信任单个 LLM 的意见，拿 2nd/3rd opinion；「所有 LLM 写的代码由另一个 LLM review，我 verify 那个 review，再让一个 agent 对全部迭代」；PR review 用 Sourcery+Codex+Claude 多工具混审。[社区/rtp429、kaydub、weeksie]（两证据源的张力见待裁决矛盾 #2）

### 4.5 量化基线（Skill 论证用）

- AI 代码 45% 含至少一个安全缺陷；结构化 review 后 <10%；具体、设计良好的提示（明确要求安全）把失败率 31.5%→24.3%——prompt 是低成本质量杠杆；更大模型≠更安全；代码专用微调反而略差（41.4% vs 39.9%）。[Veracode]
- AI 参与 PR 总 issue 约 1.7 倍；逻辑/正确性 +75%；安全最高 2.74 倍；可读性 3 倍+；过多 I/O 约 8 倍——无 AI 独有错误类型，只是更频繁更大规模。[CodeRabbit]
- AI 辅助代码认知复杂度全面恶化、重复 +81%/+115%（语法更干净但向训练分布的「平均水平代码」回归）。[CIQ]
- 重复率比两年前高 10 倍；重构占变更行比例 25%→<10%（2021→2024）。[GitClear]

---

## 已裁决矛盾（本域就地裁决，共 3 条）

1. **注释是失败品 vs 该写的注释要写**（[CleanCode]「永远先尝试用代码自解释」+ Fowler目录把 Comments 列为坏味道 vs [APSD]「先写注释」+ [Google] 注释检查项）
   **裁决：分层处理。**代码能表达的（what）交给代码——复述代码的注释、收括号注释、注释掉的代码一律删；接口的非正式信息（前置条件、高层行为、副作用、单位/边界含端点与否、决策背后的 why）只能存在于注释中，必须写——抽象只有当用户不必读实现就能用时才有意义，注释提供这个信息。AI 语境加重砝码：注释是给未来维护 agent 的上下文输入，错误注释比没有注释更糟（AI 无条件自信生成），因此 AI 生成注释必须人工对照实际行为复核（[vibecoder/R6.2][社区/gabriela_c、jazzypants]）。Clean Code 与 APSD 的表面冲突实为对象不同：前者反对的是「解释 what 的注释」，后者要求的是「承载 why 与接口契约的注释」。

2. **TDD 强制 vs vibe 场景先跑通再补测**（[superpowers] 铁律无例外 vs [mitrix] 先补集成测试再重构、社区 vibe 流程「上线能跑就行，事后补测试与整理」[社区/掘金独立开发者]）
   **裁决：按代码所处阶段分层，而非全有或全无。**(a) 进入正式维护的逻辑代码（尤其定价/权限/认证/计费）：TDD 强制——red-green 是唯一能证明「测试测的是对的东西」的方式，事后测试被已写代码偏置；(b) 探索性原型/vibe 起步阶段：允许先跑通，但**转为正式代码的门槛是特征测试兜底**——以现有行为为 spec 补集成/契约测试（关键路径 60–70% 覆盖）再动结构，这与 [mitrix] 流程一致；(c) 报告 bug 修复：无条件先写复现测试（两体系在此一致）。支撑逻辑：yagni 要求 self-testing code 作为 enabling practice——没有测试的代码库根本不具备「以后再补」的可行性，技术债只增不减 [Fowler/yagni][GitClear 数据]。

3. **DRY（消灭重复）vs 重复两次可容忍/错误的抽象比重复更贵**（[PragProg/Tip15] vs [smell-check] WET/AHA 与 duplicated-knowledge 的偶然相似例外）
   **裁决：DRY 的判据是「知识」而非「文本」，AI 语境下阈值收紧。**必须一起变化的（同一业务规则/决策，改一处不改其它就是错）→ 真重复，必须提取单一权威表示；碰巧长得像但会独立演化的（如客户端与服务端校验）→ 偶然相似，强行合并制造错误耦合；模式未清晰前允许重复两次、第三个出现时再抽象（Rule of Three / AHA）。AI 语境修正：因 AI 重复率 +81%~115% 是实测最大病灶 [CIQ][GitClear]，「重复两次」容忍度应低于人写代码，且优先查 repo 既有 helper（missed-reuse）而非立即新造抽象——先用 grep 找既有符号，找不到再考虑提取。

---

## 待裁决矛盾（需主 agent 裁决）

1. **「发现抽象应一次性设计好」（APSD：开发单元应是抽象；Design it twice；略微通用）vs YAGNI/等需要时再抽象**（[Fowler/yagni] 任何让当前代码更难理解的抽象推定有罪；[mattpocock] 一个 adapter=假想 seam；[karpathy4] 单次使用不抽象）。两者都有 AI 语境实证（CIQ 重复爆炸支持前者收紧、Karpathy over-complication 抱怨支持后者）。本域在 §3.2/§3.3 并列呈现未强行合并——Skill 需要一个统一判据（候选：按「变更热度」分层——热点文件先抽象、冷区先重复 [mattpocock/improve-codebase-architecture 的 git log 热点法]）。
2. **跨模型 review 方向性（单点实验）vs 社区多模型混审普遍实践**：[cross-model] 证明 Codex 审 Claude 负收益（-8.6pp），但仅基于 LiveCodeBench 算法题、reviewer 不跑测试的设定；[社区/weeksie、kaydub、rtp429] 的多工具混审（含跑测试、有 diff 语境）报告有效。外推有效性存疑——Skill 中写「固定方向 Claude 审 Codex」还是「多模型混审+人 verify review」需要主 agent 定夺。
3. **重构纪律（行为保持、小步、测试保护网 [Fowler][mitrix]）vs「regenerate, don't fix」**（生成便宜时找到第一个错误点、改 prompt、删光重跑 [社区/dataviz1000、NickNaraghi 转述 Anthropic]；[社区/ativzzz]「启动最新 LLM 重写整个代码库」）。前者是有人类维护、长期演进的代码库的正解；后者在生成成本趋零、代码量小、无外部集成时可能更经济。分界判据（代码库年龄/规模/集成密度/测试存量？）待裁决。
4. **AI 代码质量基线证据冲突**：[CodeRabbit][CIQ][GitClear]（AI 代码系统性更差：issue 1.7x、认知复杂度恶化）vs [METR via 05]（接受率 <44%、多数需修改但可改好）与 [社区/jf22]（投入 review 的 AI 代码可比人写更干净）。影响母表的「默认怀疑度」标定——Skill 该按「AI 代码预设更差」还是「AI 代码质量依赖流程」定调。
5. **逐行 review 门槛 vs 半黑盒信任模型**：Willison 黄金法则「不能向别人解释的代码不 commit」[05/willison-definition] vs 其 2026 自我修正「不再逐行审查，把 agent 当其他团队的服务——半黑盒，出问题时才检查」+ normalization of deviance 警告 [05/willison-convergence]。高危路径（支付/认证/数据访问）显然必须逐行，但常规 CRUD 的 review 深度行业标准未定。
