# 03 方法论（methodology）知识点提取

> 阶段2 知识点提取：只罗列、不整合、不做取舍。每个知识点带溯源（节末来源行）。
> 覆盖 `research/raw/articles/` 下全部 26 个 `methodology-*.md` 文件，逐文件精读 raw 原文提取，不依赖二手摘要。
> 英文术语/手法名保留原文，含义用中文转述。

---

## methodology-ai-refactor-mitrix.md

- 定义：重构 AI 生成代码 = 在不改变外部行为的前提下，重组其架构、可读性、可维护性；AI 代码通常缺少设计意图（design intent），比人写代码更难在重组前理解。
- 根本差异：人类开发者做取舍时会留下"意图的面包屑"——注释、命名约定、目录结构；AI 生成代码往往没有这条线索。
- 推论：重构 AI 代码不是"把某人的愿景清理得更干净"，而是先逆向工程出愿景本来是什么，再朝原过程从未建立的连贯架构重构；流程必须包含 discovery（发现），不只是 restructuring。
- Step 1 Audit Before You Touch：改任何一行前先画系统地图——主入口、API 暴露的路由、数据库表及表间数据流、认证/授权路径、第三方服务集成点。
- 审计要回答的五个问题：应用做什么（平实语言的功能清单）；主要用户流程（注册、核心操作、设置）；业务逻辑在哪（哪些文件含核心功能）；集成点在哪（DB、API、第三方）；什么真的部署在跑（live vs dead code）。
- 审计结果写进一个简单 markdown 文件 = 项目地图（project map），整个重构过程反复引用；不需要完美的架构图。
- "我们不知道认证是怎么工作的"本身就是一条 finding，应影响重构优先级。
- Step 2 依赖图：AI 代码典型病灶——文件循环 import、业务逻辑散落在表示层、工具函数做不相关的事。
- 每个模块要回答四问：import 了什么；被谁 import；有无副作用（DB 写、API 调用、文件操作）；能否隔离测试。
- 工具：madge（JS/TS 依赖图）、import-linter（强制边界）、grep import 语句。
- 依赖图阶段目标不是立刻修，而是判断哪些模块紧耦合、哪些独立；独立模块先重构，紧耦合模块须一起重构（更复杂但影响更大）。
- Step 3 先补测试再重构（最重要、被最多团队跳过）：没有测试，每次改动都是潜在回归；有测试才能自信改动并验证行为保持。
- 先给 happy path 写集成测试，不求 100% 覆盖；聚焦主用户流程：注册、核心操作、数据持久化。
- 给每个 API 端点加 contract 测试：验证常见输入下返回期望的状态码和响应形状，重构中抓破坏性变更。
- 暂时跳过单元测试：AI 代码通常太缠绕，写不出有意义的单测；重构出干净接口后单测会自然出现；现阶段集成 + 契约测试就是所需安全网。
- 以现有行为为 spec：跑应用、操作功能、写验证"当前行为"的测试——不是测行为对不对，是测别把它改掉。
- 覆盖率目标：关键路径 60-70% 即可安全重构，不必为即将重构掉的代码花几周写测试。
- Step 4 小而可验证的 PR：拒绝 big-bang / 单分支全重写；每个 PR 只做一类改动（rename / extract / move / restructure）、可独立发布、过全部已有测试、30 分钟内可审完。
- Phase 1 Cleanup（第 1-2 周）：删死代码与无用 import；修明显 bug 与不一致；统一命名；补/修基础错误处理；把该配置的硬编码值改为配置——低风险高价值，不改行为，每个 PR 都应"平凡可审"。
- Phase 2 Extract（第 3-4 周）：从 UI 组件抽业务逻辑；DB 查询抽进 repository 模块；共享工具抽独立模块；建立清晰模块边界——架构在此成形，每次抽取一个 PR，测试验证行为未变。
- Phase 3 Restructure（第 5-6 周）：文件结构对齐模块边界；重复代码合并为共享抽象；统一模式（错误处理、响应格式）；补缺失的 TypeScript 类型 / Python 类型标注——最显眼但应最轻松，因为地基已打好。
- Phase 4 Harden（第 7-8 周）：为重构后模块补全面测试；加输入校验；实现正式日志；上监控告警；写架构文档。
- Step 5 验证与监控：每阶段后跑全量测试、部署 staging、手动走全部关键用户流、监控错误率与性能指标 48-72 小时；发现问题先修再进下一阶段，绝不把变更叠在坏变更上。
- 重构 PR Checklist（10 条，每个 PR 过一遍）：测试全过（新旧）；无行为变化（除非有意且已记录）；死代码已删；命名清晰一致；错误处理存在且有意义；无"应做成配置"的硬编码；模块边界被尊重；依赖清晰声明；变更自包含（单一职责）；行为或结构变了文档已更新。
- 常见错误 1：别一次性全部重写——big-bang 在验证前堆积过多变更，永远做不完且风险复利。
- 常见错误 2：重构期间别加功能——"顺手加个 X"是 scope creep，把重构拖成数月项目；专注结构不专注功能。
- 常见错误 3：没测试别重构——那是 guessing（瞎猜）不是 refactoring。
- 常见错误 4：别把重构决策交给 AI——AI 可以帮忙做单步，但不理解你的产品需求和架构目标；当工具用，别当决策者。
- 常见错误 5：别跳过文档——重构完代码有组织了，但不写简短架构文档和更新注释，三个月后回到混乱。
- 该请专业帮助的信号：重构超一个月无清晰进展；不断发现新类别的问题；团队没有资深工程经验；生产环境有真实用户且不能宕机；对测试策略没信心；专业重构成本几乎总是低于脆弱代码导致的生产事故。
- FAQ 规模参考：1 万-3 万行的典型 MVP，彻底重构约 6-10 周；取决于缠绕程度、已有测试、是否需边重构边维护生产。
- FAQ：几乎永远不该从头重写——重写丢掉全部能跑的逻辑、边角处理和集成成果；只有架构与要构建的东西根本不兼容时才重写。
- FAQ：可以让 AI 帮忙重构 AI 代码，但仅限范围明确的任务（重命名、抽函数、加类型、写测试）；别让 AI 做架构决策或重组整个模块——AI 只优化眼前任务，不考虑长期影响。
- FAQ：说服团队优先重构的框架是速度与风险——量化绕着问题代码走的时间、调神秘故障的时间、生产事故成本 vs 重构成本。
- FAQ：重构中发现安全问题（硬编码密钥、缺输入校验、注入漏洞）→ 立即停下修掉；优先级高于任何结构改进；修复、补测试、再继续重构。

来源: research/raw/articles/methodology-ai-refactor-mitrix.md（原始 URL: https://mitrix.biz/blog/refactor-ai-generated-code）

---

## methodology-ai-review-checklist-vibecoder.md

- 前提：多数 code review 流程为人写代码设计，而 AI 生成代码以完全不同的方式失败，需要针对 AI 失败模式的 checklist。
- 人犯错的原因：误解需求、状态不好、赶工期；AI 犯错的原因：幻觉 API、忽略当前 prompt 之外的上下文、优化"看起来正确"而非"确实正确"的代码。
- 关键差异：人写出不安全的认证检查多半是累或偷工减料；AI 写出的是因为它套用了一个与你请求"相似但不相同"的训练模式——表面现象一样，失败机制不同。
- 对 AI 代码要问更难的问题："这段代码真的做了它声称的事吗？模型做了哪些对我们情境不成立的假设？"
- Veracode 2025 数据：45% 的 AI 生成代码含至少一个安全漏洞；引入结构化 review 流程后降到 10% 以下——差别就是瞄准正确失败模式的 checklist。
- AI 失败四大类（每个重要 AI 贡献都要查）：安全（借来的不安全训练模式）、逻辑（幻觉 API、边角案例）、性能（不必要的重依赖、N+1）、死代码/质量（生成不完整）；按 安全 > 逻辑 > 性能 > 质量 的顺序审——部署出去的漏洞比延迟的功能更糟；正确性是其他一切的门；性能质量改善代码库但很少立即引发故障。
- 安全检查 1：扫描硬编码密钥/凭据——在整个 diff 里搜 API key、token、password、connection string；AI 爱把示例凭据放进 config、seed data、测试 setup 函数；给 grep 命令示例，每个命中都要人工检查。
- 安全检查 2：每个数据库查询查注入——凡是用用户输入拼 SQL/NoSQL/ORM 查询的都看；AI 明知有参数化查询却不总用；对每个查询问："这字段传个单引号会怎样？"
- 安全检查 3：所有输入渲染处查 XSS——凡是把用户输入渲染到 DOM/模板的地方查转义；React 的 dangerouslySetInnerHTML 是显眼信号，vanilla JS 模板字符串同样危险；AI 图方便用 innerHTML 而 textContent 才安全。
- 安全检查 4：每个新端点验证认证——diff 里每个新 API 路由/服务端函数，确认先查认证再跑业务逻辑；AI 生成路由很快但先生成 happy path，"未认证调用会怎样"这个问题在 AI 代码里常常永远不会被提出来。
- 安全检查 5：查授权而不只认证——认证验证"你是谁"，授权验证"你能做什么"；AI 代码经常认证了用户却忘了检查该用户是否有权访问所请求的具体资源；"用户 A 摸到用户 B 的数据"是典型 AI bug。
- 逻辑检查 1：每个外部 API 调用对照现行文档验证——AI 有训练截止时间，它描述的是训练时的 API，而 API 会变；这是 AI 逻辑 bug 最常见的单一来源。
- 逻辑检查 2：错误处理完备性——AI 生成的 try-catch 处理预期错误类型、静默吞掉其他一切；看每个错误处理器在意外错误类型到来时发生什么；后台任务里"捕获即忽略"意味着任务无声停止，是特定风险。
- 逻辑检查 3：async 代码查竞态——AI 异步代码常假设操作按序完成；要找的模式：多个并发请求更新同一资源、无冲突解决的乐观 UI 更新、无事务的 DB 写；问："两个用户同时做这件事会怎样？"
- 逻辑检查 4：数据流从输入到输出逐步验证——追踪用户输入路径，每次转换是否正确处理 null/undefined，每步类型是否匹配下一步预期；TypeScript 类型不够——AI 有时用 cast 绕过编译器错误而不保证底层数据真的匹配。
- 逻辑检查 5：业务逻辑逐字对照实际需求——AI 实现的是 prompt 描述的字面而非你的意图；对定价计算、权限规则、状态迁移这类关键逻辑，把代码对照原始需求逐字读。
- 性能检查 1：新依赖审计必要性与体积——package.json 每个新包都问是否必要；AI 常在内置方法够用时导入完整工具库（因为训练数据里出现过）；用 bundlephobia.com 查非平凡新依赖的体积影响。
- 性能检查 2：查 N+1 查询——凡在循环内做数据库调用的代码都看；AI 稳定产出 N+1（先循环再取数太好写了）；对 diff 里每个循环问：数据能否用单个批量查询取回。
- 性能检查 3：新查询查缺失索引——AI 引入按列过滤/排序的新查询时很少加索引；无索引查询小数据集正常、负载下指数级劣化；对照 schema 给 WHERE / ORDER BY / JOIN 用到的列加索引。
- 性能检查 4：查不必要的重复计算——AI 会在每次调用时重算本可缓存/memoize 的值；找循环内或高频函数内的昂贵操作（DB 查询、API 调用、复杂计算）且输入不变的情况；修复通常是一行缓存，但要先看出模式。
- 质量检查 1：清除生成不完整留下的死代码——AI 有时生成被 import 但从未调用的工具函数和类型定义；在 diff 里搜无用 import 和未导出函数；死代码是维护负担和未来 review 的困惑源。
- 质量检查 2：与既有模式一致性——AI 缺少代码库约定上下文时默认用训练模式；用自定义 error 类的代码库不该出现新代码抛裸 Error；把 diff 放在周围代码的语境里读，为一致性而不只是正确性。
- 质量检查 3：命名准确性——AI 起的名字"泛泛而谈地合理"；一个叫 validateUser 实际查支付状态的函数是会困惑读者多年的命名 bug；把函数名/变量名/类型名对照代码实际行为检查。
- 质量检查 4：注释准确性——AI 无条件地自信生成注释；"返回用户全名"的注释挂在返回 ID 的函数上比没有注释更糟；把每条 JSDoc 和行内解释对照代码实际行为读。
- 常见错误：把 AI code review 当成比人 code review 更快——是"不同"不是"更短"；安全和逻辑检查每行需要同样时间，因为 AI 失败模式更隐蔽、更多样；"AI 自己检查过了"而赶时间的团队正是把漏洞发上生产的团队。
- 落地建议：把四大类做成 PR 模板里的复选框，reviewer 逐节确认后才 approve；对 PM：这不是可选开销，是发布 AI 代码的最低责任流程。
- 执行策略：安全 + 逻辑每次都跑；性能 + 质量在 AI 代码触碰数据存储、外部 API、高流量路径时加跑；十分钟的 structured review 能抓住未检 AI 代码库里到达生产的大部分问题。

来源: research/raw/articles/methodology-ai-review-checklist-vibecoder.md（原始 URL: https://blog.vibecoder.me/code-review-checklist-ai-generated-code）

---

## methodology-ai-review-continuumcode.md

