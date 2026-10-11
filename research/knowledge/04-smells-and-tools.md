# 04 AI 代码坏味道与治理工具 —— 知识点清单（阶段2）

> 精读范围: `research/raw/articles/code-smells-*`（16 篇）+ `research/raw/tools/`（16 篇）。
> 原则: 只罗列、不整合、不做取舍；每条坏味道定义/量化数据/机制描述/配置做法单独成条。
> 英文内容以中文转述，术语/工具名/规则名保留英文。抓取/精读日期: 2026-10-11。

---

# 第一部分 articles（16 篇）

## code-smells-gitclear-2025.md

- 数据集规模: GitClear 2025 回顾研究覆盖 2020 年 1 月至 2024 年 12 月共 2.11 亿（211M）行变更代码，来自约 72.9 万（729K）开发者的真实仓库，是"AI 助手时代代码质量"最大的纵向数据集。
- 研究的三个代码变更模式指标: code churn（"changed then reverted"，改了又回滚/删除的代码）、code movement（代码移动，作为重构的代理指标）、code duplication（代码重复，经典工程公敌）。
- 核心发现"4 倍代码克隆增长": 2024 年 5 行以上重复代码块（duplicated 5+ line blocks）相比此前增长 8 倍（文中先以 4x 描述 cloning 趋势、后给出 eight-fold increase 的精确数字），提示 AI 助手输出中"重复逻辑难以评估"是被低估的弱点。
- 里程碑式拐点: 2024 年"copy/pasted"（复制粘贴）行数历史上首次超过"moved"（移动/重构）行数——即复制粘贴成为比重构更主流的代码变更形式。
- 重构代理指标下滑: "code moved" 占变更行比例从 2021 年的 25% 跌到 2024 年底的 10% 以下，连续两年下滑。
- 复制粘贴占比上升: "copy/pasted" 代码占变更行比例从同期 8.3% 升至 12.3%。
- churn 定义与预测: code churn 定义为"新增后在 3 个月内被更新或删除"的代码；2024 年平均每个代码库有 4.1% 的行"departed"（即写后即弃），预计到 2026 年翻倍。
- "Copy/pasted 将成为新增代码的主导形式": 2025 年预计 copy/paste 相对增长 30%（从 12.3% 的基数继续上升）。
- churn 与复制粘贴的联动机制: 复制粘贴的代码后来被删除/回滚时会生成"departed" churn——重复是 churn 的上游。
- 转引 GitHub Copilot Research Recap (Part 3) 与 1300 名开发者定性反馈: 开发者自述"AI 让我快 88%"，但代码可维护性（maintainability）受损——主观提速与客观可维护性下降并存。
- 报告标题所指的 2024 主导趋势: "Refactoring at 8% of Changed Lines"（重构占变更行 8%）——重构占比萎缩是 2024 年的支配性趋势（该节正文未完整抓取，标题保留）。
- 材料完整性说明: 原站有 Cloudflare 防护、PDF 直链失效，以上为经 web_reader 抓取的连续原句节选；完整报告需从 GitClear 官网获取 PDF。

来源: research/raw/articles/code-smells-gitclear-2025.md（原始 URL: https://www.gitclear.com/ai_assistant_code_quality_2025_research）

## code-smells-so-survey-2025.md

- 调查规模: Stack Overflow 2025 开发者调查 AI 章节，各题有效回应约 3.3 万人（如 33,662/68.7%），其中职业开发者约 2.6 万人。
- AI 采用率: 84% 受访者正在使用或计划在开发流程中使用 AI 工具，高于去年的 76%；51% 的职业开发者每天使用 AI 工具。
- 情绪逆转: 对 AI 工具的正面评价从 2023、2024 年的 70%+ 降至 2025 年的 60%；职业开发者好感度 61% 高于学习者的 53%。
- 准确性信任缺口: 46% 的开发者"主动不信任"AI 工具输出的准确性，多于信任的 33%；只有 3% 表示"高度信任"。
- 经验越深越不信任: 资深开发者（10 年+）最谨慎——"高度信任"率最低（2.6%）、"高度不信任"率最高（20%），说明担责岗位普遍需要人工验证。
- 复杂任务能力: 2024 年 35% 的职业开发者认为 AI 工具难以处理复杂任务，2025 年降至 29%，且各经验层级看法一致；理由是"复杂任务风险太高，不值得花额外时间验证 AI 的有效性"。
- 抵抗使用 AI 的高责任系统性任务: 部署与监控（76% 不打算用 AI）、项目规划（69% 不打算用）。
- 最大挫败感: 66% 的开发者最头疼"AI 的解决方案几乎对、但差一点"（almost right, but not quite）。
- 第二大挫败感: 45% 认为"调试 AI 生成的代码更耗时"——"几乎对"直接导致调试负担。
- 人类角色定位: 在 AI 能做大部分编码任务的未来，开发者仍会向人求助的第一理由是"当我不信任 AI 的答案"（75%）——人类是质量与正确性的最终仲裁者。
- vibe coding 渗透率: 72% 的受访者不做 vibe coding，另有 5% 强调"绝不做"（合计约 77% 排斥）；该调查对 vibe coding 的定义采用 Wikipedia 版本"从 LLM 提示生成软件的过程"。
- AI agent 尚未主流: 52% 的开发者不使用 agent 或只用更简单的 AI 工具；38% 没有采用 agent 的计划。
- agent 生产力感知: 52% 的开发者认同 AI 工具/AI agent 对生产力有正面影响。
- agent 使用场景: 在工作中使用 agent 的软件开发者中 84% 用于软件开发本身；工作之外 agent 主要用于语言处理任务（49%）。
- agent 影响不对称: 约 70% 的 agent 用户认同 agent 减少了特定开发任务耗时、69% 认同提升了生产力；但只有 17% 认同改善了团队内部协作——是各项影响中最低的，即收益是个人效率而非团队层面。
- 对 agent 的担忧: 87% 的受访者担忧准确性，81% 担忧数据安全与隐私。
- agent 数据存储工具: 传统工具被复用为 agent 记忆/数据管理——Redis 43%、ChromaDB 20%、pgvector 18%。
- agent 编排工具: 开源主导——Ollama 51%、LangChain 33% 最常用。
- agent 可观测性: 开发者沿用传统监控工具而非 AI 原生方案——Grafana+Prometheus 43%、Sentry 32%。
- 开箱即用 agent 工具: ChatGPT（82%）与 GitHub Copilot（68%）是市场领导者，是多数开发者使用 AI 辅助的主要入口。

来源: research/raw/articles/code-smells-so-survey-2025.md（原始 URL: https://survey.stackoverflow.co/2025/ai）

## code-smells-dora-2024-2025.md

- DORA 2024 关键发现（AI 的收益与代价）: AI 采用显著提升个人生产力、心流（flow）与工作满意度，但同时对软件交付的稳定性（stability）和吞吐（throughput）产生负面影响——提醒团队小批量（small batch sizes）与健壮测试等基本功仍然关键。
- DORA 2024: 以用户为中心是绩效的终极驱动——优先终端用户体验的组织构建更高质量产品；持用户中心心态的开发者更高效、更满意、更不易倦怠。
- DORA 2024: 组织优先级不稳定会显著降低生产力、大幅增加倦怠，且这种负面影响极难缓解——即使有强领导力和高质量文档也依然存在。
- DORA 2024: 平台工程提升个人生产力、团队绩效与组织绩效，但可能导致变更稳定性与吞吐下降——需要围绕"开发者独立性"谨慎实施。
- DORA 2024: 变革型领导力（激励、智力刺激、支持团队）显著提升员工生产力、组织绩效与工作满意度，同时降低倦怠。
- DORA 2024: 云基础设施灵活性直接提升组织绩效；反之只为"上云"而不采用云固有的灵活性，比留在传统数据中心更有害。
- DORA 2025 核心定性: AI 的主要角色是"放大器"（amplifier），放大组织既有的优势与劣势——AI 投资的最大回报不来自工具本身，而来自对底层组织系统的战略性关注。
- DORA 2025 配套产物: DORA AI Capabilities Model（AI 能力模型）作为报告伴随指南，指导组织改进 AI 辅助软件开发的实践。

来源: research/raw/articles/code-smells-dora-2024-2025.md（原始 URL: https://dora.dev/research/2024/dora-report/ ; https://dora.dev/research/2025/dora-report/）

## code-smells-qodo-2025.md

- 调查规模: Qodo《State of AI Code Quality 2025》，609 名开发者，覆盖不同公司规模与地区。
- 三大主题之一"上下文是信任的基础": 65% 用 AI 做重构的开发者、约 60% 用 AI 做测试/编写/评审的开发者说助手"错过相关上下文"（misses relevant context）。
- 认为AI降低质量的人中 44% 归因于上下文缺失；即便在认为 AI 提升质量的"质量冠军"中也有 53% 仍想要上下文改进。
- 头号改进诉求: "改进的上下文理解"占全部投票的 26%（第一大），加上"定制团队标准"（4%）后上下文类诉求合计约 30%——高于"减少幻觉"（24%）、"更好的输出质量"（15%）、"更好处理复杂系统"（14%）。
- 推论（Qodo 观点）: 学习型、仓库级上下文引擎不是可选项，而是 SDLC 全流程准确性、质量与信任的基础。
- 主题二"信心决定采用": 幻觉率低于 20% 的开发者，合并 AI 代码而不审查的可能性是 2.5 倍（24% vs 9%）。
- 高信心工程师说 AI 让工作更愉快的可能性高 1.3 倍（46% vs 35%）。
- "信心飞轮"（Confidence Flywheel）五步模型: ①上下文丰富的建议降低幻觉 → ②准确代码通过质量检查 → ③开发者信任所见、更快交付 → ④每次合并为模型回馈更好样本 → ⑤循环随时间自我强化。
- 主题三"生产力和质量齐升——前提是评审自动化": 报告"可观"生产力提升的团队中 70% 同时报告代码质量更好——是停滞团队（16-22%）的 3.5 倍。
- 有 AI 评审在环时质量改善率达 81%（同等提速但没有 AI 评审的团队为 55%）。
- 即便交付速度没有提升，使用 AI 评审的团队质量收益也翻倍（36% vs 17%）。
- 声称"10 倍提速"的团队: 有 AI 评审的 69% 报告质量改善，无评审的仅 34%。
- 采用面数据: 82% 开发者每天或每周使用 AI 编码工具；59% 常规使用 3 个以上 AI 工具；20% 管理 5 个以上。
- 工具碎片化的代价: 同时使用 6 个以上 AI 工具的开发团队只有 28% 对 AI 代码有把握（缺信心）；这类团队仍有 38% 的时间感觉"上下文失明"。
- 采用强度按公司规模: 51% 的活跃 AI 用户在 10 人以下开发者的公司；100+ 工程师的企业中也有 25% 已越过实验阶段。
- 行业分布: 采用集中于科技/软件（56% 受访者），金融 9%，需求跨行业存在。
- AI 触及真实代码: 65% 开发者称每次提交至少四分之一由 AI 生成或塑形；15% 称超过 80% 的代码已受 AI 影响——"AI 触碰"代码正在接近与传统开发平起平坐。
- 质量净感知: 59% 说 AI 提升了代码质量，21% 说下降；78% 报告生产力收益（其中 17% 声称"10 倍"产出提升）；57% 说 AI 让工作更愉快、减轻压力。
- 幻觉量化: 25% 的开发者估计每 5 条 AI 生成建议中就有 1 条包含事实错误或误导性代码（即 20% 幻觉率量级）；对部分人是可接受的麻烦，对生产环境/安全代码库是硬停机项。
- 幻觉-信心四象限分布: "低幻觉+高信心"仅 3.8%（理想态的极少数）；"低幻觉+低信心"11.8%（即使输出准确，四分之三的低幻觉用户仍不完全信任）；"高幻觉+高信心"8.0%（可能因全程人工审查或只用于低风险区）；"高幻觉+低信心"76.4%（红区，主导群体）。
- 红区（76%）行为后果: 手动评审或重写大多数建议、即使 AI 代码看起来正确也延迟合并、避免在工作流中深度集成 AI——信任缺失侵蚀 AI 承诺的生产力收益与 ROI。
- 低幻觉仍不足够的原因: 开发者要的代码还须"匹配项目上下文与架构、对齐风格与惯例、配套自动化检查与覆盖率"——否则"正确"的建议也显得有风险。
- 测试信心差距: 不用 AI 写测试的开发者中只有 27% 对测试安全网"很有/比较有信心"；用 AI 写测试的这一数字跳到 61%——采用者信心翻倍以上（34 个百分点差距）。
- 但 AI 测试采用仍是例外而非常态，早期"与上下文脱节的通用测试生成"体验拖累了采用。
- Qodo 产品侧数据: 高严重度问题（评分 9-10）出现在 17% 的 PR 中；启用 AI 评审工具后 80% 的 PR 没有任何人类评论或评审；生成测试时若提供测试示例文件，测试采用率提升 15%；agentic chat 平均每条用户消息调用 2.5 个 MCP 工具、其中 60% 的工具使用用于上下文识别与内容检索；8% 的代码评审建议聚焦于让 PR 对齐公司既有最佳实践。
- 上下文缺失按任务分布: 重构 65%（最高）、样板代码生成 64%、编写/测试等核心任务 60%、代码评审与解释约 58%——越是依赖理解更大范围代码库的任务，AI 越容易脱靶。
- 按资历的上下文痛点: 初级 41% → 高级 52%，上下文痛点随经验增长；资深工程师质量收益最大（60%）但交付 AI 代码的信心最低（22%）。
- 手动选上下文已失效: 手动为每个提示选文件/函数/文件夹的开发者中 54% 说 AI 仍错过相关性；工具自主选择上下文时降到 33%；上下文跨会话持久存储与复用时降到 16%——上下文越自动化、越持久，AI 越有用可信。
- 风格不一致的信任代价: 收到不一致输出的开发者把"代码不符合团队标准"列为头号挫败感的可能性高 1.5 倍；很少/偶尔看到风格对齐建议的开发者中近五分之二视其为主要阻碍——每次 AI 协助都变成"修一遍"的任务，拖慢节奏、破坏心流、侵蚀信心。
- 满意度双引擎: 生产力提升 + 对 AI 代码的信心。两者兼备的工作满意度最高（61%）；只有生产力时 58%；生产力没提升时，信心成为摆动因子——高信心者正面满意度 25% vs 低信心者 14%（近 2 倍差）。

