# 整合 D：人机协作工作流（计划、上下文管理、会话/记忆、多 agent 分工、人审环节）

- 阶段 3 整合产物；整合人：知识域 D
- 输入：`knowledge/02-community-discussions.md`（下称 02）、`knowledge/05-history-ecosystem-followup.md`（下称 05）、`knowledge/06-local-materials.md`（下称 06）、`knowledge/04-smells-and-tools.md`（下称 04）、`knowledge/01-repos-deep.md`（下称 01）
- 来源标注格式：（来源: 文件 · 原始出处字段）。06 的 discussion.txt 行号简写为 D:行号。
- 整合动作：同一实践的多方表述合并为一条并并列来源；三处社区真实分歧（计划颗粒度 / 单多 agent / 规则常驻 vs 索引）已裁决，裁决嵌入对应章节并显式标注「裁决」；纯产品介绍（ap-vibe 功能清单、掘金 Copilot 推广数据、superpowers 慢抱怨中的纯情绪跟帖）与工作流无关的闲聊已移除。

---

## 1. 任务全生命周期工作流（需求澄清 → 方案确认 → 执行 → 审查 → 收尾）

### 1.1 需求澄清：让 AI 提问，人负责决定

核心共识：错位（misalignment）是 AI 编码第一大失败源，且必须在写码前消除。同一实践在多个来源反复出现，合并为「拷问式澄清」一族：

- **AI 反向提问**：初始 prompt 末尾加 "ask me up to 5 questions" / "ask me any clarifying questions"——被多人复证为「magic ticket」，且长期使用会发现自己在哪些信息上总是遗漏，反哺初始 prompt。（来源: 02 · hn-harper-reed-llm-codegen-workflow @danphilibin/@jrexilius/@nijaru；02 · hn-ask-getting-better-ai @bogtog）
- **结构化拷问会话**：mattpocock 的 grilling 技能把计划映射为「设计树」，按轮（frontier=前置已全部确定的问题集）提问，每个问题带推荐答案；分工铁律：找事实是 AI 的工作（派 sub-agent 查），做决定永远是用户的；结束条件=前沿为空、无任何被静默假设的东西。这是对 Karpathy 失败模式 1（silent wrong assumptions 静默错误假设）的系统性对策。（来源: 01 · mattpocock_skills/skills/productivity/grilling；05 · followup-mnilax-12-rules）
- **问答数量治理**：spec-kit specify 的 [NEEDS CLARIFICATION] 机制——仅当「选择显著影响范围/体验 + 多种合理解读 + 无合理默认」三条件齐备才标记，上限 3 条并按 scope > 安全 > 用户体验 > 技术细节排序，其余做有依据的猜测并记入 Assumptions；澄清问题总计不超过 5 题。（来源: 05 · spec-kit 模板机制 specify 节）
- **最优 spec 四要素**：经消歧后的 ①intent（意图）②输入输出契约 ③约束 ④前置条件——"目标+障碍，有问题我问"，不是冗长的分步指令。（来源: 02 · hn-ask-experimenting-llms-coding @Jimmc414）
- **重述确认**：口述后让 AI "tell me what you understood"，既进入结构良好格式也帮它 stay on track；"Does this make sense?" 迫使其用自己的话重述问题。（来源: 02 · hn-ask-getting-better-ai @d4rkp4ttern/@helterskelter）
- **语音输入**：口述 500 词 prompt 最完整表达意图、降低「完整描述需求」的摩擦。（来源: 02 · hn-ask-getting-better-ai @bogtog）
- **意图附加说明**：出现奇怪问题时直接问 AI 并附上「我是想解决问题」——它一般能自查出直接原因；不说这句它会不停道歉之后接着再犯。（来源: 06 · discussion.txt:8）
- **反万能规则立场**：问题规避的最佳方案不是万能规则/万能提示词，而是初始化设计 + 搞懂模型特性与工具；一上来猛堆提示词会导致注意力爆炸与灾难性遗忘。（来源: 06 · discussion.txt:24）
- 多视角重述需求（每个视角是高维空间的光锥，答案在交集）可提高需求表达质量。（来源: 02 · hn-ask-getting-better-ai @seg_lol）

### 1.2 方案确认：先审计划再放行（含裁决 a）

「先审计划、人点头才执行」是全材料中收敛度最高的实践，多方表述合并：