- 总论：审查 agent 产出 ≠ 审查同事 PR——错误不同、分布不同、"整齐划一的自信语气"把它们藏得更深。
- 核心论断：agent 代码失败是 plausible（貌似合理）而非 confused（困惑）——静默删护栏、发明本该存在的 API、放宽测试让它们通过。
- 审查方法论总纲：先看文件清单、先读删除行、测试文件单独 diff、自己跑测试而不是接受声明；机器审查有帮助但不能替代（无法知道你的意图）；diff 大到读不完 ⇒ 任务太大了。
- 直觉失灵机制：你对"哪里要放慢"的直觉是在人类代码上训练的，靠"困惑信号"触发（怪命名、含糊注释、风格漂移）；生成代码无论对错都没有这些信号，代码 uniformly confident，注意力被均匀分布而本不该均匀。
- 失败模式表（7 行，逐条）：Plausible but wrong（惯用、命名好、细看才知错 → 读逻辑别读风格）；Silent deletion（边界分支/护栏被悄悄删 → 先审删除行）；Invented API（调用一个"理应存在"却不存在的方法 → 跑起来，编译器常能抓）；Weakened test（断言被放松以通过 → 专门 diff 测试文件）；Scope creep（两文件任务动九个文件 → 看内容前先看文件清单）；Confident wrong explanation（听起来权威的理由 → 验证 claim 本身而非语气）；Duplicated instead of reused（没找到该调的 helper 就近复制了一份 → grep 它本该调用的函数名）。
- 七步审查法（顺序刻意：最便宜、产出最高的检查在前，每一步都可能让你在花费注意力之前就打回 agent）：
- 七步之 1：先看文件清单再看内容（`git diff --stat main...HEAD`）——非预期文件即 scope creep，scope creep 就是未审查变更藏身处；两文件任务动了九个文件本身就是一条 finding，不必读任何一行。
- 七步之 2：先读删除行（最高产出、最常被跳过）——agent 删边界护栏产生的 diff"读起来像简化、行为上是 bug"；只看减号行 + 被整个删除的文件（给出两条 git 命令）。
- 七步之 3：测试文件单独 diff（`git diff -- '*test*' '*spec*'`）——实现和测试同 commit 改动是正常的，断言变松不正常；单独读这个 diff，让放松的断言无法藏在五十行合法实现改动旁边。
- 七步之 4：自己跑测试——"all tests pass"是 agent 写的一句话，与代码出自同一生成过程；跑测试套件，并检查断言数量是"变多"而不是"横移"。
- 七步之 5：专查错误路径——agent 写 happy path 很好、错误处理不一致；专门看被调用方失败时会发生什么：错误被吞、被包装、被记录、还是被返回？貌似合理的变更最常在这里偏离你的约定。
- 七步之 6：从解释中抽查一条事实性 claim——挑 agent 总结里的一条断言对照代码检查；如果错了，其余一切都要仔细得多地读——自信的错误解释与自信的错误代码同源。
- 七步之 7：问一次"为什么"——问它为什么选这个方案而非显然的替代；点名约束的具体回答是好信号；含糊的回答通常意味着含糊的代码，合并前发现比合并后便宜。
- 提示：风格审查是这份清单里价值最低的，却吸走最多人力（因为最容易看见）；把风格推给 linter，省下的注意力花在第 2、3、5 步。
- 体量问题（volume problem）：agent 十分钟产出的代码多于你一小时能认真审的——这是整个领域的中心实践难题，任何审查技巧都解决不了。
- 警告：发现自己在 skim 就停下——skim 过的 agent 产出就是没审过的 agent 产出，你现在拥有没人读过的代码；省下的时间是幻觉：把工作从写代码挪到修 bug，费率更差、日期更晚，利息由 on-call 的人付。
- 缓解措施按有效性排序：缩小任务（唯一真正的修法，其余都是缓解）；agent 按逻辑边界分 commit（按 commit 审而非按 session 审）；先 plan 再写（错误方案到不了 diff）；prompt 带约束子句（从源头防 scope creep）；机器 reviewer；一个 worktree 一个 session。
- 机器审查定位：带只读工具、全新上下文、被要求怀疑的第二个 agent 能抓到真东西——它对方案没有投入、没有为它争辩过的记忆。
- 工具现状（2026-08）：Claude Code 的 /code-review（别名 /review）作为后台 subagent 审查分支领先 commit + 未提交改动，支持 --fix 与 --comment；Codex 的 /review 可指定 --base，报告 findings 不碰工作区；effort 级别用覆盖率换置信度——低/中档只报最有把握的（误报代价高时该用这档）。
- 工具陷阱：后台 review 用 --fix 应用的编辑在 session checkpoint 之外，/rewind 撤不掉，要用 git 回退。
- PR 级机器审查范例（Anthropic managed Code Review）：agent 舰队审 diff + 验证步骤把候选 findings 对照实际代码行为过滤误报；findings 标记 Important / Nit / Pre-existing 以行内评论发布。
- 设计决策 1（值得任何工具借鉴）：check run 永远以 neutral 结束，机器审查永不通过分支保护阻塞合并——"能挡路的 reviewer 第一周出错就会被关掉"。
- 设计决策 2：按仓库用 REVIEW.md 调节——重新定义什么算 important、给 nit 数量设上限、列出应保持沉默的路径；不设上限的 nit 流是 review 工具变成噪音的方式。
- 成本数据（2026-08）：Anthropic 报告每次托管审查均价 $15-$25、约 20 分钟，随 PR 大小和代码库复杂度扩展；每次 push 都审就把该数字乘以 push 次数，按仓库设触发是预算决策。
- 人机分工表：null 与边界条件（机器 Good / 人 Tedious）；被删的 guard clause（机器 Good / 人 Good if you look）；被放松的断言（机器 Good / 人 Good if 单独 diff 测试）；"这是我想要的吗"（机器 Cannot know / 只有你）；"这方案对吗"（机器 Weak / 只有你）；"契合我们在建的系统吗"（机器 Weak / 只有你）。
- 分工结论：机器擅长穷举式局部检查、无法替代意图；让机器干 tedium，把注意力花在它标为"不可知"的那两行。
- 让审查结构性便宜：review 纪律会在压力下衰减，持久解法不是更多纪律，而是把工作安排成"小 diff 是默认产出"。
- 手段 1：每个 prompt 带约束子句——"不改公共签名、不加依赖"；最便宜的反 scope creep 控制手段，只花一行。
- 手段 2：要求按逻辑边界 commit——七个小 commit 可审而一个 900 行 commit 不可审；git log -p 读起来像论证而不是一堵墙。
- 手段 3：大改动先 plan——纠正一个 plan 花一条消息；纠正一个实现花整次运行、整次审查和整次回退。
- 手段 4：一个 session 一个 worktree 一个分支——同一 checkout 里的并行 agent 产出没人能归因的混合 diff。
- 手段 5：让机器 reviewer 先跑——到你自己的阅读时机械 findings 已修掉，注意力直接从意图开始。

来源: research/raw/articles/methodology-ai-review-continuumcode.md（原始 URL: https://continuumcode.ai/guides/reviewing-ai-generated-code/）

---

## methodology-apsd-janmeppe.md

- 命题：构建有规模的软件系统，主要挑战是管理复杂度。
- 复杂度定义（书原文）："Anything related to the structure of a software system that makes it hard to understand and modify the system"（与软件系统结构相关、使系统难以理解和修改的任何东西）。
- 生理学依据：人类工作记忆约 7±2 项，"能在脑中同时抛接多少东西"是持续对抗的最大限制之一。
- 复杂度两来源：依赖（dependencies，软件开发的基本组成部分，无法完全消除但必须管理，否则得到 big ball of mud）与晦涩（obscurity，重要信息不显眼 → 制造 unknown unknowns、推高认知负荷）。
- 复杂度两种表现：change amplification（看似简单的变更要在许多不同地方改代码，系统越长大越难改）与 cognitive load（程序员需要知道的东西太多，超出工作记忆容量）。
- 黄金法则：Pull Complexity Downwards（把复杂度往下拉/收进模块内）；目标是写深模块——接口简单、实现深而复杂的模块，用封装管理复杂度。
- 每个模块应代表一个设计决策（represent a design decision），且该信息只封装在这个模块里。
- 对 TDD 的批评：TDD 是好的但缺乏推动系统设计随时间变好的反馈环；问题在于 TDD 聚焦"让具体功能跑起来"而不是找到最好设计；开发单元应是抽象（abstractions）而非功能（features）；一旦发现需要某个抽象，应一次性把它设计好。
- TDD 的结构性缺陷：流程中没有任何时点鼓励你退后一步改进设计；可以合入 10 个完成且测试良好的功能 PR，而设计随每次合入缓慢变糟。
- 代码为读者而写：代码被读的次数多于被写；读者觉得不清晰时，错的通常是代码而不是读者；模块接口对读者 obvious 尤为重要，因为接口是其他模块所依赖的东西——管理 foo(a) 比管理 foo(a,b,c,e) 容易。
- 深模块 vs 浅模块：深模块 = 功能强大 + 接口简单；浅模块 = 接口大而复杂但没有多少深度；用"接口（做什么）+ 实现（怎么做）"两部分思考每个模块是管理依赖的核心手法。
- 信息隐藏是造深模块的手段；其反面是信息泄漏（information leakage）：设计决策散布或重复在多个模块 → change amplification/耦合（改一个决策要改多个模块）。
- 信息也会通过隐式接口泄漏：比如被迫知道文件格式、或事物应执行的顺序。
- 实践中最常见的病灶是 temporal decomposition（按时间/执行顺序分解模块）；ML 例：train dataset creator / training / test dataset creator / evaluation 四模块——train 和 test creator 需要知道同一件事，该设计决策应放进单一 dataset creator 模块。
- Pull complexity downwards 具体化：模块有简单接口比有简单实现更重要；几乎永远应该把复杂度收进模块内部，让用户好过一点，哪怕自己多吃点苦。
- 配置参数示例：配置参数应有好的默认值让调用方不必设置；"你真觉得调用方能选出比你更好的配置值吗？还是你只是懒？"

来源: research/raw/articles/methodology-apsd-janmeppe.md（原始 URL: https://www.janmeppe.com/blog/a-philosophy-of-software-design-john-ousterhout/）

---

## methodology-apsd-oehler.md

### 核心要点（Key Takeaways）
- 写代码时永远试图降低复杂度。
- Working code isn't enough：主要目标是做出解决问题的好设计（这需要一点前期投资），能跑的代码只是副产品。
- 写深模块（模块功能远大于其接口）而非浅模块（接口复杂度与其功能不相称）。
- 抽象与信息隐藏是朋友：能把复杂功能藏进模块就藏进去。
- 写"略微通用"（somewhat general-purpose）的类与方法：接口通用、实现针对当前用例。
- 系统每一层应有不同的抽象；如果大量 pass-through 方法，说明分层可以改进。
- 模块有简单接口比有简单实现更重要。
- 尽量避免异常与错误：异常处理天生是复杂代码。
- 写好注释：为实现补充精确性，或向读者描述意图。
- 为变量、类、方法选好名字。
- 保持一致性：实现、代码风格、命名、接口；尽可能用接口强制一致性。

### 第 1-2 章 复杂度的本质
- 写软件的最大限制是我们理解所造系统的能力；复杂度随时间增长不可避免，但简单设计能让更大更强的系统保持可管理。
- 降低复杂度两条路：让代码更简单更直白（eliminating）；封装复杂度做模块化设计（encapsulating）。
- 软件设计是横跨整个生命周期的持续过程；系统/组件的初始设计几乎从来不是最好的。
- 判断一个设计简单比创造一个简单设计容易；一旦识别出设计过于复杂，就可以换个方法看是否更简单。
- 复杂度定义："Complexity is anything related to the structure of a software system that makes it hard to understand and modify the system."
- 复杂度的形式：系统难以理解；实现一个改进要花大量功夫；修一个 bug 很难不引另一个。反例判定：功能庞大精巧的系统如果好改，就不算（本书意义上的）复杂。
- 复杂度公式：C = Σ c_p·t_p（总复杂度 = 各部分复杂度按开发者在该部分花费时间比例加权）→ 一小部分系统很复杂但从不被触碰，可能没那么糟；优化常改的热区。
- 复杂度对读者比作者更明显：有人觉得你的"简单代码"复杂，那它就是复杂。
- 症状 1 Change Amplification：一个小改动要求在很多不同地方改代码；设计目标是减少每个设计决策影响的代码量。
- 症状 2 Cognitive Load：开发者完成任务需要知道多少；认知负荷越高学习时间越长、出错风险越大；复杂度不能用行数衡量——行数更多的方案可能因降低认知负荷而更简单。
- 症状 3 Unknown Unknowns：不清楚完成任务需要改哪些部分；最坏的复杂度表现——你需要知道某事却没有办法知道它是什么/是否是问题；问题常在改动之后才出现。
- 原因只有两个：依赖（一段代码无法被孤立地理解/修改时就存在依赖；不可消除，应保持尽可能简单和显眼）与晦涩 obscurity（重要信息不显眼，如命名不清；常是文档不足的问题，但降低晦涩的最好办法是简化系统设计）。
- 复杂度是增量累积的：不是单次灾难性错误，而是依赖与晦涩随时间累积；"我这点小复杂度没关系"很容易自我说服；一旦累积就难以消除。

### 第 3 章 Working Code Isn't Enough
- 战术编程（tactical programming）：主要焦点是让东西能跑；短视——赶 deadline 不花时间找最好设计；复杂度累积，重构帮忙但要时间，快补丁让它更糟。
- "Tactical tornado"：出代码远快于他人、完全战术式工作的开发者——烂摊子通常由别人收拾。
- 战略编程（strategic programming）：最重要的是系统长期结构；首要目标是产出"恰好也能工作的好设计"。
- 战略投资两类： proactive（尝试几种方案取最简、为每个类多花时间找简单设计）与 reactive（发现设计问题时当场修）。
- 投资额度：总开发时间的 10-20% 投在设计上；前期投入会被后期节省轻松回收。
- 创业公司语境：心态常是战术的，但坏设计的代价来得很快，可能为产品整个生命周期付高开发成本。

### 第 4 章 Modules Should Be Deep
- 模块化设计：理想世界每个模块完全独立，但模块必然互调 → 依赖；把每个模块看作接口（做什么）+ 实现（怎么做）两部分；开发者不应需要理解其他模块的实现。
- 最好的模块：接口远比实现简单。
- 接口含正式信息（参数个数/类型，语言可查）与非正式信息（高层行为如"删除参数指定的文件"、使用约束如"调用前必须先调另一方法"，靠注释、编译器查不了）；多数接口的非正式部分更大更复杂。
- 抽象 = 略去不重要细节的简化视图；接口是模块的抽象；抽象过多或过少都不行——略去了重要细节的抽象是 false abstraction。
- 深模块：功能强大 + 接口简单；极端例子：垃圾回收器——海量复杂度、零接口。
- 浅模块：接口复杂度相对功能过高；🚩 Red Flag: Shallow Module——对复杂度之战帮助不大，收益被学习和使用其接口的成本抵消。
- Classitis（类炎症）：今天的传统智慧是"类应该小"而非"类应该深"；最小化每个类的功能导致小类贡献不了多少功能、数量众多、接口累积成大复杂度。
- Java I/O 反例：为读序列化对象要创建三个对象（FileInputStream → BufferedInputStream → ObjectInputStream），前两个从不直接使用；缓冲要显式请求（忘了就慢）；更好方案：默认缓冲 + 提供不缓冲的构造器变体。
- 结论：把接口与实现分离可以藏复杂度；深模块最大化被隐藏的复杂度。

### 第 5 章 Information Hiding (and Leakage)
- 每个模块应封装少数几条知识；信息隐藏从两方面降低复杂度：简化接口；隐藏的信息不被模块外访问，让演化更简单。
- 信息泄漏（反模式）：信息通过接口暴露；也会在接口之外泄漏——两个类依赖同一文件格式时，格式一变两类都得改（即便格式不体现在接口上）。
- 看到信息泄漏要问："如何重组，让这条知识只影响一个类？"——小类可考虑合并；或把泄漏的知识抽成只封装它的独立类。
- 🚩 Red Flag: Information Leakage——同一知识在多处被使用。
- Temporal decomposition（时序分解）：系统结构对应操作发生的时间顺序（读文件/改文件/写文件 → 三个类）；读和写类都懂文件格式 → 泄漏；解法：读写核心机制放进同一个类。
- 🚩 Red Flag: Temporal Decomposition——按顺序组织类时，同一信息可能被多处使用（泄漏）。
- 设计模块时关注每个任务所需的知识，而不是执行顺序。
- HTTPRequest 例子：暴露 public Map getParams() 把整个 map 暴露（外部甚至能改它），更好的是 public String getParameter(String name)——接口更深、信息隐藏更好。
- 🚩 Red Flag: Overexposure——API 的常用功能迫使用户学习其他（少用）功能，增加用户认知负荷。
- 走过头也不行：外界需要的信息不要藏（如影响各用例性能的配置参数，应该在接口中暴露）。

### 第 6 章 General-Purpose Modules Are Deeper
- 通用模块：面向宽问题域，未来可能有意外用途；太通用可能对当前用例做不好；专用模块：聚焦当前用例以后再加。
- 折中方案"Make Classes Somewhat General-Purpose"：模块功能反映当前需要，但接口更通用；例：不写 deleteBackspace/deleteDeletekey/deleteSelection 三个方法，写 delete(PositionStart, PositionEnd) 一个。
- 自检三问：覆盖我当前所有需求的最简单接口是什么？（不减能力而减方法数，多半在造更通用的方法）这个方法会在多少场景被使用？（只服务一个特定用途 = 太专用）这个 API 对我当前需求好用吗？（要写很多附加代码才能用 = 太通用）。
- 通用接口的优势：更简单；类之间分离更干净。