来源: research/raw/articles/code-smells-qodo-2025.md（原始 URL: https://www.qodo.ai/reports/state-of-ai-code-quality/）

## code-smells-arxiv-causal-smells.md

- 论文: 《A Causal Perspective on Measuring, Explaining and Mitigating Smells in LLM-Generated Code》（arXiv 2511.15817，2025-11-19，Velasco 等 6 人）。
- 问题定义: LLM 常复制糟糕编码实践，引入 code smells（妨碍可读性、可维护性或设计完整性的模式）；既有研究只做检测或修复，缺乏"这些味道如何、何时在生成代码中出现"的理解。
- 核心度量: Propensity Smelly Score（PSC，味道倾向分数）——估计生成特定味道类型的可能性的概率指标；论文确立其作为结构质量信号的稳健性。
- 方法创新: 把 PSC 用作因果分析工具（instrument），识别生成策略、模型大小、模型架构、提示词表述（prompt formulation）如何塑造生成代码的结构属性。
- 关键发现: 提示词设计与架构选择对味道倾向起决定性作用，并由此导出能减少味道发生率的实用缓解策略。
- 用户研究: PSC 帮助开发者解读模型行为、评估代码质量——味道倾向信号可以支撑人类判断。
- 定位: 为"质量感知评估"纳入 LLM 代码评测与部署奠定基础。

来源: research/raw/articles/code-smells-arxiv-causal-smells.md（原始 URL: http://arxiv.org/abs/2511.15817）

## code-smells-arxiv-llm-smells-taxonomy.md

- 论文: 《LLM Code Smells: A Taxonomy and Detection Approach》（arXiv 2605.22976，2026-05-21，Chenail-Larcher 等 5 人）。
- 概念区分: 该系列的 "LLM code smells" 指"在源代码中集成 LLM 推理"（LLM inference integration）的糟糕编码实践——即调用 LLM 的应用代码的坏味道，不是"LLM 生成的代码"的坏味道；糟糕的 LLM 集成会损害软件系统质量。
- 产出: 自包含的分类法（taxonomy）与 9 条 LLM code smells 目录（consolidates and refines 前期工作）。
- 检测工具: SpecDetect4LLM——针对这组味道的静态源码分析工具。
- 实证规模与结果: 对 692 个开源软件项目（171,194 个源文件）评估——LLM code smells 影响 73.5% 的被分析系统；检测精度（precision）91.3%、召回率（recall）71.8%。

来源: research/raw/articles/code-smells-arxiv-llm-smells-taxonomy.md（原始 URL: http://arxiv.org/abs/2605.22976）

## code-smells-arxiv-specdetect.md

- 论文: 《Specification and Detection of LLM Code Smells》（arXiv 2512.18020，2025-12-19，Mahmoudi 等 5 人）——上述 2605.22976 的前期工作。
- 形式化: 引入 LLM code smells 概念，基于相关文献形式化定义 5 条与软件系统中 LLM 推理相关的反复出现问题实践（无既有形式目录）。
- 工具: 扩展 SpecDetect4AI 以覆盖新定义的 LLM code smells。
- 实证: 在 200 个开源 LLM 系统数据集上验证——LLM code smells 影响 60.50% 的被分析系统，检测精度 86.06%。

来源: research/raw/articles/code-smells-arxiv-specdetect.md（原始 URL: http://arxiv.org/abs/2512.18020）

## code-smells-arxiv-package-hallucination.md

- 论文: 《We Have a Package for You! — Comprehensive Analysis of Package Hallucinations in Code Generated by LLMs》（arXiv 2406.10279，USENIX Security 2025，Spracklen 等 6 人）。
- 威胁定义: package hallucination（包幻觉）——Python/JavaScript 依赖集中式包仓库 + 代码生成 LLM 的组合催生的新型软件供应链威胁；幻觉源于生成代码时的"事实冲突型错误"（fact-conflicting errors），构成新型"包混淆攻击"（package confusion attack）。
- 实验规模: 16 个流行 LLM + 2 个独立提示数据集，两种语言共生成 576,000 个代码样本用于幻觉分析。
- 幻觉率量化: 商业模型平均幻觉包占比至少 5.2%，开源模型 21.7%；共产生 205,474 个不重复的幻觉包名——凸显威胁的严重性与普遍性。
- 根因分析方向: 探索不同模型与配置如何影响生成错误包推荐的概率，并识别现象的根源成因。
- 缓解: 实现多种幻觉缓解策略，可显著减少包幻觉同时维持代码质量。
- 结论定性: 包幻觉是使用 SOTA LLM 生成代码时的持续、系统性现象，需要研究社区紧迫关注。
- 后续研究（arXiv 2608.23897, 2026-08）《Names Can Hurt: Spotting Slopsquatting Risks》: 当 LLM 编造不存在的 Python 包名，攻击者抢先在 PyPI 注册该名字（"slopsquatting"）即把幻觉变成供应链投毒；提出两层检测器——确定性 PyPI 存在性检查 + 基于 10 个特征的随机森林分类器。

来源: research/raw/articles/code-smells-arxiv-package-hallucination.md（原始 URL: http://arxiv.org/abs/2406.10279 ，USENIX Security 2025）

## code-smells-vibecheck-rules.md（40 条规则逐条罗列）

- 工具定位: vibecheck 自称 "ESLint for AI slop"，40 条捕获 AI 生成代码坏味道的规则；零配置、零 API key、零成本、本地运行（npx 直接跑或独立二进制，Bun 构建，macOS/Linux 多架构）。
- 立项依据（转引数据）: CodeRabbit 发现 AI 生成 PR 的问题数是人工 PR 的 1.7 倍；Veracode 报告 45% 的 AI 代码样本含安全漏洞。
- 实现机制: 纯正则模式匹配扫描 JS/TS/Python，无 AST 解析、无外部 API、无 AI；每条规则有检测模式与降低误报的反模式（anti-pattern）；默认跳过 node_modules/dist/build/__pycache__/.venv/锁文件/压缩代码。

### Security 类（6 条）
- 规则 1 `no-hardcoded-secrets`（error）: 源码中的 API key、token、密码等硬编码秘密。
- 规则 2 `no-eval`（error）: `eval()` 与 `new Function()` 调用。
- 规则 3 `no-sql-concat`（warn）: 用字符串拼接构造 SQL 查询。
- 规则 4 `no-innerhtml`（warn）: 使用 `innerHTML` 与 `dangerouslySetInnerHTML`。
- 规则 5 `no-py-eval`（error）: Python 的 `eval()`、`exec()`、`os.system()`、`subprocess(shell=True)`。
- 规则 6 `no-py-sql-concat`（warn）: 用 f-string 或 `.format()` 拼接 SQL 查询。

### Error Handling 类（7 条）
- 规则 7 `no-empty-catch`（error）: 空 catch 块静默吞掉错误。
- 规则 8 `no-console-error-only`（warn）: catch 块只 `console.error` 而不 rethrow。
- 规则 9 `no-swallowed-promise`（warn）: `.then()` 链没有 `.catch()`。
- 规则 10 `no-vague-error`（warn）: `throw new Error("Something went wrong")` 式含糊报错与含糊的 `Promise.reject`。
- 规则 11 `no-bare-except`（error）: `except:` 不指定异常类型。
- 规则 12 `no-pass-except`（error）: `except: pass` 静默吞错。
- 规则 13 `no-py-log-swallow`（info）: `except X:` 处理器只打日志就继续——标注为"更像 AI 痕迹而非 bug：多数是故意的"。

### Code Quality 类（9 条）
- 规则 14 `no-console-pollution`（warn）: `console.log`/`debug`/`info` 遗留在生产代码。
- 规则 15 `no-ai-todo`（info）: AI 生成的占位 TODO（`TODO: implement`、`FIXME: add`）。
- 规则 16 `no-god-function`（warn）: 超过 80 行的函数。
- 规则 17 `no-deep-nesting`（warn）: 嵌套 4 层以上而不改用早返回（early returns）。
- 规则 18 `no-double-assertion`（warn）: `as unknown as T` 式链式断言绕过 TypeScript 安全。
- 规则 19 `no-ai-attribution`（warn，可 --fix）: `// Generated by ChatGPT` 式 AI 署名注释（可用 --fix 自动删除）。
- 规则 20 `no-star-import`（warn）: `from module import *` 命名空间污染。
- 规则 21 `no-mutable-default`（warn）: 可变默认参数（`def foo(bar=[])`）。
- 规则 22 `no-py-print`（warn）: `print()` 遗留在生产代码。

### AI-Specific Tells 类（14 条）
- 规则 23 `no-obvious-comments`（info）: 复述代码的注释（`// initialize the counter`）。
- 规则 24 `no-ts-any`（warn）: TypeScript `any` 类型与 `as any` 断言。
- 规则 25 `no-hedging-comments`（info）: 不确定的犹疑注释（`// should work`、`// might not be the best approach`）。
- 规则 26 `no-step-comments`（info）: 编号步骤注释（`// Step 1: Initialize`）。
- 规则 27 `no-section-dividers`（info）: ASCII 分割线注释（`// ========`）。
- 规则 28 `no-narrator-comments`（info）: 旁白式注释（`// This function handles...`）。
- 规则 29 `no-stub-function`（warn）: 脚手架桩代码进了生产（`throw "not implemented"`）。
- 规则 30 `no-hallucinated-import-js`（warn）: import 了 npm 上不存在的包（AI 幻觉）。
- 规则 31 `no-hallucinated-import-py`（warn）: import 了 PyPI 上不存在的包（AI 幻觉）。
- 规则 32 `no-py-obvious-comments`（info）: Python 版复述代码注释（`# initialize the counter`）。
- 规则 33 `no-py-stub-function`（warn）: 抛 `NotImplementedError` 的无函数体桩函数。
- 规则 34 `no-py-hedging-comments`（info）: Python 版犹疑注释（`# should work`、`# might not be ideal`）。
- 规则 35 `no-type-ignore-blanket`（warn）: 不带具体错误码的一揽子 `# type: ignore`。
- 规则 36 `no-unused-protocol`（info）: 定义了却从未被引用的 `Protocol` 类（AI 幽灵脚手架）。

