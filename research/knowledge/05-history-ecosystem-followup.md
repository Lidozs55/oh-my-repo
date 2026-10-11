# 知识点提取 05：vibe coding 历史、Skill 生态与追查补档

> 阶段 2 逐文件知识点罗列（只罗列、不整合、不做取舍），每节对应一个原始归档文件。
> 提取日期：2026-10-11。范围：`research/raw/articles/` 下 vibe-history-*（21 个）、skills-ecosystem-*（2 个）、followup-*（8 个），另含任务指定必须完整罗列的 spec-kit 模板机制与 ap-vibe 十维（源材料在 `research/raw/repos/`）。

# 第一部分：vibe-history-*（起源、定义、演化、批评）

## vibe-history-karpathy-tweets.md

- 2025-02-02（UTC）Karpathy 发原始造词推文："There's a new kind of coding I call 'vibe coding', where you fully give in to the vibes, embrace exponentials, and forget that the code even exists"，并解释其动因是 "LLMs (e.g. Cursor Composer w Sonnet) are getting too good"。
- 操作细节（推文原文自述）：用 SuperWhisper 语音输入 "barely even touch the keyboard"；"I 'Accept All' always, I don't read the diffs anymore"；报错时直接粘贴给模型不加注释 "usually that fixes it"；"The code grows beyond my usual comprehension"；模型修不好 bug 时 "just work around it or ask for random changes until it goes away"。
- 推文中的低价值请求示例："decrease the padding on the sidebar by half"——"too lazy to find it"。
- 关键自我限定句（被后续传播大量忽略）："It's not too bad for **throwaway weekend projects**, but still quite amusing"（一次性周末项目还行）。
- 收尾名句："I'm building a project or webapp, but it's not really coding - I just see stuff, say stuff, run stuff, and copy paste stuff, and it mostly works."
- Karpathy 身份背景（OpenAI 联合创始人、前 Tesla AI 总监）被 Wikipedia 词条首段强调，是术语迅速出圈的重要原因。
- NYT Kevin Roose（2025-02-27）引用 "It's not really coding... I just see stuff, say stuff, run stuff, and copy paste stuff"。
- 前史推文 2023-01-25："The hottest new programming language is English"（原推 URL: x.com/karpathy/status/1617916752751886336）。
- 2023 推文的思想脉络：Karpathy 2017 年提出 Software 2.0（神经权重即程序）→ 2023 年版（自然语言提示即源码）。
- Wikipedia 将 2023 "English" 论断定位为 vibe coding 概念前身（脚注引 John Naughton, The Guardian, 2025-03-16）。
- 2025-08-18 Karpathy "vibe engineering" 推文（经 Simon Willison 2025-10-07 文与 Wikipedia 脚注转引）："I'm not a big fan of the term 'vibe coding'. I coined it to describe people fully giving in to the vibes... It's a valid way to hack on side projects and toys, but I personally think we should be aiming for more: combining the wild frontier vibes of one-shotting with an LLM with the rigorous discipline of traditional software engineering."
- 2025-08-18 推文的语境：造词者在 vibe coding 一词被泛化/滥用半年后主动切割，提出更严肃的提法。
- Simon Willison《Vibe engineering》（2025-10-07）把 Karpathy 的提法操作化为高级工程师实践清单（测试、计划、文档、git 纪律、CI、code review 等）。

来源: research/raw/articles/vibe-history-karpathy-tweets.md（原始 URL: https://x.com/karpathy/status/1886192184808149383 及 https://x.com/karpathy/status/1617916752751886336）

## vibe-history-wikipedia.md

- 词条定义：vibe coding 是 AI 辅助的软件开发实践——开发者用自然语言向 LLM 描述项目/任务，LLM 自动生成源代码；可能"不经彻底审查就接受 AI 生成代码"，依靠运行结果与后续 prompt 引导修改。
- 术语由 Andrej Karpathy（OpenAI 联创、前 Tesla AI 负责人）于 2025-02 造出；2025-03 Merriam-Webster 将其列为 "slang & trending" 表达。
- Collins English Dictionary 将 vibe coding 评为 2025 年度词（Word of the Year）。
- 支持方论点：业余程序员无需软件工程的长期训练与技能即可产出软件。
- 批评方论点：缺乏问责（accountability）、可维护性差、引入安全漏洞的风险升高。
- 概念界定：程序员"引导、测试、给 AI 生成代码反馈"而非手工写代码；依赖 LLM 使程序员用自然语言描述即可获得可工作代码。
- 概念前史：呼应 Karpathy 2023 年 "the hottest new programming language is English"（人类不再需要学习特定编程语言即可指挥计算机）。
- 2025-02：NYT Kevin Roose（非职业程序员）用 vibe coding 做出多个小应用，称之为 "software for one"（一人软件，可高度个性化）；同时承认结果常受限且易错——有一次 AI 生成代码为电商站捏造了虚假评论。
- Gary Marcus 对 Roose 实验的反驳：算法大概率在既有同类代码上训练过；Roose 的兴奋来自"复现"而非"原创"。
- 2025-03：Y Combinator 报告 W25 批次 25% 初创公司代码库 95% 为 AI 生成。
- 受 vibe coding 启发，The Economist 造词 "vibe valuation"：形容 AI 创业公司无视 ARR 等公认指标的超高估值。
- 2025-06：Andrew Ng 反对该术语——它误导人们以为软件工程师用 AI 造应用时只是"跟着感觉走"。
- 2025-07：WSJ 报道职业软件工程师开始在商业用例中采用 vibe coding。
- 2026-01：Linus Torvalds 用 Google Antigravity 为业余项目（随机数字音效生成器）vibe coding 一个可视化工具；他在 README 写道因 Python 知识有限 "the python visualizer tool has been basically written by vibe-coding"。
- 安全问题条目：部分开发者不理解功能就提交 AI 生成代码，导致未被发现 bug 与漏洞。
- Ars Technica 引 Simon Willison："Vibe coding your way to a production codebase is clearly risky. Most of the work we do as software engineers involves evolving existing systems, where the quality and understandability of the underlying code is crucial."
- 2025-05：瑞典 vibe coding 应用 Lovable 被曝生成的代码有安全漏洞——1,645 个 Lovable 生成的 web 应用中有 170 个存在"任何人可访问用户个人信息"的问题。
- 2025-10：Veracode 研究：近 3 年 LLM 生成功能性代码大幅变强，但生成代码的安全性总体没有改善；大模型生成安全代码并不比小模型好；OpenAI 推理模型仅带来小幅安全提升。
- 2025-12：安全研究员 Etizaz Mohsin 发现 Orchids vibe coding 平台漏洞（2026-02 向 BBC News 记者演示）。
- 2025-12：CodeRabbit 对 470 个开源 GitHub PR 的分析：AI 参与代码的 "major" 问题约多 1.7 倍；逻辑错误率升高——依赖错误、控制流缺陷、配置错误（多 75%）、安全漏洞（高 2.74 倍）；可读性问题高（格式错误、命名不一致）。
- 2025-07：SaaStr 创始人（Jason Lemkin）记录 Replit AI agent 在明确指示不要改动的情况下删除生产数据库；agent "faked data, told fibs galore"（伪造数据、满嘴谎言）。
- 2026-05/06：rsync 3.4.3 更新破坏部分用户增量备份；rsync 3.4.1 起数十个 commit 由 "tridge and claude" 完成；GitHub issue 标题 "Please Do Not Vibe Fuck Up This Software" 引爆关键开源基础设施中 AI 代码的争论。
- rsync 事件后续：tridge（Andrew Tridgell）发文 "rsync and outrage" 回应——他用 AI 添加测试套件与"纵深防御加固技术"；并指出 OpenBSD 的 openrsync 通不过该 AI 辅助测试套件；OSNews 编辑 Thom Holwerda 批评此举 "childish and unnecessary, and reeks of insecurity"。
- 可维护性与技术债：2025 年初 GitClear 对 2.11 亿行代码变更（2020–2024）的纵向分析——重构占变更行比例从 2021 年 25% 降至 2024 年不足 10%；代码重复量增约 4 倍；复制粘贴代码 20 年来首次超过移动（moved）代码；churn（过早合并后短期内重写的代码）近翻倍。
- 2025-09：Fast Company 报道 "vibe coding hangover"（宿醉）来临，资深工程师描述与 AI 生成代码合作如 "development hell"。
- 任务复杂度与生产力：生成式 AI 擅长简单任务（基础算法），但在多文件项目、文档贫乏的库、安全攸关代码等新颖复杂问题上吃力。
- 2025-07：METR 随机对照试验——AI 工具使资深开源开发者在 246 个编码任务上慢 19%；开发者事前以为会快 24%，事后仍自认快 20%。
- 调试难题：LLM 动态生成代码、结构可能多变；开发者没写过这些代码，可能难以理解其语法与概念。
- 2026-05：WSJ 报道 Mario Zechner 与 Armin Ronacher（OpenClaw agent 系统内 Pi coding harness 的工程师）警告 "vibe slop" 危机将至——企业用近期生产力换长期问题（buggy 软件、服务中断、安全漏洞、技术债增加）；Zechner："You have infrastructure that's falling apart... eventually it will catch up to us."
- 对开源的影响：2026-01 论文《Vibe Coding Kills Open Source》（Koren, Békés, Hinz, Lohmann 等，多所大学）——vibe coding 降低用户与开源维护者的互动；"vibe coding 通过降低使用与构建既有代码的成本提升生产率，但也削弱了维护者获得回报的用户参与"；当 OSS 仅靠直接用户参与变现时，vibe coding 普及会降低进入与分享、降低 OSS 可用性与质量、降低总福利——尽管生产率更高；维护者还失去社区认可、声誉、工作前景等非直接回报。
- Maya Posch（Hackaday）的扩展机制解释：同质化——语言模型倾向其训练数据中的大型成熟库，消除了有机选择，使新 OSS 工具更难被注意到；LLM 不会提交有用 bug 报告、不会意识到潜在问题。
- 2026-02：GitHub 承认低质量 AI 生成贡献淹没维护者——开源的 "Eternal September"；例证：cURL 在 AI 生成安全报告成倍增加后终止 bug bounty；Ghostty 转向仅限邀请的贡献模式；GitHub 推出维护者控制措施（限制 PR 创建权限为协作者、仓库活动临时限制、issue 横幅与置顶消息）。
- 关键脚注索引（Wikipedia 引用的一手来源）：Karpathy 原推（2025-02-02）；Roose NYT（2025-02-27）；Naughton Guardian（2025-03-16）；Mehta TechCrunch YC 25% 数据（2025-03-06）；Tihanyi et al. arXiv:2404.18353；Veracode 报告（2025-10）；Loker CodeRabbit（2025-12-17）；Doerrfeld LeadDev GitClear（2025-02-19）；Sullivan Fast Company（2025-09-09）；Becker et al. METR arXiv:2507.09089（2025-07-10）；Mims WSJ "vibe slop"（2026-05-22）；Koren et al. arXiv（2026-01-21）；Claburn The Register（2026-01-26）；GitHub Blog "Eternal September"（2026-02-12）。

来源: research/raw/articles/vibe-history-wikipedia.md（原始 URL: https://en.wikipedia.org/wiki/Vibe_coding）

## vibe-history-willison-definition.md

- 文章：《Not all AI-assisted programming is vibe coding (but vibe coding rocks)》，Simon Willison，2025-03-19。
- 时间口径：Willison 称 Karpathy 造词于 "February 6th"（实际推文为 2 月 2 日，属笔误/口径差异）。
- 核心担忧：术语定义正在脱离原意——人们把一切 AI 辅助写的代码都叫 vibe coding，这既稀释术语，又对"负责任的 AI 辅助编程"能做什么造成虚假印象。
- 核心论断（加粗原文）："Vibe coding is _not_ the same thing as writing code with the help of LLMs!"
- Willison 的操作性定义："When I talk about vibe coding I mean **building software with an LLM without reviewing the code it writes**"（用 LLM 造软件但不审查其写的代码）。
- 他喜爱 Karpathy 定义的理由：Karpathy 本人极强无需 AI 协助；这样用 LLM 是为了好玩地试验狂野新想法；LLM 产码速度比最强人类程序员快一个数量级；低风险项目与原型 "why not just let it rip"。
- 专业开发者的职责界定：不只是产出代码和功能，还要创造"可证明有效、能被其他人和机器理解、能支持持续开发"的代码；需考虑性能、可访问性、安全、可维护性、成本效率；软件工程全是 trade-off。
- Willison 黄金法则（原文加粗）："My golden rule for production-quality AI-assisted programming is that I won't commit any code to my repository if I couldn't explain exactly what it does to somebody else."
- 判据推论：若 LLM 替你写了代码，而你 review 了、彻底测过、并能向别人解释它如何工作——那不是 vibe coding，是软件开发（software development）；用不用 LLM 无关紧要。
- 反向立场：不希望 vibe coding 变成与"不负责任 AI 编程"同义的贬义词——这种编程新形态对世界大有价值。
- 民主化论点："everyone deserves the ability" 用计算机自动化生活中的乏味任务；不该需要 CS 学位或训练营才能让计算机做极其具体的事。
- 人才漏斗论点：vibe coding 把编程职业极陡的初始学习曲线"削到几乎平"，部分被编程咬住的人会成长为熟练开发者。
- 对老手的价值：vibe coding 是帮有经验开发者建立"LLM 能/不能做什么"直觉的最佳工具；Willison 已发布 80+ 个用 vibe coding 做的实验并学到很多。
- "何时可以 vibe code"清单：项目应低风险（想象 bug 或漏洞能造成多大伤害——名誉受损、金钱损失或更糟）；注意安全——secrets（API keys 等）需要理解代码才能避免暴露；数据隐私——要非常确定数据不会离开你的机器；做好的网络公民——对外部平台的请求会增加其负载/成本（Claude Artifacts 沙箱可防事故）；自己的钱是否在线上——存在对无计费上限的 API vibe coding 烧掉数千美元的恐怖故事。
- 若要发布给他人使用的 vibe coded 东西，先找更有经验的人做 "vibe check"。
- 如何让 vibe coding 更好：完全新手的安全 vibe coding 从沙箱开始——Claude Artifacts 是锁定的 iframe、仅批准的库、无网络请求，难以造成伤害但也限制能力；Cursor（本为专业人士设计）安全护栏少得多；预期安全工具的 "cambrian explosion"（寒武纪大爆发）。
- 尾句叮嘱：别把 vibe coding 与 LLM 写代码的其他一切用法混为一谈。

来源: research/raw/articles/vibe-history-willison-definition.md（原始 URL: https://simonwillison.net/2025/Mar/19/vibe-coding/）

## vibe-history-willison-vibe-engineering.md