### 第 7 章 Different Layer, Different Abstraction
- 设计良好的系统里每一层提供不同的抽象。
- Pass-through method（直通方法）：几乎只做"调用另一个方法"；说明相邻两层抽象相似。
- 🚩 Red Flag: Pass-Through Method——类之间没有清晰的责任划分。
- 见到直通方法要问"每个类各自负责哪些功能/抽象？"——多半有重叠；解法：把低层类直接暴露给高层类的调用者；在类间重新分配功能；合并类。
- 接口重复不总是坏事：dispatcher（分发器）这类情况可以接受。
- 装饰器也会造成跨层 API 重复（扩展功能却提供相同/相似 API），容易过度使用产生大量浅类；替代：把功能直接加进底层类、与现有装饰器合并、做成独立类。
- Pass-through variable（直通变量）：一个变量穿透很多层方法（如命令行传入的证书参数）；增改成本高，尽量避免。
- 消除直通变量的办法：高低层共享对象；全局变量（引入新问题）；首选 context object（把应用全局状态集中存上下文对象、构造时注入引用）——但 context 也有与全局变量类似的"这东西在哪被用了？"的问题。
- 结论：每件设计基础设施（接口、参数、函数、类）都增加复杂度，因此每个元素消除的复杂度必须多于它创造的；抽象相同的两层很可能补偿不了其基础设施成本。

### 第 8 章 Pull Complexity Downwards
- 模块有简单接口比有简单实现更重要；与模块功能相关的复杂度尽可能在模块内处理。
- 配置参数是"把复杂度推给用户"的典型：与其内部决策，导出参数让用户指定；借口是"用户更懂自己的领域"，实质常是逃避处理重要问题。
- 例子：网络协议处理丢包，重试间隔可以是配置参数，也可以基于成功传输的响应时间自动计算——后者把复杂度拉下来。
- 问自己："用户能选出比我们在这里算出的更好的值吗？"——尽量少用配置参数；不可避免时提供好默认值，只在例外情况才需要设置。
- 把复杂度拉下来的前提（三条同时满足）：拉下来的复杂度密切相关；能在应用其他地方带来许多简化；能简化该类的接口。
- 格言：宁可自己多受一点苦，也要减少用户的苦。

### 第 9 章 Better Together Or Better Apart
- 分合的目标是整个系统的复杂度最小；把系统切成大量小组件未必好：组件数量本身就是复杂度来源；分拆产生管理组件的额外代码；分拆造成分离（方法落到不同类甚至文件）；分拆可能导致重复。
- 代码相关的信号：共享信息；总是一起使用；不看懂另一块就难懂这一块——相关代码放一起更好。
- 共享信息即相聚：特定信息被两个方法/类需要 → 把它们放一起。
- 🚩 Red Flag: Repetition——重复代码说明你还没找到正确的抽象。
- 结论：选择信息隐藏最好、依赖最少、接口最深的结构。

### 第 10 章 Define Errors Out Of Existence
- 异常处理天生难写：异常代码可能比主逻辑还大；异常代码很少被执行、更难测试 → 易藏 bug。
- 过度防御式编码导致不必要的异常；异常是类接口的一部分，影响调用方；抛异常容易、处理异常难。
- 定义掉错误（define errors out of existence）：改方法定义使其不需要异常；例：unset 删变量——定义 1"不存在则抛异常" vs 定义 2"确保变量不再存在"，定义 2 无需异常。
- 消除不了的就地在低层掩盖（mask）异常以限制影响；不可恢复的错误直接崩溃（crash）是合理的。
- 结论：特殊情况（如异常）让代码更难懂；能重定义语义消除错误条件就消除。

### 第 11 章 Design It Twice
- 对每个问题总是考虑多个设计方案；都不满意就组合或再想新的。

### 第 12-13 章 注释
- "好代码自文档"只是部分成立：好命名能减少注释需求但不能替代；有些信息只能存在于注释里——调用方法的前置条件、设计决策、接口的非正式方面（高层行为描述）；抽象只有当用户不必读实现就能用时才有意义，注释提供这个信息。
- "没时间写注释"不成立：好文档的收益很快超过投入；"注释会过时"：只有代码变才需要跟着改，code review 应帮助发现 stale 注释。
- 好注释捕获设计者脑中、无法写进代码的信息，让未来修改变容易。
- 注释应描述代码中不明显的东西；使用者应能只看外部可见声明（不必读代码）就理解模块抽象。
- 注释四类：接口注释（类/方法前，描述抽象与行为、副作用、异常）；数据结构成员注释（字段旁）；实现注释（代码内，讲内部怎么工作）；跨模块注释（描述跨模块边界的依赖）。
- 🚩 Red Flag: Comment that repeats code——复述代码的注释是坏注释。
- 低层注释补充精确性：单位、边界含端点与否（inclusive/exclusive）、不变量（invariants）。
- 高层注释增强直觉：帮读者理解代码的意图与结构。
- 接口文档：提供使用类/方法所需的信息。

### 第 14-15 章 命名与先写注释
- 🚩 Red Flag: Vague Name——名字含糊的变量更容易被误用。
- 🚩 Red Flag: Hard to pick name——给变量/方法找不到简单名字，说明设计可能不干净。
- 命名要在整个应用内一致。
- 先写注释（write the comments first）：写注释可以是设计过程的一部分；好处：注释更好（聚焦方法的抽象，编码测试中会发现问题并修正）；设计更好（提前验证抽象）；写注释更愉快。
- 🚩 Red Flag: Hard to describe——难以写出简单完整的注释时，设计可能有问题。

### 第 16-18 章 修改、一致性、直白
- 修改现有代码时永远想一想：改完后当前系统设计是否仍是最好的。
- 一致性创造认知杠杆、减少错误；一致性范畴：命名、编码风格（组织内风格指南）、接口（一个接口约束多实现，懂一个就懂其他）、设计模式。
- 保障一致性：把规则和风格指南写成文档并定期 review；强制执行（能自动就自动，否则 code review）；不要改既有约定——要改就得把旧的全替换，确认值得。
- 代码应 always obvious（读一眼就明白做什么）；你的代码只有对别人 obvious 才算 obvious。
- 🚩 Red Flag: Nonobvious code——代码含义与行为无法被快速理解就改它。
- 让代码更难懂的：事件驱动编程（控制流难以跟随）、泛型容器（无名 tuple）、违反读者预期的代码。
- 软件应为易读而设计，不是为易写。
- 让代码 obvious 三法：减少所需信息量；利用读者在其他语境已获得的信息（惯例与预期）；用好的名字或注释把重要信息呈给读者。

### 第 19-20 章 趋势与性能
- OO 与继承：依赖注入优于继承——接口是朋友，继承不是。
- 敏捷：开发增量应该是抽象（abstractions）而不是功能（features）；花时间做干净且"略微通用"的设计。
- 单元测试：让开发者更敢于重构和做结构改进，从而改进系统设计。
- TDD 的问题：把注意力放在"让功能完成"而非"拿到最好设计"。
- 设计模式：当自定义方案更干净时，不要硬把问题塞进设计模式。
- 挑战一切新范式：始终从复杂度的立场审视。
- 性能：简单不仅能改进设计，通常还让系统更快；复杂代码倾向于慢，因为它做了多余或冗余的工作。

来源: research/raw/articles/methodology-apsd-oehler.md（原始 URL: https://www.oehler.dev/posts/a-philosophy-of-software-design-summary）

---

## methodology-branch-by-abstraction.md

- 定义：Branch By Abstraction 是一种以渐进方式对软件系统做大规模变更的技术，变更进行期间仍可照常定期发布系统。
- 术语来源：技术早已存在但无名；Paul Hammant 在倡导 Trunk-Based Development 时命名（他注明原始提出者是 Stacy Curl）。
- 步骤 1：起点是系统多处依赖一个想替换的模块/库/框架（supplier）。
- 步骤 2：创建一个抽象层（abstraction layer），捕获"某一段客户端代码与当前 supplier 之间的交互"。
- 步骤 3：把这段客户端代码改为完全通过抽象层调用 supplier。
- 步骤 4：逐渐把所有客户端代码迁到抽象层，直到与 supplier 的全部交互都走抽象层；迁移过程中顺手通过该抽象层改进 supplier 的单元测试覆盖。
- 步骤 5：用同一抽象层构建一个新 supplier，实现客户端某一部分所需的功能；就绪后把这部分客户端切到新 supplier。
- 步骤 5 附注：建新 supplier 期间可用 Feature Flags 在测试环境运行它，与有缺陷的旧 supplier 对比行为。
- 步骤 6：逐渐替换直到所有客户端都用新 supplier；旧 supplier 不再需要时删除；迁移完成后也可以选择删掉抽象层本身。
- 变体：有时无法只给部分客户端切换、必须一次性全切；有时可把 supplier 的功能拆成多个子组件，逐个子组件走完整个流程。
- 不变主题：用抽象层允许多个实现在系统内共存；用"一个抽象 + 多个实现"执行实现间的迁移；确保系统全程可构建可正确运行，从而替换期间可持续做 Continuous Delivery；尽可能寻找一切让变更渐进化的方法。

来源: research/raw/articles/methodology-branch-by-abstraction.md（原始 URL: https://martinfowler.com/bliki/BranchByAbstraction.html）

---

## methodology-characterization-test.md

- 定义：characterization test（又称 Golden Master Testing）= 描述（刻画）一段既有软件"实际行为"的测试，借此通过自动化测试保护遗留代码的既有行为不被无意改变；术语由 Michael Feathers 创造（出自《Working Effectively with Legacy Code》）。
- 目标：验证对参考版本的修改没有以不想要/不理想的方式改变其行为；为缺乏足够单元测试的代码提供扩展与重构的安全网。
- 理论定位：在 James Bach 与 Michael Bolton 的 test oracle 分类中属于 historical oracle（历史谕示）。
- 与传统断言测试的颠倒关系：传统测试检查"个别属性取特定值"（白名单），characterization 测试检查"没有任何属性被改变"（黑名单）；不比较单个值/属性，而是把被测过程整体的复杂结果与前一版本的同一结果比较。
- 创建方法：观察给定输入下出现什么输出；把观察到的输入-输出对写成断言（例：观察到 f(3.14) == 42，就把它写成测试）；此后系统被修改后重跑测试即可发现行为变化。
- 覆盖策略：不可能为每个输入输出对写测试；可选用语句覆盖或分支覆盖；即便这也难做到时要靠判断力；通常只覆盖"已知会发生的输入输出"就够，特别关注边界情况（edge cases）。
- 与回归测试的区别：不验证代码"正确"的行为（往往无法判定），只验证"写测试当时观察到的行为"；没有规格和测试套件时它是唯一选择——保守路径是假定旧行为即所需行为。
- 本质是 change detector（变更探测器）：检测到的变化是否符合预期/是否理想，由分析结果的人判断。
- 自动化生成：因为基于既有代码，可以自动生成——用大量相关/随机输入执行既有代码、记录输出（或状态变化）、生成一组 characterization tests；新版本跑这些测试时若有行为改变即告警。
- GUI 层应用：可与 intelligent monkey testing 结合生成捕获用例与特殊用例的复杂测试。
- 优点 1：对复杂遗留系统相对容易实现；从而"使重构成为可能"。
- 优点 2：对 PDF、XML、图片等复杂结果类型是合理方案——用断言检查全部相关属性不现实且会产生不可读/不可维护的测试代码。
- 缺点 1：依赖可重复性（repeatability）；易变与非确定性值必须从 Golden Master 和被测结果中遮蔽/移除；要移除的元素太多或太复杂时该法不可行。
- 缺点 2：不仅要求软件可重复，还要求环境与输入值稳定。
- 缺点 3：不蕴含结果正确——只帮助发现软件改动的非预期效应。

来源: research/raw/articles/methodology-characterization-test.md（原始 URL: https://en.wikipedia.org/wiki/Characterization_test）

---

## methodology-cleanarch-ndepend.md