### Framework 类（4 条）
- 规则 37 `no-express-unhandled`（warn）: async Express 路由缺少错误处理。
- 规则 38 `no-error-info-leak`（error）: 错误内部信息（`err.message`、`err.stack`）泄漏到 HTTP 响应。
- 规则 39 `no-flask-debug`（warn）: 生产环境 Flask `app.run(debug=True)`。
- 规则 40 `no-with-router`（warn）: 使用 react-router v6 起已废弃的 `withRouter` HOC。

### slop score（评分机制）
- slop score 设计: 单一数字衡量代码库携带多少"AI 残留"，按类别拆分（code-quality/security/error-handling 各自的每 KLOC 加权发现数）——"没有分类的分数是虚荣指标"。
- 计分方法: 每 KLOC、按严重度加权（error=10 分、warn=3 分、info=1 分）、单规则每 KLOC 贡献上限 20 分——因为 31 仓库扫描中 `no-deep-nesting` 一条规则产生 46% 的发现，不设上限分数就只是在测嵌套深度却声称在测 slop；触顶时输出会点名该规则。
- 分级（Grade）锚定在真实语料四分位数而非学校打分: A=70+（比语料中所有仓库干净）、B=55-69（好于上四分位）、C=40-54（四分位距内=典型）、D=25-39（低于语料）、F=<25（远低于）；中位仓库恰好=50。第一版用"90=A"学校量表，把 6 个校准仓库中的 5 个判为 F、最干净的判 D——锚定方式错误。
- 校准的可复现性: 曲线为 `100 * exp(-density * ln2 / D50)`，D50=校准语料的发现密度中位数（当前 D50=30，取 6 个仓库 adk-python/codex/App/brandmd/gemini-cli/gitea 在 ruleset 1.15.0 上 2026-08-04 测得）；完整清单随包发布（src/calibration.json），可用 `scripts/calibrate.ts <dir-of-repos> --write` 自行重推导——"手挑常数会让每个已发布分数不可证伪"，可复现性是重点。
- 分数描述代码库而非你的视图: 无论 `--severity` 显示什么、是否 baseline，全部发现都计入——写 baseline 曾把分数直接送满 100 而代码未变，故被改为"baseline 是推迟 slop 的决定而非移除"；`--min-score` 门禁配 `--fail-on` 使用。

### diff 模式语义
- diff 模式报告条件: 发现所锚定的行变了，**或你的改动引入了它**——变更前的文件状态也会被扫描，因此你改了 catch 里唯一一行 console.error，报告会落在 catch 头上；也覆盖"函数因你的追加越过长度阈值（声明行没变）"与"build 时守卫被从 console.log 上方移除"。
- 故意不复活旧债: 编辑一个本就超长函数内的一行保持安静——那笔债不是你的。
- `--staged` 读 index 而非工作区（已 stage 又编辑的文件按将提交的样子检查）；`--diff-stdin` 用 diff 中 index 头的 blob hash 校验管道里的 diff 确实描述被扫描的文件，不匹配则拒绝报告。
- 扫不了的文件绝不报 clean: 读不了的文件、超 1MB 上限的文件、二进制/符号链接/submodule 的 staged blob 会 exit 2 并点名路径；要跳过的文件应放 ignore（保持沉默）。
- diff 模式已知限制（均需非默认 git 配置）: .gitattributes clean filter 使 --diff 行号偏移（--staged 不受影响）；来自其他仓库且 index hash 短于 7 字符的 diff 无法校验（未校验扫描）；显式点名 staged 符号链接会扫描其指向物（目录扫描则拒绝）；"先改后删同一文件"的流不会被拒；纯删除不可见（只有新增行进 diff map，删掉产生发现的行不报告）；低于 rename 相似度阈值的 staged 移动表现为 add+delete（目标被当新文件）；同文件已有相同发现又新增一个时无法区分，回退到变更行匹配、新的可能漏报（baseline 同理可能藏住它）。
- diff 模式禁用评分: `--score`/`--min-score`/`--badge` 拒绝与 --diff/--staged/--diff-stdin 并用——diff 模式只扫变更行，除以 1 KLOC 会伪装成全库分数且更讨好（一个加 eval() 的提交 diff 模式得 69/B，同仓库全扫 46/C）；PR 门禁用 --fail-on 与 --max-warnings（为变更行设计），全库门禁用 --min-score。

### 门禁、退出码与自动修复
- 构建门禁: `--min-score 60` 低于阈值 exit 1，与 --fail-on/--max-warnings 并存——后者抓具体发现，前者抓全库漂移。
- badge: `--badge slop.svg` 生成自包含 shields 风格 SVG（不渲染外部图像、不调用外部服务——不向任何人报告你的 CI、也不会因他人服务器宕机而坏），与 --score/--min-score 同源计算，永不与门禁矛盾。
- 退出码语义: 0=干净或无达到 --fail-on 级别的发现；1=有达到 --fail-on 的发现或超过 --max-warnings；2=用法或运行时错误（非法旗标、坏路径）。`--fail-on never` 成功扫描恒 0。
- 计数规则: --fail-on 与 --max-warnings 只计被报告的发现（被 --severity 隐藏的不会让运行失败）；有 baseline 时只计新发现。
- 自动修复: `--fix` 当前只机械安全地移除 `no-ai-attribution`——删除 `// Generated by ChatGPT`、`// Co-Authored-By: Claude` 这类整行注释，绝不碰代码行；仅当行内容仍与扫描所见一致时才删，修后重扫保持行号准确。

### 配置、抑制与 baseline
- 配置文件 .vibecheckrc: JSON 的 rules（规则→off/warn/error/info）与 ignore（glob 列表）；所有规则默认按推荐严重度开启。
- 一次性规则选择: `--rule 'rule-id: error|warn|info|off'` 可重复；`--no-defaults` 全关后 opt-in 子集（eslint 式白名单模型）；未知规则 id 或级别是用法错误（exit 2）带提示；info 级仍受 --severity 地板约束。
- 行内抑制: `// vibecheck-disable-next-line [rule ids]`、`// vibecheck-disable-line`、文件级 `// vibecheck-disable`；裸指令抑制目标上所有规则，逗号分隔规则 id 可限定范围；`-- reason` 后缀记录理由；旧 undocumented `vibecheck-ignore` 仍作为 disable-line 别名工作。
- 抑制的解析安全: 指令用感知字符串的 lexer 解析——字符串字面量/模板字面量/正则字面量里的指令文本不会误抑制；指令必须是注释的第一个 token；抑制在扫描器内实现，CLI/GitHub Action/MCP server/VS Code 扩展全部生效。
- JSX 中的特殊形式: .tsx/.jsx 必须用表达式注释 `{/* vibecheck-disable-next-line no-eval */}`——裸 // 与 /* */ 指令被忽略，否则渲染出的元素文本可伪造指令；文件级 disable 在文件第一个 `<` 之前仍有效。
- 抑制不可静默滥用: 摘要报告抑制数量，`--show-suppressed` 列出（JSON 输出含 suppressedCount 与完整列表）。
- baseline 机制: `--update-baseline` 把当前发现写入 .vibecheck-baseline.json（建议提交），此后 exit code/--fail-on/--max-warnings 只计新发现，摘要显示"N findings (M baselined, K new)"。
- baseline 指纹: `sha1(rule|path|trimmed snippet)` 不含行号——baselined 发现可在文件内移动后存活；编辑被标记行会改变指纹、作为新发现回归（刻意改动后需重跑 --update-baseline）；全严重度都记录故与 --severity 无关；须从 baseline 时的同一目录运行（指纹用扫描根相对路径）。

### 生态集成
- VS Code 扩展: 行内诊断（squigglies）、Problems 面板、状态栏计数、保存时运行；兼容 VS Code/Cursor/Windsurf。
- GitHub Action: 自动只扫 PR 变更文件（push 事件扫全仓）；可输出 SARIF 进 Security tab（与 CodeQL 并列，稳定指纹跨 commit 追踪 alert；fail-on 失败时也上传保持 Security tab 新鲜）；不用 Action 时 `--format gh` 输出 GitHub Actions workflow commands 做 PR 行内标注，或 `--format sarif` 自行上传。
- pre-commit 集成: 官方 .pre-commit-config.yaml 配方；或直接在 .git/hooks/pre-commit 里 `npx vibecheck --staged .`（配 husky）。
- MCP server: `vibecheck --mcp`（stdio），3 个工具——scan-files（扫文件/目录）、scan-diff（扫 git diff）、get-rules（列规则）；配到 Claude Code/Cursor/Windsurf 让 agent 自动扫 slop。
- 与 ESLint 的差异定位: ESLint 抓语法与风格，vibecheck 抓"AI 生成代码中特别常见"的模式；对比表——AI 专属规则 40 vs ESLint 0 vs sloppylint 100+；犹疑注释/幻觉 import/桩检测 vibecheck 与 sloppylint 有、ESLint 无；步骤注释/分割线/GitHub Action/MCP/零配置为 vibecheck 独有；语言 JS/TS/Python。

### 真实世界扫描结果
- 31 个仓库扫描（用 Cursor、Bolt、Lovable、Replit、v0 构建）: 3,597 个文件共 14,695 个问题；46% 的发现是深嵌套（deep nesting）；Cursor 构建的仓库平均每文件 6.36 个问题（最高）；结论"每个工具留下不同的指纹"。

来源: research/raw/articles/code-smells-vibecheck-rules.md（原始 URL: https://github.com/yuvrajangadsingh/vibecheck ，README）

## code-smells-willison-slop.md

- "slop" 术语起源: Simon Willison 2024-05-08 引 @deepfates 推文——正如 "spam" 成为垃圾邮件的术语，"slop" 正成为"不受欢迎的 AI 生成内容"的术语（term of art）。
- Willison 的定义边界: 不是所有 AI 生成内容都是 slop——判定条件是"mindlessly generated and thrust upon someone who didn't ask for it"（不经思考地生成并强塞给没有索要的人）。
- slop 的典型案例: 微软 AI 生成旅游指南把 Ottawa Food Bank 列入"不容错过的景点"。
- 礼仪与伦理立场: 把 AI 生成且未经审阅的内容分享给他人是失礼的（rude）；"不发布 slop"是 Willison 个人 AI 伦理的有用底线——他愿意把名字与信誉押在他发布的东西上。
- 术语派生: AI 生成的 spam 的对应子集被 Joseph Thacker 提问后，Willison 提议命名为 "slom"。

来源: research/raw/articles/code-smells-willison-slop.md（原始 URL: https://simonwillison.net/2024/May/8/slop/）

## code-smells-yegge-junior.md

