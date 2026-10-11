# 追查补档笔记(followups)

> 2026-10-11,第一轮遗留 11 条线索的逐一追查。网页原文存 `raw/articles/followup-*.md`,仓库在 `raw/repos/`。

## 1. spec-kit(github/spec-kit)templates 精读 ✅

- 克隆至 `raw/repos/spec-kit`(已删 .git);核心在 `templates/` + `templates/commands/`。
- **流水线**: constitution(项目宪法) → specify(spec.md) → clarify(苏格拉底补问) → plan(plan.md) → tasks(tasks.md) → implement → checklist(质量门)。
- **constitution-template.md**: 项目级不可协商原则(示例含 "Test-First (NON-NEGOTIABLE)");Governance 节要求所有 PR/review 校验合规、"复杂度必须被证明合理";带版本号+批准/修订日期,宪法高于一切实践。
- **specify.md 机制**: 只写 WHAT/WHY 禁 HOW(无技术栈/API);用户故事 P1-P3 优先级且**每条独立可测**(单条即可交付 MVP);Given/When/Then 验收场景;FR-xxx 必须可测;成功标准必须可测量+技术无关;**[NEEDS CLARIFICATION] 上限 3 条**、优先级 scope>安全>UX>细节,其余用合理默认并写入 Assumptions;写完自动生成"规格质量 checklist"自校验,最多迭代 3 轮。
- **plan-template.md**: Constitution Check 是 Phase 0 前的 GATE(设计后再查一次);**Complexity Tracking 表**(违规项/为何需要/为何拒绝更简方案)——强制为复杂度辩护,直接对治 over-complication。
- **tasks-template.md**: Setup → Foundational(阻塞全部故事)→ 按用户故事分 Phase(MVP 优先)→ Polish;`[P]` 并行标记(不同文件无依赖)+ `[Story]` 可追溯;测试先写且必须先 FAIL;每 Phase 后 Checkpoint 独立验证;任务完成即打 `[X]`。
- **implement.md**: 前置脚本校验 prerequisites;checklist 是**只读质量门**(有未勾选项即 STOP 问用户);逐 Phase 执行、尊重依赖、失败即停;结束对照 spec/plan 验证 + Done When 清单。
- **checklist.md**: 核心理念 **"Unit Tests for English"——checklist 测的是"需求写作质量"而非实现**;`[x]` 语义=评审者认定需求达标,**生成命令禁止自勾**;≥80% 条目须带 traceability 引用;implement 只读不改动标记。

## 2. ap-vibe(ginsonko/ap-vibe)十维雷达 ✅

- 克隆至 `raw/repos/ap-vibe`;定义在 `src/ap_mind/project_documents.py` 的 `DIMENSIONS`。
- **十维**(0-100 分,null=未知): intent 目标符合 / logic 逻辑一致 / completeness 功能完整 / reliability 可靠恢复 / security 安全隐私 / performance 性能成本 / maintainability 可维护性 / compatibility 兼容扩展 / usability 用户体验 / validation 证据验证。
- 配套机制: 11 章项目档案(风险章内嵌十维评估);**有分数必须给 reason + evidence_refs**;"资料完整≠质量满分,雷达图没填满不等于需要人工审批"(反模板填充);章节无变化不重写;recovery 章有 do_not_repeat(下次不要重做的事)。

## 3. Karpathy explain-agent-output 推文 ✅(二手还原)

- x.com/karpathy/status/2105819303471976479(2026-10-02);x.com 直抓仍被截断,nitter/jina 全灭(客户端网络封锁),经 kgolubic.com 详解文章还原 → `followup-karpathy-explain-llm-output.md`。
- 要点: "我们将花远比现在多的时间**理解语言模型输出**";格式递进 纯文字→图→交互 HTML→3B1B 风格视频;技巧一 = 让 LLM 用 **ASD-STE100 受控英语**解释,并放宽到 "80% STE"(全严格会丢 46.8% 代码事实,宽松丢 8.5%)。生态已有 SimpleEnglish 等 skill(HN 363 分):"'Clearly' 是观点,STE 规则可数"。

## 4. Mnilax 推文全文 ✅(完整补全)

- x.com/Mnilax/status/2053116311132155938(2026-05-09,X 长文),return_format=text 抓到全文 → `followup-mnilax-12-rules.md`。
- 命名化: Karpathy 三失败模式(silent wrong assumptions / over-complication / orthogonal damage)→ Forrest Chang 4 规则(Think Before Coding / Simplicity First / Surgical Changes / Goal-Driven Execution,12 万 star)→ 作者加 8 条(模型只做判断类任务 / token 预算硬上限 / 冲突要暴露不要平均 / **写前先读("看起来正交"是代码库最危险的话)** / 测试验证意图非行为 / 每步 checkpoint / 匹配代码库规范 / fail loud)。
- 数据: 失误率 41%→11%(4 条)→3%(12 条);**超 12 条合规率反跌(76%→52%,CLAUDE.md ~200 行天花板)**;"be careful/think hard"类模糊指令=噪音;示例比规则贵 3 倍上下文且过拟合。

## 5. HN「Will vibe coding end like the maker movement?」✅