- Harper Reed 工作流：spec → 人审设计文档 → prompt → scaffold → iterate → commit。（来源: 02 · hn-harper-reed-llm-codegen-workflow）
- Karpathy：先让模型写详细设计文档（计划/假设/tradeoff/组件/测试），仔细审到好再写代码；plan mode 自带一堆会走火的假设，偏好设计文档方式。（来源: 02 · karpathy-tweet-claude-coding-notes 经验 8/9）
- Claude Code 官方建议：Plan mode（shift-tab 2x）来回讨论到满意再执行，难任务轻松 2-3 倍；把最终 plan dump 进文档、分块执行——plan mode 计划看着好，执行输出常偏离计划。（来源: 02 · hn-ask-getting-better-ai @bcherny/@moribvndvs）
- 中文实践：找一两个 agent 先把方案和细节全部敲定，再「按图索骥」照图施工（D:5）；先让 AI 分析架构并确认需求（plan 模式）→ 执行 → 审查临时方案（D:20）；标准流程=对齐需求 → 设计方案 → 完善方案 → 确认开发顺序 → 单步执行确认 → 自审报告（D:27）。
- 工具化门禁：spec-kit 流水线「constitution（每项目一次）→ specify → plan → tasks → implement → converge（每功能一轮）」，其中 Constitution Check 是 GATE（违宪未论证则 ERROR 终止）；OpenSpec 的主要控制点=人在实现前审批 plan；Kiro 每阶段多个人工审批门；superpowers writing-plans 完成后由人类伙伴评审并选择执行方式。（来源: 05 · spec-kit 模板机制；04 · speckit-sdd/openspec/kiro-specs；01 · superpowers/skills/writing-plans）
- 阶段门语义：「人类批准 = 开始下一阶段」，不是每步都问；轻量场景跑完汇报即可，重大事项（设计批准、契约切换、删旧路径）须点头。（来源: 06 · B.6 workflow-large.md）
- 驳斥「spec=瀑布」论：写码太快，spec 变更以前不敢想的现在敢了——更多迭代移到了 spec 而非回到瀑布；spec 可随走随更新。（来源: 02 · hn-vibecoding-two-years-handwriting @aaronrobinson/@kaydub）
- 在 research/planning 阶段与 AI 一起工作、对垃圾 push back、research doc 端到端看着好了再实现；planning 阶段是 AI 跑偏后最易修复的阶段（纯英文笔记）。（来源: 02 · hn-vibecoding-two-years-handwriting @jv22222；02 · hn-breaking-spell-vibecoding @zozbot234）
- 对照失败面：当前做法「15 分钟速写设计→AI 实现」 vs 人类团队的计划、pitch、收反馈、琢磨利弊、pivot、顿悟——把不完整知识交给只有你 1% 心智模型的模型不是可靠代码的配方。（来源: 02 · hn-vibecoding-two-years-handwriting @dudeinhawaii）

> **裁决 a：计划写多细——「决定层锁死、实现层留白、验收防染绿」的中间层。**
> 三方证据：①契约+意图派有数据（obra #895：对规划流程跑过 evals，contracts-only 全部更差；弱 executor 需要高度指定的计划才能执行）；②完整细节派是 superpowers writing-plans 的设计（计划含完整测试与 TDD 步骤，executor 无决策可做）；③「文档先行会写太复杂」派（D:23：先写文档会写个超级复杂的文档，照做则 token 耗光也做不出来）。
> 裁决：**计划锁定「AI 无法独自做出的决定」——Why/Files（确切路径）/契约（类型形状与签名）/验收标准（可观察行为+测试期望）/约束（架构规则），不锁定「实现」——函数体、测试代码、shell 命令、TDD 步骤序列**。依据：obra 结案版 v6.4.2 正是此形态（"一个 step 给出确切签名、文件与 spec 的值，implementer 写主体"）；AGENTIF 研究与 GiveMe-A-Name 实践（给 GPT-5.4 高层约束 spec 刻意不指定文件行，它自主修了真 bug）支持过度指定妨碍判断；qdon314 的机械批评（计划在写整个实现为何不直接写进 .py）与 hbiagi 量化案例（完整 SQL 进计划→171KB 涨到 1.2MB、plan-editor 占 61% 成本）证明计划/实现混同双输；D:23 与 Karpathy 经验 7（不过度约束解法，呈现问题与约束让模型填细节）证明实现细节写进计划反而降质。
> 两个补丁：①关键难点处例外给伪代码（marostr fork 的 intent-level plan steps + obra 自己承认 tricky bits 可能需要伪代码）；②抽象化计划有「done-signal 染绿」反向风险——executor 可把每个验收框染绿却走计划从未意图的路线（m13v），因此验收标准必须含意图级检查（对照 spec 而非只对照测试），且分层：master plan 定约束与验收 + 多个 fine-grained 实现计划固化小块（minouris）。（来源: 02 · gh-superpowers-plans-overspecify 全串；06 · discussion.txt:23）

### 1.3 执行：小步、门内自治、台账