- 文章: 《Revenge of the Junior Developer》Steve Yegge，2025-03-22，Sourcegraph 博客。
- vibe coding 的操作性定义（Yegge 版）: vibe coding 就是"让 AI 干活"（you didn't write it by hand）；对生产代码要盯紧、对原型可以放任——关注程度只取决于问题本身；它不是一种 modality（交互形态），因为 chat/agents/clusters 任何非手工形态下都可以"vibe"。
- 六波编程形态模型（Figure 1）: 传统（2022）→ 补全式 completions（2023）→ chat 式（2024）→ coding agents（2025 H1）→ agent clusters（2025 H2）→ agent fleets（2026）；两波手工形态在衰落，自 chat 起每波指数上升且增速快于前浪；vibe coding 是横跨各波的虚线。
- 各浪生产力倍率: 从 chat 起，每一波保守估计是前一波的 5 倍生产力（chat 是手工的 5x、agents 是 chat 的 5x……）；若不被更新的形态压平、给足成熟时间可到 10x。
- "agent clusters"定义: 开发者并行运行并有效管理多个 coding agents（甚至超过本机容量）。
- "agent fleets"定义（Figure 2 FY26 Org Chart）: 每个 IC 开发者像二级经理，管理 AI "manager agents"，后者监督成组的 coding agents——一个开发者之下可能一组做 bug 积压梳理、一组做新业务特性、一组做长期架构迁移；预计 2026 年初到来，因为"我们已经很擅长并行化工作"。
- 补全已死论: 还在用 CAR（Completion Acceptance Rate）衡量 AI 的团队坐在恐龙曲线上，2027 年左右滑入过时；code completions 是 "dead man walking"。
- chat 的过渡地位: chat 式编程（Copilot/Cursor/Sourcegraph/Windsurf 的 IDE 聊天）仍在上行但将被 agents 迅速反超；到 Q3 chat coding 会沦为"付不起 agent 超快方式时的最后手段"。
- agent 工作方式: 像 vibe coding 聊天但免去双向复制粘贴的苦役；agent 只在完成、卡住或烧完钱时回来找你；人类在 90-99% 的工作中不再是瓶颈。
- agent 的任务粒度纪律: agent 目前只能做中小任务；"任务图分解"（task graph decomposition）技能比 chat 时代更重要——给太大的任务（如"修完我所有 JIRA ticket"）它会上蹿下跳而一事无成；"be nice to your goose, don't overstuff it"。
- agent 行为画像: "能解决大问题、也能制造更大的烂摊子，像一个飞得有点瞎、总是有点赶的超自然快的人类开发者"；agent 会为自己写一次性程序（throwaway programs）来完成任务（如取 JIRA ticket 字段）。
- 成本量化: coding agents 烧 token 到 $10-12/小时（当下费率）；经验法则——一个 agent 实例全财年摊销约等于多雇一名初级开发者（前提是有人或 AI 让它一天忙 8-10 小时）。
- 预算建议: $25/dev/天只够三小时"骑骆驼"；应预算 $80-100/dev/天 LLM 支出，每个开发者轻松翻倍产出（同时保姆两个 agent）。
- clusters 时代的成本: 5 个并行 agent = $50/小时 ≈ $100k/年——用约 $50k/年 的额外摊销成本换取 ~5x 生产力（到 2025 Q4 含爬坡）；2026 预算里几乎肯定没这笔钱，公司将分为"有预算/没预算"两阵营；软件开发成为 pay-to-play 的子弹列车。
- clusters 推动开发上云: 本机跑不动几十上百个 agent——开发者工作负载"几乎一夜之间"迁到云端（云 IDE 数十年未成，这次会成）；还需要更多云预算。
- fleets 时代花费: 开发者每天花数千美元；即使推理成本暴跌，Jevons 悖论使用量上升抵消降价（"去看看你的 bug backlog，它基本是无限的"）。
- 裁员逻辑: 找不到钱又要保持竞争力就只能砍预算——只有一个部门适合砍（暗示非 AI 采用者的部门）；junior 更便宜且采用 AI 更快，公司留谁显而易见。
- junior vs senior 采用差异: junior（新毕业/在校/考虑返校）普遍火速拥抱 AI（把 O'Reilly AI Engineering 当岗位培训）；senior 大多挣扎——很多从未碰过 LLM，甚至有资深开发者用带彩色图表的 PDF 论证"全组应放弃 AI 回到常规编码"。
- senior 抵抗的心理机制: Yegge 借编程语言之争的经验——senior 把"被迫真的重学新东西"等同于失业、破产、死在医院台阶上；AI 拒绝者对现状有大量既得投入并误当工作保障。
- 核心口号: "It's not AI's job to prove it's better than you. It's your job to get better using AI."（不是 AI 的任务证明它比你强，而是你的任务用 AI 变得更强）。
- 就业展望: 会有大量工作，只是不再手工写码；当前招聘冻结只是公司"还不知道该做什么"的信号；参照蒸汽/电力/计算的历史，将出现远多于今天的软件开发者，生产力浪潮可提升国家 GDP 100% 以上。
- 对 agent 的工程比喻: coding agent 像隧道掘进机（power shovels 之后）——很强但贵、会严重卡住、需要全程引导，也不会一天挖穿英吉利海峡，不要设定不切实际的期望。
- 反拖延忠告: "6 个月后更快所以推迟 6 个月"等于"等交通高峰过去再出门"——路是短了，但你会最后一个到。
- 行动建议: 转 chat、弃补全、停止手写代码、学习新世界的 validation 与 verification、盯紧 coding agents；年底前"软件工程师"的新工作内容=很少直接写码、大量"带娃式"agent 管理（agent babysitting）；不确定怎么做就去问 junior developer。

来源: research/raw/articles/code-smells-yegge-junior.md（原始 URL: https://sourcegraph.com/blog/revenge-of-the-junior-developer）

## code-smells-armin-languages.md

- 文章: 《Fast and Hard Code》Armin Ronacher（Flask/Sentry 作者），2026-08-22。
- 语言摩擦消失论: "编程已被解决"的梗之下，真正清楚的是——熟悉一门语言的成本不再重要，过去对人重要的摩擦对 agent 不重要。
- 语言选择后果弱化: LLM 让语言选择比以前后果轻得多——不喜欢就可以（看似）用另一门语言重写，甚至可以让它选一门你作为程序员完全陌生的语言。
- 营销驱动选择: 人们因此更多按语言的营销来选语言；长期 Rust 程序员观察到以前不会选 Rust 的人现在也在发 Rust 代码。
- 两个 vibe shift 的归因: ①更多关于"想要快软件"的讨论；②LLM 在不回归行为的前提下优化代码的能力出众。
- 性能痴迷者+agent 友好者的重合名单: Mitchell Hashimoto、Charlie Marsh、Jarred Sumner、Daniel Lemire 等一贯痴迷快速高性能软件的人恰好都对 agent 写码持接受态度。
- autoresearch 效应: 借助 autoresearch 你甚至不需要知道所有技巧——把 agent 放上去就行（尽管知识大有帮助）。
- "硬语言"受益范围: 想要又快又小的项目 increasingly pick "hard languages"；不止 Rust，Zig 也受益——尽管 Zig 创造者与部分核心社区对 AI 相当负面。
- 具体案例: Cloudflare 新 Artifacts 服务用纯 Zig 写的 Git 协议引擎（编译成约 100KB 的 WebAssembly 模块）；Vercel 发布 fx——宣传为小而快的 Zig 编码 agent；这些项目基本都是 LLM 辅助完成的。
- 硬技术民主化: 人们突然开始用 DWARF 文件、eBPF、自定义网络驱动、自定义加密、很老的计算机硬件做出令人印象深刻的东西——这些以前对多数开发者是禁区（有些如 crypto 还被内行刻意 gatekeep）。
- 结论的两面: 世界也许会有更多 slop，但也可能会有更多"想要又快又小"的开发者。

来源: research/raw/articles/code-smells-armin-languages.md（原始 URL: https://lucumr.pocoo.org/2026/8/22/fast-hard-code/）

## code-smells-jadarma-copilot-stats.md

- 文章: 《Does GitHub Copilot Improve Code Quality? Here's How We Lie With Statistics》jadarma 博客，2024-11-20——对 GitHub 官方博客"首个关于 Copilot 代码质量影响的受控研究"的方法学批判。
- 利益声明: 作者自认反 AI 炒作、非科学家，但强调"一个大公司研究自家产品"只有阳性结论才对其有利——biased dude vs biased corporation。
- 实验任务偏置: 受试任务是给 Web 服务器写 API 端点（虚构餐厅评论站）——CRUD 是最无聊、重复、认知无挑战的开发工作，也是最容易预期 AI 改进的地方；由此推"AI 总体改进你的代码"不诚实；任务是最泛滥的 code-lab/medium/stackoverflow 级别，"GPT-2.0 抓取 Google 两周都能抄袭出来"；要测就该给复杂任务（巨型 SQL、正则、shell 部署脚本）。
- GitHub 宣称的头条数据（作者转述）: Copilot 组 56% 更可能通过全部测试；写坏味道前多写 13% 的代码；可读性 +3.62%、可靠性 +2.94%、可维护性 +2.47%、简洁性 +4.16%；PR 被接受的可能性 +5%。
- "百分比误导"批判: 百分比没有语境无意义——从 95% 提 3% 与从 32% 提 3% 完全不同；代码度量都在 3% 边缘徘徊，可能是舍入误差级别的差异（尽管 p 值可能显著）。
- 测试深度的批判: "通过全部 10 个单元测试"——总共才 10 个测试；要么整个测试运行只测一个端点，要么测试极浅（API 有大量可查之处：内容协商头、200/201/204 状态码细节等）。
- 样本数对不上的疑点: "40% 通过全部测试"且"25 名开发者通过"反推出总数 62 人，但研究宣称 200 人随机对半分——多出的"40 个 Control-er 去哪了"（原文百分比图加起来不为 100，作者讽刺"because the math was done by an LLM"）。
- "偷换定义"批判（最重的一击）: GitHub 把 "code error" 定义为"任何降低代码易于理解程度的代码"——明确**不包含**功能性错误（不影响运行的 bug），而是命名不一致、不清晰标识符、过长行、过多空白、缺文档、重复代码、过深分支/循环、功能分离不足、变量复杂度——"那不是 error，那是 linter 警告"；等价于说"逻辑错误不要紧，只要格式无瑕"。
- 主观度量的黑箱: 代码风格与评审高度主观，人类直觉是唯一度量，但研究没说怎么打分（分数/星级/点数/T 恤码？）；3% 内的小差异配上极小 p 值，度量精度存疑。
- 评审者偏置: 参与者互评（提交代码的开发者评审另外 10 份提交）——人类天然偏向与自己风格接近的代码；作者希望有第三方无偏组评分；评审者唯一已知资质是"工作 5 年+通过 10 个单测"。
- 对照组污染可能: 研究只说对照组"被指示不用任何 AI 工具"，没说对照组由"不使用 AI 工具的开发者"构成——如果对照组是被剥夺了日常工具的用户，性能下降可能是戒断效应。
- 样本细节: 243 名开发者（非宣称的 200），121/121 分组，其中仅 104/98 份"有效提交"（"有效"定义未说明——退出？编译不过？为何不计入似乎很重要）；104 vs 98 意味着 Copilot 组多 6%。
- 自相矛盾的证据: GitHub 自己承认 Copilot 组 commit 数与变更行数显著更高但平均 commit 更小——jadarma 对照 GitClear（2023）数据解释其真实含义: moved code 显著减少=更少重构清理；copy-paste 显著增加=更多重复（讽刺的是 GitHub 把重复算作 error）；churn 率显著上升=提交的代码很快又被改（并非"AI 太好用想再用"）。
- 信任排序论: 宁愿相信横跨三年、观察真实场景数千万行代码行为的研究（GitClear），而非几百个 PoC 级 TDD 实验室任务里的烂控制器。
- 结论: 即使承认客观 5% 的生产力提升，这研究面向的是有采购权的 C-suite 营销（说服他们 $470/dev/年花在压榨人力资源上）而非开发者；"如果你没有 AI 就写不出好代码，那你一开始就不该用 AI"——个人经验与手艺自豪不可替代。

来源: research/raw/articles/code-smells-jadarma-copilot-stats.md（原始 URL: https://jadarma.github.io/blog/posts/2024/11/does-github-copilot-improve-code-quality-heres-how-we-lie-with-statistics/）

## code-smells-hn-get-better-ai.md（Ask HN: How can I get better at using AI for programming?）

