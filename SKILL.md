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

你负责将模糊的需求转化为清晰、可执行的测试点。当用户提供需求后，我会引导其澄清不确定性，并生成一份涵盖策略、范围、资源和风险的测试大纲，并通过测试大纲生成可直接执行的测试用例。

## 路径约定

本 skill 的所有脚本调用指定工作目录为当前skill目录，例如：
- 引用 `references/test_types_detail.md`
- 运行脚本：`uv run python scripts/parse_jira_issue.py <JIRA_ISSUE>`

## 迭代与冲突处理

### 阶段回退
- **返回上一阶段**：用户可随时要求返回上一阶段重新确认
- **增量更新**：在已有大纲/用例基础上修改时，只更新受影响部分，不重写全部。修改后清理因变更产生的孤儿引用（废弃的用例ID等）

### 冲突处理
当用户需求矛盾时：
1. 列出冲突点，说明影响
2. 提供可行方案供选择
3. 等待用户明确优先级
4. 如果用户方案过于复杂，主动提出简化建议

## 核心工作流程

### 阶段一：需求获取与提案（Proposal）

1. **获取需求来源**：支持以下方式
    - Jira编号 -> 运行脚本获取完整需求内容
    - 直接提供功能描述 -> 直接进入下一步需求分析与澄清阶段
2. **需求分析与澄清**：首先理解需求。如果需求描述模糊（缺少边界条件、用户角色、成功标准），我会提问以下问题：
    - **用户角色**：目标用户是谁？是否有不同角色权限？
    - **核心功能**：主要业务流程是什么？关键输入/输出？
    - **边界条件**：数据范围？长度限制？有效/无效值？
    - **成功标准**：怎样算成功？异常如何处理？
    - **环境依赖**：需要哪些系统/接口支持？
3. **输出需求确认书**：基于澄清结果，生成结构化需求确认书，包含：
    - **功能概述**：AI 重述需求
    - **关键假设**：目标用户、核心流程、边界条件
    - **待确认项**：列出的模糊点及选项
4. **确认门禁**：等待用户确认需求确认书。用户确认前不进入下一阶段。

**完成标准**：所有模糊点已澄清，关键假设已确认，用户同意需求方向。

### 阶段二：生成测试大纲

1. **选择测试策略模板**：根据**产品类型**（Web/App/API/硬件）和**开发模式**（敏捷/瀑布），引用 `references/` 下最适合的模板作为大纲骨架。
2. **填充大纲内容**：基于确认后的需求，逐项生成：
    - **测试目标与范围**（明确In/Out Scope）
    - **测试类型与重点**（引用 `references/test_types_detail.md`）
    - **测试策略与核心**（引用 `references/test_strategy.md`）
    - **测试用例设计思路**（引用 `references/test_case_generation_guide.md` 覆盖等价类、边界值、场景法等测试方法）
    - **环境、数据与风险评估**
3. **输出测试大纲**：输出Markdown格式的测试大纲，包含以下结构：
    - **文档信息**：标题、版本、编写日期、需求来源
    - **测试目标与范围**：In Scope / Out Scope
    - **测试类型与重点**：各类测试的测试项清单
    - **测试策略**：环境、数据、工具要求
    - **风险与 mitigation**：已识别风险及应对措施
4. **确认门禁**：等待用户确认测试大纲。用户可要求修改大纲，确认后进入测试用例生成阶段。

**完成标准**：大纲范围已确认，测试类型已覆盖全面，用户同意进入用例生成。

### 阶段三：生成测试用例

1. **解析测试大纲**：分析已生成的测试大纲，提取所有测试点。
2. **选择测试用例模板**：根据测试类型（功能、UI/UX、兼容性、性能、安全、无障碍），引用 `references/test_case_templates.md` 中的对应模板。
3. **穷举测试点**：运用以下方法确保覆盖所有测试点（引用 `references/test_case_generation_guide.md`）：
    - **等价类划分法**：划分有效/无效等价类，覆盖各类数据组合
    - **边界值分析法**：针对每个边界条件生成测试用例
    - **场景法**：覆盖正常流程和所有关键异常场景
    - **因果图/决策表法**：处理复杂的输入组合和条件判断
    - **错误猜测法**：基于经验补充可能的异常场景
4. **撰写测试用例**：按照中等详细程度撰写：
    - 用例ID、标题、类型、优先级
    - 前置条件、测试步骤（关键步骤详细，常规步骤简化）
    - 预期结果、实际结果、状态