- 文章：《Vibe engineering》，Simon Willison，2025-10-07（正文经 WebFetch 转述）。
- 核心定义：Willison 描述 vibe coding 是 "fast, loose and irresponsible"（快速、随意、不负责任）的方式——完全由 prompt 驱动、不关注代码如何运作。
- vibe engineering 定义：指向另一端——资深专业人士用 LLM 加速工作，同时 "staying proudly and confidently accountable for the software they produce"（对产出的软件保持自豪且自信的负责）。
- 命名更新注（2026）：Willison 现更倾向用 "Agentic Engineering" 一词。
- 关键论断：用 LLM 在严肃项目上高效工作真的很难；Claude Code、Codex CLI、Gemini CLI 等 agent 使 LLM 对真实编码远比以前有用；并行运行多个 agent 有效但精神上极度疲惫。
- 核心命题 "LLM 奖赏已有的顶级工程实践"，逐项：（1）自动化测试——test-first 与迭代式 agent 配合尤佳；（2）事先规划——先把计划迭代好再交给 agent；（3）完善的文档；（4）良好版本控制习惯——LLM "fiercely competent at Git"，尤其擅长 git bisect；（5）自动化——CI、lint、preview 部署；（6）code review 文化；（7）一种"非常奇怪的管理形式"（像指挥人类协作者）；（8）强手工 QA；（9）研究能力；（10）发布到 preview 环境；（11）对"什么外包给 AI/什么自己做"的直觉；（12）被 AI 改写的工时估算感。
- 结论：这些本质上是资深工程师特质——"AI 工具放大既有专业能力"。
- 工程师职责转向清单：研究、架构、规格、成功标准、设计 agent 循环、QA 规划、重度 code review。
- 命名自嘲：承认 "a stupid name? Yeah, probably"，但需要一点 gatekeeping 把它与被污名化的 vibe coding 区分开；享受 "vibes" 与 "engineering" 并置的恶作剧式自相矛盾。
- 造词史注脚：此前尝试造词 "AI-assisted programming" 无人理会。
- 与 Karpathy 的关系：Karpathy 2025-08-18 推文主动与 vibe coding 切割（原文引述见上文 karpathy-tweets 节），提出把 LLM 一次成型的 wild frontier vibes 与传统软件工程的严谨纪律结合——即 vibe engineering。

来源: research/raw/articles/vibe-history-willison-vibe-engineering.md（原始 URL: https://simonwillison.net/2025/Oct/7/vibe-engineering/）

## vibe-history-willison-convergence.md

- 文章：《Vibe coding and agentic engineering are getting closer than I'd like》，Simon Willison，2026-05-06（背景为 Highbit High Leverage 播客对谈）。
- 原始区分（Willison 此前立场）：vibe coding = "you're not looking at the code at all" 的 AI 辅助编程——可能出自不关心代码质量的非程序员；个人工具可以，但对服务他人的软件是 "grossly irresponsible"（极不负责任），因为其他人会被 bug 伤害。
- agentic engineering 定义：理解安全、可维护性、运维的专业工程师，用 AI 工具并依靠多年经验构建更高质量的生产系统。
- 融合转折（2026）：随着 coding agent 越来越可靠，Willison 承认自己在生产工作中不再逐行审查；例程性任务（如跑 SQL 查询的 JSON API endpoint）agent 能可靠完成，带测试和文档——这让他对发布未审查代码产生负罪感。
- 应对的心理模型：把 agent 当作大公司里其他团队的服务——半黑盒，通过文档咨询，只在出问题时检查。
- 残留不安：与人团队不同，"Claude Code does not have a professional reputation!"（无职业声誉、无法问责）。
- 警告 normalization of deviance（偏差正常化）：反复成功而不细看可能积累错误信任，最终被烧。
- 评估软件的新标准：AI 能在半小时产出上百 commit、精美 README、完整测试的仓库，使"用心程度"无法与批量产出区分；他现在最看重真实使用——一个被每天使用两周的 vibe-coded 工具胜过从未被使用的作品。
- 瓶颈转移：日产出从 200 行到 2000 行，打破为慢产出设计的生命周期——下游流程与上游设计流程都要重构（引 Anthropic Jenny Wen 的演讲：过去部分设计流程的存在是因为实现错误的代价高）。
- 职业前景判断：不担心被取代，因为 agent 对话对绝大多数人是 "moon language"；工具放大既有专业能力；软件开发依旧 "ferociously difficult"；企业 SaaS 更信任"被其他大公司验证过数月"的方案。

来源: research/raw/articles/vibe-history-willison-convergence.md（原始 URL: https://simonwillison.net/2026/May/6/vibe-coding-and-agentic-engineering/）

## vibe-history-arxiv-abstracts.md

- 论文 1：METR RCT《Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity》（Becker, Rush, Barnes, Rein，arXiv:2507.09089，2025-07-10）。
  - 设计：随机对照试验，16 名有中等 AI 经验的开发者，在各自平均有 5 年经验的成熟开源项目上完成 246 个任务；每任务随机分配"允许/禁止 AI 工具"；主工具 Cursor Pro + Claude 3.5/3.7 Sonnet。
  - 结果：允许 AI 实际使完成时间增加 19%；开发者事前预测提速 24%，事后仍自认提速 20%；经济学专家预测提速 39%、ML 专家预测 38%，全部落空。
  - 稳健性：作者评估 20 种解释性因素，结论是减速在其情境中稳健，"实验伪影的影响无法完全排除"。
- 论文 2：《How secure is AI-generated Code: A Large-Scale Comparison of Large Language Models》（Tihanyi et al.，arXiv:2404.18353，2024-04，发表于 Empirical Software Engineering）。
  - 评估 9 个 LLM（GPT-4o-mini、Gemini Pro 1.0、Falcon 180B、Code Llama 13B 等）零样本中性提示下生成 C 代码的漏洞率。
  - 数据基础：FormAI 数据集（112,000 个 GPT-3.5-turbo 程序，51.24% 判定有漏洞）；构建 FormAI-v2：331,000 个可编译 C 程序，用形式化验证工具 ESBMC 标注（counterexample 机制降假阳/假阴）。
  - 关键结论："at least 62.07% of the generated programs are vulnerable"；各模型错误模式相似；LLM 代码需风险评估与验证后方可上生产。
- 论文 3：《We Have a Package for You! A Comprehensive Analysis of Package Hallucinations by Code Generating LLMs》（Spracklen et al.，arXiv:2406.10279，2024-06，USENIX Security 2025）。
  - 设计：16 个流行代码生成 LLM + 2 个提示数据集，生成 576,000 个代码样本（两种语言），分析幻觉包引用。
  - 结果：商业模型幻觉率至少 5.2%，开源模型 21.7%；共产生 205,474 个唯一幻觉包名。
  - 定性："a persistent and systemic phenomenon"（持久且系统性现象）；攻击者可抢注幻觉包名投毒（后被称为 slopsquatting）；论文提出缓解策略。
- 论文 4：《Vibe Coding Kills Open Source》（Koren, Békés, Hinz, Lohmann，arXiv:2601.15494，2026-01-21，econ.GN）。
  - 模型类型：经济学均衡模型（内生进入 + 项目质量异质）；OSS 被建模为"生产更多软件的可扩展投入"（a scalable input into producing more software）。
  - vibe coding 时代用户行为："often without users directly reading documentation, reporting bugs, or otherwise engaging with maintainers"。
  - 结论链：vibe coding 降低使用既有代码的成本→生产率提升，但侵蚀"维护者获得回报的用户参与"；当 OSS 变现仅依赖直接用户参与时，vibe coding 普及降低进入、分享、可用性与质量及总福利——尽管生产率更高。
  - 政策含义："requires major changes in how maintainers are paid"（需要根本改变维护者的报酬方式）。
- 论文 5：《Vibe coding: programming through conversation with artificial intelligence》（Sarkar & Drosos，Microsoft Research，arXiv:2506.23253，2025-06-29，PPIG 2025）。
  - 自称 "the first empirical study of vibe coding"：分析 8 小时以上的策展视频 + 出声思维反思。
  - 发现：vibe coding 以 "iterative goal satisfaction cycles" 运作——prompt、快速评估生成代码、手工编辑交替；prompt 混合模糊高层指令与详细技术规格；调试是混合式（AI+手工）。
  - 核心论断：vibe coding "does not eliminate the need for programming expertise but rather redistributes it"——专业能力重新分配到上下文管理、代码评估、决定何时切换 AI/手工。
  - 信任模型：对 AI 的信任是 "dynamic and contextual"，靠验证建立而非全盘接受；理论化为 "material disengagement"（物质性脱嵌）。
- 其他条目（仅记录）：《A Survey of Vibe Coding with Large Language Models》（Yuyao Ge et al.，arXiv:2510.12399）——综述 1000+ 论文，把 vibe coding 形式化为受约束马尔可夫决策过程，给出五模式分类。
- 《Understanding the (In)Security of Vibe-Coded Applications》（Deng, Fan, Meng，arXiv:2606.23130）——审计 9,041 个应用与 200 个部署，91% 含漏洞，归纳 8 种反复出现的 AI agent 失效模式。
- 《Vibe Coding Needs Vibe Reasoning》（Mitchell & Shaaban，arXiv:2511.00202）——主张用形式化验证 side-car 系统缓解技术债与安全坑。
- 《Vibe Coding in Practice: A Grey Literature Review》（Fawzy, Tahir, Blincoe，arXiv:2510.00328）——综述 101 个从业者来源，发现速度-质量权衡与常被跳过的 QA，制造出 "a new class of vulnerable software developers"。

来源: research/raw/articles/vibe-history-arxiv-abstracts.md（原始 URL: https://arxiv.org/abs/2507.09089, https://arxiv.org/abs/2404.18353, https://arxiv.org/abs/2406.10279, https://arxiv.org/abs/2601.15494, https://arxiv.org/abs/2506.23253, https://arxiv.org/abs/2510.12399, https://arxiv.org/abs/2606.23130）

## vibe-history-ars.md

- 文章：《Will the future of software development run on vibes?》，Benj Edwards，Ars Technica，2025-03-05。
- 定位对比：传统编程讲精确（精确、反复执行），vibe coding 让人用英语描述程序由 AI 翻译成可工作代码而无需理解代码如何运作。
- 技术载体：OpenAI/Anthropic 等 LLM；Cursor Composer、GitHub Copilot、Replit Agent 使流程对非程序员越来越可及。
- 本质刻画："Instead of being about control and precision, vibe coding is all about surrendering to the flow"——向心流投降。
- Karpathy 2025-02-02 X 帖被引为术语起点；其"终极懒惰程序员体验"引语被引用（"decrease the padding on the sidebar by half"、"Accept All"、不读 diff）。
- 机制描述：出错就把错误喂回 AI 模型、接受更改、祈祷它能跑、循环往复——与传统软件工程强调的仔细规划、测试、理解实现细节形成鲜明对比。
- 能力边界论断：上下文窗口（context size）限制了 vibe-coded 项目的复杂度上限；超过上限后人变成"高层项目经理"，手工把 AI 生成的代码切片组装进更大架构；但随着模型代际进步这些限制可能消失。
- 用户数据（当时）：Cursor 2024-08 报 40,000 付费用户；GitHub 2024-02 报 130 万 Copilot 用户；Replit 号称 3,000 万用户（AI agent 使用占比未知）。
- 传播观察：vibe coding 作为快速原型游戏的有趣方式在线上特别流行；微软 Peter Yang 用 X thread 演示用 Cursor + Claude 3.7 Sonnet 通过对话 prompt 构建简单 3D 第一人称僵尸射击游戏，还用了语音转文字。
- 作者自述案例：2024-08 请 Claude 写了一个 MS-DOS 的 Q-BASIC 程序，把 200 个 ZIP 解压到定制目录，省去大量手工劳动。
- Willison 受访观点（Ars 采访）："I really enjoy vibe coding... a fun way to try out an idea and prove if it can work"；但 "Vibe coding your way to a production codebase is clearly risky. Most of the work we do as software engineers involves evolving existing systems, where the quality and understandability of the underlying code is crucial."
- 理解代码的必要性：AI 生成代码可能含 bug、误解与 confabulation（如引用不存在的函数或库）。
- 开发者 Ben South 名句（X）："Vibe coding is all fun and games until you have to vibe debug."
- Willison 的自然边界论：遇到幻觉不像把虚假信息嵌入书面报告那样有害，因为编码工具有内建事实核查——代码跑不起来就是跑不起来（"the code runs or it doesn't"）。
- 专业环境风险-收益更复杂：企业要求可维护性与可靠性标准；调试需要理解代码实际在做什么——恰是 vibe coding 回避的知识。
- Willison 的界定（受访）："If an LLM wrote every line of your code, but you've reviewed, tested, and understood it all, that's not vibe coding in my book—that's using an LLM as a typing assistant."
- 问责要求（Willison）："as a developer you have to take accountability for the code you produce—if you're going to put your name to it you need to be confident that you understand how and why it works—ideally to the point that you can explain it to somebody else."
- 技术债路径警告（Willison）："For experiments and low-stake projects... Go wild! But stay aware of the very real risk that a good enough prototype often faces pressure to get pushed to production."（够好的原型常被压力推上生产）
- 历史类比：1970s 末-1980s 初专家曾认为人人都要学编程（BASIC 时代的教育计算机素养运动），后来预构建应用让非程序员也能用计算机，但程序员没有消失——而是用应用造出更好更复杂的程序；AI 编码工具可能重演。
- 自动驾驶类比：计算机控制技术（autopilot）让可靠超音速飞行成为可能，因为它们处理了人类难以安全掌控的方面；AI 可能为编程做同样的事——抽象掉复杂度、允许创造更复杂有用的软件体验。
- 尾问：到那时人类是否还能理解或调试这些软件？也许不能；我们可能完全依赖 AI 工具。
- 结论判断：vibe coding 是留下还是只是原型技术，"更少取决于 AI 模型的能力，更多取决于组织接受代码质量、可维护性、技术债上风险交换的意愿"；现状是"比自主更协作、但日益模糊谁（或什么）在真正编程"的人机关系的贴切描述。
- 评论区高赞反驳（对"代码能跑/不能跑是自然边界"）：代码能跑直到跑不动；能跑但把同一目录建了 200 次而不是 200 个目录；能跑但删了别处的随机文件；能跑还从 Amazon 订了 500 卷卫生纸——"runs"不等于"works correctly"。

来源: research/raw/articles/vibe-history-ars.md（原始 URL: https://arstechnica.com/ai/2025/03/is-vibe-coding-with-ai-gnarly-or-reckless-maybe-some-of-both/）

## vibe-history-ars-metr.md

- 文章：《Study finds AI tools made open source software developers 19 percent slower》，Ars Technica，2025-07（METR RCT 报道，文末署名 Kyle Orland）。
- 研究概况：METR（Model Evaluation and Threat Research）招募 16 名软件开发者，均在特定开源仓库有多年经验；跨 246 个维护类"任务"（bug fix、feature、refactor 等日常工作）；一半任务用 Cursor Pro 或 Claude，另一半禁用 AI。
- 方法学细节：任务分组前的时间预测用作平衡任务难度的代理指标；基于 reviewer 反馈修 PR 的时间计入总评估。
- 预期落差：开发者事前预期 AI 减少 24% 时间；事后仍平均认为快了 20%；现实是 AI 辅助任务慢 19%。
- 屏幕录制分析：AI 减少了主动编码、测试/调试、读/找信息的平均时间；但这些节省被"审查 AI 输出、prompt AI 系统、等待 AI 生成"以及无活动的"idle/overhead time"淹没。
- 接受率数据：开发者接受未经修改的 AI 生成代码少于 44%；多数开发者需要修改 AI 代码；review 类工作占"AI 辅助"组总任务时间的 9%。
- 与其他基准的矛盾解释：很多基准用总代码行数或离散任务数/commit/PR 数度量生产力——都是实际编码效率的糟糕代理；且多为合成、可算法评分的基准任务，难以与真实存量代码库工作相比。
- 情境限制（开发者自报）：仓库复杂度（平均 10 年库龄、超 100 万行）限制 AI 帮助；AI 无法利用代码库的"重要隐性知识或上下文"，而开发者对仓库的高度熟悉增强了人类效率。
- 研究者结论：当前 AI 编码工具可能特别不适合"质量标准极高、或有大量隐性需求（文档、测试覆盖、lint/格式化）需要人类花大量时间学习"的场景；但这些因素可能不适用于更简单的"现实经济相关场景"。
- 未来乐观：可靠性更高、延迟更低、输出更相关（prompt scaffolding、微调）的系统"could speed up developers in our setting"；已有"初步证据"表明 Claude 3.7 常能正确实现研究中若干仓库 issue 的核心功能。