- realberkeaslan: 推荐 Cursor 的 UI/UX 与 agent 上下文，工作流为"prompt→agent 干活→review 变更→重复"，清晰的变更展示是核心价值。
- jes5199: Cursor 便于边看模型行为边同时编辑；在工作需要为 code review 论证每个变更时特别有用；用几个月 Cursor 后更容易用好 Claude Code。
- listic: 关心开源替代——Cline、Aider 被提及但未试。
- ojr（负面体验）: Cursor 内存占用过大、多文件重写时幻觉、accept/reject diff 的 UI 让 git 变成噩梦；因 VSCode 系 Electron 缺陷自建 Rust 编码工具；"以为他们有资源能做内存高效的应用，结果需要顶配 MacBook 才流畅"。
- rdrd（风格定义法）: 首先精确定义"什么是你要的 idiomatic"——对 LLM 而言你的习惯不叫习惯；逐步写明代码规范与任务步骤，**不要**用"照这个文件写"这种太宽的引用；文档中给出小而简单的 Good/Bad 对照示例；初始指南与规范越小越好——"context is king"，给够用但不至于引起混乱的上下文。
- rdrd（plan 流程）: 把规范喂给 Opus 4.5 的 planning mode，让它提问补缺、产出最终 implementation plan.md，人来 review、删水分、压缩。
- XenophileJKO: 当代模型不必每次不满意就重启（Sonnet/Opus/GPT-5.x）；评审中想到更好抽象就直接 inline 要求重构，模型很少"脱轨"；工作单元太大时问题会变多——但大单元本来就有其他问题。
- rdrd（生产代码的经验）: 对要彻底评审的生产代码，有文档化的 spec 比在 agent 对话里清理更好；其团队为每个 feature 保留 plan.md（AI 之前在 Confluence 里做，流程延续）。
- Alan01252（vibe coding 个人项目经验）: ①先在 chat 模式与 AI 谈透要做的 feature、双方"达成一致"后再切 agent 模式（Google antigravity 默认如此，可能是正确范式）；②先把基础打好——AI 很容易产出一堆 slop，要像带 junior 一样提前引导；③让 AI 先写测试——BDD 对 AI 特别有效。
- Esophagus4: prompting 本身是一门技能，需要日/周/月刻意练习；约一年持续练习才对 LLM 编码感到自如。
- 8cvor6j844qw_d6: Claude Code 在高度具体且范围狭窄的任务上表现最好；发现跑偏要 course-correct（中途纠偏）；是 mundane 任务的倍增器而非替代；仍需用户对代码库有好的理解；写 commit log 的变更摘要很棒。
- mirsadm: 把一切拆成很小的任务；总让它先计划、人审计划找错；一次只做一步以全程可控——"只要不做任何有点独特的事，这流程就够好；稍有独特性它就做不好"。
- kgwxd（反方）: "听起来你在做全部实际工作，那为什么不直接自己敲代码？反正输出你都要审。"
- Iulioh（VBA 场景）: 从没收到过正确的高层 main sub，但 AI 做小函数很在行、由人来组织；指出错误的定位也很好；AI 会在你合理地**不想要**"最佳实践"的地方强行套用最佳实践。
- Frannky（"搜索器"心智模型）: 把 LLM 当搜索器（searcher）——搜索易于执行（小上下文、小而精确的问题）；代码跑不通（训练数据里没有）就不要反复重试；训练数据中代表性差的语言效果差；越具体越简洁越好；修改越少越好——离训练集越远出错概率越高。
- seg_lol（对上条的修正）: LLM 是搜索没错但搜索空间稀疏，问题的大小有欠指定风险；问题控制高维空间中被封装体积的大小；小 prompt 的唯一优势是计算成本，其他方面都是劣势。
- bogtog（语音输入法）: 用语音转写充分表达需求、让模型不用猜——常口述 500 词 prompt；绕来绕去也没关系，模型几乎总能听懂；说话比边想边打字快且不累（打字 70-90 WPM vs 说话 100-120 WPM 的舒适思考）；还可以问"你有什么问题吗"——但"有问题就问否则就做"很少真的产生提问。
- 语音工具链（多条合并线索）: binocarlos 用 whispering + OpenAI API，快捷键录停、转录进剪贴板；bogtog 用 Wispr Flow / Superwhisper（单手热键）；mattmanser 用 Aquavoice（YC，右 Ctrl 触发，可设双击、支持长停顿思考）；hn_throw2025 用 Whispering 接 Groq 的 whisper-large-v3-turbo（极便宜可靠）；quinncom 用 Spokenly + 本地 Parakeet 0.6B v3 + Cerebras gpt-oss-120b 后处理（修正技术性误听如 noJS→Node.js）；rgbrgb 用 Handy（焦点窗口转录）。

来源: research/raw/articles/code-smells-hn-get-better-ai.md（原始 URL: https://news.ycombinator.com/item?id=46255285）

## code-smells-hn-good-code-agents.md（Ask HN: Is anybody producing good code with coding agents?）

- verdverm: opencode + 开放权重模型组合的代码"一般挺好"，但**花 token 让 agent 去找常见 AI slop 模式**（即把"slop 检测"本身作为 agent 任务）；重度定制（插件替换内部系统、自定义 agent 组、按子任务选不同模型家族）；原则"don't have claude review its own code"（不让 Claude 审自己的代码）；用 GLM 5.3 flash 做代码探索/评审——便宜且能抓住大厂模型的各类错误，团队已在 glm-5.3-flash 上全面部署自定义 PR review。
- drewg123（三分法光谱）: AI 维护的代码（如可视化性能数据的 GUI）完全不管长什么样、100% vibe；在乎的代码逐 hunk 审计、给详尽风格指南、打击"20 行小作文注释"这类问题；关键任务代码自己写、让 agent 评审。
- drgo: 用 LLM 生成"自己不想写的代码"——原型、测试、benchmark、孤立的近乎复制粘贴的代码；自己的代码照旧手写——理解和修复 LLM 生成再重生成的代码，比按自己想要的方式写更难更乏味更耗时。
- tmarice（两个极端模式）: 在重要项目上多次"把自己 vibe 进死角"后只剩两种模式——不在乎的（多为 react 前端）随便造，其余全部手写；用 Django 后端天然去掉大部分 cruft，手写还保证自己真懂；对 AI 测试的评价："LLM 生成的测试相当差，即便是 xhigh thinking 的前沿模型……除了 1==1 什么都没测"；但手写测试又难挤出时间。
- leros: 用 AI 以约 5 倍速度产出与自己所写几乎相同的代码；不让 Claude Code 长时间狂奔然后面对一堆烂摊子——小 chunk 快速 review、反馈、迭代到满意再进下一步，比审一大坨更快。
- deterministic: Opus 5.5 非常擅长匹配既有编码风格——常看着代码以为是自己写的，结果是 Opus 写的；诀窍是给足风格偏好引导。
- aprdm（激进派）: "别再读/写代码了，建强 harness"——约 30 人团队大体如此运作；要解决的业务问题从来不是"写代码"。
- AnimalMuppet（对上的反驳，风险论证）: "我今天不懂这代码但它能跑"没问题；"我永远不需要再懂这代码"是完全不同的断言——代码没人懂又没人写的，当你被逼进死角时逃出来会更难还是更容易？你可能把公司押在这个答案上。
- runjake（spec 驱动派）: 全程能产出好代码，但仍要写好 spec——把 spec 写进文件（通常 Markdown），让 agent 过一遍 spec 指出漏洞与问题、更新 spec，迭代几轮后再开工开发；garbage in garbage out。
- sigbottle（agent 的 95% 问题）: 编码 agent 被 RL 训练成"把事做完"——它们宁愿冲到 95%、意识不到根本性架构缺陷、然后 hack 最后 5%，也不吸取教训重新设计；"那是你的工作"；商业场景下大量重写不好看。
- runjake（架构文档+双模型审查）: 让 agent 边建边更新架构文档；始终让另一个无既有上下文的 agent 审查项目的 slop、hack、最佳实践、安全漏洞——通常一个用 Codex、另一个用 Claude。
- piscaries（未知项的对策）: 你无法 spec 你还不知道的东西——两个办法：①让 agent 在写 spec 前"拷问"你（grill you），回答它的问题能暴露大量 unknown unknowns；②再让**不同模型**拷问 plan，问针对你产品的问题——一次就抓住了通用评审漏掉的设计问题。
- hey-hey（阅读成本 amortization 变化）: 以前我们把阅读理解成本摊销在设计与编写的时间里；现在冷启动审变更，但体验与"评审不了解的其他团队的变更"类似；好 harness（memory、specs、基于图的理解）能让你"warm"地进入——先知道"这个方法/类干 X"再读就快了。
- catchnear4321: 调好 reviewer 后像管理一组过度专精技能的团队；问题解决没变，变的是"手"；像回到系统分析师（systems analyst）时代。
- faangguyindia（自定义 harness）: 30 人团队用为缓存效率与定制工作流构建的 custom harness；"Skill Selector"用自研 Gambler v1（26B 决策模型、本地 <100ms 响应）选择技能；在既有工具上覆盖一层熟悉接口（模型在其 harness 上 RLVL 过特定工具，覆盖后注入自定义特性）。
- saluki（Claude Code 协作式流程）: 短 claude.md + db schema 等技能；大/复杂 feature 先与 Claude 做 design session、review 设计、协作；设计敲定后拆任务、逐任务/阶段协作出 plan.md 再让 Claude 构建；Claude 极擅长加测试——借此逼近 100% 覆盖率并验证满足 PRD/spec；md 文件进仓让全团队跨前后端共享上下文；PR 上跑 claude code review。
- keshwanianup: prompt 完美时 Claude Opus 4.7+ 能生成像样的**新**代码；在既有代码里修 bug（尤其 multi-repo）就很复杂。
- vivekpolavarapu: 评审耗时 5 倍是共同体验；单一代码评审工具达不到 level 4 自治；实验用多模型评审代码+设计+架构+agent 最冒险的 commit——"多个模型对一处变更争论产生的洞察远好于单模型评审"（truverif.ai panel-review）。
- sajithdilshan: 纯 vibe code 出来就是屎；先想架构与抽象、再逐块生成——那就是"我会写的同一份代码"；生成的测试反而比他手写更好（因为人懒得覆盖每个边界）。
- linesofcode（激进派）: 如果还要花很多时间读/评审代码，说明 agentic pipeline 出了问题——时间投资应前移到设计头脑风暴与设计阶段；agent 开始写码时默认其 90% 代码是稳的，剩 10% 用几轮迭代解决；当代只有关键任务代码或面向用户/agent 的界面迭代值得人审（保 dx 光滑）。
- martinmilo: 关键是保持对单元/集成测试的总览控制——那是可以任意次重跑的确定性期望；做好这部分+ linter 规则集 + 描述仓库偏好代码模式的 skills，其余就相对容易。
- kittomic（人审瓶颈论）: 人审全部 AI 输出会撞上人类理解力瓶颈；关键是清晰 spec 与架构然后让 agent 执行；时间主要投 specs 与 e2e/集成测试；比以前更看重严格六边形架构（hexagonal）与大剂量 DDD——系统分解为域、域分解为用例/端口/适配器后，AI 很能干且易于测试验证；"AI 验证一个基础 CRUD 端口是否可用"是可接受的，因为每个操作只剩不到一打代码行；"别再把自己当程序员，开始把自己当（系统设计者）"。

来源: research/raw/articles/code-smells-hn-good-code-agents.md（原始 URL: https://news.ycombinator.com/item?id=49934037）

## code-smells-hn-sloppy-code.md（Ask HN: How to deal with AI generated sloppy code）