- 一句话版本：Clean Architecture 是组织代码库的一种方式——业务规则居于中心，其他一切关注点（数据库、Web 框架、UI、消息总线）通过接口依赖这些规则，方向永不反过来；这就是模式的全部，其余都是让它在真实 .NET solution 增长过程中保持成立的手段。
- 价值主张：用 Clean Architecture 可设计出低耦合、独立于技术实现细节（数据库/框架）的应用 → 易维护、易变更、天然可测试。
- 背景问题：separation of concerns 谁都会说，但实践难——业务逻辑频繁泄漏到 UI，UI 概念（颜色、标记语言、字号）混进业务逻辑，加上数据访问更加纠缠。
- 传统分层方案：Data Access Layer（DAL）+ Business Logic Layer（BLL/domain/core）+ UI/presentation layer。
- 传统分层缺陷 1（数据库中心）：依赖方向 presentation → BLL → DAL，按同心圆重排后数据访问层居中；执行时序上合理（请求 → 业务 → 持久化），但编译期依赖也照此流动就会受害。
- 受害具体表现：与特定数据库厂商耦合（作者 SQL Server 转 Oracle 的亲身经历）；业务代码一旦认识 SqlConnection/SqlCommand/特定 schema，就开始向这些概念漂移——领域方法的参数只因表列存在而存在、校验规则跑到 SQL 所在处、若干版本后"业务层"实际是数据库的薄包装，真正的业务规则无处安放。
- 传统分层缺陷 2（伤害可测试性）：数据访问与纯计算代码混在一起 → 想测逻辑就得打数据库：慢、难 setup、不可预测；手动探索测试同样受害（引 Cockburn：数据库一宕机/一重构，程序员就没法干活，造成延迟成本与人际坏情绪）；UI 逻辑同理难以独立测试；分层到位可让 UI 与业务两个团队分开开发。
- 历史脉络：Robert C. Martin 2011 年首次提及，2012 年更正式的著名文章；其自我定位不是新发明，而是整合 onion architecture、hexagonal architecture 等先前思想并建立共享词汇。
- 四层定义：Entities（DDD 意义的业务对象）；Use Cases（用户可在应用中执行的操作）；Interface Adapters（连接外部世界与用例/实体的桥：models、views、presenters、repository 实现）；Frameworks and Drivers（外部代理：web、数据库等）。
- Dependency Rule：所有依赖指向内层；entities 层不知道应用中任何其他层——外层任何变化都不应导致它变化，反之 entities 层变化会波及外层；层数可按需增减，依赖规则不能破。
- 实现机制是 Dependency Inversion Principle（SOLID 的 D）；没有它 Clean Architecture 就是一张没有牙齿的漂亮图；有了它，代码库可毫秒级单测、换数据库不用重写业务逻辑。
- DIP 具体手法：use cases 层声明自己需要的接口（如 IOrderRepository）并永远不知道谁实现它；infrastructure 层引用 use cases 层来实现该接口——箭头因此指向内部。
- 关键一招："在需要抽象的地方声明抽象，而不是在实现抽象的地方声明"——这是 clean architecture 与"活不过真实项目"的分层图的区别。
- 典型 .NET solution 结构：MyApp.Domain（无项目引用）← MyApp.Application（只引用 Domain）← MyApp.Infrastructure（引用 Application）← MyApp.Web（引用 Application，仅在启动时引用 Infrastructure）+ 对应 tests 项目。
- Domain 纯度检验：只含业务纯 C# 类（Order、Money、EmailAddress、领域事件、不变量），零 EF 特性、零 [Table]、零 [JsonPropertyName]、零 ASP.NET 引用——"如果 Domain 只对 BCL 编译、零第三方引用，你就走对了"。
- 非贫血（non-anaemic）实体的样子：私有构造器、集合以只读暴露、工厂方法执行不变量（Order.Place 校验至少一行再置状态）；对照"带 public setter 和 Id 的 record"——很多"clean"代码库规则散落各 service，正是实体没扛起责任。
- Application 层：通过 use case 编排 domain，声明它需要的外部接口；CQRS 风格为 command/query handler，否则为 application service；handler 依赖的三个抽象全部住在 Application，不沾一行 EF/ASP.NET——单测只需给三个接口供 fake。
- Infrastructure 层：住着乱糟糟的现实——EF Core、Dapper、Service Bus、SendGrid、Stripe、文件系统、HttpClient、Redis；每个 adapter 实现 Application/Domain 声明的接口；好习惯：实现标 internal，Infrastructure 之外无人需要知道它们存在。
- Presentation 层：controllers、minimal API 端点、Razor、Blazor、gRPC、SignalR；composition root（Program.cs）是唯一同时知道 Application 与 Infrastructure 的地方（DI 容器在此接线）。
- 端点应是三行胶水：真正的工作（含领域不变量）都推向内部——测试不需要 HTTP 上下文、数据库或时钟。
- 常见坑 1：Domain 实体上有 EF Core 特性——[Required]、为 lazy loading 加 virtual、"EF 需要所以加"的无参公共构造器，都让依赖指错方向；应在 Infrastructure 用 fluent IEntityTypeConfiguration<T>，保持 Domain 纯净。
- 常见坑 2：贫血实体——Order 只是 public setter 口袋、规则全在 OrderService，分层就只是"多了几步的文件夹"；把不变量推进实体本身。
- 常见坑 3：永远只有单一实现的接口——不是每个类都需要抽象；只在跨越边界（数据库、网络、时间、随机性、文件系统、外部 API）时引入；同一层内直接调用类。
- 常见坑 4：DTO 进了 Domain——wire model/view model 属于 Presentation；Domain 类型一旦被序列化为 JSON，每个公共属性都成了 wire 契约。
- 常见坑 5："Common" 项目——人人引用的共享项目是分层的坟场：先积累 utilities、再 DTO、再领域原语、最后整个迷你应用；要共享内核就放进 Domain 并接受纪律。
- 常见坑 6：无视循环依赖——本模式生死系于无环依赖；每次 commit 跑静态分析、build 遇环即失败，没有商量余地。
- 用静态分析守护架构：把依赖规则编码成规则（枚举四层 + 禁止依赖清单，如 Domain→Application、Domain→Infrastructure、Application→Infrastructure/Presentation 等），CI 破规即挂；依赖矩阵/依赖图让分层一眼可见，趋势图能看出架构是否在逐版本腐烂。
- Clean Architecture vs N-Tier vs Vertical Slice 对比：组织原则（技术分层 / 技术分层+依赖倒置 / 按功能 feature）；依赖方向（UI→BLL→DAL / 向内 Infrastructure→Application→Domain / 每 slice 直达 DB 常见）；测试摩擦（高，需数据库 / Domain+Application 极低 / 低到中）；feature 内聚（低 / 中 / 高）；适用（小型 CRUD / 领域丰富、长生命周期产品 / 微服务、聚焦 API）；过度使用风险（紧耦合不可测 / 繁文缛节、过度抽象 / 跨 slice 重复与漂移）。
- 现实答案很少是纯的：模块化单体（每模块内 Clean Architecture、Application 项目内 vertical slices）是完全合理的形态；选择买到最多隔离的边界，越过该点就别再加仪式。
- 何时过度（honest answer）：周末项目、原型、一次性内部工具、小 CRUD 管理页不需要；"对数据库表的薄包装"式系统上四项目方案是只有摩擦没有回报——发单个 ASP.NET Core 项目、拿反馈，复杂度需要时再向外重构。
- 何时值得：多团队触碰、活过五年、非平凡业务规则、未来可能更换主要基础设施的系统——正是捷径复利最快的系统。
- FAQ：与 onion（Jeffrey Palermo, 2008）、hexagonal（Alistair Cockburn, 2005）同族，都是依赖倒置思想；clean 对四环布局最规定性、hexagonal 对 ports 最抽象；.NET 里实现基本相同。
- FAQ：不需要 MediatR 或 CQRS——两者都不属于该模式；MediatR 只是 Application 层内的进程内分发器，CQRS 只是读写模型分岔时的有用拆分；其 pipeline behaviors 真解决你问题时再上。
- FAQ：DTO/视图模型放哪——request/response 模型在 Presentation，内部 command/query 模型在 Application，Domain 类型永不跨线传输；映射发生在边缘。
- FAQ：Domain 该引用 NuGet 吗——越少越好；BCL 没问题，不可变集合包/值对象辅助库可辩护；绑定框架的（EF、ASP.NET、MediatR、AutoMapper）不属于这里。
- FAQ：横切关注点（日志、授权、校验）放哪——接口（IAppLogger<T>、ICurrentUser）在 Application，实现在 Infrastructure/Presentation；用 pipeline behaviors 包 handler 统一施加，不泄漏进 use case。
- FAQ：use case 多大——一个动词（PlaceOrder、CancelOrder、GetOrderById、ListPendingInvoices）；handler 做两件事就拆；超过 150 行的 use case 几乎总是做太多了。
- FAQ：微服务适配吗——适配且特别好：每个服务足够小，四项目开销可管理，架构保护有界上下文不泄漏；但第一天用模块化单体（每模块一套 clean 栈）通常比起微服务舰队更是好起点。

来源: research/raw/articles/methodology-cleanarch-ndepend.md（原始 URL: https://blog.ndepend.com/introduction-clean-architecture/）

---

## methodology-cleanarch-softengbook.md

- 定位：Clean Architecture 是 Robert Martin（Uncle Bob）提出的架构模式，目标：可复用性（reusability）、内聚（cohesion）、技术独立性（technology independence）、可测试性（testability）；按本书分类属于分层架构（layered architecture）。
- 中心层两类业务类：Entities 与 Use Cases。
- Entities：组织内多个系统共享的类（大学例：Student、Instructor、Course、Department 出现在学术、财务、拓展多个系统）；除数据外还可实现通用业务规则（例：每位 Instructor 必须恰好属于一个 Department）。
- Use Cases：实现系统域相关操作的类（例：为课程建新班、学生选课、取消选课、记录上课内容）。
- 第三层 Adapters：调解最外层 External Frameworks 与中心层（Use Cases/Entities）的交互；REST API 例：adapter 实现 API 端点——接收请求转发给对应 use case，并把 use case 的返回结果反向转换成 JSON 文档发给前端。
- 最外层 External Frameworks：来自库、框架、外部系统的类——数据库、发邮件库、支付提供商访问库、硬件通信库等（例：第三方信用卡支付处理类位于最外层）。
- 原书第 22 章引文："The frameworks and drivers layer is where all the details go. The web is a detail. The database is a detail. We keep these things on the outside where they can do little harm."
- Dependency Rule：给定层的类不应引用任何在外层实现的类；原书强调引文："Nothing in an inner circle can know anything at all about something in an outer circle. In particular, the name of something declared in an outer circle must not be mentioned by the code in an inner circle. That includes functions, classes, variables, or any other named software entity."
- 推论：中心层更稳定（更少变化）——entities 几乎不需修改；use cases 有时需更新，但不应因所用技术（数据库、框架、库）的变化而更新；Dependency Rule 确保 entities 与 use cases 对任何具体技术和外部框架保持干净。
- 控制反转（IoC）场景：外→内的控制流天然合法（外层方法创建内层对象并调用）；当 use case 需要调用外层实现（如 MailServiceImpl.send）时，内层不得声明外层类型的变量（违反依赖规则）——解法：在 use case 层定义 MailServiceInterface 接口作为抽象，MailServiceImpl 实现该接口；这不违规，因为是外层类在使用内层定义的代码元素（接口）。
- 结论（模式拆解）：Clean Architecture 综合了内聚、耦合、关注点分离等设计性质，SRP、DIP 等设计原则，以及 Adapter 设计模式。
- 实施建议三步：先想 Entities（主要存数据、可被未来其他系统复用的类）；再聚焦 Use Cases（实现与 Entities 相关的业务规则），并确保 Entities/Use Cases 两类类保持技术无关（"Web 是细节，数据库是细节"）；最后设计 Adapter 类——作为内部类与外部世界通信的翻译器。
- 总效果：把业务兴趣（business interests）与技术兴趣（technology interests）两类需求分开 → 系统更易测试、更易适配未来新技术。

来源: research/raw/articles/methodology-cleanarch-softengbook.md（原始 URL: https://softengbook.org/articles/clean-architecture）

---

## methodology-cleancode-cheatsheet.md

- 总定义：代码干净 = 团队里每个人都能容易看懂；干净代码可被原作者之外的开发者阅读和增强；可理解性带来可读性、可变更性、可扩展性、可维护性。
- 通用规则（7 条）：遵循标准约定；KISS——越简单越好，尽可能降低复杂度；童子军规则（Boy Scout Rule）——让营地比你来时更干净；永远找根因（root cause）；遵循最小惊讶原则（Principle of Least Surprise）；不重复自己（DRY）；不要关闭安全机制（safeties）。
- 设计规则（6 条）：可配置数据（如常量）保持在高层，易于更改；优先用多态而非 if/else 或 switch/case；把多线程代码分离出来；防止过度可配置化；使用依赖注入；遵循迪米特法则（Law of Demeter）——一个类只应知道它的直接依赖。
- 可理解性建议（6 条）：保持一致——同一类事用同一种做法；使用解释性变量（explanatory variables）；封装边界条件（boundary conditions 难以跟踪，其处理应集中一处）；优先用专门的值对象（value objects）而非原始类型；避免逻辑依赖——不要写"依赖同类中其他东西才能正确工作"的方法；避免否定式条件。
- 命名规则（6 条）：选描述性且无歧义的名字；做有意义的区分；用可发音的名字；用可搜索的名字；用命名常量替代魔法数字；避免编码——不要附加前缀或类型信息。
- 函数规则（6 条）：短小；只做一件事并做好；用描述性名字；参数越少越好（尽量不超过 3 个）；无副作用；不用 flag 参数——拆成多个可被客户端独立调用的方法。
- 注释规则（8 条）：永远先尝试用代码自我解释，不行才花时间写好注释；不要冗余（反例 `i++; // increment i`）；不加显而易见的噪音；不用收括号注释（` } // end of function`）；不要注释掉代码——直接删；注释可用于表达意图（explanation of intent）；澄清代码（clarification）；警示后果（warning of consequences）。
- 源码结构规则（10 条）：概念垂直分离；相关代码垂直紧凑；变量声明靠近使用处；相互依赖的函数靠近；相似的函数靠近；函数按"向下方向"排布；行宽保持短；不用水平对齐；用空白关联相关事物、隔开弱相关；不要破坏缩进。
- 对象与数据结构规则（9 条）：隐藏内部结构；优先用数据结构；避免半对象半数据的混合结构；保持小；只做一件事；实例变量要少（太多说明类做多件事了）；基类不应知道其派生类的任何事；宁可多写几个函数也不要"把代码传进函数来选择行为"；非静态方法优于静态方法。
- 测试规则（9 条）：每个测试一个断言；快；相互独立；可重复；自验证（self-validating）；及时（timely）；可读；易于运行；使用覆盖率工具。
- 代码坏味道（6 条）：Rigidity 僵化——软件难以改动，小改引起一连串后续修改；Fragility 脆弱——单一改动导致多处破坏；Immobility 固化——因风险和成本太高无法在其他项目复用代码片段；Needless Complexity 无谓复杂；Needless Repetition 无谓重复；Opacity 不透明——代码难以理解。
- 错误处理规则（4 条）：不要把错误处理与代码逻辑混在一起；用异常而非返回错误码；不返回 null、也不传递 null；抛出的异常要带上下文。

来源: research/raw/articles/methodology-cleancode-cheatsheet.md（原始 URL: https://gist.githubusercontent.com/cedrickchee/55ecfbaac643bf0c24da6874bf4feb08/raw）

---

## methodology-cleancode-summary.md

- 与 cedrickchee gist 同源的《Clean Code》摘要（wojteklu 版），总定义相同：干净 = 团队每个人容易看懂；可被他人阅读增强；可理解性带出可读/可变更/可扩展/可维护。
- 通用规则（此版仅 4 条）：遵循标准约定；KISS（越简单越好、尽量降复杂度）；童子军规则；永远找根因。（未含最小惊讶原则、DRY、safeties 三条）
- 设计规则（6 条，与另一版相同）：可配置数据在高层；多态优先于 if/else 与 switch/case；分离多线程代码；防止过度可配置；依赖注入；迪米特法则（类只知其直接依赖）。
- 可理解性（6 条，相同）：一致；解释性变量；封装边界条件；值对象优先于原始类型；避免逻辑依赖；避免否定式条件。
- 命名（6 条，相同）：描述性且无歧义；有意义区分；可发音；可搜索；命名常量替代魔法数字；避免编码前缀。
- 函数（6 条，相同）：短小；只做一件事；描述性命名；参数尽量少；无副作用；不用 flag 参数（拆成多个独立方法）。
- 注释（8 条，相同）：先用代码解释自己；不冗余；不加噪音；不用收括号注释；不注释掉代码（删掉）；用于意图解释；用于代码澄清；用于后果警示。
- 源码结构（10 条，相同）：概念垂直分离；相关代码垂直密集；变量靠近使用处声明；依赖函数靠近；相似函数靠近；函数向下排布；短行；不用水平对齐；空白用于关联/隔离；不破坏缩进。
- 对象与数据结构（9 条，相同）：隐藏内部结构；优先数据结构；避免混合结构；小；只做一件事；实例变量少；基类不了解派生类；多函数优于传代码选行为；非静态方法优先。
- 测试（此版 5 条）：一个测试一个断言；可读；快；独立；可重复。（不含 self-validating / timely / 易运行 / 覆盖率工具）
- 代码坏味道（6 条，相同）：Rigidity、Fragility、Immobility、Needless Complexity、Needless Repetition、Opacity。
- （此版无"错误处理"一节。）

来源: research/raw/articles/methodology-cleancode-summary.md（原始 URL: https://gist.githubusercontent.com/wojteklu/73c6914cc446146b8b533c0988cf8d29/raw）

---

## methodology-definition-of-refactoring.md

- 名词定义（原书两条定义之一）：Refactoring（名词）= 对软件内部结构所做的修改，使其更易理解、修改成本更低，且不改变其可观察行为（observable behavior）。
- 动词定义：Refactoring（动词）= 通过应用一系列（小的）重构手法来重组软件，且不改变其可观察行为。

来源: research/raw/articles/methodology-definition-of-refactoring.md（原始 URL: https://martinfowler.com/bliki/DefinitionOfRefactoring.html）

---

## methodology-fowler-refactoring-workflows.md

