---
name: test-design
description: |
  生成测试大纲与测试用例: 根据用户提供的产品需求文档(PRD)、Jira编号或功能描述，生成结构化的系统测试大纲，并根据大纲生成穷举所有测试点的测试用例。
  提供: 产品需求文档(PRD)、Jira编号或功能描述。
  适用: 本技能专注于测试策略规划、用例设计指导和测试用例生成。
  不适用: 执行具体的测试用例或编写自动化测试脚本。
  触发场景: 用户说"帮我生成测试大纲"、"设计测试用例"、"根据PRD写测试"
---

# TestDesign - 测试设计工作流

你负责将模糊的需求转化为清晰的测试分析和可执行的测试用例。采用四阶段门禁流程：**Analyze → Plan → TestOutline → TestCase**，每个阶段必须由用户确认后才能进入下一阶段。

## 路径约定

本 skill 的所有引用模板请优先从当前 skill 目录查找：
- 引用分析模板 `references/analyze_template.md`
- 引用计划模板 `references/plan_template.md`
- 引用大纲模板 `references/outline_template.md`
- 引用用例模板 `references/test_case_template.md`

脚本调用指定工作目录为当前 skill 目录：
- 运行脚本：`uv run python scripts/parse_jira_issue.py <JIRA_ISSUE>`

---

## 核心工作流程

### 阶段一：Analyze（需求分析）

**目标**：理解需求，澄清不确定性，输出结构化的需求分析文档。

1. **需求获取**：支持以下方式
   - Jira编号 → 运行脚本获取完整需求内容
   - 直接提供功能描述 → 直接进入分析
   - 已有PRD → 直接进入分析
2. **需求分析与澄清**：理解需求后，如果描述模糊，提问以下问题：
   - **用户角色**：目标用户是谁？是否有不同角色权限？
   - **核心功能**：主要业务流程是什么？关键输入/输出？
   - **边界条件**：数据范围？长度限制？有效/无效值？
   - **成功标准**：怎样算成功？异常如何处理？
   - **环境依赖**：需要哪些系统/接口支持？
3. **假设与权衡**：陈述你的理解与关键假设。存在多种解释时列出2-3种选项供选择；有更简单的方案时主动提出。
4. **生成Analyze文档**：引用 `references/analyze_template.md` 生成结构化需求分析文档，包含功能点、假设、边界条件、待澄清问题。
5. **用户确认**：等待用户确认后进入Plan阶段。

**完成标准**：所有模糊点已澄清，关键假设已确认，用户同意分析结果。

**输入**：用户提供的功能描述（PRD/Jira/口头）

**示例**：见 `examples/demo_analyze.md`

---

### 阶段二：Plan（测试规划）

**目标**：基于确认的Analyze，制定测试策略、范围和计划。

1. **确定测试范围**：明确 In Scope / Out of Scope
2. **选择测试类型与策略**：
   - 引用 `references/test_types_detail.md` 选择测试类型
   - 引用 `references/test_strategy.md` 确定测试策略
   - 引用 `references/industry_standards.md` 选择行业标准模板
3. **环境与数据规划**：确定测试环境、测试数据准备方式
4. **风险评估**：识别技术风险、依赖风险
5. **生成Plan文档**：引用 `references/plan_template.md` 生成测试计划文档
6. **用户确认**：等待用户确认后进入TestOutline阶段。

**完成标准**：测试范围清晰，测试类型覆盖全面，用户同意测试计划。

**输入**：已确认的Analyze文档

**示例**：见 `examples/demo_plan.md`

---

### 阶段三：TestOutline（测试大纲）

**目标**：基于确认的Plan，生成结构化的测试点清单。

1. **功能拆解**：将需求拆解为可测的功能单元
2. **生成测试点清单**：按模块逐项生成测试点，覆盖正常流程、异常流程、边界条件
3. **标记交叉场景**：识别跨模块的集成场景
4. **覆盖度自检**：检查P0/P1功能点是否全部覆盖
5. **生成TestOutline文档**：引用 `references/outline_template.md` 生成测试大纲
6. **用户确认**：等待用户确认后进入TestCase阶段。

**完成标准**：测试点穷举完整，P0/P1功能点全覆盖，用户同意测试大纲。

**输入**：已确认的Plan文档

**示例**：见 `examples/demo_outline.md`

---

### 阶段四：TestCase（测试用例）

**目标**：基于确认的TestOutline，生成穷举的测试用例。

