# 主题六笔记:经典代码质量方法论及其在 AI 时代的适配

> 调研日期 2026-10-11。原始归档见 `research/raw/articles/methodology-*.md`(26 篇)。
> 标注约定:`[映射]` = 本笔记作者判断的「对 AI 生成代码特别适用」的映射,非来源原文。

---

## 1. 重构的纪律(Fowler 体系)

核心定义与纪律:

- **重构 = 在不改变外部可观察行为的前提下调整代码结构**。Fowler 定义:"restructuring ... without changing its observable behavior";常见误用是把任何改代码都叫重构(Refactoring Malapropism)。小步 + 每步不破坏 + 高频跑测试是纪律本体。
  - 来源: https://martinfowler.com/bliki/DefinitionOfRefactoring.html ; https://martinfowler.com/bliki/RefactoringMalapropism.html
- **为什么小步**:小步使每一步都可验证、可回滚;行为保持靠"测试保护网 + 小步"共同保证,而不是靠人眼。
  - 来源: https://refactoring.com/catalog/ (catalog 前言部分)
- **机会式重构(Opportunistic Refactoring)**:"boy scout rule"——顺手清理,但要在时间盒内;不做大扫除式重构。
  - 来源: https://martinfowler.com/bliki/OpportunisticRefactoring.html
- **理解性重构(Comprehension Refactoring)**:读懂一段代码后,把你刚获得的理解固化成好命名/清晰结构——"把理解存进代码"。与 Litter-Pickup(顺手捡垃圾)同为机会式工作流。
  - 来源: https://martinfowler.com/articles/workflowsOfRefactoring/fallback.html
- **重构工作流分层**(Fowler 2023):
  - Laissez-faire:随手改,依赖个人自觉(默认但易积压);
  - Opportunistic:litter-pickup + comprehension,配时间盒;
  - Scheduled/umbrella:排期重构,umbrella = 一个大重构拆成多次小 PR 挂在伞下;
  - Sandboxed:先建"重构沙箱",完成前不影响主线(像 feature 分支);
  - Long-term:Branch By Abstraction——在原地建抽象层,逐个调用点迁移,全程主干可发布。
  - 来源: https://martinfowler.com/articles/workflowsOfRefactoring/fallback.html ; https://martinfowler.com/bliki/BranchByAbstraction.html
- **Strangler Fig(绞杀者模式)**:新系统包在旧系统外面逐步接管路由/功能,旧系统枯萎后拆除。这是"refactor vs rewrite"的第三条路:当模块没有安全网、改动面巨大时,用增量替换代替一次性重写。判定信号:绿地方案与绞杀方案的边界清晰度、是否有 facade 可挂。
  - 来源: https://martinfowler.com/bliki/StranglerFigApplication.html
- **特征测试(Characterization Test)**:Michael Feathers 提出——在没人理解行为、没有测试的遗留代码上,先写"锁定当前实际行为(哪怕有 bug)"的测试作安全网,再重构。对"无文档、无测试、无作者可问"的代码是第一步。
  - 来源: https://en.wikipedia.org/wiki/Characterization_test
  - `[映射]` AI 生成的存量代码 = 典型"无作者可问的遗留代码":没人真正理解它为什么这样写。特征测试/golden test 应成为 AI 重构 Skill 的第一步护栏。

## 2. 坏味道 → 重构手法映射

- **坏味道六大类**(refactoring.guru 组织法,源自 Fowler):
  1. Bloaters(膨胀):Long Method / Large Class / Primitive Obsession / Long Parameter List / Data Clumps;
  2. OO Abusers:Switch Statements / Temporary Field / Refused Bequest / Alternative Classes with Different Interfaces;
  3. Change Preventers(_change 阻止者):Divergent Change(一个类因多种原因改)/ Shotgun Surgery(一个改动散布多处)/ Parallel Inheritance Hierarchies;
  4. Dispensables(可有可无):Comments(用注释掩盖坏代码)/ Duplicate Code / Data Class(只有字段没行为)/ Lazy Class / Dead Code / Speculative Generality(投机泛化);
  5. Couplers(耦合者):Feature Envy(总想拿别的类的数据)/ Inappropriate Intimacy / Message Chains / Middle Man(纯转发);
  6. 其他:Incomplete Library Class 等。
  - 来源: https://refactoring.guru/refactoring/smells