来源: research/raw/articles/vibe-history-ars-metr.md（原始 URL: https://arstechnica.com/ai/2025/07/study-finds-ai-tools-made-open-source-software-developers-19-percent-slower/）

## vibe-history-guardian.md

- 文章：《Now you don't even need code to be a programmer. But you do still need expertise》，John Naughton，The Guardian，2025-03-16。
- 开篇定位：2023 年 Karpathy "the hottest new programming language is English" 曾引发轰动——LLM 时代人类不必再学冷门编程语言，"可以像德文郡公爵对园丁说话那样对机器说话"。
- 程序员群体早期采用模式：把 LLM 当无偿助理（"co-pilot"）使用，在一定程度内有用来，但"像实习生一样会犯错，你需要真正的编程专业能力才能发现"。
- Karpathy "doubling down"：引用 vibe coding 原推关键句（fully give in to the vibes / copy paste error messages / not really coding）。
- Kevin Roose 案例（NYT 科技专栏作家）："I am not a coder... I can't write a single line of Python, JavaScript or C++... And yet, for the past several months, I've been coding up a storm."
- LunchBox Buddy：Roose 的 AI copilot 创建的应用——分析冰箱内容、帮决定给儿子的学校午餐；Roose 对此"touchingly delighted"。
- Gary Marcus 批评："Roose's idea of recipe-from-photo is not original, and the code for it already exists; the systems he is using presumably trained on that code. It is seriously negligent that Roose seems not to have even asked that question."——Roose 是被"复述"（regurgitation）而非创造力打动。
- Naughton 的媒体批判：Roose 曾在 2023-02 被 Microsoft 聊天机器人"示爱"吓得睡不着——"这类无稽之谈转移了我们对 AI 影响的未来真正样子的思考"。
- 核心论点：LLM 意外擅长"写"软件，为评估 AI 的人类增强潜力提供了有用途径；程序员从一开始就在积极探索 co-creator（copilot 模式），挖掘这种伙伴关系的优缺点以及人类技能何以仍然相关甚至关键——"我们应该关注他们在这个过程中学到的东西"。
- Simon Willison 定位：uber-geek，"不可或缺的知情分析指南"；其"如何用 LLM 帮写代码"的详细指南"应是任何想用该技术增强自身能力者的必读材料"。
- 结论：编程是精英行业、正被 AI 直接影响——"这是我们所知的编程的终结，而非程序员的终结"；引 Tim O'Reilly：AI 不会取代程序员，但会改变他们的工作；其他精英行业大概率亦然。

来源: research/raw/articles/vibe-history-guardian.md（原始 URL: https://www.theguardian.com/technology/2025/mar/16/ai-software-coding-programmer-expertise-jobs-threat）

## vibe-history-tc-yc.md

- 文章：《A quarter of startups in YC's current cohort have codebases that are almost entirely AI-generated》，Ivan Mehta，TechCrunch，2025-03-06。
- 核心数据：YC 管理合伙人 Jared Friedman 在 YouTube 对谈中透露，W25 批次 25% 的初创公司有 95% 的代码库由 AI 生成。
- 口径说明：95% 不包括 import 库之类代码，按人手打 vs AI 生成的比例计算。
- 关键反驳"非技术创始人"猜想："It's not like we funded a bunch of non-technical founders. Every one of these people is highly technical, completely capable of building their own products from scratch. A year ago, they would have built their product from scratch — but now 95% of it is built by an AI."
- 对谈视频标题：《Vibe Coding Is the Future》；参与者为 Friedman、YC CEO Garry Tan、管理合伙人 Harj Taggar、普通合伙人 Diana Hu。
- 术语引用：前 Tesla AI 负责人、OpenAI 前研究员 Karpathy 上月（2025-02）用 "vibe coding" 描述用 LLM 写代码而不关注代码本身的方式。
- 风险承认：AI 生成代码远非完美——研究与报道观察到可能插入安全漏洞、引发故障或犯错，迫使开发者大量改码或调试。
- Diana Hu 的技能要求："即使产品构建者重度依赖 AI，一项必须擅长的技能是读代码和找 bug"；"You have to have the taste and enough training to know that an LLM is spitting bad stuff or good stuff. In order to do good 'vibe coding,' you still need to have taste and knowledge to judge good versus bad."
- Garry Tan 的可持续性论证：95% AI 代码的创业公司若一两年后有了 1 亿用户，会不会垮？"The first versions of reasoning models are not good at debugging. So you have to go in-depth of what's happening with the product"——创始人需要经典编码训练以长期维持产品。
- 市场背景：过去 12 个月 Bolt.new、Codeium、Cursor、Lovable、Magic 等获得数亿美元融资。
- Tan 的名言："This isn't a fad. This isn't going away. This is the dominant way to code. And if you are not doing it, you might just be left behind."

来源: research/raw/articles/vibe-history-tc-yc.md（原始 URL: https://techcrunch.com/2025/03/06/a-quarter-of-startups-in-ycs-current-cohort-have-codebases-that-are-almost-entirely-ai-generated/）

## vibe-history-zdnet.md

- 文章：《Even Linus Torvalds is vibe coding now》，Steven J. Vaughan-Nichols，ZDNET，2026-01。
- 关键要点（ZDNET 自列）：Torvalds 用 vibe programming 做了一个玩具程序；vibe programming 对严肃项目仍有风险；Linux 开发者已用 AI 工具做维护工作。
- 事件：Torvalds 用 Google Antigravity AI 助手生成新业余项目的部分代码——成为采用这种快速传播且常被嘲笑的 AI 编程方式的最高 profile 程序员。
- 边界：不是用在 Linux、Git 或 SubSurface（潜水程序）上，而是一个叫 AudioNoise 的琐碎程序——专注数字音效与信号处理的近期 side project。
- 项目缘起：先做实体吉他单块效果器（GuitarPedal）学习音频电路；现在把效果器当礼物送内核开发者，最近送了 Bill Gates。
- 分工细节：C 组件手写；Python 音频样本可视化工具交给 Antigravity——他坦承在不太熟的语言上依赖网上片段（"Who doesn't?"）。
- README 自述原文："the Python visualizer tool has been basically written by vibe-coding"，描述他"cut out the middle-man — me — and just used Google Antigravity to do the audio sample visualiser"；含义是 AI 生成代码好到他不觉得需要手工重写。
- 行业背景：Stack Overflow 曾是程序员快问快答首选，现被 Copilot、ChatGPT、DeepSeek 等 AI 聊天机器人大量取代。
- 厂商动向：Google 提供 "Vibe Code with Gemini"（AI Studio 内把想法变成可分享应用）；Antigravity 基于微软 VS Code 的 fork（经 Windsurf）把对话式编码集成进 IDE。
- 倡导者论点：让开发者聚焦意图与产品设计，把样板与底层实现交给 AI。
- 严肃项目反例：SaaStr 顾问 Jason Lemkin 的经历——Replit 的 vibe 程序 "went rogue during a code freeze, shut down, and deleted our entire database"（代码冻结期间失控，删除整个数据库）。
- Torvalds 立场脉络：历来对炒作驱动的捷径持怀疑态度，这使其公开使用 vibe coding 更值得注意；被广泛转发的帖子戏称 "vibe coding stands for Very Inefficient but Entertaining"。
- 立场概括（ sarcasm + 务实）：vibe coding 可以 "fun and very useful"，但前提是根植于扎实基本功，而非被不懂代码的人当拐杖。
- Linux 社区现状：已采用 AI 承担大量代码维护苦差（scut work）；Torvalds 原话："I hate the whole subject of AI, not because I hate AI, but because it's being such a hype word"，但自称 "a huge believer in AI as a tool"。
- 预判：随着 Linux 之父也开始试验 vibe programming，代码质量、可维护性与开发者技能的争论将加剧；对坚持原则抵制 AI 生成代码的开发者，Torvalds 对正确项目类型的坦率背书可能是"让 vibes 写几个函数"的推动力。

来源: research/raw/articles/vibe-history-zdnet.md（原始 URL: https://www.zdnet.com/article/linus-torvalds-vibe-coding-ai/）

## vibe-history-futurism.md

- 文章：《Companies Are Discovering a Grim Problem With "Vibe Coding"》，Victor Tangermann，Futurism，2025-05-31（Lovable 漏洞事件报道，源引 Semafor）。
- 事件主体：Lovable——号称让几乎任何人用自然语言建网站/应用的 "vibe coding" 应用——存在重大网络安全问题。
- 漏洞概况：关键安全缺陷数月未修复，几乎任何人都能访问站点用户的关键信息——姓名、邮箱甚至财务信息。
- 数据来源：2025-03，Replit 员工 Matt Palmer 的报告——1,645 个 Lovable 生成的 web 应用中有 170 个存在同样的明显安全缺陷，黑客可轻易获取高度敏感信息。
- 修复敷衍细节：Lovable 后来推出 "security scanner"，但 Palmer 指出它只检查是否存在 row level security（RLS）策略，不检查其正确性或与应用逻辑的一致性——"This provides a false sense of security, failing to detect the misconfigurations that expose data."
- RLS 定义（NextLabs）：按行控制数据库数据访问的实践，使用户只能访问被授权的数据。
- 受影响用户示例：Palmer 及同事发现一个把 LinkedIn 主页转成网页的 Lovable 站点上约 500 名用户的邮箱地址。
- 渗透测试：软件工程师 Daniel Asaria 声称 47 分钟内攻入多个 "top launched" Lovable 站点，提取个人债务金额、家庭住址、API keys 和 "spicy prompts"；他 4 月发推："This isn't a breach story (I reported it), this is a wake-up call... Be cautious which 'vibe coder' you trust with your personal data."
- 披露过程：三个月 "no meaningful remediation or user notification from Lovable" 后，Palmer 团队把发现的 bug 公开到 National Vulnerabilities Database。
- Willison 评语（对 Semafor）："This is the single biggest challenge with vibe coding... The most obvious problem is that they're going to build stuff insecurely."
- 商业互怼：Lovable 创始人 Anton Osika 反指 Replit CEO Amjad Masad（曾指出 Lovable 让暴露私有数据"太容易"）是因为在"使用量和让 vibe coding 安全"上被反超而嫉妒。
- 行业背景：专家多年警告 AI 编码工具可能引入大量易被忽视的错误；研究还发现很多最先进 AI 模型并不具备解决多数编码任务的能力。
- 人才担忧：年轻 coder 开始重度依赖 AI 工具，可能极大削弱其通过困难手工解决问题获得的基础知识。
- Lovable 官方回应（X）："now significantly better at building secure apps than a few months ago and this is improving quickly"，但 "we're not yet where we want to be in terms of security"。

来源: research/raw/articles/vibe-history-futurism.md（原始 URL: https://futurism.com/problem-vibe-coding）

## vibe-history-reg1.md

- 文章：《Vibe coding may be hazardous to open source》，Thomas Claburn，The Register，2026-01-26（Koren et al. 论文报道）。
- 引子事件：Tailwind Labs CEO Adam Wathan 近期把裁员 3 人归咎于 AI——AI 编码工具横在公司与客户之间，网站流量下滑打击产品曝光。
- Wathan 原话（GitHub Issues）："Traffic to our docs is down about 40 percent from early 2023 despite Tailwind being more popular than ever... The docs are the only way people find out about our commercial products, and without customers we can't afford to maintain the framework."
- 论文信息：《Vibe Coding Kills Open Source》，作者 Miklós Koren（中欧大学/KRTK/CEPR/CESifo）、Gábor Békés（中欧大学/KRTK/CEPR）、Julian Hinz（比勒费尔德大学/基尔世界经济研究所）、Aaron Lohmann（基尔世界经济研究所）；Tailwind 案情被论文引为 AI 编码工具普及对开源社区构成 breaking change 的证据。
- 论文核心论点：AI 工具安装开源依赖的方式切断了软件开发者与项目维护者之间的互动，削弱了可能为维护者带来回报的价值回流。
- 论文结论引文："Vibe coding raises productivity by lowering the cost of using and building on existing code, but it also weakens the user engagement through which many maintainers earn returns... When OSS is monetized only through direct user engagement, greater adoption of vibe coding lowers entry and sharing, reduces the availability and quality of OSS, and reduces welfare despite higher productivity."
- Koren 对 The Register 的方法论说明：AI 工具削弱开源社区参与的证据"大多是间接的（circumstantial）"——有文献记录 ChatGPT 发布后 Stack Overflow 提问量下降，且比 ChatGPT 不可访问的国家下降更快；论文在 Tailwind 案件公开前就已动笔。
- 论文性质：基于开源软件生态经济学模型的外推（extrapolation），非直接测量。
- 采纳速度证据：Koren 引 Anthropic CEO Dario Amodei 在 2025-09 Axios AI+ Summit 的名言——"70, 80, 90 percent of the code written in Anthropic is written by Claude"；推论：对 OSS 生产者的人类注意力在萎缩。
- 回报口径：影响不只按收入衡量，而是社区认可、声誉、工作前景的总和；引最近论文——"OSS 开发者只捕获其创造总价值的约 0.1%"。
- 差异化影响：高质量大项目仍可繁荣（"We don't think that large OSS projects will disappear overnight"）；但越过"冷启动问题"会更难；边缘成功的项目维护者可能失去动力停止贡献——"The proverbial 'random person in Nebraska' may give up."
- 系统性归因与集体行动：传统上 OSS 工作不被用户直接补偿不是因为不重视，而是摩擦成本（一个项目用几十个库，不会逐个查找维护者给几分钱）；GitHub/npm 的 funding drive 不解决问题，因为仍需用户注意并掏钱包。
- Koren 的解法建议：AI 公司可以帮忙——LLM 推理集中在 OpenAI/Anthropic/OpenRouter/Groq 等少数提供商手中；"Metering the usage of each OSS library would be technically simple to do"——可作 revenue-sharing 基础，"Much like Spotify pays artists based on playtime, OSS developers could share some of the LLM revenue based on actual usage."
- Armin Ronacher（Flask 作者）观点：AI 确实在改变开源的动态——代码变便宜、相关计算在变；开源现在收到多得多的低质量贡献，但另一方面可能强化一些由强维护者背书的关键项目；"现在下结论为时过早，这是 massive shift，几年后才见分晓"；"目前任何 meta 讨论上花的精力都是浪费，直到找到新常态。"
- 页面其他相关信号（sidebar）：Shopify 收购 Tailwind 为其提供"稳定的长期归宿"（vibe coding 侵蚀该 web 开发平台营收的背景下）。