- **任务切小**：把一切拆成超小任务、总让它先 plan、一次只做一步；AI 做自包含的中小任务、人频繁 commit——很多问题出在让 AI 做整件事，「把代码重构得更现代」这种模糊指令它会猜。（来源: 02 · hn-ask-getting-better-ai @mirsadm；02 · hn-vibecoding-two-years-handwriting @altern8）
- agent 目前只能做中小任务；「任务图分解」技能比 chat 时代更重要——给太大的任务它会上蹿下跳而一事无成（"don't overstuff your goose"）。（来源: 04 · code-smells-yegge-junior）
- **任务级上下文预算**：每个任务控制在会话上下文窗口的 80% 以内——问题不是容量而是任务对窗口的占用率。（来源: 06 · discussion.txt:6）
- **执行内自治（内联模式的停机条件）**：任务之间不停下问「要继续吗」；只有四件事能停下你：不可逆/破坏性操作、安全敏感动作、worktree 之外的副作用（merge/push 共享分支/publish）、计划破到每条路都是猜；其余冲突以 spec 为约束权威、裁决并记台账 `Ruling: 决定了什么—为什么—错了的代价`——「没有台账的偏离是秘密做的决定」。（来源: 01 · superpowers/skills/executing-plans）
- **微循环**：一句话陈述本步意图 → 应用变更 → 跑裁判（秒级：lint/类型检查/相关测试）→ 绿=原子提交 / 红=回滚拆小重试；一个单元最多尝试 3 次后视为规则问题（修规则书而非继续撞）。（来源: 06 · B.1/B.6 repo-refactor）
- **计划/队列持久化到磁盘，每轮重读**：长任务中上下文会退化，不信会话记忆；「不存在恢复会话这回事，恢复=重读计划+队列+与 git log 对账」。（来源: 06 · B.6 workflow-large.md；01 · superpowers/skills/executing-plans「会话记忆活不过压缩」）
- **Pattern-first**：同类错误第 2 次出现=规则有罪 → 修规则书 → 重新生成整批受影响文件，绝不违反规则对单文件打补丁。（来源: 06 · B.3 code-refactor.md）
- 执行中发现更好方法：adapting 意味着「违反」计划——这正是裁决 a 中间层的原因；executor 应保留工程判断并把偏离记录在案。（来源: 02 · gh-superpowers-plans-overspecify @Abioy）
- 走错头三步就重来：「找到 agent 犯第一个错的地方，改 prompt，删光全部代码从头重跑」——代码很便宜，带病续跑很贵；"regenerate, don't fix"。（来源: 02 · hn-vibe-vs-agentic-engineering @dataviz1000/@NickNaraghi）
- 长会话纠偏：第一次说 "No, it should be…" 就近乎 game over，连说 3 次基本完蛋——此时应新开会话重置而非继续对话纠偏。（来源: 02 · hn-vibe-vs-agentic-engineering @randyrand）

### 1.4 审查：生成/评审分离、两轴、跨模型

- **人审是最终仲裁**：开发者仍会向人求助的第一理由是「当我不信任 AI 的答案」（75%）。（来源: 04 · code-smells-so-survey-2025）
- **生成/评审分离铁律**：不能让 AI 同时做代码生成和代码评审/测试——要么 AI 生成+人评审，要么人生成+AI 辅助评审，绝不双 AI 同源。（来源: 04 · code-smells-hn-sloppy-code @thelostdragon）
- **两轴评审**：Standards（是否符合 repo 文档化标准 + 固定 12 条 Fowler 坏味道基线）与 Spec（是否忠实实现 issue/spec，抓缺失/scope creep/可疑实现）分两个并行 sub-agent 跑、互不污染，聚合时不合并不重排、不跨轴选唯一赢家——防止一轴遮蔽另一轴。（来源: 01 · mattpocock_skills/skills/engineering/code-review）
- **多 agent 评审流水线**：5 个并行 agent 各带独立视角（CLAUDE.md 合规/浅层 bug 扫描/git blame 历史语境/历史 PR 评论/代码注释指引）→ 每个问题独立打置信度分（0-100 rubric）→ 过滤掉低于 80 分的；附误报清单（已存在问题、linter 会抓的、学究式挑刺不算）。（来源: 01 · claude-plugins-official/plugins/code-review）
- **跨模型交叉验证**：不信任单个 LLM 的意见——见过 Claude 保证正确、喂给它 Codex/Gemini 的批评后立刻道歉；习惯拿 2nd/3rd opinion。（来源: 02 · hn-vibecoding-two-years-handwriting @rtp4me/@kaydub）
  - 实证边界（重要）：交叉评审**不对称**——Claude 审 Codex 草稿 71.6%→89.7%（有效），Codex 审 Claude 草稿 91.4%→82.8%（**不升反降**）；同模型自评对弱草稿有效（84.5%）、对强草稿无效。落地：写明方向（用 Claude 审 Codex，别反过来）、按草稿质量分层（弱→自评/跨模型，强→跳过）、评审 prompt 只给「意图+草稿，只审不改写」。（来源: 05 · followup-cross-model-review-evidence）
