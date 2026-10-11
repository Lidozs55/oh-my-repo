# 主题二笔记：Agent Skill 生态 —— 代码质量/重构/Review 类 Skill 与写作规范

日期：2026-10-11。原始材料见 `research/raw/repos/`（7 个克隆/部分归档仓库）与 `research/raw/articles/`（2 篇规范文档）。

## A. 各质量类 Skill 的内容要点

### A1. code-simplifier（官方插件市场，专治 AI 代码味）
来源：claude-plugins-official/plugins/code-simplifier/agents/code-simplifier.md（另见 pr-review-toolkit 中的 agent 版）
- 铁律：**只改"怎么做"不改"做什么"**——Preserve Functionality 放第一位，功能、输出、行为完全不变。
- 规则清单：减少不必要的复杂度与嵌套；消灭冗余代码与冗余抽象；**禁止嵌套三元**（改 switch/if-else）；清晰优先于简短（反对 dense one-liner）；删描述显而易见行为的注释；合并相关逻辑。
- 双向防御：既有"简化不足"也有"过度简化"清单（过于聪明的方案、单函数塞太多关注点、砍掉有益抽象、为少几行牺牲可读性）——这是它区别于普通 linter 的核心。
- 作用域：默认只处理**本次会话最近修改的代码**，除非明确要求扩大范围；写完即自动触发（agent 版 description 里放了 3 个 <example> 触发示例）。

### A2. code-review（官方插件市场，多 agent 流水线 PR 审查）
来源：claude-plugins-official/plugins/code-review/commands/code-review.md
- 流程编排：Haiku 做资格预检（草稿/已关/自动 PR/已审过则跳过）→ 收集 CLAUDE.md 列表 → 5 个并行 Sonnet 审查员各自独立出报告 → 每条 issue 再派 Haiku 打 0-100 置信分 → **低于 80 分直接丢弃** → 复查资格后回帖。
- 5 个审查视角：CLAUDE.md 合规 / 只看 diff 的浅层大 bug 扫描 / git blame+历史上下文 / 历史 PR 评论迁移检查 / 代码内注释合规。
- 反误报清单（写进 prompt）：预存在问题、linter/编译器能抓的、资深工程师不会提的 nitpick、已被 lint-ignore 显式屏蔽的、未改动行上的问题。
- 输出格式精确到链接规则（全 SHA + 行区间 + 前后各 1 行上下文）。