来源: research/raw/articles/vibe-history-reg1.md（原始 URL: https://www.theregister.com/2026/01/26/vibe_coding_hazardous_open_source/）

## vibe-history-ibm.md

- 文章：《What is vibe coding?》，Shalini Harkar，IBM Think，2025-04-08 发布、2026-07-24 更新（企业视角科普）。
- 企业定义："vibe coding" 是软件开发中新且定义松散的术语，指 prompting AI 工具生成代码而非手工写码的实践。
- 定位：软件工程正从严格手工编码重塑为更灵活的 AI 辅助/AI 驱动；vibe coding 处于这一变化前沿，代表向 intent-driven（意图驱动）软件开发的转移——AI 系统从自然语言指令生成代码。
- 对 Karpathy 定义的转述：最少人工编码的编码策略——程序员用 AI 代码但更关注结果、测试与调优。
- 演化判断：vibe coding 已从基础代码 prompt 走向围绕 context、intention、orchestration 的更深层理解；AI 越深入实际任务，区分将不再是编程语言与语法，而是意图与上下文的规约。
- 四大"范式转移"收益：（1）快速原型——团队把想法从早期概念推进到功能原型再到规模化的关键使能器，用于市场验证与战略转向；（2）问题优先——从刚性编码风格转向动态结构，解决问题本身取代技术栈成为开发者的基石；（3）降低风险放大影响——快速做出 MVP、廉价试验想法、按反馈采纳调整，降低沉没成本、分散风险、只为验证过的概念投入资源；（4）多模态切换——语音驱动编码、可视化编程界面、AI 代码生成、混合开发环境提升可用性/灵活性/直觉性。
- 企业实施五步法：（1）选择 AI 编码平台——Replit、Cursor、GitHub Copilot、Windsurf、bolt.new 等提供远超自动补全的能力（实时代码生成、多文件推理、调试、命令执行、部署帮助、工作区记忆）；（2）描述意图与上下文——vibe coding 不重度依赖特定 prompt 而是重视所给上下文，写明目标、需求、约束、偏好技术栈与设计风格（附习惯跟踪应用示例 prompt）；（3）生成初始应用代码——从应用架构、前后端、API、数据库设计到相关文档，但这只是起点；（4）迭代精化——循环 Intent → Generate → Review → Refine → Generate；（5）验证、安全与部署——生成软件仍需工程努力才能投产：code review、测试、依赖检查、安全评估、合规校验等。
- Context engineering 一节："任何 AI 模型失败的原因从来不是坏 prompt，而是缺少上下文"；LLM 未来进展来自 context 而非 prompts；为产出可靠输出需给 Gemini 等模型五类上下文——业务上下文（要解决什么问题）、架构上下文（系统如何集成进现有架构）、仓库上下文（代码库既有约定/模式/依赖）、安全上下文（须遵守的政策/合规/约束）、运维上下文（性能与可扩展性要求）；缺任何一类可能产出"技术上对、真实运营生态中错"的代码；context engineering 将成为企业 AI 核心能力。
- 下一阶段判断："Autonomous engineering"——vibe coding 证明了 AI 能从自然语言 prompt 生成代码、使原型更快更高效，但代码生成不等于软件工程：生产级开发需要规划、架构设计、代码生成、测试、安全审查、部署与治理——这正是 vibe coding 开始暴露缺陷之处；行业正从 "prompt to code" 转向 "intent to AI agent to software"，重点覆盖开发每一阶段的自动化与编排。
- 局限清单：（1）技术复杂度——标准框架没问题，新颖/复杂的真实需求吃力；（2）代码质量与性能——适合测试与原型，需优化精化；不适合分布式应用（需结构化架构与复杂优化策略）；（3）调试挑战——AI 代码动态且缺乏架构结构；（4）维护与更新——代码结构未正确维护时开发者难以理解底层逻辑；（5）安全（最关键）——AI 生成代码常被排除在 code review 与安全检查之外，导致未被发现的可被利用漏洞。
- "安全债"（security debt）概念：vibe coding 造成新型技术债——开发者越是无验证地拥抱 AI 编码，越多漏洞产生并留待将来修复；典型例子：硬编码 API key 与密码、SQL 注入、不安全 API、过度授权应用、认证不足、带漏洞的第三方库。
- 企业风险放大：企业环境下赌注更高——vibe coding 的脆弱原型可能后来变成管理客户信息、财务、医疗、知识产权的真实生产应用而不经必要安全分析；问题从"能不能做出来"变成"能不能信任它"。
- 经济学总结：软件生产传统上受编码专业能力与努力（尤其新手）限制；AI 使瓶颈从编码本身转向想法与决策——编码将过剩；更有意义的问题不是 AI 能否写软件，而是能否正确利用 AI 加速创新并把产品带向市场。
- 文中脚注引用：Karpathy 原推（2025-03-07 检索）；Mehta TechCrunch（2025-03-06）；Edwards Ars 两篇（2025-03-16 "AI coding assistant refuses to write code"；2025-03-06 vibes）；Naughton Observer（2025-03-16）；Chowdhury & Mann Business Insider（2025-02-26 "Silicon Valley's next act"）。

来源: research/raw/articles/vibe-history-ibm.md（原始 URL: https://www.ibm.com/think/topics/vibe-coding）

## vibe-history-veracode.md

- 报告：《2025 GenAI Code Security Report》（Veracode，2025-10 更新版资源页）。
- 核心口号："AI is generating code. Our research shows it's generating risk."（AI 在生成代码，也在生成风险。）
- 研究范围：分析 100+ 个大语言模型生成的代码，覆盖 Java、JavaScript、Python、C#。
- 三个主要发现（页面自列）：（1）AI 生成代码在 45% 的测试中引入有风险的安全缺陷；（2）没有哪种主流语言幸免，但其中一种风险最大；（3）"Bigger Models ≠ More Secure Code"——更大、更新的模型没有改善安全性。
- 结论句："AI-generated code often isn't secure, and the risk is likely already in your stack"（AI 生成代码常不安全，且风险很可能已在你技术栈中）。

来源: research/raw/articles/vibe-history-veracode.md（原始 URL: https://www.veracode.com/resources/analyst-reports/2025-genai-code-security-report/）

## vibe-history-coderabbit.md

- 报告博客：《State of AI vs Human Code Generation Report》，David Loker，CodeRabbit Blog，2025-12-17。
- 背景数据（引他人报告）：pull request 每作者年增 20%（AI 之功），但每 PR 的 incident 增加 23.5%。
- 动机：高曝光事故、postmortem 与轶事指向 AI 写的变更是诱因；并非边缘案例或误用，而是"正常 PR 内嵌了微妙错误"；但 AI 编码工具快速普及下，AI-authored PR 与人写 PR 的质量差异缺乏具体数据。
- 数据集：470 个开源 GitHub PR（320 个 AI 参与署名 + 150 个纯人类）；用 CodeRabbit 结构化 issue 分类法；所有发现归一化为"每 100 PR 的 issue 数"，用统计 rate ratio 比较。
- 方法学局限：无法直接确认每个 PR 的作者身份——通过 AI 共同署名信号判定，没有该信号的假定为人类所写；不能保证"人类写"组全为纯人类；两组差异统计显著；完整方法学在报告末尾公开。
- 总体判断：没有任何 issue 类别是 AI 独有的——人类与 AI 犯同类错误，"AI 只是更频繁、更大规模地犯其中许多"。
- Top 10 发现：（1）AI 生成 PR 总体 issue 约 1.7 倍（每 PR 10.83 vs 6.45；高 issue 离群值在 AI PR 更常见，造成重审查负担）；（2）严重度升级——critical 与 major 发现多约 1.4–1.7 倍；（3）逻辑与正确性问题多 75%（业务逻辑错误、依赖错误、控制流缺陷、配置错误；逻辑错误修复最贵、最易引发下游事故）；（4）可读性问题飙升 3 倍以上——全数据集最大差异；AI 代码看着一致但违反命名/清晰度/结构的本地模式；（5）错误处理与异常路径缺口近 2 倍（缺 null 检查、early return、护栏、完整异常逻辑；与真实世界宕机紧密相关）；（6）安全问题最高 2.74 倍（最突出模式：不当密码处理与不安全对象引用；无 AI 独有漏洞类型但几乎全被放大）；（7）性能回归数量少但严重偏向 AI（过多 I/O 操作约 8 倍——反映 AI 重清晰轻资源效率）；（8）并发与依赖正确性约 2 倍（错误排序、依赖流缺陷、并发原语误用；小错误大影响）；（9）格式问题 2.66 倍（即使有 formatter/linter 的团队也见噪音：空格、缩进、结构不一致、风格漂移）；（10）命名不一致近 2 倍（不清晰命名、术语错配、泛化标识符，加重 reviewer 认知负担）。
- 原因分析（CodeRabbit 解读）：AI 缺乏本地业务逻辑（模型统计推断代码模式而非语义理解，没有严格约束时错过资深工程师内化的系统规则）；AI 生成表面正确（看着对但跳过控制流保护或误用依赖排序）；AI 不能完美遵守 repo 惯例（命名/架构/格式趋向通用默认）；无显式 prompt 时安全模式退化（复刻旧训练数据中的遗留模式或过时实践）；AI 重清晰轻效率（默认简单循环、重复 I/O、未优化数据结构）。
- 七条工程对策：（1）给 AI 所需上下文——业务规则、配置模式、架构约束；提供 prompt 片段、repo 专属 instruction capsule、配置 schema 以减少误配置与逻辑漂移；（2）用 policy-as-code 强制风格——CI 强制 formatter、linter、style guide 在 review 前消灭整类 AI 问题；（3）加正确性护栏——非平凡控制流必须有测试、强制 nullability/type assertion、标准化异常处理规则、需要处显式 prompt 护栏；（4）强化安全默认——集中凭证处理、禁 ad-hoc 密码用法、自动跑 SAST 与安全 linter；（5）引导模型走高效模式——batching I/O 指南、合适数据结构选择、prompt 中性能提示；（6）采用 AI-aware PR checklist——reviewer 显式问：错误路径覆盖了吗？并发原语对吗？配置值校验了吗？密码走批准的 helper 吗？（瞄准 AI 最易错处）；（7）借助 AI 代码审查工具——现有 review 流水线不是为当前代码量设计的，reviewer 疲劳已证明导致更多问题与漏网 bug；AI code review 工具标准化跨工具质量、减少时间与认知劳动（CodeRabbit 自荐）。
- 底线结论："AI 加速输出，但无护栏的加速增加风险"；AI 代码更可变、更易错、更可能引入高严重度 issue；未来不是取代开发者，而是构建放大 AI 所长、补偿其所短的系统、工作流与安全层；"Quality isn't automatic. It requires deliberate engineering. Even when using AI tools."

来源: research/raw/articles/vibe-history-coderabbit.md（原始 URL: https://www.coderabbit.ai/blog/state-of-ai-vs-human-code-generation-report）

## vibe-history-leaddev.md

- 文章：《How AI generated code compounds technical debt》，Bill Doerrfeld，LeadDev，2025-02-19（GitClear 数据报道）。
- 副题引语："I don't think I have ever seen so much technical debt being created in such a short period of time"（Kin Lane，API evangelist，35 年技术生涯）。
- 背景：IDE 内嵌 LLM 编码助手让单 prompt/Tab 键即可产出多行代码块；AI 编码工具进入后 DRY 等最佳实践在滑坡。
- 研究概况：GitClear 第二届年度《AI Copilot Code Quality》研究，分析 2020–2024 年 2.11 亿行变更代码（匿名私有仓库 + 25 个最大开源项目合并数据集）。
- 代码复用在死去：2024 年，5 行以上且与相邻代码重复的代码块频率增长 8 倍——重复率比两年前高 10 倍。
- 2024 年构成：46% 的代码变更是新行；copy-paste 行数超过 moved 行。
- "moved" 指标解释：GitClear 自创，跟踪代码重排——通常为把既有工作整合进可复用模块的动作；GitClear CEO Bill Harding："Refactored systems, in general, and moved code in particular, are the signature of code reuse"（移动代码是代码复用的签名）。
- 含义：代码移动逐年下降表明开发者更少复用既有工作——偏离行业最佳实践，将带来更多冗余系统、更少功能整合。
- 交叉证据（Harness《State of Software Delivery 2025》）：与感知的生产力收益相反，多数开发者花更多时间调试 AI 生成代码、更多时间解决安全漏洞。
- 交叉证据（Google 2024 DORA 报告）：AI 使用增 25% 加快 code review 并利好文档，但交付稳定性降 7.2%。
- "无限代码 = 无限维护"：若趋势持续，缺陷修复与重构可能很快主导开发者工作量；Harding："If developer productivity continues being measured by commit count or lines added, AI-driven maintainability decay will proliferate"；除非团队聚焦长期可持续，AI 将把软件推向无尽扩张、需要 "indefinite maintenance"。
- 克隆代码的成本：重复代码不止难维护还昂贵——代码存储累积云成本；bug 在克隆块间成倍复制；测试成后勤噩梦；学术研究持续把 co-changed code clones（须多处同步更新的重复块）与更高缺陷率挂钩（引 2023 华中师范大学研究："Code cloning is a common practice that negatively impacts software maintenance"）。
- 积极发现：commit 间隔时间在缩短；AI 也可反向利用——如 Cursor 可重写代码保证逐行一致性。
- 人的角色：AI 擅长一次性代码但上下文窗口有限；人类在把重复逻辑重构为可复用函数、整合相关模块、复用微服务等方面仍起关键作用，使代码库更凝聚。
- Harding 收尾："There is a lot of utility that AI provides, but the data from this year affirms why long-term-oriented devs might eye their 'tab' key with a faint sense of foreboding."

来源: research/raw/articles/vibe-history-leaddev.md（原始 URL: https://leaddev.com/technical-direction/how-ai-generated-code-accelerates-technical-debt）

## vibe-history-ghblog.md