- **收敛循环替代一次性生成**：implement → converge 循环 until Converged；bug 修复三值裁决 verified/partial/failed，「缺验证不算修复成功」。（来源: 04 · speckit-sdd；05 · spec-kit 模板机制）
- **让人能审得动**：用 ASD-STE100 式受控语言让 LLM 输出更可读（宽松版即可——完整 STE 丢 46.8% 代码特定事实，80% 校准恰是简洁/保真的经验平衡点）；「可数、可查的清晰度规则」是人审 AI 输出的杠杆。（来源: 05 · followup-karpathy-explain-llm-output）
- **完成前验证铁律**：没有新鲜验证证据不得宣称完成——本条消息里没跑过验证命令就不能说它通过；红旗词 should/probably/seems；"agent 报 success" 不算证据，VCS diff 才算。（来源: 01 · superpowers/skills/verification-before-completion）
- **报告你没查的部分**：实际查了什么就报什么并直说没查什么——LLM 读了 6 个文件会像读了 20 个那样总结，不是不诚实，是因为总结读起来更好。（来源: 02 · karpathy-skills-PR197-IN-PRACTICE）
- **中文实践的双层审查**：AI 审完自己再审（是否存在临时方案、删死代码、写测试）→ 人工复查与测试 → 提交。（来源: 06 · discussion.txt:20）

### 1.5 收尾：清理、规则沉淀、记忆交接

- **模型清理自己的残留**：删临时/调试文件与代码、tail 构建日志确认无杂散错误和警告；每次跑完让 AI 删冗余代码、过时文档。（来源: 02 · karpathy-tweet-claude-coding-notes 经验 6；06 · discussion.txt:18）
- **规则沉淀闭环**：与 agent 结对改完一个单元后让它 "based on the current chat" 写 rules 文件（含例子+理由），下次只说 refactor；完成任务后让 agent 写规则文档同样有效。中文等价物：提示词「把规则当代码管」——读 AGENTS.md/CLAUDE.md，删掉代码里已不存在的旧规矩，留下的每条补一句为什么，确认后让本地 agent 执行。（来源: 02 · hn-ask-getting-better-ai @serial_dev/@rpwverheij；06 · discussion.txt:13）
- **紧凑报告**：改了什么/如何验证/剩余风险/显式 TODO；不生成一次性报告文件。（来源: 06 · B.7 repo-steward；01 · 多处）
- **记忆交接**：见 2.3。

---

## 2. 上下文与会话管理实践

### 2.1 会话预算：80% 上限与"从头跟到底不存在"

- 一个 agent 从头跟到尾不存在；频繁 compact 也不行——compact 太多同样导致更慢、更烧钱。（来源: 06 · discussion.txt:5）
- 真正的问题不是上下文容量而是任务占用率：每个任务控制在会话上下文窗口的 80% 以内；256K 才是舒适区间。（来源: 06 · discussion.txt:6/D:5）
- 上下文满时开新 chat，带三样东西再继续：测试+工作定义+相关文件。（来源: 02 · hn-ask-getting-better-ai @caseyw）
- 代码库和文档变大后开始幻觉（约 50% 上下文时），会真的忘记更新部分代码。（来源: 02 · hn-vibe-vs-agentic-engineering @Insanity）
- 对「大上下文窗口」的认知纠偏：千万行代码库没法工作是误解——你自己也不把千万行装脑内，靠系统布局直觉+搜索定位；LLM 同理。（来源: 02 · hn-ask-llm-coding-established-codebase @lukevp）
- context rot 有官方表述：token 越多召回越差，目标是「最大化期望结果可能性的最小高信号 token 集合」。（来源: 04 · context-engineering-anthropic）
- 1M 上下文的反直觉副作用（社区猜测+官方回应并存）：用户不再 200k 后 /compact → 表现变差；官方缓解建议包括强制更短上下文 `CLAUDE_CODE_AUTO_COMPACT_WINDOW`。（来源: 02 · gh-unusable-complex-tasks @bcherny）

### 2.2 compact 的失效模式与替代方案

- compaction 后无法回看历史（工具层缺陷）：数据完整在 transcript.jsonl 但 UI 零路径访问——用户无法审计压缩后的推理、无法回看形成 plan 的探索。（来源: 02 · gh-compaction-no-review）
- compaction 的复合故障链：项目指令被降权、活动 plan 状态丢失、压缩后 hooks 被降权（即使 SessionStart 重注入，模型把 hook 输出当低于压缩摘要的优先级）——压缩后用户没有任何恢复路径。（来源: 02 · gh-compaction-no-review @ThatDragonOverThere）
- **架构性替代：消除对历史的依赖而非恢复它**——job 状态放在上下文窗口之外的一个 markdown 文件里，决策落地即写入；会话压缩或结束时，下一个会话读那个文件而非历史（自测 6 例：状态 93,073 字符、接管时实际读 53,339）。（来源: 02 · gh-compaction-no-review @bestiaya）
- 官方机制四件套：Compaction（压缩）、Structured note-taking（笔记持久化在窗口外，事后重载——"persistent memory with minimal overhead"）、Sub-agent（干净上下文做深工作只回传 1000-2000 token 摘要）、Just-in-time retrieval（不预载，保留轻量引用运行时取）。（来源: 04 · context-engineering-anthropic）
- compaction 下各机制行为差异（选型依据）：Rules 会重新注入（持续生效）；Skills 正文仅调用时加载；Subagents 完全隔离；Hooks 完全绕过 compaction（配置在上下文之外）。（来源: 04 · steering-claude-code-blog）

### 2.3 记忆交接：索引+正文两层