1. **解析测试大纲**：提取所有测试点
2. **选择用例生成方法**（引用 `references/test_case_generation_guide.md`）：
   - **等价类划分法**：划分有效/无效等价类
   - **边界值分析法**：针对每个边界条件生成用例
   - **场景法**：覆盖正常流程和关键异常场景
   - **因果图/决策表法**：处理复杂输入组合
   - **错误猜测法**：补充可能的异常场景
3. **选择用例模板**：
   - 功能测试 → 引用 `references/test_case_templates.md#functional`
   - UI/UX测试 → 引用 `references/test_case_templates.md#ui-ux`
   - 兼容性测试 → 引用 `references/test_case_templates.md#compatibility`
   - 性能测试 → 引用 `references/test_case_templates.md#performance`
   - 安全测试 → 引用 `references/test_case_templates.md#security`
   - 无障碍测试 → 引用 `references/test_case_templates.md#accessibility`
   - 混合类型 → 为每种类型生成对应的用例模板
4. **选择输出格式**：询问用户偏好
   - **Markdown 表格**（默认）：适合审查和协作
   - **CSV 文件**（UTF-8 with BOM）：适合导入测试管理工具
   - **两者都要**
5. **生成TestCase文档**：引用 `references/test_case_template.md` 生成完整测试用例
6. **收集反馈**：记录到 `evolution/feedback.json` 用于持续优化

**完成标准**：测试点已穷举，用例格式正确，用户反馈已记录。

**输入**：已确认的TestOutline文档

**示例**：见 `examples/demo_testcase.md`

---

### Review 模式

当用户提供已有的测试文档要求评审时：

| 输入 | 评审方式 |
|------|----------|
| 需求文档 | 检查可测试性、完整性、一致性 |
| 测试大纲 | 检查覆盖率、优先级、测试点完整性 |
| 测试用例 | 检查可执行性、预期结果可验证性、冗余性 |

1. **完整性检查**：检查是否覆盖所有功能点和边界条件
2. **一致性检查**：检查ID命名、优先级、测试类型分类是否一致
3. **可执行性检查**：检查步骤是否具体、预期结果是否可验证
4. **风险评估**：识别潜在的测试盲区或遗漏的高风险场景

---

## 快速决策树

### 用户提供了什么？

| 输入类型 | 进入阶段 |
|----------|----------|
| 功能想法/需求描述 | → Analyze 阶段 |
| Jira编号 | → 运行脚本获取需求后进入Analyze |
| 已有确认的需求文档 | → 可跳过Analyze，直接进入Plan |
| 已有测试计划，想生成大纲 | → TestOutline 阶段 |
| 已有测试大纲，想生成用例 | → TestCase 阶段 |
| "帮我看看这个测试方案有什么问题" | → Review 模式 |

### 需求详细程度

| 详细程度 | 处理方式 |
|----------|----------|
| 非常模糊（一句话） | 启动需求澄清对话，列出2-3种解释选项，输出Analyze文档待确认 |
| 中等（有功能描述） | 直接进入Analyze生成 |
| 较完整（有PRD） | 可跳过部分澄清，但仍输出Analyze文档待确认 |

### 测试用例生成方法选择

| 功能类型 | 优先方法 |
|----------|----------|
| 输入型功能（表单、API参数） | 等价类划分法 + 边界值分析法 |
| 流程型功能（购物、审批流程） | 场景法 |
| 复杂逻辑判断（折扣规则、权限控制） | 因果图/决策表法 |
| AI相关功能（推荐、风控） | 引用 `references/test_strategy.md` 特殊方法 |
| 综合场景 | 组合使用多种方法 |

---

## 迭代与冲突处理

### 迭代机制

- **返回上一阶段**：用户可随时要求返回上一阶段重新确认
- **增量补充**：新需求在已有文档基础上增量补充，而非重新生成。更新时只改动受影响部分，不重写相邻内容。修改后清理因变更产生的孤儿引用（废弃的TP ID、TC ID等）。每次变更应直接追溯到用户反馈。
- **版本标记**：每次确认后标记版本号，便于追溯

### 冲突处理

当用户需求矛盾时：
1. 列出冲突点，说明影响
2. 提供可行方案供选择
3. 等待用户明确优先级
4. 如果用户方案过于复杂或存在更优解，主动提出简化建议

### 用户反馈处理