- **手法目录**(Fowler 2 版 60+ 手法,6 大组):Composing Methods(Extract Function 最常用、Inline Function)、Moving Features Between Objects(Move Function/Field)、Organizing Data(Replace Primitive with Object、Replace Conditional with Polymorphism)、Simplifying Conditional(Decompose Conditional、Replace Nested Conditional with Guard Clauses、Introduce Special Case)、Making API Calls Easier(Separate Query from Modifier、Parameterize Function)、Big Class 处理(Extract Class、Inline Class)等。
  - 来源: https://refactoring.com/catalog/ ; https://refactoring.guru/refactoring/techniques
- **经典对应关系**:Long Method→Extract Function;Duplicate Code→Extract/Pull Up;Switch Statements→Replace Conditional with Polymorphism;Speculative Generality→Inline/删除;Middle Man→Remove Middle Man / Inline;Comments→把注释内容提炼成函数名。
  - `[映射]` AI 代码高发味道清单(社区共识):Speculative Generality(AI 爱留"以后可能用到"的参数/层)、Middle Man/层层转发、Dead Code(生成到一半)、Duplicate Code(每次会话独立生成近似 helper)、Switch Statements。Skill 可做成"味道→手法"查表。

## 3. Clean Code(Uncle Bob)核心规则

- 总纲:**Clean = 别人能容易看懂**。"Code is clean if it can be understood easily by everyone on the team. With understandability comes readability, changeability, extensibility, maintainability."
- 通用:遵循团队约定;KISS;Boy Scout Rule(营地比来时更干净);找根因不只修表象。
- 命名:名副其实、避免误导、做有意义的区分(不用 a1/data2)、类名用名词、方法名用动词(说清楚做什么)。
- 函数(第 3 章,最常被引用):**短小是第一规则**;只做一件事;每个函数一个抽象层级;switch 最好埋进抽象工厂/多态;参数越少越好(>3 用对象);无副作用;指令与查询分离;DRY。
- 注释:好注释屈指可数(法务、警示、TODO);**坏注释 = 掩饰坏代码的注释**、日志式注释、被注释掉的代码;能用具名函数/变量表达的别写注释。
- 错误处理:用异常别返错误码;先写 try-catch 再写主体;别返回/传递 null(null 导致的崩溃离源头很远);别吞异常。
- 边界(Boundaries 章):第三方接口要在边界处包装/适配,不让第三方类型渗透进核心代码;边界处要测试。
- 类:组织成信息隐藏;实体类/边界类的区分。
- 系统级:构造与使用分离(dependency injection)、扩软件要增量生长。
  - 来源(gist 摘录,内容对应原书章节): https://gist.github.com/wojteklu/73c6914cc446146b8b533c0988cf8d29 ; https://gist.github.com/cedrickchee/55ecfbaac643bf0c24da6874bf4feb08
  - `[映射]` AI 代码注释问题最典型:AI 会写"复述代码"的噪音注释和过时注释(代码改了注释没改)。Clean Code 的注释观 + Fowler 的 Comprehension Refactoring(把理解写进命名而非注释)是直接可用的规则。错误处理是 AI 第二高发缺陷源(吞异常、happy-path-only)。

## 4. The Pragmatic Programmer(Hunt & Thomas)要点