- 对话达到一定数量后让 AI 生成对话记忆精简版，用 skill 交接对话、在新对话继续开发；新会话开全局记忆索引。（来源: 06 · discussion.txt:21）
- **两层结构**：全局记忆做成「索引+记忆」两部分以减少 token 消耗；新会话会让 agent 重新耗 token 了解内容，但至少少犯错、规则也会重新捡起不至于忘。（来源: 06 · discussion.txt:21）
- Karpathy 同款愿望：内置 scratchpad/notebook 承载跨会话增长的项目上下文——某种会话/项目级持久记忆，且不是整个对话转录的朴素拷贝。（来源: 02 · karpathy-tweet-claude-coding-notes 愿望 2）
- 工程化变体：TODO 文件用自由文本记想法、隔一阵告诉 agent "I updated the TODO file"（排队 prompt）；temp/ 目录丢上下文 md/txt；记忆交接时让新会话继承验证证据，避免重复劳动与结论丢失。（来源: 02 · hn-ask-experimenting-llms-coding @hsn915/@dimitri-vs；04 · context-engineering-anthropic）
- AGENTS.md 保持简洁、协作类文件入口用索引呈现——与两层记忆同构：入口索引常驻，正文按需。（来源: 06 · discussion.txt:10）

### 2.4 文件整洁度天花板效应

- 把 AI 丢进整洁度 60 分的文件里，它尽管有 80 分的书写能力，也只会发挥 60 分——需要定期清理。（来源: 06 · discussion.txt:12）
- 同向证据：Claude Code 在干净、结构良好的代码上工作得更好（跟人类一样）；组织良好、运行连贯的代码（无论谁写）都更容易迭代；垃圾代码污染 AI 的上下文、诱导它写更多垃圾。（来源: 02 · hn-cult-of-vibe-coding @tedd4u；02 · hn-vibe-vs-agentic-engineering @vehemenz；02 · hn-vibe-vs-agentic-engineering @zozbot234）
- 失控点在文件层级而非内容：AI 不会在 AGENTS.md 里乱写，但不能分辨项目文件层级，经常把信息写进高层文件——层级越深越乱、增加上下文负担且难保证来源唯一；对策：index 文件定义项目协作文件层级 + 写入规则约束（「这相当于一种编程，但 AI 读文字规则容易错漏」）。（来源: 06 · discussion.txt:10）
- 文件变大之前就拆分/分章，否则后期更难维护；实际架构与已淘汰部分的文档分开。（来源: 06 · discussion.txt:19）
- 修大文件的失败教训与成功路径：让 AI 自己记录会内容讲太长或实现打转；成功案例=Claude 子 agent 无视文件规则、按章节分批重整——即用「分批+子代理」绕开单会话重写。（来源: 06 · discussion.txt:19）
- AI 时代给项目做减法往往更重要（减法失灵就是大企业病的机构膨胀原理）。（来源: 06 · discussion.txt:15/16）

---

## 3. 行为约束技巧

### 3.1 两层约束（含裁决 c 的规则分布部分）

- **两层约束**：第一层最外面的全局约束 + 具体项目第二层更详细约束——有效果，但核心是更强的约束与边界。（来源: 06 · discussion.txt:28）
- 指令只是输入，和普通对话同一性质、同一优先级，并无特殊强制性——rule 设置了，听不听全由它：第一次会听，等你忘了它也一起忘了。（来源: 06 · discussion.txt:28/D:22）
- 模型差异是约束生效的前提变量：preview 版模型行为可能不受收敛；用国产模型时对规则的敬畏意识差；聪明模型会自言自语「这违反了用户定的规则」另想方案；训练语料里约束对应明确、练得好的模型比较听话——搞懂模型特性优于万能提示词。（来源: 06 · discussion.txt:7/24/28）
- AGENTS.md 治理：越堆越多管不住它（D:3）；严格控制 AI 又可能导致规则文件挤占上下文（D:6）——常驻规则有内建的体积税。

> **裁决 c：规则常驻上下文 vs 索引化按需加载——按「强制性×频率」三档分层，不是二选一。**
> 证据：①常驻派（两层约束、每步重读规范：D:26 的五步流程每步重读编码规范与技术文档）；②索引派（AGENTS.md 简洁+索引入口：D:10；Anthropic just-in-time retrieval 与渐进式披露三级模型）；③失效数据（CLAUDE.md 约 80% 遵循率、超 200 行急剧下降、12 条以上合规率 76%→52%；rulereceipt 解析 559 个规则文件：63% 内容不是指令、真规则中约 35% 可 hook 化；Anthropic 官方明说指令遵守边际递减、「当某事绝对不能发生时指令是错误的工具」）。
> 裁决：**第一档——可机械判定的强制规则（必须跑测试/永不碰 .env/commit 格式/文件边界）升格为 hooks/权限，物理强制且零注意力成本，不占常驻上下文；第二档——判断类规则+全局事实（命名/架构/何时提问/构建命令）常驻但极简（<200 行、≤12 条、每条可测试、两条信息不得冲突否则双双被忽略 D:noiv）；第三档——领域细节/长参考索引化，入口常驻、正文按需加载（index 文件 D:10 与记忆两层 D:21 同构）。**三档分别对应 Anthropic steering 的「确定性行为→hooks；事实→CLAUDE.md/rules；流程→skills」分工。（来源: 04 · steering-claude-code-blog；05 · followup-mnilax-12-rules；02 · gh-claudemd-rules-ignored @rulereceipt/@durban01；06 · discussion.txt:6/10/21/26/28）