- talldayo（定价对策）: 提高时薪，直到"花几百小时拆面条代码"也舒服为止。
- anonzzzies（具体定价）: 通常收 2-5 千欧元"看一眼"，然后视情况 200-500 欧元/小时开工；按代码类型分价——人写的老 PHP 要求最高费率、asp/vba 也很烂；过度架构的东西多在 Java/C#（烦人但没那么难）；cobol/fortran/c/c++ 通常还行；bash/perl/tcl 脚本通常没问题（能跑就不动）。
- al_borland（"它确实能跑"的反驳）: 如果客户仍要人来维护和优化，那"能跑"就不成立——从那个视角它不 work；清理囤积屋比轻扫除贵，价格反映工作量；客户可以选择前期写干净，或后期为难以/无法维护买单——选择权在他们。
- swah: Cursor 做脚本时是好帮手（函数建议、cmd+k），但担心"写函数容易、20 天后还要把一切都记在脑子里再写更多函数"很难；用 Zig 试过是灾难。
- agarren（理解税）: AI 能替你写代码从而极大简化软件开发，但有代价——不理解或只表面理解所写内容，维护就是噩梦；自己 20 天前写的代码尚需重新熟悉，遑论 AI；把 Cursor 当"高级 intellisense"敲整个 routine 与类型，会剥夺你对解决方案的真正理解；短期提产，长期在难重访的代码上耗时间。
- thelostdragon（生成/评审分离铁律）: 必须收紧 code review 与测试流程；**不能让 AI 同时做代码生成和代码评审/测试**——要么 AI 生成+人类评审测试，要么人类生成+AI 辅助评审测试，绝不双 AI；作者认为第二种更好（AI 支持测试与评审，生成仍是 Developer 的领域，近期看不到 AI 写生产级代码）；开发者可用 AI 生成片段再调成生产就绪——当下两全其美。
- ratg13（地基比喻）: 软件像房子——给你地基烂的房子往上盖，唯一的改进选项是看有什么可 salvage 然后重来（理想情况下次别犯同样错误）。
- meiraleal（需求侧效应）: 这正是 AI 时代软件工程师需求只增不减的方式——CEO 们做出"糟糕但成功的 MVP"，很快需要雇佣称职专业人士走下一程。
- derefr（语料风格论+伪代码技巧）: LLM 的输出（文字或代码）总是与训练数据同风格；Java 训练语料既臃肿企业化、又多由 junior 甚至学生写成（公开 Java 学校项目仓库太多）；技巧——让 AI 先用更简洁低样板高表达的语言（如 Ruby）写"伪代码解"，再让它把自己的伪代码翻译成 Java。
- jprete（对上的澄清）: OP 是在比较两种条件（Java slop vs LLM slop），因为两者有共同成因——工具让人做出"还能跑但难懂"的过度复杂系统；OP 并非说 LLM slop 是 Java 写的。
- srinathkrishna（设计模式积怨）: 在 Java 商店工作时——从 C 的务实方式来被 Java 生态搞得抓狂；遇到多位坚持用 factory、builder 与晦涩设计模式的资深工程师，永远在畅谈"未来某场景会被重构"；一度确信 OOP 设计模式是资深者发明的 gatekeeping。
- manmal（deletability 原则）: GoF 等模式常在无需要处被套用；作者如今的指导原则是 deletability/unpluggability——让"移除一个组件或行为"尽可能容易的结构；仍会用相同模式但绝不盲用、用量大减；Swift 值类型+闭包支持常靠 struct 走完 90%，不需要 protocol 或 class。
- PhilipRoman（C 生态烂设计实例）: 某公司改个 wifi 网名要动 10 个进程（本质只是一条发给驱动的 netlink 消息）；守护进程太多后换成"单进程多线程"新架构，却无视线程安全、到处盲目粘贴 hostapd 代码；一切以字符串传递与解析——C 的优点（速度、简洁）全无、缺点（ABI 破坏等）全占；没听说过数据库或纯文本文件，数据存在 XML/JSON"数据库"里，又嫌完整 XML 解析器太贵于是自制要求换行的私有 XML 解析器。
- duskwuff（概率偏置机制）: LLM 输出还有隐性的"唠叨偏置"（blathering），尤其在代码补全这类开放场景；语言模型偏好高概率输出——如果生成高度刻板的内容（样板 getter/setter、文档注释）是"合适"的，它就比生成应用特定的内容（算法的实际实现）更可能生成前者。
- agentultra（专家路线）: 专业知识+好的验证自动化工具——TLA+、Coq/Agda/Lean、规格综合、property-based testing、传统单元/功能测试+苦干；像做咨询（驯服没有测试、无人懂的古董代码），价值在于在高于代码的层面工作，让团队重新能理解并扩展系统。
- dmitrygr（宿命论）: "它只在他们机器上能跑"；什么都不用做，问题会自我解决——技术债终将压垮他们，而且很快。
- golergka: 单人创始人完全可以用自己写的烂代码起步、之后付钱请专业人员解开——AI 没有改变这一点。
- jcgrillo（ slop 的深层诊断）: sloppy 代码背后通常是 sloppy 的想法；清晰的思考产生称职的执行；警惕任何过不了 smell test 的代码库——真深挖下去会处处发现错误的前提（flawed premises）。
- overspeed（魔鬼代言人）: AI 让非技术者 bootstrap 出能用的应用；小批量生成再缝合会缺全局设计——"sloppy"在于难以维护扩展，但它 works（商标式的 works™）；鉴于技能差距，实现背后的想法不一定绑定实现质量。
- amradio1989（以 AI 治 AI）: 应对 AI slop 的方式就是用 AI——区别在于你能提供比经验不足者更好的 guidance；更好的引导产生更干净的结果；最好现在就练起来，因为未来（即当下）就是 AI 生成代码与 AI 辅助代码维护。

来源: research/raw/articles/code-smells-hn-sloppy-code.md（原始 URL: https://news.ycombinator.com/item?id=41677207）

---

# 第二部分 tools（16 篇）

## hooks-claude-code-reference.md（Claude Code Hooks 官方参考）

- 事件类型-会话级: SessionStart / SessionEnd / Setup。
- 事件类型-每轮: UserPromptSubmit / UserPromptExpansion / Stop / StopFailure。
- 事件类型-Agent 循环: PreToolUse（可阻断）/ PostToolUse / PostToolUseFailure / PostToolBatch / PermissionRequest / PermissionDenied。
- 事件类型-其他: Notification、MessageDisplay、SubagentStart/Stop、TaskCreated/Completed、PreCompact/PostCompact、ConfigChange、FileChanged、WorktreeCreate/Remove 等。
- 阻断核心机制（退出码）: 0=成功（JSON 字段生效；静默不等于批准）；**2=阻断**，stderr 作为原因反馈给模型；其他码=非阻断错误；官方明言"如果你的钩子要强制执行策略，用 exit 2"（exit 1 不阻断）。
- JSON 精细控制: PreToolUse 用 hookSpecificOutput.permissionDecision = allow/deny/ask/defer，配合 updatedInput（可改写工具参数）与 additionalContext；PostToolUse 可用 decision:"block" 回溯打断——工具已执行，但把 stderr 反馈给 Claude 迫使其修正。
- onFailure:"block"（v2.1.295+）: 钩子自身启动失败/超时/输出非法时也阻断动作——否则失败的钩子会静默放行一切。
- 超时语义: 超时的 PreToolUse 钩子**不阻断**——"别指望一个卡死的钩子充当门禁"。
- HTTP 钩子: 只有 2xx + JSON body 才能阻断。
- matcher 语法: "*"/"" 匹配全部；纯字母数字下划线连字符为精确名或 |/`,` 列表；含其他字符按 JS 正则（如 mcp__server__.*）。
- if 字段: 用权限规则语法（如 Bash(rm *)）过滤，属 best-effort；**硬性 allow/deny 应交给权限系统而非钩子**。
- 钩子处理器类型五种: command（shell）/ http（POST JSON）/ mcp_tool / prompt（单轮 LLM 评估）/ agent（实验性子代理）。
- 组织治理: 管理端可 allowManagedHooksOnly + 管理设置，实现组织级不可覆盖的护栏。
- 注入防御: 钩子输出 additionalContext 应是事实陈述——命令式注入会触发模型的 prompt-injection 防御；system-reminder 标签被转义。
- 输出与继承限制: 钩子输出上限 10000 字符；钩子继承父环境。
- 配置层级（优先级从高到低）: managed > local(.local) > project(.claude/settings.json，可入库共享) > plugin(hooks/hooks.json) > user。
- 定位意义: hooks 是把"代码质量约束"从概率性提示升级为确定性执行的标准通道；社区所有 guardrail 工具（gryph/safety-net/agent-guard/stop-that-shit）都构建在 PreToolUse/PostToolUse 之上。

来源: research/raw/tools/hooks-claude-code-reference.md（原始 URL: https://code.claude.com/docs/en/hooks）

## hooks-community-guide-konishi.md（Konishi 指南，逐条罗列）

### 代码质量钩子模式（6 个配方）
- 配方 1「写后自动格式化」: PostToolUse 匹配 Write|Edit，从 stdin JSON 取 tool_input.file_path，按扩展名跑 ruff(.py)/prettier(TS/JS/CSS/MD)/gofmt(Go)；formatter 输出走 stderr 以免被误解析为 JSON decision；**脚本恒 exit 0——"formatting is a convenience, not a gate"（格式化是便利不是门禁）**。
- 配方 2「审计日志」: PostToolUse（matcher *，async:true）用 jq 把带时间戳的工具调用记录追加到 JSONL；async 使其不占关键路径。
- 配方 3「Turn guard（Stop 门）」: 有未提交变更时 block 一次，用 marker 文件防无限循环。
- 配方 4「SessionStart 注入」: stdout（git branch、最近 5 条 commit、status）直接进入上下文，纯 echo 无需 JSON。
- 配方 5「Pre-compact 检查点」: matcher "auto" 时先快照草稿笔记（防 compaction 丢失）。
- 配方 6「UserPromptSubmit 策略」: stdout 喂模型；decision:"block" 拦截违规 prompt（如部署冻结期）。

### 两条返回通道（强制语义）
- 通道 1（退出码，粗粒度）: 0=成功；**2=阻断**（stderr 作为原因回给模型）；其他非零=非阻断错误、被忽略。
- 通道 2（stdout JSON，细粒度）: 多数事件用顶层 decision:"block"+reason；**PreToolUse 不同**——用 hookSpecificOutput.permissionDecision (allow/deny/ask/defer) + updatedInput；搞混两种 JSON 形状是最常见 bug。

### 反模式（7 条）
- 反模式 1: 慢钩子——同步 gate 每次调用都跑；要快、限时，日志/格式化用 async:true。
- 反模式 2: 用 exit 1 而非 exit 2 → 被拦的动作照样执行。
- 反模式 3: 无终止条件的 Stop/SubagentStop 钩子 → 死循环。
- 反模式 4: matcher 写 mcp__memory 是精确匹配；mcp__memory__.* 才是全服务器。
- 反模式 5: 期望 hook 的 allow 能松动权限规则的 deny/ask——不能。
- 反模式 6（安全）: 钩子以完整 shell 权限运行——审查第三方仓库的钩子如同审查 postinstall；updatedInput 改写型钩子是高风险代码。
- 反模式 7（治理）: 忽略配置层级 Managed > Local > Project > Plugin > User；managed settings 提供组织级不可覆盖护栏。

### 金句
- "A system prompt is a request. A hook is a guarantee."（系统提示是请求，钩子是保证）——CLAUDE.md 说服、permissions 过滤、hooks 强制并响应。

来源: research/raw/tools/hooks-community-guide-konishi.md（原始 URL: https://hidekazu-konishi.com/entry/claude_code_hooks_complete_guide.html）

## steering-claude-code-blog.md（Anthropic《Steering Claude Code》）

- 核心论点（确定性 vs 概率性）: "模型选择运行 formatter"与"formatter 自动运行"是两回事；"当某事绝对不能发生时，指令是错误的工具"。
- 退化条件: 模型在"压力下、长会话中或含糊情境里"不会遵守提示规则，还会被 prompt injection 劫持——真护栏必须确定性（hooks PreToolUse exit 2 / 权限系统）。
- 机制分工-Hooks: 一切"必须确定性发生"的事——编辑后跑 linter、阻断命令、PreCompact 备份。
- 机制分工-Rules（路径限定 paths: frontmatter）: 具体约束/惯例（如"所有 API handler 必须用 Zod 校验输入"）；关注点散布多目录但非全部时用路径规则而非全局 CLAUDE.md。
- 机制分工-Skills: 程序性工作（部署流程、发布清单、review 流程）应在主线程内展开时用 Skill 而非塞进 CLAUDE.md。
- 机制分工-Subagents: 并行/隔离的旁路工作，只回传摘要。
- 机制分工-CLAUDE.md: 只放"必须一直知道的事实"（构建命令、布局、惯例），保持 <200 行。
- 上下文成本: 根 CLAUDE.md 成本最高——"每一行无论相关与否都耗 token"；规模化后"每个团队都追加自己的指令而没有任何东西被删除"（append-only 规则腐烂）。
- compaction 下的各机制行为: Rules 在 compaction 后会重新注入（因此持续生效）；Skills 正文仅在调用时加载（compaction 后被调用的 skill 重新注入共享预算、最旧先丢）；Subagents 完全隔离（"never enters the parent conversation at all"）；Hooks 完全绕过 compaction（配置在上下文之外）。
- 指令遵守的边际递减: 系统提示法永不 compaction 但昂贵；追加指令对遵守率有边际递减——指令越多遵守越松。
- 经验法则总结: 确定性行为→hooks；事实→CLAUDE.md/rules；流程→skills；隔离旁路→subagents。