- 总问题：多数团队声称常做重构，却不了解重构可融入的不同工作流（workflows），因此错过把重构更深嵌入开发活动的机会。
- TDD Refactoring：重构常在 TDD 语境中被教授，即 red-green-refactor 循环——(1) 加一个针对尚未实现功能的测试（specification by example），变红；(2) 用最简单（可以粗糙）的实现让它变绿；(3) 用重构让已实现功能的整体代码库尽量干净。
- Two Hats（两顶帽子）隐喻（源自重构早期）：重构帽——每个改动都是小的行为保持（behavior-preserving）改动，只在测试全绿时重构，任何测试变红都说明出了错；串起小步可以更快、更低风险，因为不会陷入 debugging。加功能帽——其余一切改动（加新测试、打破既有测试都是正常的），不限于行为保持，但明智的做法仍是小步并尽快回到绿。
- 两顶帽子的纪律：编程中可以频繁换帽（也许每几分钟一次），但一次只能戴一顶；分开两步使工作专注——让测试通过时只想功能不想结构，变绿后再在安全的小步重构模式里专心设计。
- Litter-Pickup Refactoring（顺手捡垃圾）：在代码库里遇到烂区块（能力不足的开发者写的、高手状态差时写的、半年前自己不懂事写的），顺手清理——下次再碰它时更快；常被称为 camp site rule（营地规则）：让代码比你发现时更好。
- Comprehension Refactoring（理解性重构）：Ward Cunningham 的解释——每当你必须搞清楚一段代码在干什么，你就在脑中建立了一些理解；建立之后应把这份理解移入代码，让后人不必再从头在脑中重建。（作者注：可论证它是 litter-pickup 的一种，但触发点不同所以视为不同类。）
- 机会式重构的公共流程：时刻留意不合格的代码（团队学习后，几个月前写的代码也会显得差）；简单修复或有利于当前功能时立即修；重构必须在测试全绿（stable code-base）的代码库上进行——可用版本控制 stash 当前工作或暂时禁用导致失败的在制品；用重构清理问题代码；若重构拖得超出合理长度，stash 起来稍后回来；若当下做太费力或工作不好 stash，记下笔记、做完功能后再做。
- 完成的标准：把功能做完还不够——你必须让你碰过的代码干净（至少比发现时更干净）；注意两顶帽子之间行动的分离，这种分离有助于专注。
- Preparatory Refactoring（预备性重构）：开始加新功能时发现既有结构与将做的事不合——先戴着重构帽把既有代码重构成"现在已知道是对的形状"，再加功能；常能让整体交付快于不做准备的直接加（刷漆前刮墙贴胶带的类比：不是刷漆但让刷漆更快、漆面更持久）。
- Planned Refactoring（计划式重构）：团队用"refactoring stories"之类的机制把重构排进计划，修需要专门投入的大型问题区。
- Planned 的警告信号：计划式重构是多数团队的必要组成，但也是"其他工作流做得不够"的信号——若你的重构大部分只发生在计划工作中，那是坏味道，应考虑如何把其他重构工作流融入日常工作。
- Long-Term Refactoring（长期重构）：有些重组超出单次开发周期、跨越多个月（替换大模块、更换持久化框架、解开依赖纠缠）；仍可用重构完成——团队就"粗略的最终状态"和"到达那里的粗略计划"达成一致，然后在日常工作中顺手做朝目标方向推进的重构；因为所有变更都是重构，代码库在加功能的同时始终保持可工作状态；常用技术是 Branch By Abstraction（用支持当前实现与替换实现的抽象层）。
- 经济学辩护（回答"重构是浪费的返工吗"）：重构让代码更易理解 → 后续变更更快更便宜；预备性重构在做它所预备的功能时就能回本；除非确信以后能靠更快的工作收回投资，否则不要重构；重构应与加功能结合进行——用重构把东西弄干净，但不要试图一次彻底修好，关键是多次经过代码库的渐进改进。
- 总汇：最有效地使用重构需要把全部工作流无缝结合进开发工作；代码库难以理解和修改就是在拖慢你——这是需要更多重构的信号；对多数团队这意味着在日常（day-to-day）工作流中投入更多，引入持续改进。
- 六种工作流全名：TDD Refactoring / Litter-Pickup Refactoring / Comprehension Refactoring / Preparatory Refactoring / Planned Refactoring / Long-Term Refactoring。
- 逻辑链：Refactoring → Clean Code → Faster Delivery。

来源: research/raw/articles/methodology-fowler-refactoring-workflows.md（原始 URL: https://martinfowler.com/articles/workflowsOfRefactoring/fallback.html）

---

## methodology-github-review-ai-code.md

- 背景定位：审查 Copilot、ChatGPT 等 AI 工具生成的代码正成为现代开发者工作流的必备部分；对遗留代码库和大型 PR 尤其需要彻底的 review 流程；人力专长 + 自动化工具结合才能保证 AI 代码达到质量标准、对齐项目目标与最佳实践。
- 第 1 步 功能检查先行：永远先跑自动化测试和静态分析；确认代码可编译、全部测试通过、检查新增警告/错误；用 CodeQL 与 Dependabot 抓漏洞和依赖问题；用 GitHub Code Quality 抓可靠性/可维护性问题并看覆盖率。
- 第 1 步示例 prompt：问"验证这次变更缺哪些功能测试？""这段代码可能引入哪些漏洞或安全问题？"
- 第 2 步 验证上下文与意图：检查 AI 代码是否契合项目目的与架构；对照需求与设计模式审查产出；自问"这段代码解决的是对的问题吗？遵循我们的约定吗？"
- 第 2 步上下文喂法：用 README、文档、近期 PR 作为给 AI 的起点上下文；告诉 AI 哪些来源可信、哪些不要用、给它好例子；把 AI 的研究/规划产出提炼成结构化工件（structured artifacts），作为后续 AI 任务（如代码生成）的上下文。
- 第 3 步 评估代码质量：在自动工具之上，人的标准仍然重要——看可读性、可维护性、清晰命名。
- 第 3 步红线：不要接受"难以跟随"或"重构比重写还慢"的代码；偏好文档完善、注释清晰的代码。
- 第 4 步 细查依赖：对新包/新库保持警惕——确认依赖真实存在且在被积极维护；考察来源与贡献者是否可信、非竞争性；审查许可证兼容性（例：MIT 项目里引入 AGPL-3.0，或无声明许可证的依赖）。
- 第 4 步 AI 特有威胁：警惕幻觉或可疑包（并不存在的包）、slopsquatting（利用假/恶意包对 LLM 发起的攻击）；Copilot 给的包设置也要自己验证；用 Copilot 检查与公开代码的匹配。
- 第 5 步 AI 特有的坑：找幻觉 API、被忽略的约束、错误逻辑；警惕"测试被删除或跳过而不是被修复"；对"看起来对"但与你意图不符的代码保持怀疑。
- 第 5 步示例 prompt：问"删掉失败测试的理由是什么？给出修好测试而不是删掉它的替代方案。""这段代码可能没正确处理哪些复杂情形、边角案例、场景？""这段代码提出了哪些需要人类判断或领域专长才能评估的技术问题？"
- 第 6 步 协作 review：请队友审复杂或敏感变更；用 checklist 确保关键 review 点（功能、安全、可维护性）全覆盖；在团队内分享成功的 prompt 与模式。
- 第 7 步 能自动化就自动化：CI 检查风格、lint、安全、代码质量、覆盖率；Dependabot 做依赖更新与告警；CodeQL 或同类扫描器做静态分析；考虑用有推理能力的 AI agent 自动化部分 review——例如构建"自审 agent"按你的标准评估草稿 PR（准确性、语气、业务逻辑），再请求人工审查。
- 第 8 步 持续改进流程：把 review AI 代码的最佳实践写成文档；鼓励团队"AI champion"分享技巧与工作流；更新 onboarding 与贡献指南（用 CONTRIBUTING.md 记录对 AI 生成源码/内容的期望）；参考 Copilot Cookbook 并把有用的 recipe 分享进团队文档。

来源: research/raw/articles/methodology-github-review-ai-code.md（原始 URL: https://docs.github.com/en/copilot/tutorials/review-ai-generated-code）

---

## methodology-google-review-comments.md

- 四句总纲：Be kind（和善）；Explain your reasoning（解释你的理由）；在"给出明确指示"与"只指出问题让开发者自己决定"之间取得平衡；鼓励开发者简化代码或添加代码注释，而不是只向你解释复杂度。
- 礼貌（Courtesy）：保持客气尊重的同时对开发者清晰有帮助；一种做法是"永远评论代码、绝不评论开发者"——尤其要说可能 upsetting 或 contentious 的话时。
- 反例/正例：坏："这里没有任何并发收益，你为什么用线程？"；好："这里的并发模型给系统增加了复杂度，我却看不到任何实际性能收益。既然没有性能收益，这段代码最好用单线程而不是多线程。"
- 解释为什么（Explain Why）：好的例子帮开发者理解你为何提意见；不必每条都解释，但恰当时候给出你的意图、所依据的最佳实践、或你的建议如何改善代码健康。
- 给予指导（Giving Guidance）：修 CL 是开发者的责任不是 reviewer 的——你不必做详细方案设计或替他写代码；但也不应不帮忙：在"指出问题"与"直接指导"之间找平衡。
- 指出问题的好处：帮开发者学习、让 review 更轻松、常带来更好方案（开发者比 reviewer 更贴近代码）；但有时直接指示、建议甚至代码更有帮助。
- 双目标：首要目标是拿到尽可能好的 CL；次要目标是提升开发者技能（使其将来需要的 review 越来越少）。
- 正向强化：人从"做得好的强化"中学习，不只是从"可以更好的地方"；看到喜欢的东西也要评论——开发者清理了混乱算法、加了 exemplary 测试覆盖、或你从 CL 里学到了东西；同样要说明你喜欢的原因，鼓励其延续好实践。
- 给评论标严重度（Label comment severity）：区分"必须改"与"指导/建议"；三个标签——Nit: 小事，技术上该做但影响不大；Optional（或 Consider）: 我认为可能好但非严格必需；FYI: 不指望你在这个 CL 做，但未来可想想；这让 review 意图显式化、帮作者排定各评论优先级。
- 标签的必要性：没有标签时作者可能把所有评论都当强制项，哪怕有些只是信息性或可选——标签避免这种误解。
- 接受解释（Accepting Explanations）：你请开发者解释一段你看不懂的代码时，结果通常应该是他把代码重写得更清晰；偶尔加一条代码内注释也是合适的回应——前提不是在解释过度复杂的代码。
- 原则：只写在 code review 工具里的解释对未来代码读者没有帮助；仅在少数情况下可接受——你在审不熟悉的领域，而开发者解释的是正常读者本来就知道的东西。

来源: research/raw/articles/methodology-google-review-comments.md（原始 URL: https://google.github.io/eng-practices/review/reviewer/comments.html）

---

## methodology-google-review-looking.md

- 前置说明：核对以下每一点时都要结合"The Standard of Code Review"（总体放行原则）。
- Design（设计）：review 最重要的事是 CL 的整体设计——CL 中各部分代码的交互是否合理？这个改动属于你的代码库还是该放库（library）里？它与系统其余部分整合得好吗？现在是不是加这个功能的合适时机？
- Functionality（功能）：CL 做了开发者想做的事吗？开发者想做的事对这段代码的用户好吗？"用户"通常同时指最终用户（受变更影响时）和开发者（将来要"使用"这段代码的人）。
- Functionality 审查姿态：通常预期开发者已充分测试、到达 review 时已能正确工作；但 reviewer 仍应思考边界情况、找并发问题、像用户一样思考、并确保光读代码就能看出的 bug 不存在。
- Functionality 验证时机：变更对用户可见（如 UI 改动）时最重要——光读代码难以理解影响，可让开发者给 demo 或自己打补丁验证。
- 并发审查：CL 中存在并行编程、理论上可能死锁/竞态时要特别想功能——这类问题很难靠运行发现，需要开发者与 reviewer 双方仔细推演；（附注：这也是不要使用可能出现竞态/死锁的并发模型的好理由——它让 review 和理解代码变得非常复杂。）
- Complexity（复杂度）：CL 是否比应有的更复杂？在每个层次检查——单行、函数、类；"太复杂"通常= "代码读者无法快速理解"，也可= "开发者调用或修改这段代码时很可能引入 bug"。
- Over-engineering（过度工程，复杂度的特定类型）：代码比需要的更通用、或加了系统目前并不需要的功能；reviewer 应对过度工程格外警惕（especially vigilant）。
- Over-engineering 的处置原则：鼓励开发者解决"现在就知道需要解决"的问题，而不是解决开发者猜测未来可能要解决的问题——未来问题应该等它到来、能看到真实形态与需求时再解决。
- Tests（测试）：按变更性质要求单元/集成/端到端测试；除紧急情况外，测试应与生产代码在同一个 CL 里加入。
- Tests 质量四问：测试正确、合理、有用吗？代码坏了测试真的会失败吗？代码变化后会产生误报（false positives）吗？每个测试的断言简单有用、且不同测试方法之间分离得当吗？
- Tests 的元规则：测试不会测试它们自己，我们几乎不为测试写测试——必须由人确保测试有效；测试也是需要维护的代码，不能因为是"主二进制之外"就接受测试中的复杂度。
- Naming（命名）：开发者为一切选了好名字吗？好名字 = 长到足以完整传达它是什么/做什么，又不至于长到难读。
- Comments（注释）：注释清晰易懂吗？都真的必要吗？注释通常在解释"代码为什么存在"时有用，不应解释"代码在做什么"。
- Comments 的推论：如果代码不够清晰到能自我解释，应该把代码改得更简单；例外（正则、复杂算法常从"讲做什么"的注释中获益）——但多数注释用于代码本身无法承载的信息，比如决策背后的推理。
- Comments 的存量检查：也看看 CL 之前就有的注释——也许有现在可以删掉的 TODO、或有"劝阻做这个改动"的注释等。
- Comments 与文档的区分：类/模块/函数的文档应表达代码的用途、如何使用、使用时的行为——与行内注释不同。
- Style（风格）：确认 CL 遵循相应语言的 style guide；想提 style guide 之外的改进点时加 "Nit:" 前缀，表示可选不阻塞；绝不要基于个人风格偏好阻塞 CL。
- Style 与变更分离：作者不应把大的风格改动与其他改动混在一起——这会让 CL 里难以看清真正改了什么、使 merge/rollback 更复杂；想重排整个文件应先发一个纯重排 CL，再发功能变更 CL。
- Consistency（一致性）：既有代码与 style guide 冲突时，style guide 是绝对权威——guide 要求的必须遵守；guide 只是建议（recommendations）时是判断题，除非局部不一致太令人困惑，否则倾向遵循 guide；无其他规则适用时与既有代码保持一致；无论哪种情况，都鼓励作者为清理既有代码提 bug 单并加 TODO。
- Documentation（文档）：CL 改变了用户构建/测试/交互/发布代码的方式时，检查是否同步更新了相关文档（README、g3doc 页、生成的参考文档）；CL 删除或废弃代码时考虑文档是否也该删；文档缺失就开口要。
- Every Line（每一行）：一般情况下，逐行看你被指派 review 的所有代码；数据文件、生成代码、大数据结构有时可扫过——但绝不要扫过人写的类/函数/代码块就假定里面没问题。
- Every Line 的分寸：有些代码值得更仔细审查（自行判断），但至少要确保你理解所有代码在做什么。
- 读不懂时的处理：如果代码太难读、拖慢了 review，应告知开发者并等其澄清——Google 聘的是优秀工程师，你也是其中之一；你看不懂的代码，其他开发者多半也看不懂，所以你要求澄清也在帮助未来的开发者。
- 超出资格时：你看得懂但不具备审某部分的资格时（尤其隐私、安全、并发、无障碍、国际化等复杂议题），确保 CL 上有一个够格的 reviewer。
- Exceptions（例外情形）：多名 reviewer 时你可能只被要求审某些文件、或只审某些方面（高层设计、隐私/安全影响等）；此时在评论里注明你审了哪些部分，倾向于 "LGTM with comments"；若要等其他 reviewer 审完其余部分再给 LGTM，也要明确注释设定期望；CL 达到期望状态后尽快响应。
- Context（上下文）：把 CL 放进更宽的语境看——review 工具只显示改动周围几行，有时要看整个文件才能确认改动合理（例：只见新增 4 行，看全文件才发现它们落在一个 50 行、早该拆分的函数里）。
- 系统级语境：也要在"整个系统"层面想这个 CL——它在改善系统代码健康，还是在让系统更复杂、更少测试？不要接受降低系统代码健康的 CL；多数系统通过许多小变更累积变复杂，所以连新变更里的小复杂度都要阻止。
- Good Things（好事）：看到 CL 里的好东西要告诉开发者，尤其当它出色地回应了你此前的意见；code review 常只盯着错误，但同样应给出对好实践的鼓励与欣赏；从 mentoring 角度，告诉开发者"哪里做对了"有时比指出错误更有价值。
- Summary Checklist（总结清单，逐条）：代码设计良好；功能对代码用户有益；UI 变更合理且好看；并行编程安全；代码没有超出必要的复杂度；开发者没有实现"未来可能需要但现在不确定需要"的东西；有合适的单元测试；测试本身设计良好;一切命名清晰；注释清晰有用、多数解释 why 而非 what；文档恰当（一般在 g3doc）；符合 style guide。
- Summary 的行动项：确保逐行审完被指派的代码、看上下文、确保在改善代码健康、并夸奖开发者做的好事。