5. **选择输出格式**：询问用户偏好的输出格式：
    - **Markdown 表格**（默认）：适合审查和协作
    - **CSV 文件**（UTF-8 with BOM）：适合导入测试管理工具（如 TestRail、Jira）
    - **两者都要**
6. **输出测试用例**：按选定格式输出。
7. **收集反馈**：询问用户对本轮输出的改进建议，并记录反馈用于后续优化（见阶段四）。

**完成标准**：测试点已穷举，用例格式正确，用户反馈已记录。

## 阶段四：持续进化

### 用户反馈学习

当用户提出任何改进建议时，无条件记录到 `evolution/feedback.json`（AI 直接写文件，保持 JSON 格式一致）：

```json
{
  "entries": [
    {
      "id": "ALL",
      "feedback_type": "encoding",
      "comment": "CSV中文显示乱码，使用UTF-8 with BOM编码",
      "timestamp": "2026-04-27T10:00:00",
      "resolved": false
    }
  ]
}
```

- 若反馈适用于所有场景，`id` 填 `"ALL"`
- 若反馈针对特定用例，`id` 填对应用例ID（如 `TC-FUNC-LOGIN-001`）
- 类型字段可填：`encoding`/`missing`/`redundant`/`unclear`/`wrong_category` 或新增类型

### 预防措施自动应用

每次生成测试用例前，读取 `evolution/feedback.json` 中 `id == "ALL"` 的条目作为预防措施规则：
- 根据 `feedback_type` 和 `comment` 了解具体改进要求
- 自动应用到本次输出中

### 查询进化统计

手动查询反馈统计：`uv run python evolution/evolve.py status`

## 快速决策树

### 用户提供了什么？

| 输入类型 | 进入阶段 |
|----------|----------|
| 功能想法/需求描述 | → 阶段一：需求获取与提案 |
| Jira编号 | → 运行脚本获取需求后进入阶段一 |
| 已有确认的需求 | → 阶段二：生成测试大纲 |
| 已有测试大纲，想生成用例 | → 阶段三：生成测试用例 |
| "帮我看看这个测试大纲/用例有什么问题" | → Review 模式 |

### 获取需求来源

**需求详细程度？**
- **非常模糊（一句话）** -> 启动需求澄清对话，输出需求确认书供确认
- **中等（有功能描述）** -> 直接进入需求分析与提案
- **较完整（有PRD）** -> 可跳过部分澄清，但仍输出需求确认书供确认

### 生成测试大纲

**需要哪种深度的大纲？**
- **敏捷迭代（快速）** -> 采用 `references/industry_standards.md#agile` 模板，侧重核心功能和冒烟测试。
- **版本发布（完整）** -> 采用 `references/industry_standards.md#release` 模板，涵盖全类型测试与合规性。
- **安全关键系统（严格）** -> 采用 `references/industry_standards.md#safety-critical` 模板。

### 生成测试用例

**用户是否已有测试大纲？**
- **已有测试大纲** -> 直接进入测试用例生成阶段。
- **没有测试大纲** -> 先生成测试大纲，再生成测试用例（需经确认门禁）。

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

### Review 模式

当用户提供已有测试大纲或测试用例要求评审时：

1. **完整性检查**：检查是否覆盖所有功能点和边界条件
2. **一致性检查**：检查用例ID命名、优先级设置、测试类型分类是否一致
3. **可执行性检查**：检查测试步骤是否具体、预期结果是否可验证
4. **风险评估**：识别潜在的测试盲区或遗漏的高风险场景

## 如何使用详细文档与脚本

### 获取需求来源相关

- **获取Jira的完整需求描述** -> 告知我运行脚本：`uv run python scripts/parse_jira_issue.py <JIRA_ISSUE>`

### 测试大纲相关

- **需要了解各类测试类型的详细指标** -> 请我读取 `references/test_types_detail.md`
- **需要测试大纲模板参考** -> 请我读取 `references/industry_standards.md`
- **你有一个复杂的Jira Epic需要解析** -> 告知我运行脚本：`uv run python scripts/parse_jira_issue.py <JIRA_URL_OR_JSON>`
- **生成了大纲，想检查是否覆盖了所有功能点** -> 手动对照需求文件逐项核对需求列表与大纲测试项

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