来源: research/raw/tools/steering-claude-code-blog.md（原始 URL: https://claude.com/blog/steering-claude-code-skills-hooks-rules-subagents-and-more）

## context-engineering-anthropic.md（Anthropic《Effective Context Engineering for AI Agents》）

- 第一原则: 上下文是有限资源——存在 "context rot"（token 越多召回越差）与注意力预算；目标是"找到最大化期望结果可能性的最小高信号 token 集合"。
- 系统提示的 "right altitude"（合适高度）: 避免两个极端——脆硬编码 if-else 与空洞泛化；"specific enough to guide behavior effectively, yet flexible enough"（足够具体以有效引导行为，又足够灵活）。
- 迭代方法: 从最小提示开始，**基于观察到的失败**再追加指令（而非预防性堆规则）。
- 机制 1 Compaction（压缩）: 临近上限时总结对话并重启窗口；Claude Code 保留摘要+最近 5 个访问文件；对 agent trace 调优压缩提示（先最大化召回再提精度）；轻量做法是清理旧工具输出。
- 机制 2 Structured note-taking / agentic memory（结构化笔记/代理记忆）: 把笔记持久化在上下文窗口之外（todo list、NOTES.md），事后重载——"persistent memory with minimal overhead"；Claude-plays-Pokémon 证明可在数千步/上下文重置后保持连贯。
- 机制 3 Sub-agent architectures（子代理架构）: 专职子代理在干净上下文里做深工作，只回传 1000-2000 token 的"condensed, distilled summary"；复杂研究任务显著优于单代理。
- 机制 4 Just-in-time retrieval（按需检索）: 不预载，保留轻量引用（路径/查询/链接）运行时取；元数据（目录结构、命名、时间戳）提供导航信号；混合策略（CLAUDE.md 预载+按需检索）——"do the simplest thing that works"。
- 对 guardrails 的推论 1: 长会话质量下降是"规则失效"的物理原因——护栏必须放在上下文之外（hooks/权限/CI），compaction 后仍生效。
- 对 guardrails 的推论 2: 记忆交接（memory handoff）——notes 文件让新会话/子代理继承验证证据，避免重复劳动与结论丢失。
- 选择启发: 长对话→compaction；里程碑工作→笔记；并行研究→多代理。

来源: research/raw/tools/context-engineering-anthropic.md（原始 URL: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents）

## speckit-sdd.md（GitHub Spec Kit）

- 工作流（每特性一次、逐个在 agent 会话中调用）: /speckit-constitution（项目原则，每项目一次，聚焦代码质量、测试、可维护性）→ /speckit-specify（需求→spec）→ /speckit-plan（技术方案）→ /speckit-tasks（可执行任务分解）→ /speckit-implement + /speckit-converge（实现后对照 spec 工件检查）。
- 收敛循环门禁: implement→converge 循环"until convergence reports Converged"——用收敛报告替代一次性生成。
- 验证三值裁决: "verified, partial, or failed"——**missing verification 不算修复**（与 verification-before-completion 精神一致）。
- 工件持久化: 全部为 Markdown 于 .specify/ 目录，可人审、可 diff。
- 可选质量门: "需要额外质量门时，加 clarification、checklist 与一致性分析"。
- 理念: 先定义 what/why 再决定 how；未知通过**编辑工件**解决而非重新生成阶段（anti-regeneration，反重生成）。
- 扩展命令: /speckit-bug-assess|fix|test（bug 修复也走 spec 流程）；/speckit-assess-intake|research|define|shape|decide（创意评估，产出 go / needs-clarification / kill 决策）。
- 支持范围: Copilot 默认；Codex 等经 integration key；安装 specify-cli（Python 3.11+/uv）；约 141k stars，MIT。
- 定位评估: 过程性门禁（probabilistic + 人工审批），依赖 agent 遵循命令流程；与 hooks 的机器强制互补。

来源: research/raw/tools/speckit-sdd.md（原始 URL: https://github.com/github/spec-kit）

## openspec.md（OpenSpec 轻量规格层）

- 定位: 解决"需求只存在于聊天历史中"导致的不可靠——人机在写码前先对齐（plain Markdown spec 层）；自我定位 "fluid not rigid"，适合存量（brownfield）代码库。
- 与竞品对比（官方口径）: Spec Kit 彻底但重（刚性阶段门、重型 Markdown、Python 依赖）；OpenSpec 更轻、自由迭代；对比 Kiro 无 IDE 锁定；对比无规格则"可预测而无仪式感"。
- 工作流 4 步: /opsx:explore（可选规划对话）→ /opsx:propose（生成变更目录）→ /opsx:apply（按 tasks 实现并勾选）→ /opsx:archive（归档）。
- /opsx:propose 产物结构: proposal.md（why/what）+ specs/（Requirement/Scenario 的 WHEN-THEN 块）+ design.md + tasks.md（清单），**人在写码前 review**。
- 归档机制: /opsx:archive 把变更归档到 openspec/changes/archive/<date>-<name>/ 并更新主 spec——"每个变更一个目录+归档时合并回主 spec"是防止规格腐烂的结构化做法。
- 门禁哲学: 刻意最小——"no rigid phase gates"，主要控制点是**人在实现前审批 plan**；expanded profile 增加 /opsx:verify。
- 其他: 30+ AI 工具适配（命令拼写各异）；npm/Homebrew 安装；Stores(beta) 支持跨仓库共享只读规格；约 71.6k stars。
- 机制启示: 评审点放在实现之前（杠杆最大的人工门）。

来源: research/raw/tools/openspec.md（原始 URL: https://github.com/Fission-AI/OpenSpec）

## kiro-specs.md（Kiro 规格）

- 三工件结构: 每个 spec 生成 ①requirements.md（或 bugfix.md——用户故事+验收标准；bugfix 则记录当前行为/期望行为/不变行为）；②design.md（技术架构、时序图、数据流、错误处理、测试策略）；③tasks.md（离散可跟踪任务、实时状态更新）。
- Feature Spec 两种变体: Requirements-First 与 Design-First，**每阶段多个人工审批门（approval gates）**。
- Bugfix Spec 特点: 系统性根因分析 + 回归预防。
- Quick Spec: well-understood 特性跳过审批门、一键生成三工件。
- 任务并行机制: 构建依赖图，把独立任务分组为 waves，Wave 1 并发执行（IDE/CLI/Web 均支持）。
- Correctness: property-based testing，IDE-only 可选验证。
- 机制启示: "验收标准写进 tasks + 每阶段人工 gate"是 IDE 级 SDD 的标准形态；依赖图 wave 并行提高无人干预吞吐，但 gate 仍是人。
- 材料勘误: EARS 语法未在此页提及（社区常提的 EARS "WHEN...THE SYSTEM SHALL..." 句式未经此源确认）。

来源: research/raw/tools/kiro-specs.md（原始 URL: https://kiro.dev/docs/specs/）

## kiro-hooks.md（Kiro Hooks）

- 配置结构: JSON 配置于 .kiro/hooks/（工作区）或 ~/.kiro/hooks/（全局），会话启动时自动激活。
- 触发器: 事件驱动（PascalCase）——PostFileSave（agent 编辑/保存文件后）、PreToolUse/PostToolUse（工具调用前后）、Stop（任务完成）等；matcher 用正则过滤路径或工具。
- 动作类型 1 Command: 在项目根跑 shell 命令，stdin 收到会话上下文 JSON；默认超时 60s。
- 动作类型 2 Agent: "把一个 prompt 注入当前对话，引导 agent 行为"（inject a prompt into the current conversation, steering the agent's behavior）——概率性干预通道。
- 典型用法 1「自动 lint」: PostFileSave 匹配 `\.(ts|tsx)$` 时跑 `npx eslint --fix`——agent 保存即格式化/修复，无需提示。
- 典型用法 2「门禁危险操作」: PreToolUse 检查前置条件后放行/阻断。
- 典型用法 3「强制标准」: 自动跑 linter/formatter/typecheck。
- 典型用法 4「提交前验证」: Stop 钩子可带 confirm 块人工确认（confirmCommand 动态提示）。
- 机制启示: 与 Claude Code hooks 同构——事件→matcher→命令动作（确定性）或 prompt 注入（概率性）；"保存即 lint"是静态检查融入 AI 工作流的最常见形态。

来源: research/raw/tools/kiro-hooks.md（原始 URL: https://kiro.dev/docs/hooks/）

## agents-md-spec.md（AGENTS.md 开放规范）

- 定义: 给 AI 编码 agent 的项目上下文的 Markdown 开放标准——"a README for agents"；6 万+开源项目采用。
- 放置与层级: 仓库根目录；monorepo 可在子包内嵌套 AGENTS.md；规则为 **"The closest AGENTS.md to the edited file wins."**（离被编辑文件最近的 AGENTS.md 优先）。
- 指令优先级: 用户聊天中的显式指令覆盖一切；OpenAI 仓库内部有 88 个 AGENTS.md（大型 monorepo 实证）。
- 内容与格式: 项目概览、构建/测试命令、代码风格、测试说明、安全注意；"像对新同事交代的事"（PR 规范、commit 格式、部署步骤）；无必填字段、纯 Markdown 任意标题。
- 行为杠杆与风险: **若列出测试命令，agent 会自动尝试运行并修复**——规则即行为的杠杆，也是风险面。
- 工具兼容: Codex、Jules、Cursor、Amp、Aider（.aider.conf.yml read）、Gemini CLI（context.fileName）、Zed、Warp、VS Code、Devin 等，一份文件通用。
- 治理归属: 源自 OpenAI Codex / Amp / Jules / Cursor / Factory 合作，现由 Linux Foundation 下的 Agentic AI Foundation 管理；无版本化方案。
- 机制定性: 规则文件是被读入上下文的"概率性指令"。
- 注入风险（引 arXiv 2610.09264）: 最新研究证明规则文件本身是 prompt injection 攻击面——可被注入恶意提示诱导依赖替换（slopsquatting）。
- 治理三要求: 来源可信、体积受控（CLAUDE.md <200 行共识）、定期删除失效规则（steering 博客指出的"append-only 腐烂"）。

来源: research/raw/tools/agents-md-spec.md（原始 URL: https://agents.md/）

## codex-sandboxing.md（OpenAI Codex CLI 沙箱）

- 基本机制: Codex 本地任务默认运行在沙箱中——限制模型可访问的文件、可在无审批下运行的命令、以及互联网访问。
- 沙箱三档: read-only（只读）/ workspace-write（工作区可写、网络默认禁）/ danger-full-access。
- 强制层级: 底层依赖 OS 级机制（macOS Seatbelt / Linux Landlock 类系统调用隔离），不是提示词约定——**进程层面强制**。
- 配套审批策略: approval policy（untrusted / on-failure / on-request / never）决定何时升级到用户确认。
- 权限最小化三段式: 默认只读→需要时放开工作区写→显式才给完全访问。
- 网络默认禁的双重意义: 防"依赖幻觉（slopsquatting）+ 数据外泄"的第一道确定性防线——包都装不下来时，幻觉包无法伤害你。
- 纵深防御组合: OS 沙箱 + 审批策略 + hooks 构成从物理到策略的防御纵深；agent 的"行为约束"最终要落到进程边界而非措辞。

来源: research/raw/tools/codex-sandboxing.md（原始 URL: https://developers.openai.com/codex/sandbox）

## cursor-rules.md（Cursor Rules 规则系统）