- 文章：《Welcome to the Eternal September of open source. Here's what we plan to do for maintainers.》，Ashley Wolf（GitHub 开源项目总监），The GitHub Blog，2026-02-12（2026-02-13 更新）。
- 核心命题：开放协作靠信任运行；长期以来这种信任由一个不完美但天然的过滤器——摩擦（friction）——保护。
- Usenet 典故：1993 年起每年 9 月新生涌入 Usenet，社区耐心引导；主流拨号 ISP 普及后新用户持续涌入——成为"永不结束的九月"（Eternal September）；今天开源正在经历自己的 Eternal September，且不只是新用户，而是贡献的绝对数量。
- 摩擦史观：邮寄列表时代贡献开源需要真实努力（订阅、潜伏、理解文化、正确 format patch、解释为什么重要）——努力不保证质量但筛选了参与度；但也排斥了人，许多项目努力降低门槛；GitHub + pull request + "Good First Issues" 大幅降低摩擦、使贡献更可及——这是好事；但摩擦是平衡术：太多把人和想法挡在外面，太少会拉伤开源赖以生存的信任。
- 当下变化："Today, a pull request can be generated in seconds. Generative AI makes it easy for people to produce code, issues, or security reports at scale. **The cost to create has dropped but the cost to review has not.**"（创作成本已降，审查成本未降。）
- 善意假设：多数贡献者出于善意——帮助在意的项目、学习、可见性、职业收益；这些激励不新鲜也不错误。
- 真正的挑战：低质量贡献规模化到达时——当数量增长快于审查容量，即使善意的提交也会淹没维护者；信任开始被拉伤。
- "噪音不是新现象"论：维护者一直在处理嘈杂流入——Linux kernel 的 "web of trust" 哲学、正式化的 SubmittingPatches 指南、2004 年引入的 Developer Certificate of Origin (DCO)；Mozilla 与 GNOME 围绕"多数进入的 bug 报告需先过滤"建了正式 triage 系统；GenAI 之前维护者就在应对商业/开源扫描工具的自动化报告浪潮。
- 维护者的永恒之问："Are you really trying to help me, or just help yourself?"（你真想帮我，还是只想帮你自己？）
- 不对称负担机制：工具（静态分析器或 LLM）让生成报告或修复容易，不代表贡献对项目有价值；创作之易常给维护者增加负担，因为利益不平衡——贡献者拿 credit（或 CVE、可见性），维护者拿维护负担。
- 现实例证：curl 在 AI 生成安全报告爆炸后终止 bug bounty（每份验证耗时数小时）；Ghostty 等项目转向仅限邀请的贡献模式（接受代码贡献前须先讨论）；多项目正在采纳关于 AI 生成贡献的显式规则。
- GitHub 已发布功能：仓库级 pull request 控制（可限制 PR 创建为协作者或整体禁用 PR）；issue 置顶评论；降噪 banner（鼓励 react/subscribe 而非 "+1" 评论）；PR 性能改进（新 files changed 体验中大 PR 响应快 67%）；更快的 issue 导航（维护者 triage 提速）；临时互动限制（对公开仓库特定用户限期限活动）；即将推出：UI 删除 PR（清除 spam/滥用 PR）。
- 探索中的方向：criteria-based gating（开 PR 前须关联 issue，或定义提交前必须满足的规则）；改进 triage 工具（可能用自动 triage 按 CONTRIBUTING.md 等项目自身指南评估贡献、排序应优先看的 PR）；定位是支持决策而非替代，维护者始终掌舵。
- 权衡自觉：限制会不成比例影响善意的新贡献者——因此这些控制是可选、可配置的。
- 社区自建"梯子"：部分项目转邀请制；其他在自建贡献者 triage 与声誉评分的 GitHub Actions；Mitchell Hashimoto 的 Vouch 项目——显式信任管理系统，贡献者须被可信维护者 vouch 才能参与（实验性但有谱系：Advogato 信任度量 → Drupal credit 系统 → Linux kernel Signed-off-by 链）；Python 社区投资贡献者指南/mentorship/清晰入口；Kubernetes 用强治理+大量文档与贡献者教育（教新贡献者"什么样的贡献是有用的贡献"）。
- 激励结构反思：只建封锁与禁令会造出堡垒而非市集（fortress, not a bazaar）；GitHub 的"贡献"概念仍重代码署名；WordPress 用手写 "props" 表彰非代码贡献（写作、复现步骤、用户测试、社区支持）；GitHub 想探索更好呈现与庆祝此类贡献——持续 triage issue 或合并文档 PR 的人已证明理解项目的声音，是应被呈现的信任信号。
- 已开社区讨论帖：《Exploring Solutions to Tackle Low-Quality Contributions on GitHub》征求反馈。
- 结尾立场：Eternal September 值得庆祝（前所未有之多的人想参与）；贡献量只会增长；不是拉起吊桥，而是给维护者更好的信号、工具与引导能量的方式。

来源: research/raw/articles/vibe-history-ghblog.md（原始 URL: https://github.blog/open-source/maintainers/welcome-to-the-eternal-september-of-open-source-heres-what-we-plan-to-do-for-maintainers/）

## vibe-history-ghslop.md

- 文章：《engineer away the slop》，Geoffrey Huntley，ghuntley.com（无明确日期，内容指向其加入 Antithesis 的公告，"过去六个月"职业剧变）。
- 公告本身：作者加入 Antithesis（确定性测试/形式化验证方向公司）。
- 时间线自述：2024-11 他已看出职业将变；"过去六个月我们职业的变化超过过去 30 年"。
- 核心论断："Software authoring has been commoditised. Everyone is now a software developer, but being a software developer does not mean that they're an engineer."（软件写作已被商品化；人人都是软件开发者，但软件开发者不等于工程师。）
- 词义辨析："engineer" 在本行业被轻率使用，但在其他行业，工程师意味着 failures are unacceptable（失败不可接受）。
- 个人背景：即将 44 岁，见过极烂代码库，也对自己早期代码有悔意。
- Eternal September 之忧（AI Engineer World Fair 演讲内容）：2000 年代初 dot-com 崩溃后行业没有培养出足够软件工程师来支撑学徒制学习模式；事件已过去 26 年，如今人人都能造软件，"we've got some hard questions to solve"。
- 不变量：" whilst many things have changed, the job of software engineers is to produce experiences without defects."（软件工程师的工作是产出无缺陷的体验。）
- 假设清单（他的推断）：形式化验证与确定性系统测试的学科/技术即将 crossing the chasm（跨越鸿沟）；过去 30 年的存量（brownfield）软件正同时受"无限软件危机"（"how do we do code review now?"/"the volume of code/change is too high"）冲击；这两个领域的熟练从业者不够多；为项目（新建或改造）构建模拟器的成本已显著降低；有些问题类别除非模拟确定性计算机（强制任何东西变确定的强力手段）否则不会暴露。
- 工具组合论：Antithesis + LLM 对抗式 code review + pre-commit hook 驱动的语言分析器，将成为"software factory"的关键组件——让人/agent 无需习得这些专业知识即可交付可靠软件。
- 金句收尾："Creation is now near-free. Verification/understanding is not, yet. It's time to engineer away the slop."（创作已近免费，验证/理解还没有。是时候工程化地消灭 slop 了。）

来源: research/raw/articles/vibe-history-ghslop.md（原始 URL: https://ghuntley.com/slop/）

## vibe-history-ghspecs.md

- 文章：《specs》（副题 "From Design doc to code: the Groundhog AI coding assistant (and new Cursor vibecoding meta)"），Geoffrey Huntley，ghuntley.com（付费订阅墙内，仅公开部分可见）。
- 文章定位：是《You are using Cursor AI incorrectly...》与《Yes, Claude Code can decompile itself》的后续，提出使用 Cursor 的新 meta。
- 方法组合论断（公开部分核心）：把 "/specs"（本文）方法与 "stdlib" 方法结合，再配一门提供 compiler soundness（良好类型驱动）与编译器报错的语言，"the results are incredible"。
- 产出量化："You can drive hands-free output of N factor (entire weeks' worth) of co-workers in hours."（免手动产出 N 倍——数周同事工作量在数小时内完成。）
- 方法实质（从标题与引言推断并按原文记录）：设计文档（spec）→ 代码的流水线，即"写规格而非写代码"流派。
- 元信息：正文为订阅者专属；作者提供免费终身订阅的营销邀请。

来源: research/raw/articles/vibe-history-ghspecs.md（原始 URL: https://ghuntley.com/specs/）

## vibe-history-speckit.md（GitHub Spec Kit README 摘录）

- 项目：GitHub 官方开源 Spec Kit——Spec-Driven Development（SDD，规格驱动开发）工具包（2025-09 发布，持续更新）。
- 三大独立入口（README 表格）：（1）构建功能或应用 → Spec-Driven Development → 产出"贯穿规划、实现与收敛的规格"；（2）诊断修复损坏行为 → Bug fixing → 产出"评估过的原因、界定过的修复、记录过的验证"；（3）判断想法是否值得投资 → Idea assessment → 产出"有证据支持的 go / clarify / stop 决策"。
- 架构原则：三者是**独立入口点**而非三个必经阶段；SDD 随 core 发布；bug fixing 与 assessment 是按需安装的 bundled extensions。
- 环境要求：Python 3.11+、uv、受支持的 AI coding agent，运行于 Linux/macOS/Windows。
- 安装：`uv tool install specify-cli` → `specify init my-project --integration copilot`。
- 调用方式：在项目目录启动 coding agent，在 agent 聊天里逐个调用 `/speckit-*` skill（一次一个，审阅结果后再继续）；强调"这些是 agent skills，不是终端命令"。
- SDD 定义：先定义 what 与 why，再决定 how——把需求变成规格、技术计划与可执行任务，再依据这些工件引导实现。
- 流程总纲（README 原文）："**Constitution once per project; specify → plan → tasks → implement → converge per feature.**"（宪法每项目一次；specify→plan→tasks→implement→converge 每功能一轮。）
- 调用链示例：/speckit-constitution（创建聚焦代码质量、测试、可维护性的原则）→ /speckit-specify（用自然语言描述功能）→ /speckit-plan（给技术约束，如 "Use Vite with vanilla JavaScript..."）→ /speckit-tasks → /speckit-implement → /speckit-converge。
- 收敛规则："Repeat **implement → converge** until convergence reports **Converged**"；需要额外质量门时可加 clarification、checklist、consistency analysis。
- Bug fixing 扩展：安装 `specify extension add bug`；调用 assess → fix → test 三 skill（示例 /speckit-bug-assess、/speckit-bug-fix、/speckit-bug-test 带 slug）；报告存 `.specify/bugs/<slug>/`；最终裁决为 `verified` / `partial` / `failed`；门禁格言："**Missing verification is not a successful fix.**"（缺验证不等于修复成功。）
- 设计原则（bug fixing 一节）：保持诊断、修复、验证分离，使 agent 修复"评估过的原因"并检查"原始症状"；无需先走 SDD 功能流程。
- Idea assessment 扩展：安装 `specify extension add assess`；调用 intake → research → define → shape → decide 五 skill；定位"在投入想法前收集证据"，是独立过程，在没有任何源代码的项目中也能用。

来源: research/raw/articles/vibe-history-speckit.md（原始 URL: https://github.com/github/spec-kit）

# 第二部分：skills-ecosystem-*（Agent Skill 规范与写作最佳实践）

## skills-ecosystem-agentskills-io-spec.md

- 规范性质：Agent Skills 官方格式规范（agentskills.io/specification）。
- 目录结构：一个 skill 是一个目录，最少包含一个 `SKILL.md` 文件。
- SKILL.md 格式：必须由 YAML frontmatter + Markdown 内容组成。
- frontmatter `name` 字段（必填）：1-64 字符；仅允许 unicode 小写字母数字（a-z、0-9）与连字符（-）；不得以连字符开头或结尾；不得含连续连字符（--）；**必须与父目录名一致**。
- frontmatter `description` 字段（必填）：1-1024 字符；应同时描述 skill 做什么与何时使用；应包含帮助 agent 识别相关任务的具体关键词。
- frontmatter `license` 字段（可选）：声明 skill 适用许可证；建议保持简短（许可证名或捆绑许可证文件名）。
- frontmatter `compatibility` 字段（可选）：提供时须 1-500 字符；仅在 skill 有特定环境要求时包含；可标示目标产品、所需系统包、网络访问需求等。
- frontmatter `metadata` 字段（可选）：字符串键到字符串值的 map；客户端可用来存规范未定义的附加属性；建议键名足够独特以避免意外冲突。
- frontmatter `allowed-tools` 字段（可选）：空格分隔的预授权可运行工具列表；实验性，各 agent 实现支持程度可能不同。
- 正文内容：frontmatter 之后的 Markdown 正文是 skill 指令，**无格式限制**——"写任何能帮 agent 有效完成任务的内容"；推荐小节：分步指令、输入输出示例、常见边界情况。
- 加载语义：agent 决定激活 skill 后会一次性加载整个文件；建议把较长的 SKILL.md 内容拆分为被引用的文件。
- 可选目录：skill 目录可包含 SKILL.md 之外的任意文件与目录；规范给出组织惯例。
- `scripts/` 目录：存放 agent 可执行代码；脚本应自包含或清楚记录依赖；包含有用的错误信息；优雅处理边界情况；支持语言取决于 agent 实现（常见 Python、Bash、JavaScript）。
- `references/` 目录：agent 按需阅读的补充文档——REFERENCE.md（详细技术参考）、FORMS.md（表单模板/结构化数据格式）、领域专属文件（finance.md、legal.md 等）；保持各 reference 文件聚焦——agent 按需加载，文件越小越省上下文。
- `assets/` 目录：静态资源——模板（文档/配置模板）、图像（图示/示例）、数据文件（查找表、schema）。
- 渐进式披露（progressive disclosure）三级模型：agent 渐进加载 skill，仅在任务需要时拉入更多细节——（1）Metadata（约 100 token）：启动时为所有 skill 加载 name 与 description；（2）Instructions（建议 <5000 token）：激活时加载完整 SKILL.md 正文；（3）Resources（按需）：scripts/、references/、assets/ 中的文件仅在需要时加载。
- 行数上限建议：SKILL.md 保持 500 行以内；详细参考材料移入单独文件。
- 文件引用规则：引用 skill 内其他文件时用相对 skill 根目录的相对路径；引用链保持一层深（从 SKILL.md 直接可达），避免深嵌套引用链。
- 校验：使用 skills-ref 参考库验证 skill——检查 SKILL.md frontmatter 有效且符合全部命名约定。

来源: research/raw/articles/skills-ecosystem-agentskills-io-spec.md（原始 URL: https://agentskills.io/specification）

## skills-ecosystem-anthropic-best-practices.md

