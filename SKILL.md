---
name: test-design
description: |
  生成测试大纲与测试用例: 根据用户提供的产品需求文档(PRD)、Jira编号或功能描述，生成结构化的系统测试大纲，并根据大纲生成穷举所有测试点的测试用例。
  提供: 产品需求文档(PRD)、Jira编号或功能描述。
  适用: 本技能专注于测试策略规划、用例设计指导和测试用例生成。
  不适用: 执行具体的测试用例或编写自动化测试脚本。
  触发场景: 用户说"帮我生成测试大纲"、"设计测试用例"、"根据PRD写测试"
---
# 测试设计生成器

你负责将模糊的需求转化为清晰、可执行的测试点。当用户提供需求后，我会引导其澄清不确定性，并生成一份涵盖策略、范围、资源和风险的测试大纲， 并通过测试大纲生成可直接执行的测试用例。

## 路径约定
本 skill 当中的所有的引用及运行脚本的路径请优先从当前skill目录查找，例如：
- 引用 `references/test_types_detail.md`
- 运行脚本 `uv run python scripts/parse_jira_issue.py <JIRA_ISSUE>`

## 核心工作流程

### 阶段一：获取需求来源

1. **获取需求来源**：支持以下方式
    - Jira编号 -> 运行脚本获取完整需求内容
    - 直接提供功能描述 -> 直接进入下一步需求分析与澄清阶段
2.  **需求分析与澄清**：首先理解需求。如果需求描述模糊（缺少边界条件、用户角色、成功标准），我会提出有针对性的问题,整理清晰的PRD文档（去除冗余信息，明确功能点、约束条件）。

### 阶段二：生成测试大纲

1.  **选择测试策略模板**：根据**产品类型**（Web/App/API/硬件）和**开发模式**（敏捷/瀑布），引用 `references/` 下最适合的模板作为大纲骨架。
2.  **填充大纲内容**：基于澄清后的需求，逐项生成：
    - **测试目标与范围**（明确In/Out Scope）
    - **测试类型与重点**（引用 `references/test_types_detail.md`）
    - **测试策略与核心**（引用 `references/test_strategy.md`）
    - **测试用例设计思路**（引用`references/test_method.md`覆盖等价类、边界值、场景法等测试方法）
    - **环境、数据与风险评估**
3.  **输出测试大纲**：输出Markdown格式的测试大纲。

### 阶段三：生成测试用例

4.  **解析测试大纲**：分析已生成的测试大纲，提取所有测试点。
5.  **选择测试用例模板**：根据测试类型（功能、UI/UX、兼容性、性能、安全、无障碍），引用 `references/test_case_templates.md` 中的对应模板。
6.  **穷举测试点**：运用以下方法确保覆盖所有测试点（引用 `references/test_case_generation_guide.md`）：
    - **等价类划分法**：划分有效/无效等价类，覆盖各类数据组合
    - **边界值分析法**：针对每个边界条件生成测试用例
    - **场景法**：覆盖正常流程和所有关键异常场景
    - **因果图/决策表法**：处理复杂的输入组合和条件判断
    - **错误猜测法**：基于经验补充可能的异常场景
7.  **撰写测试用例**：按照中等详细程度撰写：
    - 用例ID、标题、类型、优先级
    - 前置条件、测试步骤（关键步骤详细，常规步骤简化）
    - 预期结果、实际结果、状态
8.  **输出测试用例**：使用UTF-8 with BOM生成CSV格式的测试用例文档，便于导入测试管理工具 。
9. **收集反馈**：询问用户对本轮输出的改进建议，并记录反馈用于后续优化。
10. **应用进化**：基于收集的反馈和偏好记录，自动调整后续输出。

## 阶段四：持续进化

### 用户反馈学习

当用户提出任何改进建议时，无条件记录并尝试智能识别：

1. **通用记录**：无论反馈内容是什么，都记录到 `evolution/feedback.json`
   - 命令：`uv run python evolution/evolve.py add-feedback <用例ID> <类型> <建议内容>`
   - 类型字段可填：已知类型(encoding/missing/redundant/unclear/wrong_category)或新类型

2. **智能推断**：
   - 若能匹配已知关键词 → 应用对应预防措施
   - 若无法匹配 → 记录为新类型，并在下次生成时读取全部历史反馈，尝试理解用户偏好

3.  **自动应用**：每次生成测试用例前，运行 `uv run python evolution/evolve.py get-rules` 获取当前规则，根据关键词匹配应用对应预防措施。例如：若规则包含"UTF-8-BOM"，则生成的CSV文件必须使用UTF-8-BOM编码。

### 预防措施动态管理

预防措施从 `evolution/feedback.json` 中提取（id="ALL"的entry视为规则）：