### 3.2 强制性阶梯：钩子 > 挂代理 > 规则文件 > skills/MCP

- 社区排序：钩子是目前大模型工具里强制性最高的；并驾齐驱的是挂代理；再次是容易被上下文稀释的 AGENTS.md；其他 skills 或 MCP 不具备太多强制性。（来源: 06 · discussion.txt:11）
- 钩子是拦截点/卡口：满足条件一定触发、属应用层机制，不管上下文怎么稀释都执行；可用钩子实现轮巡或设触发词强制调用 skills。（来源: 06 · discussion.txt:11）
- "A system prompt is a request. A hook is a guarantee."——CLAUDE.md 说服、permissions 过滤、hooks 强制并响应；exit 2 阻断且 stderr 原因回给模型。（来源: 04 · hooks-community-guide-konishi；04 · hooks-claude-code-reference）
- 机制分工实证：mhofer1976 的诊断——CLAUDE.md 像 system message 在对话开头被读，对话变长规则逐渐被忘（HEAD 位置、Lost in the Middle）；durban01 两堆分法——可执行的规则根本不该是指令应是 hooks，判断类规则留在 CLAUDE.md（会随上下文退化且无解）；yurukusa——"CLAUDE.md 是给模型的建议；Hooks 是代码执行——物理上阻止动作"。（来源: 02 · gh-claudemd-rules-ignored）
- 但 hooks 也不是银弹：hook 每轮重注入的项目硬约束仍不绑定（8 小时会话中 agent 仍向下游推荐该规则禁止的 workaround）——「信息 present 且 available，存在不等于被遵守」；持久记忆里的安全规则在 subagent dispatch 时不绑定。结论：约束要多层冗余，且不可替代人审。（来源: 02 · gh-claudemd-rules-ignored @petrinhu）
- 规则文件自身是攻击面：AGENTS.md/cursorrules 从网上复制时应视为潜在 prompt injection 载体（可诱导依赖替换）。（来源: 04 · pkg-hallucination-rule-file-injection）

### 3.3 规则文件的写法与失效模式

- 规则数量天花板：12 条以上合规率骤降（18 条时 76%→52%）——Claude 模式匹配到「规则存在」而不真读；针对自己真实犯过的错保留 6 条好过 12 条里 6 条用不上。（来源: 05 · followup-mnilax-12-rules）
- 无效写法（负结果清单）："Be careful"/"think hard"/"really focus" 是纯噪音（合规率跌到 ~30%，不可测试）；"act as senior" 无效；在 CLAUDE.md 放示例而非规则（3 个示例 ≈ 10 条规则的上下文成本且过拟合）；依赖可能不存在的工具的规则会静默失效（换成能力无关措辞）。（来源: 05 · followup-mnilax-12-rules）
- 每条规则应回答「这防止什么失误」——行为契约不是愿望清单；换成具体祈使句（"state assumptions explicitly"）。（来源: 05 · followup-mnilax-12-rules）
- 两条信息冲突时它会两条都忽略——精确语言是关键，别用跨领域歧义词。（来源: 02 · hn-ask-getting-better-ai @noiv）
- scope 写法：对「什么在改动范围内/不在」要极其显式且保持窄；绝不说「X 看起来不对/多余」——模型会当作动手重构/删除的邀请。（来源: 02 · karpathy-tweet-claude-coding-notes 经验 1/2）
- 纠正的持久化：把用户纠正（"don't do X"/"always use Y"）提取为 feedback memories，经 SessionStart/PreCompact/Stop hooks 自动运行——修不了 HEAD 位置问题但让纠正活过压缩、每轮重读。（来源: 02 · gh-claudemd-rules-ignored @junaidtitan）
- 范例：Mnilax 12 规则在 50 任务 × 30 代码库 × 6 周上把失误率 ~41%→3%，合规率几乎零额外注意力成本（新规则覆盖原 4 条未覆盖的失败模式，不争夺同一注意力预算）——规则库的价值在覆盖不同失败模式而非数量。（来源: 05 · followup-mnilax-12-rules）

### 3.4 显著信号与抽背（针对规则稀释）

- 用国产模型时在铁律里加明显信号：称呼、emoji、特殊标志——称呼变了或不发 emoji 了，说明规则被稀释，就再喂一轮。（来源: 06 · discussion.txt:7）
- 被动约束用钩子轮巡：每 5-8 轮抽背——七条铁律随机抽一条问记不记得，不记得就重读。（来源: 06 · discussion.txt:7）
- 同原理的产出侧观察：CODEX 工作难追踪、阅读量过大——加识别符号方便观察 AI 行为是个思路（可观测性信号）。（来源: 06 · discussion.txt:9）
- 模型自查手段：给模型自检工具（如 Puppeteer MCP 让 Claude 在浏览器里自检）再提 2-3 倍。（来源: 02 · hn-ask-getting-better-ai @bcherny）