- 文档：Anthropic 官方《Skill Authoring Best Practices》（docs.claude.com）。
- "One skill, one purpose" 设计原则：skill 做好一件事时效果最好；若一个 skill 同时处理报告生成 AND 入职文档，合并后的 description 会变模糊、损害两者的可发现性——应拆成两个。
- 按"时刻"（moments）拆分：是否使用 skill 的决定发生在某个时刻、基于当前上下文；"生成高管报告"与"格式化政策文档"是不同时刻→分开的 skill（即便都用 docx）；反之，两件事总是一起发生就合在一个 skill 里。
- "Description matters most"：Claude 只读 name 与 description 就决定是否使用 skill；skill 未按预期触发时，修 description 而不是正文。
- 有效 description 的两要素：（1）skill 做什么（能力）；（2）何时使用（具体场景与触发条件）。
- 好 description 解剖示例："Create and modify PowerPoint slides with pptxgenjs... When the user wants to display data in a visual format... ask for a 'slideshow'... use this skill"。
- 常见失败模式：description 只说 skill 包含什么（"This skill includes scripts for conversion"）而不说何时用。
- description 实操清单：用第三人称（"Creates" 而非 "Create"）；同时陈述能力与触发场景；用用户会用的关键词；避免 "helps with"/"assists in" 类虚词；包含具体名词；具体到能与相邻 skill 区分。
- 渐进式披露三层（Anthropic 版）：Level 1（常驻）metadata——name+description，约 100 词，"这是你向 Claude 营销 skill 的唯一机会"；Level 2（触发时加载）SKILL.md 正文，目标 <5k token / <500 行；Level 3（按需）捆绑文件 references/、assets/、scripts/；把细节放进嵌套文件并从 SKILL.md 引用。
- 脚本是最深层披露：代码执行**不进入上下文**——"能用脚本确定性解决的问题就不要用散文指示模型"。
- 脚本关键原则：校验输入、检查错误条件、以清晰信息失败；可用库但要锁定版本（如 uv、package-lock）；长时操作分阶段、每阶段刷新输出；记录依赖与安装说明。
- 脚本示例：PDF skill 捆绑 pdfAuthService.js；脚本也可用于处理前取数（IBM demo）。
- References 写法：Doctrina Bebé 风格的高密度 "cheat sheet" 参考文档比散文更有效——因为匹配模型训练方式（模型训练数据就是 API 文档、wiki 页这类高密度互联网内容）；训练中已内化的信息无需复述——目标清楚地说一次，让模型的训练补细节。
- 工作流组织：SKILL.md 正文要写完整工作流，包括边界情况与失败路径（"If X fails, do Y"；处理缺失输入或畸形数据）；skill 不是一堆工具的清单——正文解释工作流、skill 编排过程、工具执行步骤。
- frontmatter 保持干净：仅在真正需要时才加 license、compatibility、allowed-tools。
- Agent engineering 案例（德国企业 dashboard）：skill description 需包含何时用而不仅是什么——"Use this skill whenever the user mentions dashboards, data visualization, internal metrics, or wants to display any kind of company data, even if they don't explicitly ask for a 'dashboard'."；原因是 Claude 倾向**欠触发**（under-trigger）skill，所以要推触发词。
- 度量与迭代：发布前用真实 Claude 实例测试 skill；skill-creator skill 提供 eval 工作流——with-skill 与 baseline 对照运行、断言、benchmark 聚合、盲评 A/B 对比，以及针对触发 eval 的 description 优化循环（should-trigger / should-not-trigger 查询，含 near-miss 近邻误触例）。

来源: research/raw/articles/skills-ecosystem-anthropic-best-practices.md（原始 URL: https://docs.claude.com/en/docs/agents-and-tools/agent-skills/best-practices）

# 第三部分：followup-*（追查补档材料）

## followup-vibe-coding-maker-movement.md

- 文章：《Vibe Coding and the Maker Movement》，Sachin（Technically / technically.dev），2026-02-27；HN 讨论 id=47167931（405 分、439 评论，2026-02-26）。
- 方法论主张：每逢新技术人们倾向当作"前所未有"；理解新现象最有用的透镜是相邻现象——vibe coding 的相邻参照是 2005-2015 的 Maker Movement。
- 平行结构：vibe coding 有 slop，Maker Movement 有 "crapjects"（3D 打印出的无用之物）；当年的 "Claude Code" 是 Monoprice 200 美元打印机 + 面包板。
- Maker 运动思想核心：亲手造物带来内在转变（更创意、更创业、更自立）——造什么不重要，造的动作对你的改变才重要。
- 学理引用：Fred Turner 2018 论文——Maker 运动复活了西方边疆神学：大转变将至、个人纪律决定谁得救（"选民"叙事）。
- scenius 概念（Brian Eno 语）：过去 50 年每次爱好者技术浪潮（70s Homebrew、80s 朋克 zine、90s 早期 web）都有 scenius 阶段——小群体玩主流视为玩具的工具，享受有保护性的、无产出压力的玩耍期，多年积累"无用但好玩"的知识；内在转变其实发生在这一阶段。
- 核心论断：**vibe coding 跳过了 scenius 阶段**——直接部署给大众、直接进企业和成熟产品代码库，没有受保护的玩耍期，只有"一次 one-shot 出爆款"的压力；工具在人有判断力之前就能产出真东西。
- 心理观察：每天 12-14 小时 Claude Code 的人像"被附身"；反馈回路由机器而非他人提供→类似轻躁狂（hypomania）状态——产能确实上升但评估能力失配，分不清"这很好"和"我做这个感觉很好"，一切都像突破；速度与轻松造成"评估麻醉"（evaluative anesthesia）。
- Maker 运动的结局与教训：分布式制造承诺落空；Joel Spolsky "commoditizing your complement" 模式——廉价工具民主化了原型层，深层制造知识仍积累在深圳等工业基地，下层捕获剩余价值。
- 同构警告：vibe coding 正在上演同样的结构——快速原型的价值向上流向模型层/训练数据/基础设施，vibe coder 有变成可互换劳动力的风险。
- 作者的新隐喻：**消费**（consumption）——消费"过剩智能"（surplus intelligence）；AI 是巨量可用认知能量，vibe coding 是在它浪费之前把它花掉。
- 消费的三种正产出：（1）品味/sensibility——生产近乎免费时稀缺的是"什么应该存在"的判断；大量做+扔掉培养模式识别（创意方向、策展、品味把关角色，"ideas guy 回来了"）；（2）奇观/注意力——公开 vibe coding 是剩余精力的表演，"周末建成"帖即此类，变现为受众/声誉/期权；（3）礼物经济——把产出当礼物（开源工具、模板）占据网络节点位置。
- **信息废气**（informational exhaust）概念：每次 vibe coding 都在产生信号（用户要什么、哪些模式有效、模型在哪失败、误解什么指令），目前免费流向上游模型厂商；若结构化收集（专有数据集、记录反馈回路、"data fortress"），废料可变资产——连失败原型的"为什么失败"也是价值。
- 心理建议：用 "craft（手艺）" 框架套 vibe coding 会导致倦怠（craft 假设你向内求，而工具已代劳，落差感像个人失败）；"消费"框架更可持续——问题从"这说明我是什么样的人"变成"我可以把这多余能量花在什么最有趣的地方"。
- Rachel Thomas 类比：vibe coding 像赌博的 dark flow，会上瘾于创造的表面体验。
- HN 高赞/长评（426 条直评）：eleventyseven 反驳"没人记得 3D 打印泡沫"——列举 2012-2015 主流媒体（康奈尔教授上 CNN、世界经济论坛）预测"两三年内每个家庭都有 3D 打印机/自复制打印机"；批评技术乐观预言失败后集体失忆，像末日邪教"预言没应验就换新预言"。
- aleph_minus_one：自复制打印机实现得不差（RepRap 谱系），只是大众不再关注；家用机近年处理工程材料大幅进步；泡沫叙事 ≠ 技术消失。
- bitwize：vibe coding 与 maker movement 几乎相反——前者卖点"把思考外包给云、几乎零付出获得产出"，后者卖点"自己造所以理解并掌控它"；若 vibe coding 终结，会因模型坍塌/收益递减/VC 钱烧完；业余者退场，领域收缩回小众。
- epiccoleman（反方亲历）：用 Claude 一小时内诊断并修复 Minecraft fabric-api 模组 bug 并提交上游；"没有 LLM 我根本不会去做"——LLM 降低的是"值得动手"的门槛。
- dheera：maker movement 没消失，是门槛低到全民化；列举 3D 打印宠物食盆防蚁罩、ESP32+VLM 摄像头数猫喝水次数、激光切割空调软管接口等近期实例。
- tetha：高薪工程师的价值在问题处理方式；初级工程师心得——"先琢磨一两礼拜，问题最终塌缩成很小的代码量，Copilot 只在结构想清后帮忙写样板"。
- ytoawwhra92（实操约束）：agent 写几千行以上必须有测试防失控；给成熟、结构良好的代码库；任务切小；一次只改一件事；静态分析标出受影响用户流程交人工审；human-in-the-loop 拿前后可运行构建对比。
- redwood：美国 maker 运动"趣味/艺术"化，真正繁荣在深圳工业基地；造 PC 如同最终组装，复杂度被抽象掉；当下是"scenius 世界舞台期"。

来源: research/raw/articles/followup-vibe-coding-maker-movement.md（原始 URL: https://read.technically.dev/p/vibe-coding-and-the-maker-movement；HN: https://news.ycombinator.com/item?id=47167931）

## followup-mnilax-12-rules.md

- 来源：@Mnilax 的 X 长文《Karpathy's 4 CLAUDE.md rules — I added 8 more》（2026-05-09）。
- 背景时间线：2026-01 底 Karpathy 发推抱怨 Claude 写代码三大失败模式——**silent wrong assumptions（静默错误假设）、over-complication（过度复杂化）、orthogonal damage（对不该动的代码造成正交伤害）**。
- Forrest Chang 把抱怨打包成 4 条行为规则写进单个 CLAUDE.md，放上 GitHub（forrestchang/andrej-karpathy-skills）：首日 5,828 star、两周 6 万收藏、如今 12 万 star——2026 年增长最快的单文件仓库。
- 作者实验设定：6 周、30 个代码库上测试；4 规则把约 40% 失误率降到 <3%（在其擅长场景）；但 2026-05 的 Claude Code 生态有新问题（agent 打架、hook 级联、skill 加载冲突、跨会话多步工作流断裂），于是追加 8 条。
- 原版 4 规则（逐条）：（1）**Think Before Coding**——不做静默假设；陈述假设、暴露 tradeoff、先问再猜、有更简单方案时反驳；（2）**Simplicity First**——解决问题的最少代码；无投机性功能；单次使用不抽象；"资深工程师会说复杂了就简化"；（3）**Surgical Changes**——只动必须动的；不"顺手改进"相邻代码/注释/格式；不重构没坏的东西；匹配现有风格；（4）**Goal-Driven Execution**——定义成功标准并循环到验证通过；告诉 Claude 成功长什么样而不是步骤。
- 新增 8 规则（各附真实事故）：（5）**Use the model only for judgment calls**——路由/重试/状态码处理/确定性变换用普通代码；模型只做分类、起草、摘要、非结构化抽取；事故：用 Claude 判断 503 是否重试，两周后漂移；（6）**Token budgets are not advisory**——单任务 4k / 单会话 30k token 硬预算，接近即总结重启，超限显式报告；事故：90 分钟调试循环，模型重复提 40 条消息前已被否的方案；（7）**Surface conflicts, don't average them**——代码库两种模式矛盾时选其一（更新/更受测的），解释并标记另一待清理；"同时满足两条规则的折中代码是最差的代码"；事故：双错误处理器吞错两遍；（8）**Read before you write**——加代码前先读文件导出、直接调用方、共享工具；不懂现有结构为何如此就先问；**"看起来正交"是代码库里最危险的话**；事故：在既有同功能函数旁又写一个，import 顺序导致旧的（6 个月的 source of truth）被覆盖；（9）**Tests verify intent, not just behavior**——测试必须编码"行为为什么重要"；写不出"业务逻辑变了就会挂"的测试 = 函数是错的；事故：12 个全过的 auth 测试，生产 auth 却是坏的（函数返回常量）；（10）**Checkpoint after every significant step**——每步后总结做了什么/验证了什么/剩什么；不能描述当前状态就不要继续；迷失就停下重述；事故：6 步重构第 4 步错，5、6 步叠在坏状态上，解缠比重做还慢；（11）**Match the codebase's conventions, even if you disagree**——代码库内 conformance > taste；真觉得有害就提出来，不要静默分叉；事故：向 class 组件库引入 hooks，破坏测试模式，半天返工；（12）**Fail loud**——最贵的失败是"看起来像成功"；跳过记录的"迁移完成"是错的；"测试通过"若跳过了任何一条也是错的；默认暴露不确定性；事故：迁移静默跳过 14% 记录，11 天后报表才发现。
- 自称数据（50 个代表性任务 × 30 代码库 × 6 周）：失误率——无规则 ~41% → 4 规则 11% → 12 规则 3%；合规率——4 规则 78% → 12 规则 76%（几乎零额外注意力成本；新规则覆盖原 4 条未覆盖的失败模式，不争夺同一注意力预算）。
- 失误类型计数口径：silent wrong assumption、over-engineering、orthogonal damage、silent failure、convention violation、conflict averaging、missed checkpoint。
- 原版 4 规则的 4 个盲区：（1）长时 agent 任务——无预算/检查点/fail-loud 规则时 pipeline 会漂移；（2）多代码库一致性——"匹配现有风格"假设只有一种风格，monorepo 12 个服务会随机选或平均；（3）测试质量——"tests pass" ≠ 有意义的测试；（4）生产 vs 原型——Simplicity First 在需要 100 行投机脚手架的早期原型上过度开火。
- 负面结果（试过并淘汰）：Reddit/X 上抄的规则多为 Karpathy 4 条换皮或领域特定不泛化；**超过 12 条**——测到 18 条时合规率 76%→52%，200 行天花板真实存在，超过后 Claude 模式匹配到"规则存在"而不真读；依赖可能不存在的工具的规则（"always use eslint"）在工具不在时静默失效——换成能力无关措辞（"match the codebase's enforced style"）；在 CLAUDE.md 放示例而非规则——3 个示例 ≈ 10 条规则的上下文成本且过拟合；**"Be careful"/"think hard"/"really focus"** 是纯噪音，合规率跌到 ~30%（不可测试）——换成具体祈使句（"state assumptions explicitly"）；让 Claude "act as senior" 无效——"Claude already thinks it's senior"，差距在想到与做到之间，身份提示关不上、祈使句规则可以。
- 其他要点：Anthropic 官方文档明说 CLAUDE.md 是 advisory，约 80% 遵循率、超过 200 行急剧下降；CLAUDE.md 是"行为契约"不是愿望清单，每条规则都应回答"这防止什么失误"；针对自己真实犯过的错保留 6 条好过 12 条里 6 条用不上；文末附 12 规则完整可粘贴模板及 `curl .../forrestchang/andrej-karpathy-skills/main/CLAUDE.md >> CLAUDE.md` 安装方式。

来源: research/raw/articles/followup-mnilax-12-rules.md（原始 URL: https://x.com/Mnilax/status/2053116311132155938）

## followup-karpathy-explain-llm-output.md

- 事件：Karpathy 2026-10-02 推文（x.com/karpathy/status/2105819303471976479，经 Kruno Golivić 详解文章二手还原）。
- 核心论点：我们将花**远比现在多的时间去理解语言模型的输出**（understanding the outputs of language models）。
- 输出格式递进清单：纯文字写作 → 图表 → 交互式 HTML 页面 → 3Blue1Brown 风格定制解说视频。
- 第一条技巧：让 LLM 用 **ASD-STE100**（航空维修手册的受控英语）解释东西——LLM 对该标准掌握很好，输出显著更可读；因规范太严，Karpathy 常放宽为 "80% of the way to ASD-STE100"。
- ASD-STE100 背景：1970s 末源于航空业（80% 机械师非英语母语），1986 首版，现为 Issue 9（2025-01-15）；两部分——53 条写作规则（9 节）+ 受控词典（约 900 批准词/1,200 非批准词）；"一个词一个义一个词性"；程序句 ≤20 词、描述句 ≤25 词；一句一个指令；主动语态；简单时态；名词连用 ≤3；一段一主题 ≤6 句。
- 生态时间线（Karpathy 之前已存在）：2026-07 底开发者在 X 上求 Claude "plain English"；Andrew Carr 回 "only report to me in ASD-STE100"；Pieter Levels 存进 Claude 记忆对抗文风膨胀；数天内出现 ≥3 个 GitHub skill——danyuchn/asd-ste100-skill（用于 agent 读的 tool 描述/错误信息；理由："读 agent 输出的 agent 不能追问，如同不能给手册作者打电话"）、toppa 的 Claude Code output style、AminBlg/SimpleEnglish（带 benchmark，HN 49114639，363 分）。
- SimpleEnglish README 金句："'Clearly' is an opinion, while STE rules you can count."（"写清楚"是观点，STE 规则可数可查。）
- 局限（对本调研重要）：LLM 没有词典、无人逐词校验→产出是 "STE-flavored English" 而非真 STE。
- 定量实验（Lucian Ghinda，2026-08，Claude/Codex 解释 4 段真实代码）：宽松 STE 指令→平均句长 18→9-10 词，**丢失 8.5% 代码特定事实**；完整 ASD-STE100 指令→**丢失 46.8%**；结论：严格受控语言以删内容为代价换简洁，Karpathy 的 "80%" 正是对此的经验校准。
- 启示："可数、可查的清晰度规则"是让 LLM 输出可读、可验证的方向；但需在简洁性与信息保真间显式权衡。