来源: research/raw/articles/methodology-google-review-looking.md（原始 URL: https://google.github.io/eng-practices/review/reviewer/looking-for.html）

---

## methodology-google-review-standard.md

- 首要目的：code review 的首要目标是让 Google 代码库的整体代码健康（overall code health）随时间持续改善；一切工具与流程都为此设计。
- 需要平衡的张力：一方面开发者必须能推进任务——从不提交改进，代码库就永不改善；reviewer 让任何变更都极难进入，会打消开发者将来做改进的积极性。
- 另一方面：reviewer 有责任确保每个 CL 的质量不使代码库健康度随时间下降；这一点很微妙，因为代码库常在时间压力下走捷径、以许多微小的健康度下降的方式退化；reviewer 对所审代码有所有权与责任（一致性、可维护性等）。
- 最高原则（the senior principle among all guidelines）：一旦 CL 确定能改善所做系统的整体代码健康，reviewer 总体上应倾向批准（favor approving）——即使 CL 并不完美。
- 原则的限制：例如 CL 加了一个 reviewer 不想要的功能，即便代码设计良好，reviewer 也可以拒绝。
- "没有完美代码，只有更好代码"：reviewer 不应要求作者把 CL 的每个小角落打磨完才批准；应权衡"前进的需要"与"所提改动的重要性"；追求的不是完美而是持续改进——一个整体上改善可维护性/可读性/可理解性的 CL，不应因"不完美"被拖延数天或数周。
- Nit 惯例：reviewer 随时可留"这里可以更好"的评论，但不重要时加 "Nit: " 前缀，让作者知道这只是可选的抛光点。
- 底线：本文档的任何内容都不构成"签入确定会恶化系统整体代码健康的 CL"的理由——唯一例外是紧急情况（emergency）。
- Mentoring（辅导功能）：code review 可以承担教学功能（语言、框架、通用软件设计原则）；留下帮开发者学新东西的评论永远没问题——知识分享本身就是改善代码健康的一部分；纯教育性、对达标不关键的评论加 "Nit: " 或注明不强制在本 CL 解决。
- 原则 1：技术事实与数据（technical facts and data）凌驾于观点与个人偏好。
- 原则 2（风格）：style guide 是绝对权威；纯风格问题（空格等）不在 guide 内的属于个人偏好——风格应与现有代码一致；若此前无既定风格，接受作者的。
- 原则 3（设计）：软件设计问题几乎从不是纯风格或纯偏好问题——它们基于底层原则，应按原则权衡而非按个人意见；有时存在几个同样有效的选项，若作者能（通过数据或扎实的工程原则）证明几种方法同样有效，reviewer 应接受作者的选择；否则由标准软件设计原则决定。
- 原则 4（兜底）：无其他规则适用时，reviewer 可要求作者与当前代码库保持一致——只要不恶化整体代码健康。
- 冲突解决第 1 步：开发者与 reviewer 任何时候首先应基于本文档及 CL 作者指南/Reviewer 指南的内容寻求共识。
- 冲突解决第 2 步：特别难达成共识时，面谈或视频会议比在评论区拉锯更有效（若这样做，务必把讨论结果作为评论记录在 CL 上，留给未来读者）。
- 冲突解决第 3 步：升级（escalate）——常见路径：更大范围的团队讨论、Technical Lead 表态、代码 maintainer 决定、Eng Manager 协助；不要因为双方达不成一致就让 CL 一直挂着。

来源: research/raw/articles/methodology-google-review-standard.md（原始 URL: https://google.github.io/eng-practices/review/reviewer/standard.html）

---

## methodology-kiss-wikipedia.md

- 定义：KISS（"Keep it simple, stupid"）是设计原则，美国海军 1960 年首次记录；含义是简单性应成为设计目标；与飞机工程师 Kelly Johnson 关联；"KISS principle" 一词 1970 年已流行。
- 命名细节：缩写据称为 Kelly Johnson（洛克希德 Skunk Works 首席工程师，U-2、SR-71 黑鸟等的设计者）所创；变体 "Keep it Short and Simple" 在 1938 年 Minneapolis Star 已有记载；流行写法带逗号，Johnson 原写法无逗号（"Keep it simple stupid"），许多作者仍用无逗号版。
- 起源故事（原则的最佳例证）：Johnson 给设计工程师团队一小把工具，挑战他们正在设计的喷气机必须能由普通机械师在战地条件下只用这些工具维修——"stupid" 指的是"东西怎么坏"与"可用于修理的复杂程度"之间的关系。
- 使用范围：美军广泛使用（尤其海军与空军），并进入软件开发领域。
- 变体写法：keep it simple, silly / keep it simple and straightforward / keep it simple, soldier / keep it simple, sweetie。
- 思想渊源（极简主义概念家族）：奥卡姆剃刀；"Simplicity is the ultimate sophistication"；莎士比亚"简洁是智慧的灵魂"；密斯·凡·德·罗"Less is more"；Bjarne Stroustrup"Make Simple Tasks Simple!"；Dr. Seuss 论冗余写作；克鲁伊夫"踢简单足球最难"；圣埃克苏佩里"完美不是无可增添，而是无可删减"；Colin Chapman（莲花车队创始人）"Simplify, then add lightness"；爱因斯坦（疑为编者转述）"尽可能简单，但不能更简单"；乔布斯"简化、简化、简化"（简化自梭罗）；帕金森第三定律（约1957）"扩张即复杂，复杂即衰亡——越复杂，死得越快"；Heath Robinson / Rube Goldberg 装置是蓄意过度复杂的"非 KISS"幽默示例。
- 电影动画中的应用：新手动画师会"过度动画"（角色动得太多、做得太多），Richard Williams 与迪士尼九元老都劝动画师"KISS"。
- 软件开发中的相关概念（See also 列表）：DRY、极简主义（Minimalism）、Unix 哲学、Rule of least power、Worse is better（Less is more）、YAGNI 等。

来源: research/raw/articles/methodology-kiss-wikipedia.md（原始 URL: https://en.wikipedia.org/wiki/KISS_principle）

---

## methodology-opportunistic-refactoring.md

- 核心主张：从人们最开始问"重构如何纳入开发过程"（要不要设重构阶段、迭代占比多少、谁来做重构）起，Fowler 的回答是——虽有排期式重构的一席之地，但更鼓励把重构当作机会式（opportunistic）活动：无论何时何地代码需要清理，就由当时在场的人（whoever）清理。
- 具体含义：任何时刻有人看到代码不如它应有的清晰，就应当场（right there and then）或在几分钟内顺手修掉。
- 营地规则（camp site rule）：这种机会式重构常被称为营地规则——永远让代码比你发现时更好；团队人人如此，则每天对代码库健康做出微小而规律的贡献。
- 时机 1（预备性）：开始实现新功能/修 bug 前，发现若把既有类的 API 改个结构、任务会更容易——先把它重构成应有的样子，再加功能。
- 时机 2（去重）：加功能时发现自己要写的代码与既有代码重复——先重构既有代码把重复清理掉再继续。
- 纪律前提：这种对代码的持续关注很重要——但记住只在测试全绿时重构。
- 时机 3（收尾前）：功能做出来了，但发现如果改变与既有类的交互方式会更好——在认为自己"做完"之前抓住这个机会改掉。
- 时机 4（正忙别的事时）：在做到的事的途中看到机会——与其打断当前思路，不如记下来，等就绪再回来；但别拖太久，当天回来、赶在真正"done"之前。
- 对"重构抢功能时间"质疑的回答：重构的全部意义就是让代码库更好用，让团队更快交付价值；不抓住机会重构，代码库逐渐退化，你将面对进度变慢和与赞助方谈"重构迭代"的艰难对话。
- 兔子洞（rabbit hole）风险：修一个又见一个，很快深陷 yak shaving；技能性的机会式重构需要良好判断——知道何时收手；想让代码"完美如愿景"可以等下一次再访；每次都改善一点点，反复叠加会对高频访问区域产生聚焦的大影响——那正是干净代码最值钱的地方。
- 非局部性不是障碍：机会式重构可能命中你正在工作的类之外的类；"缺少局部性"不应阻止你当下就改——把改动留到"改天"的诱惑很大，但改天常常不来。
- 对测试弱的区域要警惕：重构依赖良好的回归测试套件；要碰测试薄弱的部分时，合理做法是顺手补一两个测试（只要别滑进兔子洞太深）；另一个技巧：故意制造一个错误看测试能否抓住，以此感受安全网的成色。
- 流程摩擦警告：警惕任何给机会式重构制造摩擦的开发实践，如强代码所有权（strong CodeOwnership）或 FeatureBranch——这是他对 feature branching 的首要顾虑：分支上的人常被劝阻做机会式重构，因为会让 merge 更难，尤其分支存活超过几天时（脚注：现代工具有帮助，但仍会被语义冲突 SemanticConflicts 绊倒）。
- 组织信号：多数团队重构做得不够，所以要注意任何"劝退重构"的因素；任何时候你感到被劝阻做一个小重构（你确信只要一两分钟），任何这样的障碍都是一个 smell，应触发一次团队讨论——记下这个劝退时刻，至少带进下次回顾会（retrospective）。
- 总立场：重构从一开始就应像写 if 语句一样，是编程中常规、不可分割的一部分——常被误解为"需要计划出来"；确实可以专门安排一两天攻打挡路数月的顽疙瘩，但用好重构的团队几乎不需要计划重构，而是把重构视为持续的小调整流，让项目保持在 DesignStaminaHypothesis 的 happy curve 上。

来源: research/raw/articles/methodology-opportunistic-refactoring.md（原始 URL: https://martinfowler.com/bliki/OpportunisticRefactoring.html）

---

## methodology-pragprog-official-tips.md

《程序员修炼之道》20 周年版官方 100 条 tips 全列表（官方站转载，带页码）：