- **DRY(Don't Repeat Yourself)**:知识的每一份表示应唯一;重复是"知识"的重复不单是文本——注释与代码、配置与常数的重复也算。DRY 失败→shotgun surgery。
- **Orthogonality(正交性)**:组件互不牵连;改 A 不应破坏 B。实现手段:封装、避免共享全局数据、避免 side effect。正交性测试:"如果需求变了,有多少模块要改?"
- **ETC(Easier to Change,20 周年版新增总原则)**:所有工程决策的仲裁标准——选更容易改的那个。
- **Tracer Bullets(曳光弹)**:先打一个端到端能跑的最小骨架(不是 prototype,是留着用的),再逐步加肉——用真实反馈校准。
- **Stone Soup / 煮石头汤**:从小成果开始,逐步吸引资源做大——渐进式推进。
- **Broken Windows(破窗)**:不修的小瑕疵诱发更多破坏;见到就修。
- **No Silver Bullet / 不要迷信**;**Estimate to avoid surprises**;**It's not a bug, it's an unmet expectation**(版本不同)。
- 官方 20 周年版 tips 全列表(权威表述):70+ 条,如 "Care About Your Craft"、"Provide Options, Don't Make Lame Excuses"、"DRY"、"Eliminate Effects Between Unrelated Things"、"Use Tracer Bullets"、"Crash Early"、"Design to Contract"、"Deploy Early and Often"、"Don't Live with Broken Windows"、"Test Early, Test Automatically, Test Often"。
  - 来源: https://pragprog.com/tips/
  - `[映射]` ETC 对 AI 时代是元原则:AI 让"改"变便宜,但让"理解存量改动"变贵——ETC 应升级为"选更容易被 AI(和新人)读懂的版本"。曳光弹式 = vibe coding 的正确姿势:先端到端骨架后补质量,与"一次生成整个系统"对照。

## 5. A Philosophy of Software Design(Ousterhout)

- **复杂度是根本恶**:"Complexity is anything related to the structure of a software system that makes it hard to understand and modify the system."
- **复杂度公式** C = Σ c_p·t_p(各部分复杂度按开发时间加权)→ 优化常改的热区,不是一次性代码。
- **复杂度三症状**:Change Amplification(一处需求要改 N 处)、Cognitive Load(要懂很多才能改)、Unknown Unknowns(不知道要懂什么——最致命)。
- **复杂度两来源**:Dependencies(依赖,不可消除但可收拢)与 Obscurity(重要信息不显眼:坏命名、缺文档、非直觉约定)。
- **复杂度是增量累积的**,不是单次大错——每天"先这样吧"叠加而成。⇒ 复杂度预算观。
- **Deep Modules vs Shallow Modules(核心)**:深模块 = 功能强大、接口窄(GC 是极深模块:海量复杂度,零接口);浅模块 = 接口复杂但功能薄(层层 wrapper 是浅模块的典型)。**模块的价值在"藏了多少"不在"分了多少层"**。
- 其他设计法则:Information Hiding(深模块的实现机制)、High-level 与 low-level 分层、"Comments are part of the design"(先写接口注释再实现)、"Working Code Isn't Enough"(写到能用 vs 写到好)、一般与特殊(general-purpose 略超当前需求但不投机)、Red Flags 清单(浅模块、信息泄漏、时间耦合、暴露内部、传胶水参数、晦涩命名…可作 review checklist)。
  - 来源: https://www.oehler.dev/posts/a-philosophy-of-software-design-summary ; https://www.janmeppe.com/blog/a-philosophy-of-software-design-john-ousterhout/
  - `[映射]` **Ousterhout 可能是对 AI 代码最有解释力的框架**:AI 极擅长产出"看起来分层了"的 shallow modules(接口/实现 1:1 的转发层、五层 service 各做一点),Unknown Unknowns 正是"没人读过的 AI 代码"的定义性症状。Skill 可内置判定:接口面 ≥ 实现体量 ⇒ 浅模块 ⇒ 合并/内联;Red Flags 直接作为 AI 代码扫描清单。

## 6. Clean Architecture(Uncle Bob)

- **核心目标**:最大化"变更成本曲线的平缓度"——业务逻辑不因框架/DB/UI 变更而被迫修改。
- **依赖规则(Dependency Rule)**:源码依赖只能指向内层。Entities(企业级业务规则)← Use Cases(应用业务规则)← Interface Adapters(控制器/展示器/网关)← Frameworks & Drivers(Web/DB/UI)。内层不知道外层存在。
- **Entities/Use Cases 应是纯对象**,框架是不可替换的细节:业务逻辑不该 import Spring/Express/FastAPI 的类型。
- **边界(Boundaries)按需画**:不是每个项目都要全四层;独立可测试、可替换的外部世界才值得开边界(呼应 YAGNI)。
- SOLID 作为类级准则:SRP(一个模块只对一个 actor 负责——"职责"定义为"同一变更原因")、OCP(加功能不改旧代码)、LSP、ISP(窄接口)、DIP(依赖抽象)。
  - 来源: https://blog.ndepend.com/introduction-clean-architecture/ ; https://softengbook.org/articles/clean-architecture
  - `[映射]` 双刃:一方面 AI 生成的"过度分层"(为每个 entity 生成 repository+service+controller+DTO 五件套)违反 Clean Architecture 的本意(按需画边界)与 Ousterhout 深模块论;另一方面"依赖方向"是检查 AI 代码的强约束——业务逻辑文件 import 了框架细节即为红旗,可静态检查。

## 7. Google《How to do a code review》

- **总原则(standard.html)**:review 的首要职责是"代码正确且可理解",同时教育、维护规范;有分歧时"总体上让代码更好"即可放行——不因完美阻塞("LGTM with nits");reviewer 要给出建设性意见而非命令;风格问题交给工具;设计/功能可整体建议"另一种更简单的做法"。
- **看什么(looking-for.html)——核对清单**:
  - **Design**:代码与系统整体契合吗?交互是否良好?
  - **Functionality**:从用户视角对不对?并发/边界?并发改动会互相踩吗?
  - **Complexity**:**能一行行删掉吗(过度设计检查)?**会不会有"用不上的功能"?——Google 明确把 over-engineering 列为 review 关注点。
  - **Tests**:测试正确、有针对性、有回归价值?测试自身也要 review。
  - **Naming**:名字够不够"像话"?
  - **Comments**:注释说的是"为什么"吗?会被同步更新吗?
  - **Style/Docs**:一致性、文档更新。
- **注释规则(comments.html)**:
  - Courtesy & respect:评论代码不评论人;"Why did you..."要改写为建议式("It looks like X; consider Y")。
  - **注释要给解释/依据**,不是命令——给 rationale、给可参考的权威链接(设计文档/风格指南)。
  - **Label comment severity**:Nit(小毛病,不必阻塞)/ Optional(建议)/ Issue(必须改)——分级让作者知道哪些必须做。
  - 有分歧:线下沟通 > 评论区拉锯;仍僵持则升级,以"代码健康"为准,不以'谁赢'为准。
  - 来源: https://google.github.io/eng-practices/review/reviewer/standard.html ; .../looking-for.html ; .../comments.html
  - `[映射]` severity 分级(Nit/Optional/Must)+ "给 rationale 不给命令"天然适配 AI review prompt:让 review agent 输出结构化分级意见;looking-for 清单(尤其 Complexity 的"能不能删"一问)可整体移植为 AI 代码审查 checklist 的母版。

## 8. 2025–2026:AI 代码 review / 重构的特化方法

### 8.1 Continuum《How to review AI-generated code》(2026-08 更新)
- **核心洞察:agent 代码的失败模式是"plausible"(貌似合理)而非"confused"**——人类错误的信号(慌乱命名、含糊注释、风格漂移)在生成代码中不存在;代码"uniformly confident",直觉不知道该在哪放慢。
- 失败模式表:**plausible-but-wrong / silent deletion(静默删护栏)/ invented API(幻觉 API)/ weakened test(放宽断言让测试过)/ scope creep(两文件任务动九个文件)/ confident wrong explanation(编造理由)/ duplicated instead of reused(重复造 helper)**。
- **七步审查法**(按性价比排序):
  1. 先看文件清单再看内容(`git diff --stat`)——非预期文件即 scope creep;
  2. **先读删除行**(被删的 guard/边界分支,删护栏的 diff 看起来像简化);
  3. **测试文件单独 diff**(断言变松不能藏在 50 行实现改动里);
  4. 自己跑测试,"all tests pass"是 agent 的 claim 不是事实;
  5. 专查错误路径(吞/包/记/抛?);
  6. 抽查解释里的一条事实性 claim(一条错→全部仔细看);
  7. 问一次"为什么选这个方案"。
- **体量问题**:"agent 十分钟产出 > 你一小时能认真审的"——唯一真解是**缩小任务粒度**;其余是缓解:按逻辑边界要求分 commit、先 plan 再写、**每个 prompt 带约束子句("不改公共签名、不加依赖")**、一 worktree 一 session。
- **机器审查分工表**:机器擅长 null/边界穷举、删 guard、放宽断言;**机器不能做的是"这是我想要的吗/方向对吗/契合系统吗"——意图必须留给人**;review bot 永远 neutral 不阻塞合并(会挡路的 bot 第一周就被关);nit 数量要 cap。
- 来源: https://continuumcode.ai/guides/reviewing-ai-generated-code/

### 8.2 Vibecoder《Practical Code Review Checklist for AI-Generated Code》(2026-04)
- AI 失败四大类:**安全(借来的不安全训练模式)/ 逻辑(幻觉 API、边角案例)/ 性能(不必要重依赖、N+1)/ 死代码(生成不完整)**;按此顺序审(安全>逻辑>性能>质量)。
- 引 Veracode 2025:**45% AI 生成代码含至少一个安全漏洞;有结构化 review 流程后降到 10% 以下**。
- Security 五查:硬编码密钥(全 diff grep)、注入(每个拼 SQL/查询问"单引号会怎样")、XSS、**每个新端点查认证**、**认证≠授权(user A 能否摸到 user B 数据)**。
- Logic 五查:**每个外部 API 调用对照现行文档(训练截止)**、错误处理完备性(静默吞错)、async 竞态("两个用户同时…?")、数据流 null/undefined 逐步检查(类型断言 cast 不可信)、业务逻辑逐字对照需求(AI 实现的是 prompt 字面而非意图)。
- 来源: https://blog.vibecoder.me/code-review-checklist-ai-generated-code

### 8.3 GitHub 官方 Copilot 教程《Review AI-generated code》
- 8 步:功能检查先行(编译/测试/CodeQL/Dependabot)→ 验证上下文与意图(架构契合、README/PR 当上下文喂给 AI)→ 代码质量(可读性、"重构比重写还慢的代码别收")→ **细查依赖(包是否真实存在/在维护、license、slopsquatting 幻觉包攻击)** → **AI 特有坑(hallucinated API、被删/被跳过的测试、"看着对但不对")** → 协作 review(checklist 保证覆盖)→ 自动化(CI lint/security/coverage)→ 持续沉淀(把 AI review 预期写进 CONTRIBUTING.md)。
- 来源: https://docs.github.com/en/copilot/tutorials/review-ai-generated-code

### 8.4 Mitrix《How to Refactor AI-Generated Code Safely》(2026-05)
- 差异定位:**AI 代码"从未被设计过"**——没有意图的面包屑(注释/命名/结构),重构 = 先逆向出意图再重构;过程必须包含 discovery。
- 安全重构步骤:**Audit before touch(先画项目地图:入口/路由/表/认证/集成点,写成 markdown)→ 依赖图(madge/import-linter 找环与耦合;独立模块先改)→ 先补测试(happy-path 集成测试 + API contract 测试,不求 100% 覆盖)→ 小而可验证的 PR 逐步改 → 验证监控**。
- "我们不知道认证是怎么工作的"本身就是 finding,应影响重构优先级。
- 来源: https://mitrix.biz/blog/refactor-ai-generated-code

## 9. KISS / YAGNI / Over-engineering 判定

- **YAGNI(Fowler,权威表述)**:YAGNI ≠ 不做设计,而是**"只在有能力立即需要时才实现"**;条件仍为真时才采纳。最大误区:把 YAGNI 当"不写可测试/灵活代码"的借口——Fowler 明确:先重构到灵活再上功能,才是 YAGNI 的完整实践。
  - 来源: https://martinfowler.com/bliki/Yagni.html
- **KISS**:源于工程传统(凯利 Johnson:"让飞机简单到坏了战地机械师都能用零件修");软件语境 = 简单性优先于聪明;权威定义与历史。
  - 来源: https://en.wikipedia.org/wiki/KISS_principle
- **Over-engineering 判定标准**(跨来源汇总):Google review 清单之问"这行能删吗/有没用不上的功能吗?"(https://google.github.io/eng-practices/review/reviewer/looking-for.html);Ousterhout:为假设需求付的抽象税 = shallow module + speculative generality;Fowler YAGNI:想象的需求不算需求。
  - `[映射]` AI 把 over-engineering 的边际成本打到近零(多生成一层 wrapper 不费 AI 什么事),但**维护成本不变**——"生成便宜、理解昂贵"的不对称使 YAGNI 在 AI 时代从美德升级为硬约束。Skill 应把"删除测试"("能不能删掉这层?")作为每次审查的固定动作。

---

## 10. [映射] 汇总:对 AI 生成代码特别适用的三条洞察(作者判断)

1. **经典方法论没有失效,但权重重排**:Ousterhout 的"复杂度=难懂+难改、深模块"和 Google 的"能不能删"从建议升格为核心判据,因为 AI 的典型缺陷已不是"写不出来"而是"生成得太多太浅"(浅模块、投机泛化、层层转发)。Clean Code 的函数/注释规则、错误处理规则照用;风格类规则交给 linter。
2. **行为保持纪律从"美德"升格为"安全设施"**:AI 存量代码=无作者的遗留代码 → 特征测试/golden tests 先行(Feathers)+ Branch By Abstraction/Strangler Fig 做增量替换 + 小步可回滚 PR(Mitrix 流程)。同时必须防"AI 自己违反纪律":审查删除行、单独 diff 测试、自己跑测试(Continuum 三查),防 silent deletion 与 weakened tests。
3. **审查对象从"代码"扩展到"代码+声明"**:AI 会同时生成代码和(貌似合理的)解释,二者来自同一生成过程——review 必须抽查解释中的事实性 claim、验证依赖包真实存在(slopsquatting)、对照现行 API 文档;人的注意力应从"看得懂的 tedium(机器查)转向意图(只有人能查)"。

## 11. 待深挖线索

- Fowler《Workflows of Refactoring》中 sandboxed/umbrella 的细节未完全展开(归档含全文,可再提炼)。
- Veracode 2025 报告原文(45%→10% 数字的一手来源)未归档。
- Ousterhout "Red Flags" 完整清单在 oehler.dev 归档中,值得整理成独立 checklist;与 Google looking-for 合并成"AI 代码 review 母表"是 Skill 的直接素材。
