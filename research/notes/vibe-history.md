# 主题一提炼笔记：Vibe Coding 的起源、定义、演化与批评

> 调研日期：2026-10-11。归档正文见 `research/raw/articles/vibe-history-*.md`（共 21 个文件，覆盖约 24 个来源）。

## 0. 时间线关键节点

- **2023-01-25** Karpathy: "The hottest new programming language is English"（Software 2.0 心态的自然语言版）→ vibe coding 概念前身（Karpathy 推文，经 Guardian Naughton 专栏转引）
- **2025-02-02** Karpathy 原始推文造词 "vibe coding"："fully give in to the vibes... forget that the code even exists"，并自我限定 "not too bad for throwaway weekend projects"（https://x.com/karpathy/status/1886192184808149383）
- **2025-02~03** 出圈：NYT Kevin Roose "LunchBox Buddy" 实验（2025-02-27）；Ars Technica 首篇深度报道（2025-03-05）；TechCrunch 报道 YC W25 批次 25% 初创公司代码库 95% AI 生成（2025-03-06）；Merriam-Webster 收录为 "slang & trending"（2025-03-08）
- **2025-03-19** Simon Willison《Not all AI-assisted programming is vibe coding》划定定义边界（https://simonwillison.net/2025/Mar/19/vibe-coding/）
- **2025-05~07** 批评数据涌现：GitClear 技术债报告（2025-02 发布，2025 持续发酵）；Lovable 曝出 170/1645 应用泄露用户数据（Semafor/Futurism，2025-05）；METR RCT：AI 使资深开发者慢 19%（2025-07-10）；SaaStr/Replit agent 删库事件（2025-07）
- **2025-08-18** Karpathy 主动切割："I'm not a big fan of the term 'vibe coding'"，提出结合工程纪律 → vibe engineering 方向
- **2025-09~11** 范式升级：GitHub 发布 Spec Kit（spec-driven development 工具，2025-09）；Fast Company "vibe coding hangover"（2025-09-09）；Collins 词典年度词（2025-11-06）；CodeRabbit 对比报告（2025-12-17）
- **2026** 主流化与反思：Torvalds 自认 vibe coding 玩具项目（2026-01）；论文《Vibe Coding Kills Open Source》（arXiv:2601.15494，2026-01-21）；rsync "Please Do Not Vibe Fuck Up This Software" 事件（2026-05/06）；WSJ "vibe slop" 警告（2026-05-22，引 Armin Ronacher/Mario Zechner）；GitHub "Eternal September of open source" 官方回应（2026-02-12）；Willison 自述 vibe coding 与 agentic engineering 融合（2026-05-06）

## 1. Karpathy 原始推文与语境

来源：https://x.com/karpathy/status/1886192184808149383（全文经 Wikipedia Cite tweet 脚注与 Willison 博客双重转引，存 `vibe-history-karpathy-tweets.md`）

- 操作特征四件套："Accept All" always / 不读 diff / 报错直接粘贴无注释 / "the code grows beyond my usual comprehension"
- 工具链：Cursor Composer + Claude Sonnet + SuperWhisper 语音输入（"barely even touch the keyboard"）
- 自我限定被后续传播大量丢失："It's not too bad for **throwaway weekend projects**, but still quite amusing"
- 名句收尾："it's not really coding - I just see stuff, say stuff, run stuff, and copy paste stuff, and it mostly works"
- 造词者身份（OpenAI 联创/前 Tesla AI 总监）是术语半天出圈的关键（Wikipedia 首段即强调）
- 前史：2023-01 "The hottest new programming language is English"——Naughton（Guardian 2025-03-16）将其定位为 vibe coding 的概念前身；Karpathy 的 Software 2.0 论（2017）→ English-as-language（2023）→ vibe coding（2025）一脉相承
- 2025-08-18 后续推文：明确不喜欢术语被泛化，"a valid way to hack on side projects and toys, but I personally think we should be aiming for more"，主张 LLM 一次成型 + 传统工程纪律结合（vibe engineering）

## 2. 定义辨析（边界之争）

来源：Willison 2025-03-19（主）；Wikipedia；Merriam-Webster；IBM；Ars Technica；Sarkar & Drosos 论文

