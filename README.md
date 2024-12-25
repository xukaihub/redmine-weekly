# Redmine Weekly Report Generator

一个用于生成 Redmine 周报和年度总结的工具。

## 功能特点

- 生成指定日期所在周的工作报告
- 生成当前周的工作报告
- 生成整年的周报汇总
- 生成年度工作总结
- 支持按项目分类统计
- 支持状态分布统计
- 支持月度趋势分析

## 安装

1. 克隆仓库:

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

3. 配置:

复制 `config.ini.example` 为 `config.ini` 并填写相关配置:

```ini
[redmine]
url = https://your-redmine-url
username = your-username
password = your-password
user_id = your-user-id
```

## 使用方法

### 基本用法

```bash
# 生成本周的周报
python redmine_weekly_report.py

# 生成指定日期所在周的周报
python redmine_weekly_report.py -d 2024-03-15

# 生成指定年份的所有周报
python redmine_weekly_report.py -a -y 2024
```

### 命令行参数

- `-h, --help`: 显示帮助信息
- `-d DATE, --date DATE`: 生成指定日期所在周的报告 (格式: YYYY-MM-DD)
- `-a, --all`: 生成整年的所有周报
- `-y YEAR, --year YEAR`: 指定年份 (默认为当前年份)

### 输出文件

报告将保存在 `weekly_reports_YYYY` 目录下:

- `week_XX_YYYYMMDD-YYYYMMDD.md`: 单周报告
- `weekly_summary_YYYY.md`: 年度周报汇总 (仅在生成整年报告时创建)
- `yearly_summary_YYYY.md`: 年度工作总结 (仅在生成整年报告时创建)

## 配置说明

### config.ini

```ini
[redmine]
url = https://your-redmine-url # Redmine 服务器地址
username = your-username # 用户名
password = your-password # 密码
user_id = your-user-id # 用户 ID
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

