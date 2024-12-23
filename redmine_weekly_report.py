from redminelib import Redmine
from datetime import datetime, timedelta
import pytz
from collections import defaultdict
import os
import configparser

class RedmineWeeklyReport:
    def __init__(self, url, username=None, password=None, api_key=None):
        # 初始化Redmine连接
        if username and password:
            self.redmine = Redmine(url, username=username, password=password)
        elif api_key:
            self.redmine = Redmine(url, api_key=api_key)
        else:
            raise ValueError("Username and password or API key must be provided")
        
        # 设置时区为亚洲/上海
        self.timezone = pytz.timezone('Asia/Shanghai')

    def get_date_range(self):
        """获取上周的日期范围"""
        today = datetime.now(self.timezone)
        # 获取上周一和上周日的日期
        last_monday = today - timedelta(days=today.weekday() + 7)
        last_sunday = last_monday + timedelta(days=6)
        return last_monday.date(), last_sunday.date()

    def get_user_activities(self, user_id, start_date, end_date):
        """获取指定用户在日期范围内的活动"""
        activities = defaultdict(list)
        
        try:
            # 只获取问题更新
            issues = self.redmine.issue.filter(
                updated_on=f"><{start_date}|{end_date}",
                author_id=user_id,
                status_id='*'
            )
            
            # 存储问题更新
            activities['issues'] = list(issues)
            
            print(f"Debug: Found {len(activities['issues'])} issues")
            
        except Exception as e:
            print(f"Error fetching activities: {str(e)}")
        
        return activities

    def get_monday_sunday(self):
        """获取本周的周一和周日日期"""
        today = datetime.now(self.timezone)
        monday = today - timedelta(days=today.weekday())
        sunday = monday + timedelta(days=6)
        return monday.date(), sunday.date()

    def categorize_issues(self, issues):
        """将问题按项目分类"""
        categories = defaultdict(list)
        for issue in issues:
            try:
                project_name = issue.project.name if hasattr(issue, 'project') else '其他'
                categories[project_name].append(issue)
            except AttributeError as e:
                print(f"Warning: Failed to categorize issue {issue.id}: {str(e)}")
                categories['其他'].append(issue)
        return categories

    def get_year_weeks(self, year=None):
        """获取指定年份的所有周一和周日日期"""
        if year is None:
            year = datetime.now(self.timezone).year
        
        # 获取该年第一天
        first_day = datetime(year, 1, 1, tzinfo=self.timezone)
        
        # 调整到第一个周一
        first_monday = first_day - timedelta(days=first_day.weekday())
        
        # 获取该年最后一天
        last_day = datetime(year, 12, 31, tzinfo=self.timezone)
        
        weeks = []
        current = first_monday
        while current.year <= year:
            monday = current.date()
            sunday = (current + timedelta(days=6)).date()
            if sunday.year >= year:  # 确保至少包含该年的某一天
                weeks.append((monday, sunday))
            current += timedelta(days=7)
        
        return weeks

    def generate_yearly_reports(self, user_id, year=None):
        """生成整年的周报"""
        if year is None:
            year = datetime.now(self.timezone).year
        
        weeks = self.get_year_weeks(year)
        reports = []
        
        print(f"Generating reports for {year}, total {len(weeks)} weeks...")
        
        for i, (monday, sunday) in enumerate(weeks, 1):
            print(f"Processing week {i}/{len(weeks)}: {monday} to {sunday}")
            activities = self.get_user_activities(user_id, monday, sunday)
            
            if any(activities.values()):  # 只保存有活动的周报
                report = self.generate_weekly_report(user_id, monday, sunday)
                reports.append((monday, sunday, report))
        
        return reports

    def generate_weekly_report(self, user_id, monday=None, sunday=None):
        """生成周报"""
        if monday is None or sunday is None:
            monday, sunday = self.get_monday_sunday()
        
        activities = self.get_user_activities(user_id, monday, sunday)
        
        report = f"# 本周工作总结\n\n"
        report += f"**时间范围：** {monday.strftime('%Y-%m-%d')} 至 {sunday.strftime('%Y-%m-%d')}\n\n"
        
        if not activities['issues']:
            report += "> 本周无记录的活动\n"
            return report
        
        # 问题更新（按项目分类）
        report += "## 问题处理\n\n"
        categorized_issues = self.categorize_issues(activities['issues'])
        
        # 按项目名称排序
        for project_name in sorted(categorized_issues.keys()):
            report += f"### {project_name}\n\n"
            for issue in categorized_issues[project_name]:
                try:
                    status = issue.status.name if hasattr(issue, 'status') else '未知状态'
                    report += f"- [{issue.subject}]({self.redmine.url}/issues/{issue.id}) (#{issue.id}) [{status}]\n"
                except AttributeError as e:
                    print(f"Warning: Failed to process issue {issue.id}: {str(e)}")
            report += "\n"
        
        return report

    def generate_yearly_summary(self, reports, user_id):
        """生成按项目分类的年度总结"""
        project_issues = defaultdict(list)
        all_issues = []
        
        # 遍历所有周报，收集问题
        for monday, sunday, report in reports:
            activities = self.get_user_activities(user_id, monday, sunday)
            if activities['issues']:
                all_issues.extend(activities['issues'])
                categorized = self.categorize_issues(activities['issues'])
                for project, issues in categorized.items():
                    project_issues[project].extend(issues)
        
        # 生成年度总结
        summary = f"# {monday.year}年工作总结\n\n"
        
        # 添加年度概述
        summary += "## 年度概述\n\n"
        
        # 统计数据
        total_issues = len(all_issues)
        total_projects = len(project_issues)
        status_count = defaultdict(int)
        for issue in all_issues:
            status = issue.status.name if hasattr(issue, 'status') else '未知状态'
            status_count[status] += 1
        
        # 生成统计表格
        summary += "### 数据统计\n\n"
        summary += "| 指标 | 数值 |\n"
        summary += "|------|------|\n"
        summary += f"| 处理问题总数 | {total_issues} |\n"
        summary += f"| 涉及项目数 | {total_projects} |\n"
        for status, count in sorted(status_count.items()):
            summary += f"| {status}问题数 | {count} |\n"
        summary += "\n"
        
        # 项目分布
        summary += "### 项目分布\n\n"
        summary += "| 项目 | 问题数 | 占比 |\n"
        summary += "|------|--------|------|\n"
        for project, issues in sorted(project_issues.items(), key=lambda x: len(x[1]), reverse=True):
            count = len(issues)
            percentage = (count / total_issues) * 100
            summary += f"| {project} | {count} | {percentage:.1f}% |\n"
        summary += "\n"
        
        # 月度趋势
        monthly_count = defaultdict(int)
        for issue in all_issues:
            month = issue.updated_on.strftime('%Y-%m')
            monthly_count[month] += 1
        
        summary += "### 月度趋势\n\n"
        summary += "| 月份 | 问题数 |\n"
        summary += "|------|--------|\n"
        for month in sorted(monthly_count.keys()):
            summary += f"| {month} | {monthly_count[month]} |\n"
        summary += "\n"
        
        # 添加分隔线
        summary += "---\n\n"
        
        # 按项目详细列表
        summary += "## 项目详细\n\n"
        for project_name in sorted(project_issues.keys()):
            summary += f"### {project_name}\n\n"
            status_issues = defaultdict(list)
            for issue in project_issues[project_name]:
                status = issue.status.name if hasattr(issue, 'status') else '未知状态'
                status_issues[status].append(issue)
            
            for status in sorted(status_issues.keys()):
                summary += f"#### {status}\n\n"
                for issue in status_issues[status]:
                    summary += f"- [{issue.subject}]({self.redmine.url}/issues/{issue.id}) (#{issue.id})\n"
                summary += "\n"
            
            summary += "---\n\n"
        
        return summary