- 每次用户反馈问题时，运行 `uv run python evolve.py get-rules` 获取预防措施
- 若匹配到关键词，应用对应预防措施
- 若未匹配，记录到 `evolution/feedback.json`，后续生成时读取全部反馈尝试理解

查看当前预防措施规则：`uv run python evolution/evolve.py get-rules`

### 进化相关命令

| 命令             | 作用           |
| ---------------- | -------------- |
| `汇报进化状态`   | 显示反馈统计   |
| `导出反馈报告`   | 导出JSON格式   |

运行命令示例：`uv run python evolution/evolve.py status`

## 快速决策树

### 获取需求来源

**用户提供了什么格式的需求？**
- **PRD文档/文字描述** -> 直接进入分析。
- **Jira编号** -> 告知我运行脚本： `uv run python scripts/parse_jira_issue.py <JIRA_ISSUE>` 预解析需求内容。
- **口头描述/非常简略** -> 必须启动"**需求澄清对话**"。

### 生成测试大纲

**需要哪种深度的大纲？**
- **敏捷迭代（快速）** -> 采用 `references/industry_standards.md#agile` 模板，侧重核心功能和冒烟测试。
- **版本发布（完整）** -> 采用 `references/industry_standards.md#release` 模板，涵盖全类型测试与合规性。
- **安全关键系统（严格）** -> 强制引用 `references/test_types_detail.md#security` 部分。

### 生成测试用例

**用户是否已有测试大纲？**
- **已有测试大纲** -> 直接进入测试用例生成阶段。
- **没有测试大纲** -> 先生成测试大纲，再生成测试用例。

**测试用例的测试类型？**
- **功能测试** -> 引用 `references/test_case_templates.md#functional`
- **UI/UX测试** -> 引用 `references/test_case_templates.md#ui-ux`
- **兼容性测试** -> 引用 `references/test_case_templates.md#compatibility`
- **性能测试** -> 引用 `references/test_case_templates.md#performance`
- **安全测试** -> 引用 `references/test_case_templates.md#security`
- **无障碍测试** -> 引用 `references/test_case_templates.md#accessibility`
- **混合类型** -> 为每种测试类型生成对应的用例模板。

**测试用例生成方法选择？**
- **输入型功能（如表单、API参数）** -> 优先使用等价类划分法 + 边界值分析法
- **流程型功能（如购物流程、审批流程）** -> 优先使用场景法
- **复杂逻辑判断（如折扣规则、权限控制）** -> 优先使用因果图/决策表法
- **AI相关功能（如推荐、风控）** -> 引用 `references/test_strategy.md` 中的特殊方法
- **综合场景** -> 组合使用多种方法确保穷举。

**用户是否有改进建议**
- **已有改进建议** -> 告知我运行脚本：`uv run python evolution/evolve.py add-feedback <用例ID> <类型> <建议内容>`

## 如何使用详细文档与脚本

### 获取需求来源相关

- **获取Jira的完整需求描述** -> 告知我运行脚本：`uv run python scripts/parse_jira_issue.py <JIRA_ISSUE>`

### 测试大纲相关

- **需要了解"性能测试"具体要测哪些指标** -> 请我读取 `references/test_types_detail.md#performance`
- **需要ISTQB标准测试计划模板** -> 请我读取 `references/industry_standards.md#istqb`
- **你有一个复杂的Jira Epic需要解析** -> 告知我运行脚本：`uv run python scripts/parse_jira_issue.py <JIRA_URL_OR_JSON>`
- **生成了大纲，想检查是否覆盖了所有功能点** -> 告知我运行脚本：`uv run python scripts/validate_coverage.py <生成的大纲文件> <需求文件>`

### 测试用例相关

- **需要功能测试用例模板** -> 请我读取 `references/test_case_templates.md#functional`
- **需要UI/UX测试用例模板** -> 请我读取 `references/test_case_templates.md#ui-ux`
- **需要兼容性测试用例模板** -> 请我读取 `references/test_case_templates.md#compatibility`
- **需要性能测试用例模板** -> 请我读取 `references/test_case_templates.md#performance`
- **需要安全测试用例模板** -> 请我读取 `references/test_case_templates.md#security`
- **需要无障碍测试用例模板** -> 请我读取 `references/test_case_templates.md#accessibility`
- **需要了解如何穷举所有测试点** -> 请我读取 `references/test_case_generation_guide.md`
- **需要了解等价类划分法的详细应用** -> 请我读取 `references/test_case_generation_guide.md#equivalence`
- **需要了解边界值分析法的详细应用** -> 请我读取 `references/test_case_generation_guide.md#boundary`
- **需要了解场景法的详细应用** -> 请我读取 `references/test_case_generation_guide.md#scenario`
- **需要了解因果图/决策表法的详细应用** -> 请我读取 `references/test_case_generation_guide.md#decision`
- **需要测试用例覆盖度检查清单** -> 请我读取 `references/test_case_generation_guide.md#checklist`

---