- **Willison 的操作性定义**："Vibe coding = building software with an LLM **without reviewing the code it writes**"。金句："I won't commit any code to my repository if I couldn't explain exactly what it does to somebody else"（不审查、不能解释 → 不是工程，是 vibe coding）
- **被稀释的担忧**：媒体把一切 AI 辅助编程都叫 vibe coding，Willison 认为这既稀释术语又给"负责任的 AI 辅助编程"造成虚假印象；Andrew Ng（2025-06，Business Insider）也反对该词误导大众以为工程师"跟着感觉走"
- **Karpathy 原意 vs 大众用法**：原意=娱乐性周末项目的心态放权；大众用法=一切"说人话生成软件"；两者在"是否读代码"上是分水岭（Ars Technica 引 Willison："If an LLM wrote every line of your code, but you've reviewed, tested, and understood it all, that's not vibe coding... that's using an LLM as a typing assistant"）
- **词典定义**（Merriam-Webster 2025-03-08）："coder does not need to understand how or why the code works, and often will have to accept that a certain number of bugs and glitches will be present"（存 Wikipedia 脚注；Collins 2025 年度词）
- **学术定义**（Sarkar & Drosos, arXiv:2506.23253，Microsoft Research 首个实证研究）：vibe coding = 以对话为介的编程，"iterative goal satisfaction cycles"（prompt → 快速评估 → 手工编辑），专业能力被**再分配**而非消除——转向上下文管理、快速代码评估、AI/手工切换决策；理论化为 "material disengagement"
- **企业定义**（IBM Think，2025-04 发布 2026-07 更新）：vibe coding 是"loosely defined term"，企业版五步法（选平台→描述意图与上下文→初稿→迭代→验证安全部署）实质上把 vibe coding 工程化收编，并预告 "autonomous engineering" 下一阶段
- **Willison 的再融合（2026-05-06）**：随着 agent 可靠性提升，他承认自己生产工作也不再逐行审查——vibe coding 与 agentic engineering 边界塌缩；新心理模型：把 agent 当"其他团队的半黑盒服务"；新评估标准：真实使用时长 > 代码外观质量；警告 normalization of deviance（偏差正常化）

## 3. 演化：从梗到工作方式到范式

来源：TechCrunch YC；ZDNet；Willison vibe engineering；GitHub Spec Kit；IBM；ghuntley /specs/