def load_config():
    """加载配置文件"""
    config = configparser.ConfigParser()
    config_file = 'config.ini'
    
    if not os.path.exists(config_file):
        raise FileNotFoundError(f"配置文件 {config_file} 不存在")
    
    config.read(config_file, encoding='utf-8')
    return config

def main():
    # 加载配置
    config = load_config()
    
    # 获取配置信息
    REDMINE_URL = config['redmine']['url']
    USERNAME = config['redmine']['username']
    PASSWORD = config['redmine']['password']
    USER_ID = config['redmine'].getint('user_id')
    YEAR = config['report'].getint('year')
    
    # 创建报告实例
    reporter = RedmineWeeklyReport(REDMINE_URL, username=USERNAME, password=PASSWORD)
    
    # 生成整年报告
    reports = reporter.generate_yearly_reports(USER_ID, YEAR)
    
    # 保存所有报告
    if reports:
        # 创建年度报告目录
        report_dir = f'weekly_reports_{YEAR}'
        os.makedirs(report_dir, exist_ok=True)
        
        # 保存每周报告
        for monday, sunday, report in reports:
            # 使用周数作为文件名
            week_num = monday.isocalendar()[1]
            filename = f'{report_dir}/week_{week_num:02d}_{monday.strftime("%Y%m%d")}-{sunday.strftime("%Y%m%d")}.md'
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"Saved report to {filename}")
        
        # 生成周报汇总
        weekly_summary = f"# {YEAR}年工作周报汇总\n\n"
        for monday, sunday, report in reports:
            week_num = monday.isocalendar()[1]
            weekly_summary += f"## 第{week_num}周 ({monday.strftime('%Y-%m-%d')} 至 {sunday.strftime('%Y-%m-%d')})\n\n"
            weekly_summary += report + "\n---\n\n"
        
        # 生成年度项目总结
        yearly_summary = reporter.generate_yearly_summary(reports, USER_ID)
        
        # 保存周报汇总
        weekly_summary_file = f'{report_dir}/weekly_summary_{YEAR}.md'
        with open(weekly_summary_file, 'w', encoding='utf-8') as f:
            f.write(weekly_summary)
        print(f"Saved weekly summary to {weekly_summary_file}")
        
        # 保存年度项目总结
        yearly_summary_file = f'{report_dir}/yearly_summary_{YEAR}.md'
        with open(yearly_summary_file, 'w', encoding='utf-8') as f:
            f.write(yearly_summary)
        print(f"Saved yearly summary to {yearly_summary_file}")
    else:
        print("No reports generated.")

if __name__ == '__main__':
    main() 