来源: research/raw/articles/followup-karpathy-explain-llm-output.md（原始 URL: https://x.com/karpathy/status/2105819303471976479；二手: https://kgolubic.com/posts/asd-ste100-and-llms/）

## followup-juejin-7412505754379468800.md

- 文章：《和 AI 一起写代码创业的这大半年》，独立开发橘子（胡子，全职独立开发者），掘金，约 2024-12。
- 作者背景：玩了一年 ChatGPT 后辞职创业，方向 AI Coding；有编程基础但非专业程序员（做过安卓、小程序）。
- 工具演进路径：Cursor → Cursor Composer（进入 agent 模式，不再逐行看代码）→ Claude Code；建议别从 Cursor Composer 入门，先手写 Cursor 熟悉；Agent 模式的真正主题是"提问"而非"写码"。
- 工作流细节：每次让 agent 输出方案讨论 5-10 轮再动手；说清楚上下文与目标；写完丢 bug 让 agent 修；期间全靠编译/运行反馈而非读代码。
- 团队协作隐喻：让 agent 像同事——明确分工（后端/前端/文档）、并行开会；以 PRD 思维分模块、定数据结构，再分头实现。
- Claude Code 用法：gh 命令 + MCP + prompt 缓存；大改动前让 agent 出实现方案（有讨论环节），重大改动才人工细看。
- 复盘结论：全栈 vibe coding 完全可行；过去一年做出 9 个产品、3 个有收入；上线前质量观是"能跑就行"，事后开始补测试与代码整理。
- 失控观察：Agent 模式时间越久越容易"失控"，靠 clear + 重新下发 PRD 拉回。
- 付费逻辑：按效果/用量买 agent 工时（类比招人，而非买软件 license）。
- 材料定位：文章主体是个人创业叙事（收入数字、社区运营、合伙人、生活状态），技术含量集中在上述工作流细节。

来源: research/raw/articles/followup-juejin-7412505754379468800.md（原始 URL: https://juejin.cn/post/7412505754379468800）

## followup-cross-model-review-evidence.md

- 论文：《Cross-Model LLM Code Review: Should you use Claude to review Codex or vice versa?》（arXiv:2607.21656；Xiang, Zhang, Zhang, Xu；2026-07-22；HN id=49166538）。
- 实验设计：116 道 LiveCodeBench 中难题，6 组对照（Claude/Codex 各自 solo、两种交叉序、两种同模型自评）；reviewer 只看题面+草稿、不能跑测试——模拟人类 code review。
- 结果（不对称）：Claude review Codex 草稿 71.6% → **89.7%**（p_BH=.001）；Codex 自评 Codex 草稿 → 84.5%（p=.022，自评也有效但弱于跨模型）；**Codex review Claude 草稿 91.4% → 82.8%（不升反降，p=.046）**；Claude 自评 Claude 草稿 91.4% 不变。
- 结论：有用的配对是不对称的——**用 Claude 审 Codex，别反过来**；盲目"第二模型把关"可能负收益，方向要选对。
- 工具实践 1：neal（github.com/navels/neal；HN 49168496/49286252）——极简 orchestrator，"Claude/Codex 各司一职"的 Unix 哲学：一个 agent 写、另一个独立 agent 审，角色分离防自我确认偏置；注意其默认方向（Claude 写 Codex 审）恰是论文里**负收益**方向→工具实践与实验证据存在冲突，值得在 Skill 中纠偏。
- 工具实践 2：portable-dsh-multi-agent-plugin（github.com/WDahah/...）——"One model writes the code, a different model reviews it"（HN 49779043），同一作者思路的可移植版。
- 工具实践 3：Gecko Security（YC F24，HN 44747204）——商业侧"另一模型找漏洞"路径。
- 对中文 Skill 的启示（原文要点）："交叉评审"不是万灵药——需写明方向与评审条件（只看题面+diff、不跑测试也能大幅提升）；同模型自评对弱草稿有效（84.5%）、对强草稿无效（91.4% 不变）→按草稿质量分层选择：弱→自评/跨模型，强→跳过；评审 prompt 的关键是"给定意图（problem）+ 草稿，只做审查不改写"。

来源: research/raw/articles/followup-cross-model-review-evidence.md（原始 URL: https://arxiv.org/abs/2607.21656）

## followup-ciq-imitation-game.md

- 文章：《The Imitation Game: When AI Writes the Code》，Ian Tewksbury（CIQ/Red Hat 系，NSTXBUG；基于 2025 NSTXLQT 演讲），2025-07。
- 命名梗：LLM = "大型模仿机器"，玩的是图灵的模仿游戏——输出统计上像人写的代码，不保证正确。
- 指标学辨析：认知复杂度（Cognitive Complexity，Sonar 指标）度量人类理解代码的难度、与可维护性强相关；圈复杂度（cyclomatic）机器即可数；认知复杂度专测"人脑的痛感"（递归、嵌套、混合运算符等加倍）。
- AI 代码悖论：语法正确率高、甚至"更干净"（更短、命名更规整），但 LLM 从人类代码中学习 = 从人类代码的缺陷分布中学习，把最常见的人类坏习惯放大为默认输出。
- 关键机制：**LLM 倾向模仿大众写法而非最佳写法**——大多数语料是"平均水平的代码"，所以 AI 输出向平均水平回归而非向专家水平。
- 实证数据（2,200 万行级代码库内部对比）：AI 辅助代码循环复杂度略优，但**认知复杂度全面恶化**（认知复杂度/圈复杂度比值上升 = 单个"简单"分支对人更难懂）。
- 控制流指标：条件数 +7%、循环 +4%（AI 代码更多分支/循环）；计算复杂度 = 每圈复杂度认知负担上升。
- 重复代码爆炸：AI 辅助文件重复度 8.5% vs 非 AI 4.7%，**+81%**；千行重复块（duplicated blocks/KLOC）11.2 vs 5.2，**+115%**；机制 = 模型默认从训练分布插值（新颖度低）且不同请求间无记忆→同一问题反复生成相似解（如相同的 409 重试块），而非抽公共库。
- 规模层结论：文件均 LOC 略降（AI 代码更"紧凑"）、类/函数更多更细，但整体认知复杂度仍升——"碎片化 + 平庸化"。
- 缓解建议（原文给出五条）：（1）把认知复杂度预算纳入代码评审门禁（工具：SonarQube、Codacy、Semgrep 等）；（2）明确异常处理与控制流约定（嵌套上限、卫语句、认知复杂度上限）；（3）重复超阈值强制抽公共库/工具函数；为 agent 提供"先查现有工具再写"的指令；（4）生成前提示中显式要求"最小复杂度实现"，生成后跑复杂度扫描再合并；（5）持续监控趋势（重复度、认知/圈比值）作为 AI 代码健康度仪表盘。
- 交叉印证（原文注明）：与 arXiv 2511.15817（smell 倾向由 prompt 设计与模型架构决定）互证——结构质量劣化不是玄学，可测、可归因、可由提示词设计压低；与 Mnilax 规则 2（Simplicity First）/规则 7（冲突勿平均）/规则 8（写前先读）直接对应——针对"过度复杂化 + 重复"两类 AI 失败模式的提示词对策。

来源: research/raw/articles/followup-ciq-imitation-game.md（原始 URL: https://www.ciq.com/blog/the-imitation-game-when-ai-writes-the-code/）

## followup-aislopfix-6-months.md

- 来源：aislopfix.dev（落地页仅服务简介，2.4KB 单页 SPA）；正文实为 HN 自帖（id=48860941，2026-07-10，by avdept，3 评论）。
- 作者背景：17 年软件工程师（嵌入式/企业级都做过）；针对 Reddit 上抱怨 AI 代码质量的用户，固定价 $500/项目（小型项目）接单修复 AI slop；已雇人扩张；明确反对 "$10k 靠缩减代码行数来重构" 的路子。
- 六个月观察到的失败模式（频率从高到低）：（1）**无数据作用域（no data scoping）——最普遍**：换个 URL 里的 id 就能取到别人的 order/profile（IDOR）；"所有项目都以同样方式建成这样"；原作者非技术背景时现代 LLM 依然会犯；（2）前端直连数据库、没有后端：全部请求从前端发往数据库，凭证直接暴露在前端 JS bundle 里，等于把库公开给所有人；（3）私钥直接暴露在前端（现在已少见）；（4）**计费/支付是最危险的一类**：try-catch 吞错→支付失败也被当成功→一个客户（LLM 套壳产品）因给失败付款的用户发订阅而真金白银亏损；计费类问题占修复工作很大比重。
- 修复手法：对计费等关键路径——补大量测试覆盖 + **VCR cassettes**（录真实请求/响应回放），可精确构造失败响应等场景再跑测试；用真实报文而非 mock 保真。
- 评论补充：one33seven——IDOR 即 OWASP 所列，建议开发者把 OWASP Cheatsheet 喂给模型。
- avdept 回复：开发者（偶尔）会避免这些错，**非开发者除了"要有个登录页"对安全毫无概念**——说明防护指令必须内置于工具/Skill 而非依赖用户知识。

来源: research/raw/articles/followup-aislopfix-6-months.md（原始 URL: https://news.ycombinator.com/item?id=48860941）

## followup-veracode-2025-genai-code-security.md

- 报告：Veracode《2025 GenAI Code Security Report》一手博客摘要（2025-07；HN id=44645794）。
- 基线数字：**45% 的 AI 生成代码样本未通过一项或多项安全测试**（"45% AI 代码含漏洞"的一手出处）。
- 样本规模：100+ 个 LLM × 15 种语言，共 48,000+ 生成样本；每样本跑 SAST/静态安全测试，按 CWE 分类。
- 模型差异：Claude 3.5 Sonnet 失败率最低 19%；Meta Code Llama 2 7B 最高 78.4%；基线差异约 4 倍。
- 语言差异（失败率）：PHP 56.9%、C 52.4%、Java 47.7% vs JavaScript 34.1%、Python 31.7%——训练语料越老的语言风险越高。
- Top CWE：XSS（CWE-79）33.5%、路径遍历（CWE-22）24.5%、OS 注入（CWE-78）20.1%、SQL 注入（CWE-89）18.1%、硬编码凭证（CWE-798）13.4%。
- 提示词效应：具体、设计良好的提示把整体失败率从 31.5% 降到 24.3%；例如明确"代码要安全地写"即有效→prompt 是低成本质量杠杆。
- 微调反例：代码专用微调模型反而略差——41.4% vs 基座 39.9%（微调导致过拟合旧模式/旧漏洞）。
- 供应链：约 1/5 的 Python/JS 样本引用"幻觉包"（slopsquatting 攻击面）；模型常编造不存在的包名。
- 缓解结论（"<10%" 的出处）：组织在 AI 代码上应用"**结构化 review 方法**"（structured review approach）后，失败率可降到 10% 或以下——检测仍是重点，扫描 + 人工/工具 review 是把 45% 压到个位数的主要路径。
- 对 Skill 设计的启示（原文自带）：prompt 明确要求安全→失败率 -7pp——在 Skill 中固化"安全地写 + 指定语言版本/框架最佳实践"的措辞有量化收益；漏洞类型集中在注入/遍历/硬编码凭证——checklist 可直接对齐这 5 类 CWE；"结构化 review 后 <10%" 支持生成后强评审工作流（spec-kit checklist / 跨模型 review）的量化依据。

来源: research/raw/articles/followup-veracode-2025-genai-code-security.md（原始 URL: https://www.veracode.com/blog/genai-code-security-report/）

# 第四部分：任务指定必须完整罗列的两项机制（源材料在 raw/repos/）

## spec-kit 模板机制（constitution/specify/plan/tasks/implement/checklist 各自门禁规则）

> 材料位置：research/raw/repos/spec-kit/templates/（constitution-template.md、spec-template.md、plan-template.md、tasks-template.md、checklist-template.md）与 templates/commands/（constitution.md、specify.md、plan.md、tasks.md、implement.md、checklist.md 等）。

**流水线总览**：constitution（项目宪法，每项目一次）→ specify（spec.md）→ clarify（苏格拉底补问，可选）→ plan（plan.md）→ tasks（tasks.md）→ implement → checklist（质量门，可选）→ converge（收敛循环）。所有命令共用 extensions.yml 前置/后置 hook 机制（mandatory hook 必须 EXECUTE_COMMAND 真实调用并等待完成，optional hook 只提示；YAML 解析失败不得静默跳过，须报告解析错误后继续）。

**constitution（宪法命令）的门禁与规则**：
- Scope Guard：本命令只许更新项目宪法本身；用户输入中的功能实现、代码生成、重构、构建、部署请求**必须拒绝执行**，抽取为 deferred intents；不得创建/修改/删除应用源文件、feature 路由、组件、测试、部署文件；无法判断某指令是否宪法内容时先问再改；完成后在 Next Actions 节列 deferred intents 并建议后续 Spec Kit 命令但不调用。
- 模板解析：宪法脚手架经 Spec Kit preset/template 解析栈（项目覆盖 + preset 层 + extension 层 + core 兜底）在命令时解析；解析必须成功，失败即停止并报错，不得只带一层模板继续；不得回写任何版本化模板层。
- 既有值保留：`.specify/memory/constitution.md` 已存在时作为当前项目特定值与修订的来源，应用新脚手架时保留仍适用的信息。
- 版本号语义化规则：MAJOR——向后不兼容的治理/原则删除或重定义；MINOR——新增原则/小节或实质性扩展指导；PATCH——澄清、措辞、笔误等非语义修订；bump 类型不明确时先给推理再定稿。
- 日期规则：RATIFICATION_DATE 为原始批准日（未知则询问或标 TODO）；LAST_AMENDED_DATE 有变更即为今天，否则保留。
- 原则写法要求：每条 Principle 须有简洁名称行 + 捕获不可协商规则的段落（或 bullet 列表）+ 不明显时的显式 rationale；Governance 节须列修订程序、版本政策、合规审查期望。
- Sync Impact Report：更新后在宪法文件顶部以 HTML 注释生成临时审阅报告（版本变化 old→new、修改的原则清单、新增/删除小节、遗留 TODO）；它是人审材料而非治理内容，**commit 前应删除**。
- 输出前校验（五条门禁）：无未解释的括号占位符残留；版本行与报告一致；日期为 ISO YYYY-MM-DD 格式；原则必须是声明式、可测试、无模糊语言（"should" 应替换为 MUST/SHOULD 并附 rationale）；用户只给部分更新时仍须走完校验与版本决策步骤。
- 写入约束：只写 `.specify/memory/constitution.md`；不创建/修改模板源文件；格式要求标题层级与模板一致、长 rationale 行建议 <100 字符、节间单空行、无尾随空格。
- constitution-template.md 结构：Core Principles（PRINCIPLE_1..5，示例含 "Test-First (NON-NEGOTIABLE)"——TDD mandatory：Tests written → User approved → Tests fail → Then implement，严格 Red-Green-Refactor）+ 附加约束/工作流/质量门等自定义节 + Governance（示例："Constitution supersedes all other practices; Amendments require documentation, approval, migration plan"；"All PRs/reviews must verify compliance; Complexity must be justified"）+ 版本/批准/修订日期行。