### 3.5 其他行为微技巧

- before/after 成对示例 + negative prompt（基于过往挫败列出不想要的事）；「照这个文件做」这种太宽的引用无效。（来源: 02 · hn-ask-getting-better-ai @rdrd/@cat_plus_plus/@hurturue）
- course correct 后发 self-reflection prompt，把需人工澄清的东西移回规则文件——「它写 claude.md 比我写得好」。（来源: 02 · hn-ask-getting-better-ai @tlarkworthy）
- "it's OK if you don't know"——管理语气和预期，否则 LLM 会朝你给的任何风车冲刺。（来源: 02 · hn-harper-reed-llm-codegen-workflow @becquerel）
- 把 AI 当 junior 工程师（聪明、快、但缺经验）或「稍微不称职但非常快的实习生的经理」：清晰 scoped 任务+清晰期望与验收标准+可能处给自由度+信任但验证。（来源: 02 · hn-claude-code-dumbed-down @koverstreet；02 · karpathy-tweet-claude-coding-notes 心法）

---

## 4. 多 agent 协作模式与成本（含裁决 b）

### 4.1 分歧图谱

- **反多 agent 阵营**：现在人人都在造 agent orchestrator 却没听到多少成功故事——「我怀疑这只是更精致的烧 token 方式」；多 agent 编排的失效观察（agent 打架、hook 级联、skill 加载冲突、跨会话多步工作流断裂）；本地同时跑约 3 个 agent（codex/gemini CLI 分 tab）+worktrees——再多就喂不活也管不过来；团队 agent 影响不对称：70% 认同减任务耗时，仅 17% 认同改善团队协作。（来源: 02 · hn-ask-experimenting-llms-coding @cedws；05 · followup-mnilax-12-rules；02 · hn-ask-llm-coding-established-codebase @siliconc0w；04 · code-smells-so-survey-2025）
- **context piping 成本是真实的**：「我把全部时间都花在 context piping 上了」（催生 spec/recipe 自动应用方案）；重量级案例：计划携带完整 SQL → plan-editor subagents 带 740k-967k token 上下文运行、占加权成本 ~61%（implementer+code reviewer 仅 ~7%）、计划 46 小时从 171KB 涨到 1.2MB——编排层自己吃掉了执行层。（来源: 02 · hn-ask-experimenting-llms-coding @zmgsabst；02 · gh-superpowers-plans-overspecify @hbiagi）
- **多 agent 收益也是真实的**：跨模型评审 +18pp（方向正确时，见 1.4）；「一个 agent review 另一个 agent 的作品效果好得惊人」（Pythagora 配 2 个不同 Reviewer agent）；多个模型对一处变更争论产生的洞察远好于单模型评审；Anthropic 官方：专职子代理在干净上下文里做深工作、只回传 1000-2000 token 摘要，复杂研究任务显著优于单代理。（来源: 05 · followup-cross-model-review-evidence；02 · reddit-chatgptcoding-top-year 帖4；04 · context-engineering-anthropic）
- **中间立场（含中文社区）**：「一个 agent 从头跟到底不存在」（D:5）——但频繁 compact 同样不行；上下文更少的 subagent 表现更好——让 fresh context 的 subagent 只读必要文档、以精简上下文干活；superpowers 的内联 vs subagent 二选一交付：内联只付一个上下文+末尾一个评审者，subagent 模式每任务付新实现者+新评审者（每个都从零重读代码库）。（来源: 06 · discussion.txt:5；02 · gh-superpowers-plans-overspecify @envictor；01 · superpowers/skills/executing-plans）
- **流程重税的实证**：superpowers 用户普遍抱怨 brainstorming→writing-plans→subagent-driven-development 一个 feature 要几小时、10 分钟的请求跑 30-45 分钟；规避法：2-3 个 chat 分工（chat1 规划、chat2 评审、chat3 执行）；trivial 任务不应被强制进全套流程（brainstorming-manual 变体的动机）；慢的根源之一疑似 subagent 自动选 heavy 模型+最高 effort。（来源: 02 · gh-superpowers-slowness @YOMXXX/@AkshayAdiga1997/@dmalis/@ChenTingToDo）