- **2025-03-06 TechCrunch/YC**（https://techcrunch.com/2025/03/06/a-quarter-of-startups-in-ycs-current-cohort-have-codebases-that-are-almost-entirely-ai-generated/）：YC 管理合伙人 Jared Friedman 透露 W25 批次 25% 公司 95% 代码 AI 生成（不计 import 等样板）；关键：创始人全部"highly technical"；视频标题即《Vibe Coding Is the Future》；Garry Tan："This is the dominant way to code. And if you are not doing it, you might just be left behind"；GP Diana Hu 反向提醒："In order to do good 'vibe coding,' you still need to have taste and knowledge to judge good versus bad"
- **Vibe engineering（2025-08~10）**：Karpathy 提法 → Willison《Vibe engineering》(2025-10-07) 系统化：LLM "reward 顶级工程实践"（自动化测试/test-first、先计划后执行、文档、git 纪律——LLM "fiercely competent at Git"、CI/lint/preview、code review 文化、"非常奇怪的管理形式"、手工 QA）；结论"AI 放大既有专业能力"；2026 注：更倾向叫 Agentic Engineering
- **Spec-driven development（2025-09 起）**：GitHub 官方 Spec Kit（https://github.com/github/spec-kit）："Build with a spec"；流程 = 项目级 constitution（代码质量/测试/可维护性原则）一次 + 每功能 specify → plan → tasks → implement → converge；口号级主张：先写规格再写码，是对"prompt 碰运气"的工程化纠偏
- **ghuntley /specs/**（Geoffrey Huntley，2025）："From Design doc to code"——design doc（spec）+ stdlib 方法 + 编译器类型健全性 = "hands-free output of N factor（数周同事工作量）in hours"；代表"spec 驱动 + 类型兜底"流派
- **Torvalds 效应（2026-01，ZDNet）**：Linus 用 Google Antigravity 给业余项目 AudioNoise 的 Python 可视化工具 vibe coding，README 自述 "basically written by vibe-coding"；但 C 核心仍手写；内核社区同时用 AI 做维护苦力；被网友戏称 vibe coding = "Very Inefficient but Entertaining"；标志性意义：最高profile程序员亲自示范"玩具可用、生产慎用"的边界
- **术语族谱**：vibe coding（2025-02）→ vibe engineering（2025-08）→ agentic engineering（2025 末~2026）→ vibe slop（2026，贬义回收）；派生词：The Economist "vibe valuation"（2025-06，讽刺 AI 创业估值）、slopsquatting（2025 下半年，供应链攻击）

## 4. 批评与实证数据（代码质量/安全/技术债）

### 4.1 代码质量与技术债

- **GitClear（LeadDev 报道，2025-02-19，https://leaddev.com/technical-direction/how-ai-generated-code-accelerates-technical-debt）**：211M 行代码变更（2020-2024）；2024 年 5+ 行相邻重复代码块频率 **8 倍**增长、重复率比两年前高 **10 倍**；46% 变更是新行，copy-paste 行数首超 moved 行（20 年来首次）；refactor 占比从 2021 年 25% 降到 10% 以下；churn（合并后短期重写）近翻倍；API evangelist Kin Lane："35 年职业生涯从未见过如此短时间产生这么多技术债"；Harding 警告：若继续用 commit 数/行数度量生产力，"AI 驱动的可维护性衰退将扩散"
- **CodeRabbit（2025-12-17，https://www.coderabbit.ai/blog/state-of-ai-vs-human-code-generation-report）**：470 个开源 PR 分析；AI 参与代码总体问题 **1.7×**、critical/major 更多、逻辑/正确性问题 +75%、可读性问题 3×+、异常处理缺口 ~2×、安全问题最高 **2.74×**、格式问题 2.66×、命名不一致 ~2×；背景数据：PR/作者 +20% YoY 但 incident/PR +23.5%；建议：给 AI 上下文、policy-as-code、正确性护栏、安全默认值、AI-aware PR checklist
- **Fast Company "vibe coding hangover"（2025-09-09）**：资深工程师描述与 AI 生成代码合作的 "development hell"（经 Wikipedia 转引，正文存档未获，Wayback 拦截）
- **DORA 2024 / Harness 2025**（LeadDev 文转引）：AI 使用 +25% → 交付稳定性 -7.2%；多数开发者花更多时间调试 AI 代码与修安全漏洞

### 4.2 安全漏洞

- **Veracode 2025 GenAI Code Security Report（2025-10，https://www.veracode.com/resources/analyst-reports/2025-genai-code-security-report/）**：100+ LLM 跨 Java/JS/Python/C# 测试；**45%** 测试中 AI 生成代码引入有风险安全缺陷；"Bigger Models ≠ More Secure Code"（更大更新的模型安全未改善）；唯一例外是 OpenAI 推理模型小幅提升
- **Lovable 事件（Semafor 2025-05-29 + Futurism 2025-05-31，https://futurism.com/problem-vibe-coding）**：Replit 员工 Matt Palmer 报告 1,645 个 Lovable 生成应用中 **170 个**存在 RLS 配置错误导致任何人可读用户个人数据（姓名/邮箱/财务信息）；"security scanner" 只查 RLS 策略存在性不查正确性 → false sense of security；工程师 Daniel Asaria 47 分钟攻入多个"top launched"站点拿到住址、债务金额、API keys；Willison 评语："The most obvious problem is that they're going to build stuff insecurely"
- **Tihanyi et al.（arXiv:2404.18353，EMSE）**：FormAI-v2 331K 个 LLM 生成 C 程序，ESBMC 形式化验证标注：**至少 62.07% 有漏洞**；GPT-3.5 上一代数据 51.24%
- **Vibe-coded 应用安全审计（arXiv:2606.23130）**：9,041 应用 + 200 部署，**91%** 含漏洞，归纳 8 种 AI agent 反复失效模式

### 4.3 生产力悖论

- **METR RCT（arXiv:2507.09089，2025-07-10；Ars Technica 报道存档）**：16 名资深开源开发者、246 任务随机对照：允许 AI 实际**慢 19%**；事前预测快 24%、事后仍自认快 20%（感知与现实双向背离）；经济学家预测 +39%、ML 专家预测 +38% 全错

### 4.4 供应链：包幻觉与 slopsquatting

- **Spracklen et al.（arXiv:2406.10279，USENIX Security 2025）**："package hallucination"：16 LLM 生成 576K 样本，商业模型幻觉率 ≥5.2%、开源模型 **21.7%**，共 205,474 个唯一幻觉包名；"a persistent and systemic phenomenon"；攻击者抢注幻觉包名即 slopsquatting 投毒——非程序员 vibe coder 缺乏辨别依赖真伪的能力，是重灾区

### 4.5 对开源生态的冲击

- **Koren et al.《Vibe Coding Kills Open Source》（arXiv:2601.15494，2026-01-21；The Register 报道 2026-01-26，https://www.theregister.com/2026/01/26/vibe_coding_hazardous_open_source/）**：经济学均衡模型：AI 依赖安装切断用户-维护者互动（不读文档/不报 bug）；仅靠用户参与变现的 OSS 在 vibe coding 普及下进入、分享、质量、福利齐降——尽管生产率升；现实佐证：Tailwind Labs CEO Adam Wathan 因文档流量较 2023 年初 -40% 裁员 3 人（文档是其商业产品唯一曝光渠道）；ChatGPT 发布后 Stack Overflow 提问量可测地下降；Anthropic CEO Amodei 2025-09："70, 80, 90 percent of the code written in Anthropic is written by Claude"；解法建议：LLM 推理商按库使用量计量分成（"Spotify pays artists"模式）；引用研究：OSS 开发者只捕获其创造总价值的 ~0.1%
- **GitHub 官方《Eternal September of open source》（2026-02-12，https://github.blog/open-source/maintainers/welcome-to-the-eternal-september-of-open-source-heres-what-we-plan-to-do-for-maintainers/）**：核心命题"**the cost to create has dropped but the cost to review has not**"；curl 因 AI 生成安全报告泛滥终止 bug bounty（每份验证耗时数小时）；Ghostty 转邀请制贡献；官方对策：PR 创建权限限协作者、issue 置顶评论、降噪 banner、大 PR diff 提速 67%
- **rsync 事件（2026-05/06，Register/OSNews，经 Wikipedia 转引）**：rsync 3.4.3 增量备份损坏；3.4.1 起数十 commit 由 "tridge and claude" 完成；issue 标题 "Please Do Not Vibe Fuck Up This Software" 引爆关键开源基础设施中 AI 代码之争；tridge 回应：AI 用于加测试套件与纵深防御加固

### 4.6 "Vibe slop" 与 AI slop 概念合流

- **WSJ（2026-05-22，经 Wikipedia 转引）**：Mario Zechner 与 Armin Ronacher（Pi coding harness/OpenClaw）警告 "vibe slop" 危机：企业用近期生产力换长期问题（bug、宕机、漏洞、技术债）；Zechner："infrastructure that's falling apart... We can play this game for a couple more months, or maybe even years, but eventually it will catch up to us"
- **Geoffrey Huntley "engineer away the slop"（https://ghuntley.com/slop/）**："Software authoring has been commoditised. Everyone is now a software developer, but being a software developer does not mean that they're an engineer"（工程师一词在其他行业意味着 failure 不可接受）；"Creation is now near-free. Verification/understanding is not, yet"；预言形式化验证 + 确定性测试（他加入 Antithesis）将 crossing the chasm；对比软件工程学徒制断层 → 另一场 Eternal September
- AI slop 原指 LLM 低质文本/内容泛滥；"vibe slop" 把它接到代码侧：外观精美（README/测试/commit 全齐）但内核未经验证的批量软件（Willison 2026-05：AI 半小时百 commit 仓库使"用心"不可辨识）

## 5. 各方人物立场速查

- **Karpathy**：造词者→限定者（周末项目）→修正者（vibe engineering）；一贯心态：LLM 让编程民主化但工程纪律不可丢
- **Simon Willison**：定义守门人（"不读代码才是 vibe coding"）；同时是 vibe coding 最大辩护者（人人应有自动化能力、80+ 实验）；2026 承认边界塌缩但仍守"问责"底线（agent 无职业声誉）
- **Gary Marcus**：NYT Roose 实验批评者——"recipe-from-photo 不是原创，代码早已存在，系统是在既有代码上训练的…为 regurgitation 兴奋是严重疏忽"（Guardian 2025-03-16 转引）
- **YC（Friedman/Tan/Hu）**：拥抱派，但 Hu 强调 "taste"、Tan 强调调试能力是长期生存线
- **Andrew Ng**：反术语派（误导外行以为工程=凭感觉），但亲 AI 辅助
- **Linus Torvalds**：实用派——玩具可以 vibe，核心手写；"AI 作为工具的坚定信徒"，但厌恶 hype
- **Armin Ronacher**：警觉派——开源低质贡献暴增，但强维护者项目可能因信任而强化；"massive shift，几年后才见分晓"（Register 2026-01 采访）
- **Geoffrey Huntley**：极端实践派→验证派：早期鼓吹 chat/fork 快速交付，2025-26 转向 "engineer away the slop"（形式化验证创业公司 Antithesis）

## 6. 对构建中文 Skill 的启示线索（供主 agent 参考）

1. "是否读/能否解释代码"是区分 vibe coding 与工程实践的可操作判据，可直接落进 Skill 的决策规则（原型/玩具 vs 生产/服务他人分轨）
2. 实证数据密度高（62%/45%/1.7×/19% slower/91%），适合做成"何时必须人工审查"的量化触发器与反例库
3. 演化谱系（vibe coding → vibe/Agentic engineering → spec-driven）本身就是"低质代码优化"的方法论阶梯：宪法/规格（Spec Kit constitution）、测试先行、类型健全、验证侧车（arXiv:2511.00202 Vibe Reasoning）、确定性测试（Antithesis）
4. 安全专项：secrets 暴露、RLS/权限配置、包幻觉（slopsquatting）、依赖正确性——vibe coder 高频翻车点清单