- 四种规则类型（按注入方式）: ①Always——每次会话都注入；②Auto Attached——frontmatter globs 命中上下文文件时注入；③Agent Requested——agent 依据 description 自行决定拉取；④Manual——仅 @mention 时注入。
- 格式与优先级判定: .mdc 文件 + frontmatter——alwaysApply: true（恒注入，忽略 globs/description）；false+globs（按文件自动挂载）；false+仅 description（agent 自选）；都无（手动）。
- 三层规则作用域: Project Rules 在 .cursor/rules（版本控制；裸 .md 被忽略）；User Rules 全局；Team Rules 面板管理且可 enforced；优先级 Team > Project > User。
- AGENTS.md 兼容: 支持 AGENTS.md（根目录+嵌套，更深的更具体者优先）。
- 引用语义: 规则内 @file 引用**不内联展开**——agent 需要时才用工具读取；必须始终在场的内容要写进规则正文。
- 最佳实践 1: 单条规则 <500 行，大规则拆成可组合的小规则。
- 最佳实践 2: 具体、可执行，像内部文档一样写，带例子。
- 最佳实践 3: 引用文件而非复制内容，避免过时。
- 最佳实践 4: **不要重复 linter 能做的事**（style guide 交给 linter）。
- 最佳实践 5: 只在 agent 重复犯错时才加规则；规则进 git、随模式演进更新。
- 机制定性: Cursor 把"规则注入"做成四级可控开关（always/glob/agent-choice/manual），本质都是概率性影响；官方实践明确把确定性部分外包给 linter——与 Anthropic steering 博客同一共识。

来源: research/raw/tools/cursor-rules.md（原始 URL: https://cursor.com/docs/context/rules）

## biome-cli-agent-safe-flags.md（Biome CLI 的 agent 安全标志）

- 基本发现: Biome CLI **没有**专门的 --agentic / agent 模式（2026-10 检索确认）；Ruff changelog 亦无 agentic 标志（Ruff 0.14.0 无此特性）——agent 集成靠既有标志组合。
- 错误容忍组标志（agent 常写半成品代码）: --skip-parse-errors（跳过语法错误文件而非整体失败）、--format-with-errors=true（带语法错误也格式化）、--no-errors-on-unmatched。
- 安全修复分级: --write/--fix 默认只应用 safe fixes；--unsafe 需显式传入——防止 agent 应用破坏性修复。
- 非交互检查: biome ci 不改文件只检查（CI 门禁形态）。
- 脚本化抑制: biome lint --suppress --reason=STRING 写带理由的注释抑制（可审计）。
- 窄化调用: --only/--skip/--changed/--since/--staged + stdin(--stdin-file-path) 支持针对刚编辑文件快速检查。
- 设计启示 1: 安全修复/不安全修复分级——agent 只许跑安全级。
- 设计启示 2: 语法错误容忍——agent 中间态文件不应让整个 lint 崩溃。
- 设计启示 3: stdin/staged/changed 增量接口——供 PostToolUse 钩子对刚写的文件即时反馈。
- 泛化结论: pre-commit / golangci-lint / eslint 同理——真正的杠杆在"谁在何时以何种权限调用它们"（hooks 自动调用 vs CI 拒绝），而非工具本身。

来源: research/raw/tools/biome-cli-agent-safe-flags.md（原始 URL: https://biomejs.dev/reference/cli/）

## guardrails-ai.md（Guardrails AI 框架）

- 机制: Python 框架，在应用内运行 Input/Output Guards——"detect, quantify and mitigate"特定风险；并帮助从 LLM 生成结构化数据。
- 拦截模型: Guard 拦截 LLM 的输入与输出，在其继续之前经过验证器（validator）。
- Guardrails Hub: 预构建验证器集合（每类风险一个），可组合。
- 定位边界: 通用 LLM 应用可靠性（结构化输出、风险校验），非专为编码 agent 设计。
- 对编码场景的映射: "验证器组合+输入/输出双向拦截+失败后重试/修正"是 guardrail 的通用程序化形态；编码场景对应物为 PreToolUse（输入侧，拦工具调用）+ PostToolUse（输出侧，拦刚写的代码）+ lint/测试反馈环迫使模型自我修正。
- 生态观察: 编码 agent 的护栏基本不走 hosted 框架，而走 CLI hooks 生态（Claude Code/Codex hooks + 本地策略引擎）。

来源: research/raw/tools/guardrails-ai.md（原始 URL: https://www.guardrailsai.com/docs）

## local-repos-guardrail-mechanisms.md（本地仓库机制挖掘：stop-that-shit / superpowers / gryph / claude-code-safety-net / agent-guard）

### 1. stop-that-shit（lennney）——契约式 Guard
- 定位: Skill（建议层）+ Guard（机器强制层）双形态，克制 AI 的过度防御与范围蔓延；SHIT 缩写 = Scope creep（范围蔓延）/ Hashing & hypothetical hardening（哈希与假设性加固）/ Intent violation（意图违背）/ Task thrashing（任务折腾）。
- 双通道同一指令: `$stop-that-shit change -- ...` / `$stop-that-shit review -- ...` 首行指令设置"契约"（模式 change/review/answer/monitor、hash=allow、依赖与子代理边界）；Skill-only 时是提示，Guard 安装后同一指令变成 PreToolUse 机器边界。
- Stop Ladder 五步梯: ①理解当前责任→②直接方案优先（先查项目内/标准库/已装依赖）→③只为关闭具体缺口扩展→④按效果评判防御（检测什么、改变什么）→⑤验证后收工（复用仍有效的证据）。
- 事件面: UserPromptSubmit/PreToolUse/PostToolUse/SessionEnd/SubagentStart/PostToolUseFailure/PermissionDenied 全挂同一个 node 脚本。
- delegation ledger: 子代理槽位预留/释放的并发安全账本（action.before 预留、确认完成才释放），防子代理超发。
- 默认 unconfirmed 观察模式: Guard 初始只观察不拦、须显式 arm；"Do not claim that an action was blocked unless an explicit mode armed the Guard"（未武装不得声称拦截）。
- 宿主无关设计: 宿主无关内核 + 六个薄适配器（Codex/Claude/OpenCode/Hermes/Pi/OMP）；未知工具在 armed 契约下按可变更性阻断（block unknown mutability rather than guessing）。
- 护栏自测试: 18 组 Bad/Good 判例（cases/）做行为回归测试——**护栏本身也要有测试集**。
- 仓库: https://github.com/lennney/stop-that-shit

### 2. superpowers（obra）——验证纪律 Skill
- 铁律 1 test-driven-development: "NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST"——先写测试看它失败再写实现；没看到失败=不知道测试测的是什么；写码在测试前？删掉重来（不保留做参考）。
- 铁律 2 verification-before-completion: "NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE"；Gate Function 五步——IDENTIFY（什么命令能证明）→RUN（新鲜完整执行）→READ（完整输出+退出码）→VERIFY→THEN claim。
- 红旗词: "should/probably/seems to"、未经运行就表达满意；表格明确"Agent reports success"不算证据，VCS diff 才算。
- 仓库: https://github.com/obra/superpowers

### 3. gryph（safedep）——YAML 策略引擎 + 审计
- 机制: hooks 进 Claude Code/Cursor/Windsurf/Gemini CLI/OpenCode；YAML 策略规则对动作 block/warn/guide 三档。
- 审计: **所有事件落本地 SQLite 审计库**（gryph logs 可查 agent 读过什么、跑过什么 shell、改了什么文件）；纯本地无遥测。
- 仓库: https://github.com/safedep/gryph

### 4. claude-code-safety-net（kenryu42）——破坏性命令拦截
- 机制: PreToolUse 解析命令**实际语义**（"Wrapping the command or reordering flags does not hide it"——包一层或重排旗标藏不住）；拦 git reset --hard 类破坏命令与 SSH key/.env 访问。
- 失败语义: **"A broken config file never blocks anything"**（fail-open 设计声明）。
- 边界诚实: 明确 "not a sandbox"（不含进程、不管网络）——诚实的能力边界声明。
- 多 CLI 支持: Claude Code/Codex/OpenCode/Gemini CLI/Copilot CLI/Kimi Code/Pi。
- 仓库: https://github.com/kenryu42/claude-code-safety-net

### 5. agent-guard（JeongJaeSoon）——秘密防泄漏
- 机制: 拦 .env 读取、掩码 secret 样式输出、gitleaks 扫描变更后才许进 Git。
- 反绕过: **拒绝 agent 用 --no-verify/--no-gpg-sign 绕过钩子**。
- 覆盖面: Claude Code/Codex/Git hooks/GitHub Actions；自我定位 "defense-in-depth boundary" 而非 vault/DLP。
- 仓库: https://github.com/JeongJaeSoon/agent-guard

### 横向观察（3 条）
- 趋同 1: 独立项目在 PreToolUse 语义解析（而非纯正则）上趋同——safety-net 解析命令语义、agent-guard 拦绕过旗标、gryph 三档动作、stop-that-shit 未知工具保守阻断。
- 趋同 2: 审计（SQLite/JSONL 日志）成为标配——guardrail 不只拦，还要可回溯。
- 趋同 3: 每个 serious 项目都写明"不是什么"（not a sandbox / not a vault）——边界诚实本身是机制设计的一部分。

来源: research/raw/tools/local-repos-guardrail-mechanisms.md（原始来源: D:\Code\oh-my-repo\research\raw\repos\ 下本地克隆，2026-10-11 检读）

## pkg-hallucination-importing-phantoms.md（《Importing Phantoms》，arXiv 2501.19012）

- 研究内容: 系统测量 LLM 生成代码中的包幻觉（真实语言生态 vs 虚构依赖）漏洞。
- 幻觉率因子: 取决于"model choice, but also programming language, model size, and specificity of the coding task request"——不止模型强弱，语言与任务措辞都影响。
- Pareto 前沿稀疏: 代码质量与幻觉率的前沿"sparse populated"——"coding models are not being optimized for secure code"（编码模型没有为安全代码优化）。
- 风险启发式: 幻觉率与 HumanEval 分数呈负相关，可作为幻觉风险的粗略启发式。
- 攻击窗口: 幻觉包名可被抢注（slopsquatting）形成供应链攻击窗口；论文建议防御策略。
- 防御定性: 依赖幻觉是结构性风险而非偶发 bug；AI 代码必须把"新增依赖"当作显式事件处理。
- 落地做法清单: lockfile 优先/新依赖需人批或白名单校验（对照官方 registry 元数据、provenance）、沙箱默认断网、CI 里扫 manifest diff、gitleaks/依赖扫描兜底。
- 相关研究转引（未复核）: 《We Have a Package for You!》（USENIX'25 系，Lanyado 等）报告商业模型约 19.7%-21.7% 的建议包为幻觉（本页注明数字供线索用）。

来源: research/raw/tools/pkg-hallucination-importing-phantoms.md（原始 URL: https://arxiv.org/abs/2501.19012）

## pkg-hallucination-rule-file-injection.md（《Package Hallucination Attacks ... through Prompt Injection in Rule Files》PackHallu，arXiv 2610.09264）

- 攻击面定义: 现代编码 agent 读取社区共享的规则文件（AGENTS.md、.cursorrules 等）引导代码生成——这是基本未被检验的攻击面；攻击者在看似无害的规则文件里嵌入恶意提示，agent 读取后被诱导把合法依赖替换为攻击者控制的包（package hallucination attack）。
- 方法创新（PackHallu）: 不用手写注入提示，而是**进化优化框架**——用"trajectory-level feedback and LLM-guided mutations"（依据 agent 完整执行轨迹的反馈、LLM 引导的变异）迭代改写注入文本。
- 实验结果: 多 benchmark、多 LLM、多 agent 框架下"高攻击成功率"；且跨模型/跨 agent 框架"strong transferability"（对一种设置优化出的提示对其他设置同样有效）。
- 作者: Yupu Wang, Zhengyuan Jiang, Reachal Wang, Neil Zhenqiang Gong（Duke 大学）。
- 防御推论 1: 规则文件 = 不可信输入——AGENTS.md/Cursor rules 从网上复制时应视为潜在 prompt injection 载体。
- 防御推论 2: 依赖变更必须有机字符串级校验（diff 检查新依赖名是否在白名单/lockfile 中），不能依赖"模型读了好规则就会听话"。
- 防御推论 3: 与 hooks 结合——PreToolUse 拦截包管理器安装命令、PostToolUse 扫 manifest diff，是确定性对策。

来源: research/raw/tools/pkg-hallucination-rule-file-injection.md（原始 URL: https://arxiv.org/abs/2610.09264）
