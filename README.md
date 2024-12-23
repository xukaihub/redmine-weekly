# Redmine Weekly Report Generator

一个用于生成 Redmine 周报和年度工作总结的 Python 工具。

## 功能特点

- 自动获取 Redmine 上的工作记录
- 按项目分类展示问题处理情况
- 支持生成单周报告和年度汇总
- 自动保存为 Markdown 格式文件
- 支持中文项目名称和状态显示
- 生成年度统计概述（含数据统计、项目分布、月度趋势）

## 目录结构
```
├── README.md # 说明文档
├── redmine_weekly_report.py # 主程序
└── weekly_reports_2024/ # 生成的报告目录
├── yearly_summary_2024.md # 年度汇总报告
└── week_/ # 各周报告
```

## 安装

1. 克隆仓库：

```bash
git clone https://github.com/xukaihub/redmine-weekly.git
cd redmine-weekly
```

2. 安装依赖：
```bash
python3 -m venv venv
source venv/bin/activate
pip install python-redmine pytz
```

## 配置

创建 `config.ini` 配置文件：

```ini
[redmine]
url = https://git.nationalchip.com/redmine  # Redmine服务器地址
username = your-username                     # 用户名
password = your-password                     # 密码
user_id = 1234                              # 用户ID（数字）

[report]
year = 2024                                 # 要生成报告的年份
```

## 使用方法

1. 复制并修改配置文件：
```bash
cp config.ini.example config.ini
# 编辑 config.ini 填入你的配置
```

2. 运行程序生成报告：
```bash
python redmine_weekly_report.py
```

2. 程序会自动：
   - 创建 `weekly_reports_2024` 目录
   - 生成每周的工作报告
   - 生成年度汇总报告

## 报告格式

### 周报格式

```markdown
# 本周工作总结

**时间范围：** 2024-01-01 至 2024-01-07

### 项目名称
- [问题标题](问题链接) (#问题编号) [问题状态]
```

### 年度汇总格式

```markdown
# 2024年工作总结

## 年度概述

### 数据统计

| 指标 | 数值 |
|------|------|
| 处理问题总数 | 157 |
| 涉及项目数 | 5 |
| 已解决问题数 | 123 |
| 进行中问题数 | 28 |
| 待处理问题数 | 6 |

### 项目分布

| 项目 | 问题数 | 占比 |
|------|--------|------|
| GoXceed软件平台 | 78 | 49.7% |
| 软件基础平台 | 45 | 28.7% |
| Aquila软件平台 | 20 | 12.7% |
| Draco软件平台 | 14 | 8.9% |

### 月度趋势

| 月份 | 问题数 |
|------|--------|
| 2024-01 | 35 |
| 2024-02 | 42 |
| 2024-03 | 28 |
| 2024-04 | 31 |
| 2024-05 | 21 |

---

## 项目详细

### GoXceed软件平台

#### 已解决
- [修复音频驱动问题](问题链接) (#397457)
- [更新驱动文档](问题链接) (#397458)

#### 进行中
- [优化性能问题](问题链接) (#397460)

---

### 软件基础平台

#### 已解决
- [更新构建脚本](问题链接) (#397238)

---
```

## 注意事项

1. 确保有正确的 Redmine 访问权限
2. 用户ID需要使用数字ID，可以从个人资料页面URL获取
3. 只会生成有活动记录的周报
4. 建议先测试单周再生成年度报告

## 常见问题

1. 认证失败
   - 检查用户名和密码是否正确
   - 确认 Redmine 服务器地址是否正确

2. 找不到活动记录
   - 确认用户ID是否正确
   - 检查指定时间范围内是否有活动

## 贡献

欢迎提交 Issue 和 Pull Request

## License

MIT License

## 作者

xukai(xukai@nationalchip.com)