- Tip 1 Care About Your Craft：在乎你的手艺——除非在乎做好，否则何必以开发软件度过一生。
- Tip 2 Think! About Your Work：关掉自动驾驶、夺回控制，持续批判和评估自己的工作。
- Tip 3 You Have Agency：你有主动权——这是你的人生，抓住它并把它变成你想要的样子。
- Tip 4 Provide Options, Don't Make Lame Excuses：提供选项而非蹩脚借口——别说做不到，说明能做到什么。
- Tip 5 Don't Live with Broken Windows：别与破窗共存——见到坏设计、错误决定、烂代码就修。
- Tip 6 Be a Catalyst for Change：做改变的催化剂——无法强加改变于人，展示未来的可能并帮他们参与创造。
- Tip 7 Remember the Big Picture：记住大局——别沉入细节忘了查看周围正在发生什么。
- Tip 8 Make Quality a Requirements Issue：质量是需求问题——让用户参与确定项目真实的质量要求。
- Tip 9 Invest Regularly in Your Knowledge Portfolio：定期投资知识组合——让学习成为习惯。
- Tip 10 Critically Analyze What You Read and Hear：批判性分析所读所闻——不被供应商、媒体炒作或教条带走，按你与你的项目来分析信息。
- Tip 11 English is Just Another Programming Language：英语只是另一门编程语言——像写代码一样写文档：遵循 DRY、ETC、自动化等。
- Tip 12 It's Both What You Say and the Way You Say It：说什么与怎么说同样重要——好想法不能有效传达就毫无意义。
- Tip 13 Build Documentation In, Don't Bolt it On：文档要内建而非外挂——与代码分开创建的文档更可能不正确、过时。
- Tip 14 Good Design Is Easier to Change Than Bad Design：好设计比坏设计更容易改——对代码而言"设计好"意味着能通过改变来适应使用者。
- Tip 15 DRY—Don't Repeat Yourself：每一份知识在系统内必须有单一、无歧义、权威的表示。
- Tip 16 Make It Easy to Reuse：让复用容易——容易复用人们就会复用；创建支持复用的环境。
- Tip 17 Eliminate Effects Between Unrelated Things：消除不相关事物间的影响——设计自包含、独立、有单一明确目的的组件。
- Tip 18 There Are No Final Decisions：没有最终决定——把每个决定看作写在沙滩上，为变化做计划。
- Tip 19 Forgo Following Fads：别追风潮——Neal Ford："昨天的最佳实践会变成明天的反模式"；基于 fundamentals 而非时尚选择架构。
- Tip 20 Use Tracer Bullets to Find the Target：用曳光弹找靶——通过尝试并观察落点来逼近目标。
- Tip 21 Prototype to Learn：原型是为了学习——其价值不在产出的代码而在学到的教训。
- Tip 22 Program Close to the Problem Domain：贴近问题域编程——用问题域的语言设计与编码。
- Tip 23 Estimate to Avoid Surprises：先估算以避免意外——开工前估算能提前发现潜在问题。
- Tip 24 Iterate the Schedule with the Code：日程随代码迭代——用实现中获得的经验修正项目时间表。
- Tip 25 Keep Knowledge in Plain Text：知识用纯文本保存——纯文本不会过时，有助于杠杆化你的工作并简化调试与测试。
- Tip 26 Use the Power of Command Shells：用好命令 shell——GUI 不够用时用 shell。
- Tip 27 Achieve Editor Fluency：编辑器练到熟练——编辑器是最重要的工具，要能快速准确地让它做你要的事。
- Tip 28 Always Use Version Control：永远用版本控制——版本控制是你工作的时间机器，可以回去。
- Tip 29 Fix the Problem, Not the Blame：修问题不追责——bug 是谁的都无所谓，它仍是你的问题、仍需修复。
- Tip 30 Don't Panic：别慌——对星际搭车客和开发者都成立。
- Tip 31 Failing Test Before Fixing Code：修码前先写会失败的测试——先创建一个能揭示 bug 的聚焦测试再去修。
- Tip 32 Read the Damn Error Message：把错误信息读进去——多数异常都说明了失败的是什么和在哪里，幸运时还有参数值。
- Tip 33 "select" Isn't Broken：别赖 select——在 OS、编译器甚至第三方产品/库里发现 bug 很罕见；bug 最可能在应用里。
- Tip 34 Don't Assume It—Prove It：别假设，要证明——在实际环境里用真实数据和边界条件证明你的假设。
- Tip 35 Learn a Text Manipulation Language：学一门文本处理语言——每天大量时间在处理文本，何不让计算机代劳一部分。
- Tip 36 You Can't Write Perfect Software：写不出完美软件——保护你的代码和用户免受不可避免的错误。
- Tip 37 Design with Contracts：契约式设计——用契约记录并验证代码恰好做到它声称的事，不多不少。
- Tip 38 Crash Early：尽早崩溃——死掉的程序通常比残废的程序造成的损害小得多。
- Tip 39 Use Assertions to Prevent the Impossible：用断言防住不可能——"不可能发生"就用断言确保它不发生；断言验证假设，保护代码对抗不确定的世界。
- Tip 40 Finish What You Start：有始有终——分配资源的函数或对象应负责释放它。
- Tip 41 Act Locally：就地行动——让可变变量与打开资源的作用域短且可见。
- Tip 42 Take Small Steps—Always：永远小步——小步走、检查反馈、先调整再前进。
- Tip 43 Avoid Fortune-Telling：避免算命——只朝你能看清的前方看那么远。
- Tip 44 Decoupled Code Is Easier to Change：解耦的代码更易改——耦合把事物绑在一起，很难只改一件。
- Tip 45 Tell, Don't Ask：告诉，别问——别从对象取值、变换后再塞回去；让对象自己干活。
- Tip 46 Don't Chain Method Calls：别链式调用方法——访问一个东西时尽量别超过一个点。
- Tip 47 Avoid Global Data：避免全局数据——它相当于给每个方法都加了一个额外参数。
- Tip 48 If It's Important Enough To Be Global, Wrap It in an API：真重要到要全局，就包进 API——但前提是你真的、真的要它全局。
- Tip 49 Programming Is About Code, But Programs Are About Data：编程关乎代码，程序关乎数据——一切程序都是把输入转换为输出；用变换（transformation）来开始设计。
- Tip 50 Don't Hoard State; Pass It Around：别囤积状态，传着用——别把数据扣在函数或模块内部。
- Tip 51 Don't Pay Inheritance Tax：别交继承税——考虑更适合需求的替代：接口、委托、mixin。
- Tip 52 Prefer Interfaces to Express Polymorphism：用接口表达多态——接口让多态显式且不带继承引入的耦合。
- Tip 53 Delegate to Services: Has-A Trumps Is-A：委托给服务——组合胜过继承；不要继承服务，要容纳它。
- Tip 54 Use Mixins to Share Functionality：用 mixin 共享功能——mixin 免继承税地给类加功能；与接口组合获得无痛多态。
- Tip 55 Parameterize Your App Using External Configuration：用外部配置参数化应用——上线后可能变的值、随环境/客户不同的值，保持在应用之外。
- Tip 56 Analyze Workflow to Improve Concurrency：分析工作流以改进并发——从用户的工作流中挖掘并发。
- Tip 57 Shared State Is Incorrect State：共享状态就是错误状态——共享状态打开的蠕虫罐通常只能靠重启来收拾。
- Tip 58 Random Failures Are Often Concurrency Issues：随机故障常是并发问题——时序与环境的变化会以不一致、不可复现的方式暴露并发 bug。
- Tip 59 Use Actors For Concurrency Without Shared State：用 Actor 获得无共享状态的并发——用 Actor 管理并发状态，无需显式同步。
- Tip 60 Use Blackboards to Coordinate Workflow：用黑板协调工作流——用黑板协调分散的事实与 agent，同时保持参与者间的独立与隔离。
- Tip 61 Listen to Your Inner Lizard：听内心蜥蜴的话——当感觉代码在"推挤"你，那是潜意识在告诉你有什么不对。
- Tip 62 Don't Program by Coincidence：别巧合式编程——只依赖可靠的东西；警惕偶然复杂度，别把碰巧当成有计划。
- Tip 63 Estimate the Order of Your Algorithms：估算算法量级——写代码前对耗时建立感觉。
- Tip 64 Test Your Estimates：实测你的估算——算法的数学分析不能告诉你一切；在目标环境里给代码计时。
- Tip 65 Refactor Early, Refactor Often：尽早重构、经常重构——像给花园除草和整理一样，在需要时重写、返工、重架代码；修问题的根。
- Tip 66 Testing Is Not About Finding Bugs：测试不是为了找 bug——测试是进入代码的一个视角，反馈代码的设计、API 与耦合。
- Tip 67 A Test Is the First User of Your Code：测试是代码的第一个用户——利用它的反馈指导后续动作。
- Tip 68 Build End-To-End, Not Top-Down or Bottom Up：端到端构建，而非自顶向下或自底向上——构建小的端到端功能块，边做边学问题。
- Tip 69 Design to Test：为测试而设计——写第一行代码前就开始想测试。
- Tip 70 Test Your Software, or Your Users Will：你不测软件，用户就会替你测——无情地测试，别让用户替你找 bug。
- Tip 71 Use Property-Based Tests to Validate Your Assumptions：用基于性质的测试验证假设——它会尝试你从没想到要试的东西、以代码本不该被使用的方式锻炼它。
- Tip 72 Keep It Simple and Minimize Attack Surfaces：保持简单并最小化攻击面——复杂代码是 bug 的温床，也给攻击者可乘之机。
- Tip 73 Apply Security Patches Quickly：尽快打安全补丁——攻击者部署利用有多快，你就得更快。
- Tip 74 Name Well; Rename When Needed：起好名，需要就改名——命名是向读者表达意图，意图一变就立刻改名。
- Tip 75 No One Knows Exactly What They Want：没人确切知道自己要什么——可能知道大方向，但不知道沿途的曲折。
- Tip 76 Programmers Help People Understand What They Want：程序员帮人弄清想要什么——软件开发是用户与程序员的共同创造行为。
- Tip 77 Requirements Are Learned in a Feedback Loop：需求在反馈环中习得——理解需求需要探索与反馈，用决策的后果来精炼最初的想法。
- Tip 78 Work with a User to Think Like a User：与用户一起像用户一样思考——这是了解系统将如何被真正使用的最佳方式。
- Tip 79 Policy Is Metadata：策略是元数据——别把 policy 硬编码进系统，表达为系统使用的元数据。
- Tip 80 Use a Project Glossary：使用项目词汇表——创建并维护项目全部特定术语与词汇的唯一来源。
- Tip 81 Don't Think Outside the Box—Find the Box：别跳出框框——找到框：面对不可能的问题时识别真实约束，问自己"必须这样做吗？必须做吗？"
- Tip 82 Don't Go into the Code Alone：别独自进代码——编程可能艰难吃力，带个朋友。
- Tip 83 Agile Is Not a Noun; Agile Is How You Do Things：Agile 不是名词而是做事方式——agile 是形容词。
- Tip 84 Maintain Small Stable Teams：维持小而稳定的团队——人人互信互赖。
- Tip 85 Schedule It to Make It Happen：排上日程才会发生——为反思、实验、学习、技能提升安排时间。
- Tip 86 Organize Fully Functional Teams：组织全功能团队——围绕功能而非工种组织：别把 UI/UX 与 coder、前端与后端、测试与数据建模、设计与部署分开；建能端到端、增量迭代构建代码的团队。
- Tip 87 Do What Works, Not What's Fashionable：做有效的，而非时髦的——别因为别的公司在用就采纳某种方法；采纳在你团队、你情境中有效的。
- Tip 88 Deliver When Users Need It：用户需要时就交付——别因流程要求而等数周数月。
- Tip 89 Use Version Control to Drive Builds, Tests, and Releases：用版本控制驱动构建、测试、发布——用 commit/push 触发构建测试发布，用版本控制 tag 部署生产。
- Tip 90 Test Early, Test Often, Test Automatically：早测、常测、自动测——随每次构建运行的测试远比躺在书架上的测试计划有效。
- Tip 91 Coding Ain't Done 'Til All the Tests Run：测试全跑过才算做完——无需多言。
- Tip 92 Use Saboteurs to Test Your Testing：用"破坏者"测试你的测试——在源码的独立副本中故意注入 bug，验证测试能抓住。
- Tip 93 Test State Coverage, Not Code Coverage：测状态覆盖而非代码覆盖——识别并测试重要的程序状态；只测代码行不够。
- Tip 94 Find Bugs Once：一个 bug 只发现一次——人类测试员发现一个 bug 应是最后一次由人发现它；此后交给自动测试把关。
- Tip 95 Don't Use Manual Procedures：别用手工程序——计算机会以相同顺序一次又一次执行相同指令。
- Tip 96 Delight Users, Don't Just Deliver Code：取悦用户而非仅交付代码——开发为用户产出商业价值并让他们每天愉悦的方案。
- Tip 97 Sign Your Work：在作品上签名——早期工匠以签名为荣，你也应如此。
- Tip 98 First, Do No Harm：首先，无害——失败不可避免，确保没有人因它受害。
- Tip 99 Don't Enable Scumbags：别纵容烂人——否则你也有变成烂人的风险。
- Tip 100 It's Your Life. Share it. Celebrate it. Build it. AND HAVE FUN!：这是你的人生——分享它、庆祝它、建造它，并享受乐趣。

来源: research/raw/articles/methodology-pragprog-official-tips.md（原始 URL: https://pragprog.com/tips/）

---

## methodology-refactoring-catalog.md

Fowler《Refactoring》第 2 版官方在线目录（含第 1 版与 Ruby 版手法），每条列出第 2 版名与别名：

- Change Function Declaration（别名 Add Parameter / Change Signature / Remove Parameter / Rename Function / Rename Method）
- Change Reference to Value
- Change Value to Reference
- Collapse Hierarchy
- Combine Functions into Class
- Combine Functions into Transform
- Consolidate Conditional Expression
- Decompose Conditional
- Encapsulate Collection
- Encapsulate Record（别名 Replace Record with Data Class）
- Encapsulate Variable（别名 Encapsulate Field / Self-Encapsulate Field）
- Extract Class
- Extract Function（别名 Extract Method）
- Extract Superclass
- Extract Variable（别名 Introduce Explaining Variable）
- Hide Delegate
- Inline Class
- Inline Function（别名 Inline Method）
- Inline Variable（别名 Inline Temp）
- Introduce Assertion
- Introduce Parameter Object
- Introduce Special Case（别名 Introduce Null Object）
- Move Field
- Move Function（别名 Move Method）
- Move Statements into Function
- Move Statements to Callers
- Parameterize Function（别名 Parameterize Method）
- Preserve Whole Object
- Pull Up Constructor Body
- Pull Up Field
- Pull Up Method
- Push Down Field
- Push Down Method
- Remove Dead Code
- Remove Flag Argument（别名 Replace Parameter with Explicit Methods）
- Remove Middle Man
- Remove Setting Method
- Remove Subclass（别名 Replace Subclass with Fields）
- Rename Field
- Rename Variable
- Replace Command with Function
- Replace Conditional with Polymorphism
- Replace Constructor with Factory Function（别名 Replace Constructor with Factory Method）
- Replace Control Flag with Break（别名 Remove Control Flag）
- Replace Derived Variable with Query
- Replace Error Code with Exception
- Replace Exception with Precheck（别名 Replace Exception with Test）
- Replace Function with Command（别名 Replace Method with Method Object）
- Replace Inline Code with Function Call
- Replace Loop with Pipeline
- Replace Magic Literal（别名 Replace Magic Number with Symbolic Constant）
- Replace Nested Conditional with Guard Clauses
- Replace Parameter with Query（别名 Replace Parameter with Method）
- Replace Primitive with Object（别名 Replace Data Value with Object / Replace Type Code with Class）
- Replace Query with Parameter
- Replace Subclass with Delegate
- Replace Superclass with Delegate（别名 Replace Inheritance with Delegation）
- Replace Temp with Query
- Replace Type Code with Subclasses（别名 Extract Subclass / Replace Type Code with State/Strategy）
- Return Modified Value
- Separate Query from Modifier
- Slide Statements（别名 Consolidate Duplicate Conditional Fragments）
- Split Loop
- Split Phase
- Split Variable（别名 Remove Assignments to Parameters / Split Temp）
- Substitute Algorithm
- 目录标签体系（filter tags）：basic / encapsulation / moving-features / organizing-data / simplify-conditional-logic / refactoring-apis / dealing-with-inheritance / collections / delegation / errors / extract / parameters / fragments / grouping-function / immutability / inline / remove / rename / split-phase / variables。
- 目录用途说明：每张卡片显示第 2 版名称及别名（如它替换的第 1 版手法名），链接到手法的在线页面（含 sketch）；可按关键字与出书筛选。

来源: research/raw/articles/methodology-refactoring-catalog.md（原始 URL: https://refactoring.com/catalog/）

---

## methodology-refactoring-malapropism.md

- 现象：refactoring 一词已从少数人知晓变成行业口头禅，但常被用在不适当的场合。
- Fowler 的自我定位澄清：他不是重构之父/发明者，只是记录者（documenter）。
- 误用判别 1：如果有人说"系统因为重构坏了两三天"，基本可以确定他们做的不是重构。
- 误用判别 2："重构一份文档"也不是重构——两者都只是 restructuring（重组）。
- 概念层级：restructuring 是对整体各部分的任何重排，是非常一般的词，不蕴含任何特定做法；refactoring 是其中一种非常具体的技术，建立在"使用一系列小的、保持行为的变换（这些变换本身也叫 refactorings）"之上。
- 操作性判据：如果你在做重构，系统每次坏掉的时间不应超过几分钟；并且他看不出如何对"没有良好定义行为的东西"做重构。
- Fowler 的立场：即便可能是场打不赢的仗，他仍想保持 DefinitionOfRefactoring 的精确性；可能存在其他好的重组技术，但它们是不同的东西——用这个词时大家应清楚指什么。

来源: research/raw/articles/methodology-refactoring-malapropism.md（原始 URL: https://martinfowler.com/bliki/RefactoringMalapropism.html）

---

## methodology-refactoring-techniques.md

Refactoring.Guru 手法目录（按 6 组组织，含各组说明）：

- 组 1 Composing Methods（组合方法）：重构的很大部分是正确地组合方法；多数情况下过长的方法是万恶之源——方法内部的代码诡变会掩盖执行逻辑、使方法极难理解更难修改；本组手法精简方法、消除重复、为后续改进铺路。
  - Extract Method（提炼函数）
  - Inline Method（内联函数）
  - Extract Variable（提炼变量）
  - Inline Temp（内联临时变量）
  - Replace Temp with Query（以查询取代临时变量）
  - Split Temporary Variable（分解临时变量）
  - Remove Assignments to Parameters（移除对参数的赋值）
  - Replace Method with Method Object（以函数对象取代方法）
  - Substitute Algorithm（替换算法）
- 组 2 Moving Features between Objects（在对象间搬移特性）：即便功能在类间分布得不完美仍有救；本组展示如何在类间安全搬移功能、创建新类、对公众访问隐藏实现细节。
  - Move Method（搬移函数）
  - Move Field（搬移字段）
  - Extract Class（提炼类）
  - Inline Class（内联类）
  - Hide Delegate（隐藏委托关系）
  - Remove Middle Man（移除中间人）
  - Introduce Foreign Method（引入外加函数）
  - Introduce Local Extension（引入本地扩展）