> **裁决 b：按任务生命周期分段，而不是「单 vs 多」二选一。**
> 裁决：**规划期用单会话深上下文（规划需要全局视野，拆开反而丢失一致性）；执行期按任务边界换 fresh-context 单元（每任务或每几任务一个干净上下文，只带该任务的必要文档）；评审期必用独立上下文（最强可用模型或跨模型，方向按 1.4 的不对称证据选）。**依据：长会话退化有大量证据（2.1/2.2），「从头跟到底」出局；但中间编排层的 context piping 有实测 61% 成本案例与「更精致的烧 token」批评，故编排要浅——执行并行度甜点区很低（实现 agent ≤2 个，token 成本 3-10 倍），机械批量变更才 fan-out 给子代理且只带回结论；评审者最受益于更强模型/独立上下文（投入花在刀刃上）。频率校准：简单/已明确的工作不强制进全套多阶段流程（trivial 任务裸跑即可），与 superpowers 慢抱怨的教训一致。（来源: 06 · B.3 code-refactor「上下文与并行」节；01 · superpowers/skills/executing-plans；02 · gh-superpowers-slowness）

### 4.2 多 agent 的具体形态与工具支撑

- 每任务新实现者+新评审者（subagent-driven）vs 本会话实现+末尾一个终审评审者（inline）——后者用「spec 是简报、台账是记忆、TDD 是每任务闸门、终审评审者是第二双眼睛」保住前者的两样收益；终审是整次运行买的唯一新上下文，不许跳过、不许用自己读 diff 顶替。（来源: 01 · superpowers/skills/executing-plans）
- 评审者拿到的是精心裁剪的上下文——绝不是你的会话历史；派 subagent 让 diff 与评估活在它的上下文里，只有 findings 回来（保护主上下文）。（来源: 01 · superpowers/skills/requesting-code-review）
- 团队级形态：Claude Code + worktrees（shell 脚本管理）+ 根目录 guardrails 目录+README 指引 agent 找适用规则 + stacked PRs（堆叠 PR 解开 validation/review 瓶颈、对 PR 尺寸膨胀形成向下压力）+ 多 review 机器人并跑。（来源: 02 · hn-ask-llm-coding-established-codebase @weeksie）
- 探索性重写实验放独立 worktree；机械批量变更派子代理只带回结论。（来源: 06 · B.3 code-refactor.md）
- 失败警示：初始速度正是「Loss Disguised as a Win」——开局烙进致命错误假设，最终全部还回去；多 agent 编排不改变这一点（反而因初期快而放大）。（来源: 02 · hn-breaking-spell-vibecoding @JSR_FDED）

---

## 5. 已裁决矛盾（汇总）

1. **计划颗粒度**（1.2 裁决 a）：锁决定层（Why/Files/契约签名/验收/约束）、放实现层（函数体/测试代码/步骤序列），关键难点例外给伪代码；验收标准须防「染绿式背离」。superpowers v6.4.2 官方结案、AGENTIF、hbiagi 成本数据三方收敛。
2. **单 vs 多 agent**（4.1 裁决 b）：按生命周期分段——规划单会话、执行 fresh-context 浅编排（实现并行 ≤2）、评审独立上下文/跨模型；简单任务不强制全流程。
3. **规则常驻 vs 索引化**（3.1 裁决 c）：按强制性×频率三档——机械规则升 hooks（零注意力成本）、判断类常驻但极简（<200 行/≤12 条）、细节索引化按需加载。

---

## 6. 待裁决矛盾（交主 agent）

1. **人审深度**：Willison 黄金法则「不能向别人解释的代码就不 commit」vs 其 2026 融合论（agent 当半黑盒服务、不再逐行审，但要警惕 normalization of deviance 偏差正常化）——信任边界随 agent 可靠性移动到哪一档？分级判据（风险×可验证性）需要主 agent 定。（来源: 05 · vibe-history-willison-definition/vibe-history-willison-convergence）
2. **审查自动化程度**：激进派「时间投资前移到设计，默认 90% 代码是稳的，只有关键任务/界面迭代值得人审」vs 保守派「我今天不懂这代码没问题、我永远不需要懂是完全不同的断言——你可能把公司押在这个答案上」。（来源: 04 · code-smells-hn-good-code-agents @linesofcode vs @AnimalMuppet）
3. **过程纪律 vs 模型能力演进**：capability-first 派「随着模型变好，skill 应教意图理解与工程判断、少教固定细节流程」vs process-first 派（superpowers）「详细计划让弱模型也能执行，evals 显示更抽象的计划全部更差」——Skill 的默认姿态按当前模型能力还是按能力上升曲线设计？影响本 Skill 的整体颗粒度。（来源: 02 · gh-superpowers-plans-overspecify @GiveMe-A-Name vs @obra）
4. **AI 代码质量上限**：「所有 AI 代码都低于在乎质量的人类」vs 「投入时间 train/prompt/verify/review 的 LLM 代码可以比人写的更干净」——决定 Skill 目标定在「止损到人类水平」还是「超越人类水平」。（来源: 02 · hn-ask-getting-better-ai @Fire-Dragon-DoL vs @jf22）
5. **规则治理的投入产出**：中文社区「让 AI 治理规则文件比让它写代码效果差太多、容易被气到」+「钩子抽背铁律」vs Mnilax 的 12 规则 41%→3% 数据（但其口径为自测）——规则工程化的收益边界在哪，需要主 agent 权衡两类证据的置信度。（来源: 06 · discussion.txt:3/7 vs 05 · followup-mnilax-12-rules）