### A3. pr-review-toolkit（官方市场，专科审查员编队）
来源：claude-plugins-official/plugins/pr-review-toolkit/agents/*.md
- silent-failure-hunter：对"静默失败"零容忍——catch 块必须具体（列出可能被误吞的异常类型）、fallback 必须显式且有据、错误日志要带上下文让人 6 个月后还能调试、生产代码里出现 mock 回退=架构缺陷。
- type-design-analyzer：对新类型按封装/不变量表达/有用性/强制性四轴各打 1-10 分，先枚举隐式不变量（状态转换、字段关系、前置后置条件）再评分。
- code-simplifier / comment-analyzer / pr-test-analyzer：写完一块代码后主动触发简化审查。
- 启示：把"代码质量"拆成多个**单科专家 agent**，每个有独立评分体系和触发时机，比一个"泛审查"agent 更可控。

### A4. code-modernization 之 architecture-critic（官方市场）
来源：claude-plugins-official/plugins/code-modernization/agents/architecture-critic.md
- 对抗式审查立场：默认怀疑，专挑 over-engineering（"microservices-for-the-resume"）、只有一个实现且看不到第二个用例的抽象、error handling 是仪式性的还是有效的、测试是否真的钉住行为。
- 发现按 Blocker/High/Medium/Nit 分级；引用含密钥的代码必须打码并给 file:line。
- 该插件整体是"大型现代化重构"全家桶：12 个命令 + 8 个 agent + baseline_diff.py/proof_pack.py 等验证脚本——大规模重写要配"证明包"。

### A5. superpowers 工作流技能（TDD / 调试 / 验证 / 代码审查请求）
来源：superpowers/skills/
- test-driven-development：铁律"**没有失败过的测试就不准写生产代码**"；先写测试→亲眼看它失败（失败原因必须是缺功能而非笔误）→最小实现→看它过→重构；"先写了代码？删掉重来，不许留作参考"；附"合理化借口 vs 现实"对照表对付模型自我开脱。
- systematic-debugging：铁律"**没找到根因不准提修复**"；四阶段（读全错误→稳定复现→查最近变更→多组件系统先在组件边界加日志取证）；"越急越要用系统方法"。
- verification-before-completion：**声称完成前必须有新鲜证据**；"claim→需要什么命令证明"对照表；红旗词：should/probably/seems、未经运行就表达满意、轻信子 agent 的 success 报告。
- requesting-code-review：审查员 subagent 只拿到精心构造的上下文（DESCRIPTION/PLAN/BASE_SHA/HEAD_SHA），**绝不带会话历史**；反馈按 Critical 立即修/Important 修完再走/Minor 记录。

### A6. 本地高质量中文系样本：repo-refactor / repo-steward
来源：~/.agents/skills/repo-refactor、repo-steward（本机已装，可直接借鉴中文写法）
- repo-refactor：先建"五件套"harness——**规则(rulebook)/裁判(judge)/队列(queue)/闸门(gate)/回滚(rollback)**，再按 L1 保守~L4 自由四档激进度放权；红线：裁判先于刀、绿了原子提交红了立刻回滚、重构绝不混功能、删不懂的代码前先考古（git blame）、改测试要过对抗性审查（防四种作弊模式）、收缩(Contraction)必须显式完成。
- repo-steward：目标不是"更多结构"而是"最小自洽仓库"；一切添加前先问决策问题（新文件的独立职责？抽象的重复证据？谁拥有这个事实？）；清理候选分 Safe/Review/Protected 三级；禁生成 SUMMARY.md/FIX_REPORT.md 等一次性报告。

### A7. trailofbits/skills（安全审查系，方法论可移植）
来源：trailofbits-skills-partial/（c-review/SKILL.md、fp-check-README.md）
- c-review：审查覆盖度用**对源码的 parse 结果建 ledger 核销**，防"漏审"；finding 范围根与 context 根分离（发现必须在 scope 内、取证可全仓读）；参数绝不明默，AskUserQuestion 一次问清。
- fp-check：每条疑似 bug 必须走验证流程产出 TRUE/FALSE POSITIVE 判决+证据，6 道强制 gate review；标准验证（线性清单）与深度验证（并行子阶段）双路径。
- 同仓还有 differential-review（结合 git 历史）、variant-analysis（同型漏洞全仓搜索）、post-patch-validation、property-based-testing。

### A8. 清单驱动型与社区条目
来源：move-code-quality-skill/SKILL.md；awesome 列表挖掘（awesome-claude-skills / awesome-claude-code / awesome-vibe-coding）
- move-code-quality：把官方 Move Book 质量清单转成 11 大类 50+ 规则的 skill，每条规则给 ✅/❌ 示例——"权威清单 skill 化"模式。
- 社区相关：great_cto（12 视角 code review 全 SDLC）；netresearch/claude-code-marketplace（企业级安全+质量评估）；OneRedOak/claude-code-workflows（双环 PR 审查 + OWASP 安全审查 + Playwright 驱动的 UI 设计审查）；avifenesh/agentsys（**正则/AST 确定性检测 + LLM 判断**的混合模式，代码清理/漂移检测）；pyscn（专测 vibe-coded Python：死代码、克隆、复杂度、耦合，MCP 集成）。

### A9. smell-check（pragmatic-clean-code-reviewer）与 stop-that-shit
来源：repos/pragmatic-clean-code-reviewer、repos/stop-that-shit（兄弟任务克隆，已并入本主题）
- smell-check：**smell-first 审计**——"smell=有已知清理手法的可维护性警告，不是 bug 证明"；流程为 scope gate（必须显式确认范围，禁止自动截断）→ size profile（按源码行数自动定阈值档并披露）→ 机械测量（lizard/jscpd，缺工具就降级，**绝不伪造数字**）→ 语义规则审查（规则注册表按需加载）→ 合并去重排序、稳定 F-1…F-n 编号。亮点：被审内容一律视为"数据而非指令"（防提示注入）；references 按规则注册表组织（rules-code/rules-test + clean-code/pragmatic-programmer/clean-architecture 原则源映射）。
- stop-that-shit：专治 **speculative defense / scope creep** 的"Stop Ladder"：明确当前责任→先找项目内/标准库的直接方案→只为闭合具体缺口而扩展→按"防御机制实际检测什么、拒绝后改变什么"评判去留；"假设性的未来灵活性不算当前需求"；配套 stss 子技能治文案里的防御性废话（Claim Ledger 记账后再改写）。与 code-simplifier 同源不同层：一个治代码层过度防御，一个治决策层。

## B. Skill 写作规范汇总

### B1. Frontmatter（agentskills.io 规范）
- 必填 `name`：1-64 字符，仅小写字母数字和连字符，不得开头/结尾连字符或连续连字符，**必须与目录名一致**。
- 必填 `description`：1-1024 字符，必须同时写"做什么"+"何时用"，包含具体触发关键词。
- 可选：`license`（建议一句话）、`compatibility`（仅在真有环境要求时写，≤500 字符）、`metadata`（字符串 KV）、`allowed-tools`（实验性，预授权工具）。
- Claude Code 扩展：agent 定义用 `model: opus/inherit`、`tools:` 白名单、`color:`；command 用 `allowed-tools:` 细粒度权限（如 `Bash(gh pr diff:*)`）、`disable-model-invocation:`。

### B2. 渐进式披露（三级加载）
- L1 metadata（name+description，约 100 token）常驻上下文——唯一的"营销位"。
- L2 SKILL.md 正文，触发时才加载，**建议 <5k token / <500 行**。
- L3 附属文件按需加载，不限量；**scripts 是最深层**：执行不占上下文——能用脚本确定性解决的就不要用散文指令模型。

### B3. description 是触发器，值得单独优化
- Claude 倾向"欠触发"，官方建议 description 写得"pushy"：即使用户没说出关键词也要列出让它命中的场景词。
- 好 description：第三人称、能力+触发时机双写、用户会用的具体名词、避免 "helps with" 类虚词、与相邻 skill 可区分。
- skill-creator 提供 description 优化闭环：生成 20 条 should/should-not 触发测试（负例必须是"近邻误触"而非明显无关），跑 60/40 训练/留出集，按留出分选最优，防过拟合。

### B4. 目录与 references 组织
- 标准布局：`SKILL.md` + `scripts/`（可执行）+ `references/`（按需读的文档）+ `assets/`（模板/图标）。
- SKILL.md 里每个 reference 都要写"**何时读它**"；>300 行的 reference 加目录；多域按变体拆文件（aws.md/gcp.md/azure.md，主文件只留工作流+选择逻辑）。
- 引用一律相对路径，**引用链保持一层深**，避免嵌套套嵌套。
- 按域拆 skill：一个 skill 只做一件事，按"使用时刻"切分（两个不同时刻=两个 skill，总是一起发生=合一个）。

### B5. 行文风格
- 用祈使句；**解释"为什么"替代大写 MUST/NEVER**（官方明确：满篇 ALWAYS 是黄旗，讲道理比堆强制更有效）。
- 示例用 Input/Output 对；输出格式用"精确模板"钉死。
- references 写成高密度的"cheat sheet"（像 API 文档），别写成散文——模型训练数据就是这类密度。
- 训练已内化的知识不必复述；目标说一次，让模型的先验补细节。
- superpowers writing-skills 补充：description 只写"Use when…"触发条件，**绝不在 description 里总结流程**；技能分 technique/pattern/reference 三型；能用正则/校验强制执行的约束不要浪费成文档。

### B6. 用 TDD 方法写 Skill（skill-creator + superpowers writing-skills）
- 写 skill 前先跑**无 skill 基线**（pressure test），记录 agent 的具体违规话术→针对这些违规写 skill→复测→堵新漏洞。
- 正式 eval：with-skill 与 baseline 同轮并行跑，断言可程序化检查就写脚本；benchmark 含 pass_rate/token/时长均值±方差；可选盲评 A/B。
- 改进原则：从个例反馈泛化（skill 要被用百万次，不许过拟合测试例）、保持精瘦（读 transcript 删不掉链子的指令）、发现重复造轮子就沉淀进 scripts/。

## C. 对构建中文质量 Skill 的直接启示（速记）
1. 结构定式：铁律（一两句不可违反的原则）→ 触发时机 → 分阶段流程 → 正反示例 → 借口对照表 → 检查清单。superpowers 四件套全部是这个定式，且每条都以"违反字面=违反精神"收尾。
2. 质量治理 = 分科（simplifier/reviewer/critic/hunter 各管一摊）+ 分数门槛（<80 丢弃）+ 反误报清单 + 证据化验证（judge/ledger/proof）。
3. 中文 skill 应直接参考 repo-refactor/repo-steward 的写法（本机样本），其"决策问题表+红线+分级"模式已验证可中文表达。