- 帖: news.ycombinator.com/item?id=47167931(405 分/439 评,2026-02-26);原文 read.technically.dev → `followup-vibe-coding-maker-movement.md`(全文+高赞评论摘录)。
- 原文核心: vibe coding **跳过了 scenius(受保护玩耍)阶段**直接进生产;"评估麻醉"(速度感麻痹判断力);价值上移模型层;产出=品味/奇观/礼物三种正产品+**信息废气**(失败原型的信号可结构化为资产)。
- 高赞评论: bitwize "vibe coding 与 maker 相反:思考外包 vs 自己造所以理解";epiccoleman 反例(降低'值得动手'门槛);ytoawwhra92 实操(小任务+成熟库+静态分析标流程+前后构建对比)。

## 6. 掘金 7412505754379468800 ✅

- 全文抓取成功 → `followup-juejin-7412505754379468800.md`。
- 实践者自述(Cursor→Composer→Claude Code): 动手前方案讨论 5-10 轮;PRD 思维分模块定数据结构;gh+MCP+prompt 缓存;**agent 时间越久越易失控,靠 clear+重发 PRD 拉回**;上线观"能跑就行",事后补测试——中文圈典型 vibe coder 质量观样本。

## 7. Veracode 2025 GenAI Code Security Report ✅(一手确认)

- veracode.com/blog/genai-code-security-report/ → `followup-veracode-2025-genai-code-security.md`。
- **45% 失败率出处确认**(100+ LLM×15 语言×48k 样本 SAST);Claude 3.5 Sonnet 19% vs Code Llama 2 7B 78.4%;PHP 56.9%/C 52.4%/Java 47.7% vs JS 34.1%/Py 31.7%;Top CWE: XSS 33.5%/路径遍历 24.5%/OS 注入 20.1%/SQLi 18.1%/硬编码凭证 13.4%;**好提示词 31.5%→24.3%**;代码微调模型反而更差;**结构化 review 后可降到 ≤10%**——"<10%"确为一手结论。

## 8. 跨模型交叉 review 证据 ✅(找到对照实验)

- → `followup-cross-model-review-evidence.md`。
- **arXiv 2607.21656**(2026-07,116 道 LCB 中难题,6 组对照): Claude 审 Codex 71.6%→**89.7%**(p=.001);Codex 自评→84.5%;**反向 Codex 审 Claude 91.4%→82.8%(负收益!)**;Claude 自评无变化 → 交叉评审**不对称**,方向比"是否有第二模型"更重要。
- 工具: navels/neal(写/审角色分离)、WDahah multi-agent plugin;neal 默认方向恰是论文负收益方向——实践与证据冲突点。

## 9. arXiv 2511.15817 ✅(复核)

- "A Causal Perspective on Measuring, Explaining and Mitigating Smells in LLM-Generated Code"(Velasco 等,William & Mary 系)。
- PSC(Propensity Smelly Score)概率度量某模型生成特定 smell 类型的倾向;因果分析表明 **prompt 设计与模型架构决定 smell 倾向**,据此提出缓解策略;用户研究表明 PSC 信号可辅助人的质量判断。前轮已存 `code-smells-arxiv-causal-smells.md`,本次复核一致;摘要无 "defensive over-programming" 字样(该提法不在本文)。

## 10. CIQ「The Imitation Game」✅

- ciq.com/blog/the-imitation-game-when-ai-writes-the-code/ → `followup-ciq-imitation-game.md`。
- LLM=模仿机器,向"平均水平代码"回归;2,200 万行内部对比: AI 代码圈复杂度略优但**认知复杂度恶化**(认知/圈比值升);**重复代码 +81%(8.5% vs 4.7%)、千行重复块 +115%**——模型跨请求无记忆,同一问题反复生成相似解;缓解=认知复杂度门禁+重复阈值强制抽库+"先查现有工具再写"指令。

## 11. aislopfix.dev 文章 ✅(正文在 HN 自帖)

- 站点本身是 2.4KB 单页 SPA 无文章;正文找到: **HN 48860941**(2026-07-10, avdept)→ `followup-aislopfix-6-months.md`。
- 6 个月修 slop 观察: 头号问题 **无数据作用域(IDOR)**("所有项目都同样建法",非技术作者+现代 LLM 仍犯);前端直连库/凭证进 JS bundle;**计费最危险**(try-catch 吞错→失败支付当成功→真实亏损);修法=关键路径 VCR cassettes 真实报文回放测试;非开发者"对安全除登录页外零概念"→防护须内置于工具。

## 交叉综合(给 Skill 设计)

- 失败模式命名已收敛: silent wrong assumptions / over-complication / orthogonal damage(§4)+ IDOR 与计费吞错(§11)+ 认知复杂度与重复(§10)+ 五大 CWE(§7)。
- 量化杠杆: 好提示词 -7pp(§7)、12 条规则 41%→3% 且超载反跌(§4)、Claude 审 Codex +18pp 但反向 -9pp(§8)、结构化 review 45%→<10%(§7)。
- 可复用结构: spec-kit 的"checklist=需求的单元测试+评审者持勾选权"、complexity 辩护表、[NEEDS CLARIFICATION]≤3;ap-vibe 的"分数必须带 reason+evidence、null 合法、未变化不重写、do_not_repeat"。