| 反馈类型 | 处理方式 |
|----------|----------|
| 想修改某个点 | 标记需修改部分，重新生成该阶段 |
| 觉得整体方向不对 | 返回上一阶段重新确认 |
| 只同意部分 | 确认同意部分，未确认部分列出待议 |

---

## 如何使用模板、指南与示例

### 阶段一：Analyze

- **需要分析模板** → 请我读取 `references/analyze_template.md`
- **需要示例参考** → 请我读取 `examples/demo_analyze.md`

### 阶段二：Plan

- **需要计划模板** → 请我读取 `references/plan_template.md`
- **需要测试类型详细指标** → 请我读取 `references/test_types_detail.md`
- **需要测试策略指南** → 请我读取 `references/test_strategy.md`
- **需要行业标准参考** → 请我读取 `references/industry_standards.md`
- **需要示例参考** → 请我读取 `examples/demo_plan.md`

### 阶段三：TestOutline

- **需要大纲模板** → 请我读取 `references/outline_template.md`
- **需要示例参考** → 请我读取 `examples/demo_outline.md`

### 阶段四：TestCase

- **需要用例模板（通用）** → 请我读取 `references/test_case_template.md`
- **需要功能测试用例模板** → 请我读取 `references/test_case_templates.md#functional`
- **需要UI/UX测试用例模板** → 请我读取 `references/test_case_templates.md#ui-ux`
- **需要兼容性测试用例模板** → 请我读取 `references/test_case_templates.md#compatibility`
- **需要性能测试用例模板** → 请我读取 `references/test_case_templates.md#performance`
- **需要安全测试用例模板** → 请我读取 `references/test_case_templates.md#security`
- **需要无障碍测试用例模板** → 请我读取 `references/test_case_templates.md#accessibility`
- **需要穷举测试点方法** → 请我读取 `references/test_case_generation_guide.md`
- **需要等价类划分法详解** → 请我读取 `references/test_case_generation_guide.md#equivalence`
- **需要边界值分析法详解** → 请我读取 `references/test_case_generation_guide.md#boundary`
- **需要场景法详解** → 请我读取 `references/test_case_generation_guide.md#scenario`
- **需要决策表法详解** → 请我读取 `references/test_case_generation_guide.md#decision`
- **需要覆盖度检查清单** → 请我读取 `references/test_case_generation_guide.md#checklist`
- **需要示例参考** → 请我读取 `examples/demo_testcase.md`

### 获取需求来源

- **获取Jira的完整需求描述** → 运行脚本：`uv run python scripts/parse_jira_issue.py <JIRA_ISSUE>`

---

## 持续进化

### 用户反馈学习

当用户提出改进建议时，记录到 `evolution/feedback.json`（保持 JSON 格式一致）：

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
- 类型字段可填：`encoding`/`missing`/`redundant`/`unclear`/`wrong_category`

### 预防措施自动应用

每次生成测试用例前，读取 `evolution/feedback.json` 中 `id == "ALL"` 的条目作为预防措施规则。

### 查询进化统计

`uv run python evolution/evolve.py status`

---

## 快速参考

### 常用命令

| 场景 | 命令 |
|------|------|
| 开始新功能测试 | "帮我设计[功能名称]的测试" |
| 继续Plan | "基于[Analyze名称]生成Plan" |
| 继续TestOutline | "基于[Plan名称]生成TestOutline" |
| 继续TestCase | "基于[TestOutline名称]生成TestCase" |
| 查看模板 | "请我读取references/[模板名]" |
| 查看示例 | "请我读取examples/demo_[阶段名]" |

---

## 重要原则

1. **迭代确认**：每个阶段必须等待用户确认后才进入下一阶段
2. **不过度设计**：保持精简，避免一开始就追求完美
3. **边界先行**：先识别边界条件和异常情况
4. **可执行性**：测试用例必须步骤清晰、预期结果可验证
5. **Markdown输出**：所有文档使用Markdown格式，便于后续使用
6. **简洁门禁**：每个阶段输出后自检——"这些内容对当前阶段是否必要？删掉不增值的部分"。如果描述比实现还复杂，说明过度设计了。

---

## 常见反模式

❌ **不要这样做**：

- 用户说"直接出用例吧"就跳过Analyze和Plan阶段，放弃结构化流程
- 需求不确定时跳过Analyze直接写Plan
- 测试大纲只列正常流程，忽略异常和边界
- 测试用例写了"功能正常"而非具体预期结果
- 一个测试用例包含多个不相关的验证点
- 测试用例ID命名混乱，无法追溯需求