- 组 3 Organizing Data（组织数据）：帮助处理数据、用丰富的类功能替代基本类型；另一重要成果是解开类关联的纠缠，使类更可移植更可复用。
  - Change Value to Reference（将值对象改为引用对象）
  - Change Reference to Value（将引用对象改为值对象）
  - Duplicate Observed Data（复制"被观察数据"）
  - Self Encapsulate Field（自封装字段）
  - Replace Data Value with Object（以对象取代数据值）
  - Replace Array with Object（以对象取代数组）
  - Change Unidirectional Association to Bidirectional（将单向关联改为双向）
  - Change Bidirectional Association to Unidirectional（将双向关联改为单向）
  - Encapsulate Field（封装字段）
  - Encapsulate Collection（封装集合）
  - Replace Magic Number with Symbolic Constant（以字面量常量取代魔法数）
  - Replace Type Code with Class（以类取代类型码）
  - Replace Type Code with Subclasses（以子类取代类型码）
  - Replace Type Code with State/Strategy（以状态/策略取代类型码）
  - Replace Subclass with Fields（以字段取代子类）
- 组 4 Simplifying Conditional Expressions（简化条件表达式）：条件逻辑会随时间越来越复杂，有一组专门手法对抗。
  - Consolidate Conditional Expression（合并条件表达式）
  - Consolidate Duplicate Conditional Fragments（合并重复的条件片段）
  - Decompose Conditional（分解条件表达式）
  - Replace Conditional with Polymorphism（以多态取代条件）
  - Remove Control Flag（移除控制标记）
  - Replace Nested Conditional with Guard Clauses（以卫语句取代嵌套条件）
  - Introduce Null Object（引入空对象）
  - Introduce Assertion（引入断言）
- 组 5 Simplifying Method Calls（简化函数调用）：让方法调用更简单易懂，进而简化类之间的交互接口。
  - Add Parameter（添加参数）
  - Remove Parameter（移除参数）
  - Rename Method（函数改名）
  - Separate Query from Modifier（将查询函数与修改函数分离）
  - Parameterize Method（令函数携带参数）
  - Introduce Parameter Object（引入参数对象）
  - Preserve Whole Object（保持对象完整）
  - Remove Setting Method（移除设值函数）
  - Replace Parameter with Explicit Methods（以明确函数取代参数）
  - Replace Parameter with Method Call（以函数调用取代参数）
  - Hide Method（隐藏函数）
  - Replace Constructor with Factory Method（以工厂函数取代构造函数）
  - Replace Error Code with Exception（以异常取代错误码）
  - Replace Exception with Test（以测试取代异常）
- 组 6 Dealing with Generalization（处理概括/泛化）：围绕继承层级搬移功能、创建新类与接口、在继承与委托间互换的抽象类手法。
  - Pull Up Field（字段上移）
  - Pull Up Method（函数上移）
  - Pull Up Constructor Body（构造函数体上移）
  - Push Down Field（字段下移）
  - Push Down Method（函数下移）
  - Extract Subclass（提炼子类）
  - Extract Superclass（提炼超类）
  - Extract Interface（提炼接口）
  - Collapse Hierarchy（折叠继承体系）
  - Form Template Method（塑造模板函数）
  - Replace Inheritance with Delegation（以委托取代继承）
  - Replace Delegation with Inheritance（以继承取代委托）

来源: research/raw/articles/methodology-refactoring-techniques.md（原始 URL: https://refactoring.guru/refactoring/techniques）

---

## methodology-smells-catalog.md

Refactoring.Guru 坏味道目录（6 大类 22 种，含各类定义）：

- 类别定义 Bloaters（膨胀物）：膨胀到庞然大物、难以处理的代码/方法/类；通常不会立刻出现，而是随程序演化逐渐累积（尤其当没人努力清除它们时）。
  - Long Method（过长函数）
  - Large Class（过大的类）
  - Primitive Obsession（基本类型偏执）
  - Long Parameter List（过长参数列）
  - Data Clumps（数据泥团）
- 类别定义 Object-Orientation Abusers（面向对象滥用者）：对 OOP 原则的不完整或错误应用。
  - Alternative Classes with Different Interfaces（异曲同工的类）
  - Refused Bequest（被拒绝的遗赠）
  - Switch Statements（switch 惊悚现身）
  - Temporary Field（令人迷惑的暂时字段）
- 类别定义 Change Preventers（变化阻止者）：在一处改代码就要在其他许多地方也改，程序开发因此变得更复杂更昂贵。
  - Divergent Change（发散式变化）
  - Parallel Inheritance Hierarchies（平行的继承体系）
  - Shotgun Surgery（霰弹式修改）
- 类别定义 Dispensables（可有可无物）：没有意义、不需要的东西——不存在反而让代码更干净、更高效、更易懂。
  - Comments（注释——被归为"可有可无物"，指用注释掩盖本应重构的代码）
  - Duplicate Code（重复代码）
  - Data Class（纯数据类——只有字段没有行为）
  - Dead Code（死代码）
  - Lazy Class（冗赘类）
  - Speculative Generality（投机泛化/夸夸其谈通用性——为"未来可能"而存在的抽象）
- 类别定义 Couplers（耦合器）：促成类之间过度耦合，或展示"用过度委托替代耦合"的后果。
  - Feature Envy（依恋情结）
  - Inappropriate Intimacy（狎昵关系）
  - Incomplete Library Class（不完善的库类）
  - Message Chains（过度耦合的消息链）
  - Middle Man（中间人）
- 站点附注：Other Smells 分类下收录 Incomplete Library Class（"其他坏味道"组）。

来源: research/raw/articles/methodology-smells-catalog.md（原始 URL: https://refactoring.guru/refactoring/smells）

---

## methodology-strangler-fig.md

- 隐喻来源：2001 年昆士兰雨林度假见到绞杀榕（strangler fig）——藤在树洞发芽，从宿主树汲取养分直到触地生根、树冠取光，最终自给自足，宿主树可能枯死、榕树成为其形状的回声；这种渐进替换宿主的过程被 Fowler 用作遗留系统现代化方式的类比。
- 命名演变：原帖题为 "Strangler Application"，流行中人们常略去植物学来源只说 "strangler"；Fowler 担心其暴力含义，改题 "Strangler Fig Application" 强调隐喻根源——新标题最终"绞杀"了旧标题。
- 问题背景：软件系统支撑人类大量活动但常做得不好——数十年建成、少有投入保持健康；业务与技术平台变化迫使系统变化，但变化常以"补丁摞补丁"完成，每个补丁都让未来的适应更难；最终人们意识到无法再打补丁，需要全面现代化。
- 对"简单替换"方案的否定：知道旧系统做什么，就用更好技术原样造一个新系统——这个看似简单的计划大多数时候折戟：替换严肃 IT 系统耗时漫长而用户等不起新功能；替换看似容易规格化，但既有行为的细节往往难以搞清；更糟的是其中很多行为根本不被人想要，造它们是浪费。
- 替代方案：渐进式现代化——像绞杀榕一样，从小的新增物开始（通常是建在遗留代码库之上、却与其分离的新功能），逐步把行为从遗留系统搬进新代码库。
- 四大高层活动（Ian Cartwright、Rob Horn、James Lewis 定义，顺序不代表先后）：理解想要达成的成果（understand the outcomes）；决定如何把问题拆成更小的部分；成功交付这些部分；改造组织使其能持续进行。
- 活动 1（成果）：对期望成果必须"水晶般清晰"；常见目标是混乱的——不同群体想要不同东西；需尽早建立对齐并定期重温以强化对齐、检查优先级是否该变。
- 活动 2（拆分）：理想软件应由可独立替换的清晰组件构成，遗留系统很少如此；需要找到可插入系统的接缝（seams）来切分（脚注：设计良好的系统里这些接缝本已存在，但这样的系统是独角兽）；识别系统如何支撑多个业务需求、把单个需求抽成新组件常有帮助。
- 活动 3（交付）：接缝隔离出小组件后开始替换；组件小则引入新软件风险小；一旦运转，业务即可从新组件收获价值 → 更早的投资回报；同时学到更多"如何替换遗留系统及其业务后果"，帮助后续做出更好决策。
- Transitional architecture（过渡架构）：人们常 balk 于必须建造"让新旧系统共存、现代化完成后即拆除"的过渡架构；看似浪费，但渐进法带来的风险降低与更早回值超过了它的成本。
- 活动 4（组织变革）：贯穿始终的是更广泛的组织变革——遗留系统僵硬脆弱，是因为产出它们的设计思维和组织流程就把它们造成这样；组织文化与领导力不变，新系统会陷入同样的烂摊子；需要引入新开发实践，包括按 Conways Law 重组开发组织及其与业务的连接。
- 诚实的边界：绞杀榕式遗留现代化不会让这件事变"容易"——深度嵌入业务流程的软件系统替换从来没有容易的；它做的是让投资与回报渐进且可见地发生，让组织演化其软件与业务流程以更好支持当前环境，并（也许更重要）演化"做这件事的方式"为更可持续的 future。

来源: research/raw/articles/methodology-strangler-fig.md（原始 URL: https://martinfowler.com/bliki/StranglerFigApplication.html）

---

## methodology-yagni.md

- 定义：Yagni 原为缩写 "You Aren't Gonna Need It"（你不会需要它），源自 ExtremeProgramming 的口号，后被敏捷团队泛用；含义是：我们假想软件未来需要的某种能力，现在不该构建，因为"你不会需要它"。
- 谱系：yagni 指 XP 的 Simple Design 实践（白皮书第 1 版；第 2 版改称相关的 incremental design 概念）；与 90 年代末主流的"谨慎前期规划"软件工程原则形成鲜明对比。
- 词源轶事：短语源自 C3 项目上 Kent Beck 与 Chet Hendrickson 的早期对话——Chet 带来一系列"系统很快会需要"的能力，Kent 对每一个回答"you aren't going to need it"；Chet 很快以善于发现 yagni 应用时机而闻名。
- 术语状态：虽始于首字母缩写，Fowler 认为它已进入词汇表成为普通单词，故不大写。
- 术语约定："presumptive feature"（假想功能）= 支持一个"尚未开放使用"的功能的任何代码。
- 示例场景（Minas Tirith 保险创业）：定价组件正在加风暴风险，已知六个月后需要海盗风险定价；既然正在改定价引擎，不如顺手把海盗定价也做了——yagni 反对此做法：既然六个月后才需要，就不该现在建（若开发需两个月，还有四个月才该动手）。
- 论据 1（需求预测大概率错）：我们现在认为需要这个假想功能，很可能是错的——敏捷方法的语境本就接受需求会变；计划驱动 guru 会反驳说需求分析没做好，Fowler 反驳：预先弄清需求既难又贵，且即便弄清也可能被黑天鹅（冈多海军剿灭海盗）掀翻整个商业模式。
- 成本 1 Cost of build（建造成本）：分析、编程、测试这个最终无用的功能的全部投入——这是显然的代价。
- 成本 2 Cost of delayed value（延迟价值成本）：即使我们对需求的判断完全正确，把力气花在假想功能上就没建别的功能；若先做风暴险销售软件，可提前两个月上线收费——代价是两个月的风暴险收入。
- 成本对比的正确算法：人们建假想功能的常见理由是"现在建比以后建便宜"，但该对比至少要计入延迟成本，最好再乘以"建了不需要的功能"的概率——你的胜算最多 ⅔。
- ⅔ 数字出处：Kohavi et al 分析微软产品已上线功能的价值，发现即便有谨慎的前期分析，也只有 ⅓ 的功能改善了它们设计要改善的指标。
- 思想实验技巧：辅导开发者时，Fowler 让他们想象"以后要引入该能力时需要做的重构"——通常这个想象就足以说服他们"以后加并不会显著更贵"；这种想象的另一个产出是：现在就做"容易做、几乎不增复杂度、却显著降低未来成本"的事——例如错误信息用查找表而非内联字面量，简单且让未来的国际化更容易。
- Jeremy Miller 引语：从未被使用的扩展点不只是浪费的工时，它很可能还会挡你的路。
- 成本 3 Cost of carry（持有成本）：假想功能的代码给软件增加复杂度，使修改与调试更难，从而抬高其他功能的成本；例子中海盗定价的复杂度可能让风暴险销售组件多花两周——这两周双重打击：额外建造成本 + 额外延迟成本；从现在到假想功能开始有用之间的每个功能都要付持有成本；若最终从不需要，则要一直付到把它删除为止（假设会删），外加删除成本。
- 第三类假想功能 the right feature built wrong（建错的正确功能）：团队对用户与代码库持续学习，常发现六个月前写的功能不是现在认识的该有的样子——此时累积了 TechnicalDebt，要考虑修复成本或长期绕行成本。
- 汇总框架：三类假想功能（unsuccessful / right-feature-built-wrong / successful），忽视 yagni 会招致四种成本。
- 论域扩展：以上虽以用户可见功能为例，同样适用于"支持未来灵活性的抽象"——建风暴风险计算器时想现在就放抽象与参数化以支持未来其他风险，yagni 说别做：可能不需要其他定价功能，即便需要，你现在的抽象构想也不会匹配你实际需要时学到的东西；这不是放弃一切抽象，而是"任何让当前需求的代码更难理解的抽象都被推定有罪（presumed guilty）"。
- 小尺度 yagni：yagni 最显眼的是大功能，但更频繁出现在小事上；Fowler 自己的代码高亮正则例子——预计以后可能需要只高亮正则中的 group，但因为还没需要，就没实现，直到真需要为止；同理不加"还没准备用"的字段和方法。
- 小决策的累积效应：小 yagni 决策飞在项目规划的雷达之下——开发者很容易花一小时加一个"确信很快会用到"的抽象；但上述全部论证仍然适用，大量小 yagni 决策累积起来显著降低代码库复杂度、加快更需要的功能的交付。
- 最常见的误解（核心辨析）：yagni 只适用于"为假想功能而建进软件的能力"，不适用于"让软件更容易修改的努力"——yagni 只有在代码易于改变时才是可行策略，因此为重构投入 effort 不违反 yagni（重构让代码更柔韧）；同理适用于 SelfTestingCode 与 ContinuousDelivery：它们是演进式设计的 enabling practices，没有它们 yagni 从有益实践变成诅咒（a curse）；yagni 有着"被演进式设计使能、又反过来使能演进式设计"的奇妙性质。
- 推论 1：yagni 不是忽视代码库健康的借口；yagni 要求（并使能）柔韧的代码。
- 推论 2：yagni 只适用于"现在引入、但直到以后才利用的额外复杂度"——为未来做的事若并不实际增加软件复杂度，就没有理由搬出 yagni。
- 诚实的边界：确有应用 yagni 出问题、面临昂贵变更的情形；棘手之处在于这些案例事前难识别、事后好记住（人们容易记住 yagni 失败、忘记 yagni 省力）；Fowler 的判断：yagni 失败相对罕见，代价容易被 yagni 成功的收益盖过（脚注：这是 availability bias 的后果）。

来源: research/raw/articles/methodology-yagni.md（原始 URL: https://martinfowler.com/bliki/Yagni.html）

---

## 提取统计

- 文件数：26（`research/raw/articles/methodology-*.md` 全部）
- 本文件为阶段2"只罗列、不整合"产物；整合与取舍留待后续阶段。