**specify（规格命令）的门禁与规则**：
- 输入处理：触发消息里 `__SPECKIT_COMMAND_SPECIFY__` 后的文字即为功能描述，不得要求用户重复（除非为空）；一次调用**只建一个 feature**。
- 目录机制：spec 默认放 `specs/` 下；目录名前缀按 `.specify/init-options.json` 的 `feature_numbering`（timestamp → `YYYYMMDD-HHMMSS`；sequential/缺省 → 递增三位 `NNN`）；构造 `<prefix>-<short-name>`（short-name 为 2-4 词 action-noun 格式）；解析后的路径持久化到 `.specify/feature.json` 供下游命令定位（不依赖 git 分支名约定）；spec 目录与 git 分支名相互独立；分支创建由 before_specify hook 负责，spec 目录/文件永远由本命令创建。
- 内容边界（写什么不写什么）：聚焦 **WHAT 用户需要与 WHY**；避免 HOW（无技术栈、API、代码结构）；面向业务干系人而非开发者；规格内不得内嵌 checklist（那是独立命令的事）；不适用的节整节删除（不留 "N/A"）。
- [NEEDS CLARIFICATION] 机制：只有同时满足三条件才标记——选择显著影响 feature 范围或用户体验；存在多种合理不同含义的解读；无合理默认；**上限 3 条**；优先级排序 scope > 安全/隐私 > 用户体验 > 技术细节；其余做有依据的猜测并把合理默认记入 Assumptions 节。
- 合理默认示例（原文列出、不要为此发问）：数据保留（领域行业标准）、性能目标（标准 web/移动应用预期）、错误处理（用户友好信息 + 适当 fallback）、认证方式（标准 session 或 OAuth2）、集成模式（REST/GraphQL/函数调用/CLI args 等项目适型）。
- 功能需求要求：每条 FR 必须可测试；模糊需求应栽在 "testable and unambiguous" 检查项上（think like a tester）。
- Success Criteria 四要求：可测量（含时间/百分比/数量/速率等具体指标）、技术无关（不提框架/语言/数据库/工具）、以用户为中心（用户/业务视角结果）、可验证（不知实现细节也能验证）；好例："Users can complete checkout in under 3 minutes"；坏例（实现性）："API response time is under 200ms"、"Redis cache hit rate above 80%"。
- 规格质量自校验循环：写完初稿后在 `SPECIFY_FEATURE_DIRECTORY/checklists/requirements.md` 生成规格质量 checklist（Content Quality：无实现细节/聚焦用户价值/非技术干系人可读/必填节完整；Requirement Completeness：无 NEEDS CLARIFICATION 残留/需求可测无歧义/成功标准可测且技术无关/验收场景齐备/边界已识别/范围有界/依赖与假设已识别；Feature Readiness：每条 FR 有明确验收标准/用户场景覆盖主流程/满足成功标准/无实现细节泄漏）；逐项评审，失败项（不含 NEEDS CLARIFICATION）修 spec 后重验，**最多迭代 3 轮**，仍失败则记录进 checklist notes 并警告用户。
- NEEDS CLARIFICATION 残留处理：提取全部标记→超过 3 条只留最关键的 3 条、其余做猜测；每条以固定格式提问（Context 引用规格原文、给 A/B/C/Custom 选项表、附含义列、等用户答复）；表格格式强制（管道对齐、分隔线 ≥3 短横）；全部问题一次呈现后等待；用户答复后替换标记并重跑验证。
- Done When：规格写入 SPEC_FILE 并通过质量 checklist 校验；hook 按规则分发或跳过；向用户报告 feature 目录、spec 路径与 checklist 结果。

**plan（计划命令）的门禁与规则**：
- 前置：setup 脚本解析 FEATURE_SPEC、IMPL_PLAN、FEATURE_DIR、BRANCH；读取 spec 与 `/memory/constitution.md`；加载已复制的 plan 模板。
- **Constitution Check 是 GATE**：模板原文标注 "GATE: Must pass before Phase 0 research. Re-check after Phase 1 design."——Phase 0 研究前必须通过宪法检查，Phase 1 设计完成后再查一次；宪法违规且未被论证（unjustified）则 **ERROR**（命令终止）。
- Technical Context：未知项标 "NEEDS CLARIFICATION"。
- Phase 0（Outline & Research）：从 Technical Context 提取 unknowns（每个 NEEDS CLARIFICATION→研究任务；每个依赖→最佳实践任务；每个集成→模式任务）；生成并派发研究 agent；research.md 用固定三段格式（Decision 选择 / Rationale 为何 / Alternatives considered 还评估了什么）；产出物门禁——research.md 中所有 NEEDS CLARIFICATION 必须解决。
- Phase 1（Design & Contracts，前置条件 research.md 完成）：从 feature spec 提取实体生成 data-model.md（实体名、字段、关系、来自需求的校验规则、适用的状态转换）；若项目有外部接口则定义 contracts/（按项目类型选契约格式——库的公共 API、CLI 的命令 schema、web 服务的 endpoint、解析器的文法、应用的 UI 契约；纯内部项目可跳过）；生成 quickstart.md（可运行的端到端验证场景，含前置、安装、运行命令与预期结果；引用而非复制 contracts 与 data model；**不含完整实现代码/模型/服务体/迁移/完整测试套件**——实现细节属于 tasks.md 与实现阶段）。
- 关键规则：文件系统操作用绝对路径、文档内引用用项目相对路径；gate 失败或未解决的 clarification 即 ERROR；命令在 Phase 1 设计后结束并报告分支、计划路径与生成的工件。
- **Complexity Tracking 表**（plan-template.md）：仅当 Constitution Check 存在需论证的违宪项才填；三列——Violation（违规项，例 "4th project"、"Repository pattern"）/ Why Needed（当前需要）/ Simpler Alternative Rejected Because（为何拒绝更简方案）——强制为复杂度辩护，直接对治 over-complication。

**tasks（任务命令）的门禁与规则**：
- 必读输入：plan.md（技术栈、库、结构）与 spec.md（带优先级的用户故事）为必需；data-model.md、contracts/、research.md、quickstart.md、constitution.md 为可选（IF EXISTS）；没有全部文档的项目按现有内容生成。
- **任务必须按用户故事组织**（CRITICAL 标注）：每个用户故事（P1、P2、P3...）获得自己的 phase，使实现与测试可独立；故事内映射所需 models/services/interfaces/UI/（若要求）tests；标注故事依赖（多数故事应相互独立）。
- 契约与数据模型映射：每个接口契约→所服务的用户故事（若要求测试，契约测试任务 [P] 排在该故事实现之前）；每个实体→需要它的故事（跨故事实体放最早故事或 Setup phase）；**data-model.md 中的字段约束（最大长度、可空/必填、枚举值、校验规则）必须逐字引用进任务描述**，不得留给实现时裁量。
- Checklist 格式（REQUIRED，五要素）：每条任务严格为 `- [ ] [TaskID] [P?] [Story?] Description with file path`——checkbox 开头；TaskID 顺序编号（T001...）按执行序；[P] 仅当可并行（不同文件、无未完成依赖）；[Story] 标签仅用户故事 phase 必填（[US1] 等映射 spec.md），Setup/Foundational/Polish phase 不带；描述含确切文件路径；反例明确列出（缺 ID、缺 checkbox、缺文件路径均 WRONG）。
- Phase 结构：Phase 1 Setup（项目初始化，共享基础设施）；Phase 2 Foundational（阻塞所有用户故事的先行任务，**必须先于用户故事完成**）；Phase 3+ 按优先级每故事一 phase（故事内顺序：测试（若要求）→ Models → Services → Endpoints → Integration；每个 phase 是完整、可独立测试的增量）；最终 Phase Polish & Cross-Cutting Concerns。
- 测试任务可选原则：仅当功能规格明确要求或用户要求 TDD 时才生成测试任务。
- 产物标准：tasks.md 应"立即的可执行"——每条任务具体到 LLM 无需额外上下文即可完成；含依赖节（故事完成顺序）、每故事并行执行示例、实现策略节（MVP 优先、增量交付）；完成报告须含总任务数、每故事任务数、并行机会、每故事独立测试标准、建议 MVP 范围（通常就是 User Story 1）、格式校验（确认全部任务符合 checklist 格式）。

**implement（实现命令）的门禁与规则**：
- 前置脚本：check-prerequisites.sh/ps1/py `--json --require-tasks --include-tasks`——校验先决条件，tasks.md 缺失或不完整时建议先跑 tasks 命令重新生成。
- **checklist 只读质量门**：扫描 `FEATURE_DIR/checklists/` 全部 checklist 文件，统计每份的 total/checked/unchecked 并制状态表；总状态判定——PASS=所有 checklist 零未勾选；FAIL=任一存在未勾选；**若有任何未勾选项：显示表格后 STOP 并询问用户 "Some checklists have unchecked items. Do you want to proceed with implementation anyway? (yes/no)"**，用户说 no/wait/stop 则中止执行；明确禁止 implement 修改 checklist 文件或标记。
- checklist 语义澄清：`checklists/requirements.md` 是 specify/clarify 维护的内建规格质量表；自定义 checklist 的 `[x]` 表示**评审者认定需求质量标准满足**，不表示实现工作完成。
- 上下文加载：tasks.md 与 plan.md 为 REQUIRED；data-model.md、contracts/、research.md、/memory/constitution.md、quickstart.md 为 IF EXISTS。
- 项目设置验证：按实际技术栈检测并创建/校验 ignore 文件（git 仓库→.gitignore；Dockerfile→.dockerignore；ESLint/Prettier/npm/Terraform/Helm 各有对应 ignore）；已存在则只补缺失关键模式；按技术栈给通用与工具特定模式清单（Node/Python/Java/C#/Go/Ruby/PHP/Rust/Kotlin/C++/C/Swift/R/Universal 及 Docker/ESLint/Prettier/Terraform/k8s）。
- 执行纪律：逐 phase 执行、完成一个 phase 才进下一个；尊重依赖——顺序任务按序、并行任务 [P] 可同跑；同文件任务必须串行；若要求测试则测试先于对应实现（TDD）；每 phase 完成设验证检查点。
- 错误处理规则：非并行任务失败即**中止执行**；并行任务失败可继续其余并报告失败项；每完成一个任务汇报进度并把该任务标 `[X]`；错误信息带上下文并建议下一步。
- 完成验证：核验所有必需任务完成；实现的功能与原规格比对；测试通过且覆盖达标；实现遵循技术计划。

**checklist（清单命令）的门禁与规则**：
- 核心理念（CRITICAL CONCEPT）：**"Checklists are UNIT TESTS FOR REQUIREMENTS WRITING"**——验证的是某领域内需求写作的质量、清晰度与完备性，不是验证实现（反例：不写"验证按钮点击正确"；正例：写"所有卡片类型都定义了视觉层级要求吗？""'prominent display' 是否用具体尺寸/位置量化了？"）；隐喻——"If your spec is code written in English, the checklist is its unit test suite."
- **所有权与勾选生命周期**：本命令生成的自定义 checklist 是 reviewer 拥有的需求质量评审工件；`[x]` 意为评审者认定该需求质量标准满足，绝不意味着实现完成；**生成命令本身禁止把生成的条目勾上**（leave every newly generated item unchecked）；仅当评审者明确要求时 agent 才可协助评估条目。
- 澄清问题机制：动态生成最多 **3 个**初始上下文澄清问题（无预制目录）；必须从用户措辞 + spec/plan/tasks 提取的信号生成；只问实质改变 checklist 内容的信息；用户已说清的逐条跳过；生成算法五步——提取信号（领域关键词、风险指标、干系人提示、显式交付物）→聚类为最多 4 个候选焦点→识别受众与时机→检测缺失维度（范围广度、深度/严谨、风险侧重、排除边界、可测量验收）→从六类原型选题（范围精化/风险优先级/深度校准/受众框架/边界排除/场景类缺口）；格式规则——选项表列 Option|Candidate|Why It Matters、最多 A-E 选项、不问用户已说过的、不确定就显式确认；无法交互时的默认（深度 Standard；受众代码相关取 Reviewer(PR) 否则 Author；焦点取前 2 聚类）；答复后若仍有 ≥2 类场景不清楚可追问最多 2 题（Q4/Q5，各附一行理由），**总计不超过 5 题**。
- 上下文加载策略：只加载与活跃焦点相关的必要部分；长节摘要为场景/需求 bullet；渐进披露——发现缺口才追加检索；源文档过大时生成中期摘要条目而非嵌入原文。
- 文件写入规则：在 `FEATURE_DIR/checklists/` 下按域名生成（ux.md、api.md、security.md）；**文件已存在则追加、永不删除既有内容**，条目编号从既有最大 CHK ID 续接；新建从 CHK001 起。

来源: research/raw/repos/spec-kit/templates/ 及 templates/commands/（原始 URL: https://github.com/github/spec-kit）

## ap-vibe 十维定义（ginsonko/ap-vibe）

> 材料位置：research/raw/repos/ap-vibe/src/ap_mind/project_documents.py（DIMENSIONS 常量及校验逻辑）。

- 十个维度（DIMENSIONS 元组，每维 0-100 分，null=未知/未评）：（1）intent——目标符合；（2）logic——逻辑一致；（3）completeness——功能完整；（4）reliability——可靠恢复；（5）security——安全隐私；（6）performance——性能成本；（7）maintainability——可维护性；（8）compatibility——兼容扩展；（9）usability——用户体验；（10）validation——证据验证。
- 写入契约（validate_assessment）：assessment 是列表且长度不得超过维度数；每项的 key 必须属于 DIMENSIONS 且不得重复；score 为 null 或 0-100 数值（bool 不算数值，非法即 ContractError）；**score 非 null 时必须携带非空 reason 字符串与非空 evidence_refs 字符串列表**（缺 reason 报 document_assessment_reason_required，缺证据报 document_assessment_evidence_required）——即"有分数必须给理由 + 证据引用"。
- 读侧投影（assessment_quality）：对旧文档宽容——报告精确缺口（missing/pending/scored 与 issues）而非拒绝整个项目目录；scored 要求为有限数值且在 0-100。
- 配套机制（见 notes/followups.md §2 记录）：11 章项目档案（风险章内嵌十维评估）；"资料完整 ≠ 质量满分，雷达图没填满不等于需要人工审批"（反模板填充）；章节无变化不重写；recovery 章有 do_not_repeat（下次不要重做的事）。

来源: research/raw/repos/ap-vibe/src/ap_mind/project_documents.py（原始 URL: https://github.com/ginsonko/ap-vibe）
