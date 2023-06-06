"""
[['工号', '姓名', '性别', '职称'], ['jpq01', 'Peiquan Jin', 1, 6]]
[['课程号', '课程名', '主讲学时', '年份', '学期'], ['CSCOMP001', '数据库系统及应用', 50, 2023, 1], ['CSCOMP011', '高级数据库系统', 70, 2022, 1]]
[['论文名', '发表源头', '发表年份', '类型', '级别', '排名', '是否通讯作者'], ['ZB+tree:一种ZNS SSD感知的新型索引结构', '计算机研究与发展', 2023, 1, 4, 2, True], ['ZoneKV: A Space-Efficient Key-Value Store for ZNS SSDs', 'DAC', 2023, 1, 1, 2, True]]
[['项目名称', '项目来源', '项目类型', '开始年份', '结束年份', '项目总经费', '承担经费'], ['面向异构混合内存的NVM感知索引及自适应学习方法研
究', '国家自然科学基金委', 1, 2021, 2024, 580000.0, 300000.0], ['量子安全数据库系统关键技术研发及产业化', '安徽省科技厅', 2, 2022, 2025, 2000000.0, 1000000.0]]
"""


"""
h1 center 教师教学科研工作统计
h2 教师基本信息
工号:01234 姓名:张三 性别:男 职称:教授
h2 教学情况
课程号:CSCOMP001 课程名∶数据库系统及应用 主讲学时: 30 学期: 2023春
课程号:CSCOMPO11 课程名︰高级数据库系统 主讲学时:60 学期: 2023秋
h2 课程号:CSCOMPO11课程名︰高级数据库系统主讲学时:60学期: 2023秋
1.ZB+tree:一种ZNS SSD感知的新型索引结构，计算机研究与发展，2023，中文CCF-
A，排名第2，通讯作者
2. ZoneKV: A Space-Efficient Key-Value Store for ZNS SSDs，DAC，2023，CCF-A,
排名第2，通讯作者
h2 承担项目情况
1．面向异构混合内存的NVM感知索引及自适应学习方法研究，国家自然科学基金委，国家级项目，2021-2024，总经费: 580000，承担经费:300000
2.量子安全数据库系统关键技术研发及产业化，安徽省科技厅，省部级项目，2022-
2025，总经费:2000000，承担经费:1000000
"""
import pdfkit

# 定义 HTML 表格
html = """
<html>
<head>
<style>
h1 {
    text-align: center;
}
h2 {
    border-bottom: 1px solid black;
    padding-bottom: 0.25em;
    margin-bottom: 0.5em;
}
p {
    margin-top: 0.5em;
    margin-bottom: 0.5em;
}

ol {
    list-style-type: decimal;
    margin-top: 0;
    margin-bottom: 0.5em;
    padding-left: 1.5em;
}
</style>
</head>
<body>
<h1>教师教学科研工作统计</h1>

<h2>教师基本信息</h2>

<p>工号:01234 姓名:张三 性别:男 职称:教授</p>

<h2>教学情况</h2>

<p>课程号：CSCOMP001  课程名：数据库系统及应用  主讲学时：30  学期: 2023春</p>
<p>课程号：CSCOMP011  课程名：高级数据库系统    主讲学时：60  学期: 2023秋</p>
</ul>

<h2>发表论文情况</h2>

<ol>
    <li>ZB+tree:一种ZNS SSD感知的新型索引结构，计算机研究与发展，2023，中文CCF-A，排名第2，通讯作者</li>
    <li>ZoneKV: A Space-Efficient Key-Value Store for ZNS SSDs，DAC，2023，CCF-A,排名第2，通讯作者</li>
</ol>

<h2>承担项目情况</h2>

<ol>
    <li>面向异构混合内存的NVM感知索引及自适应学习方法研究，国家自然科学基金委，国家级项目，2021-2024，总经费: 580000，承担经费:300000</li>
    <li>量子安全数据库系统关键技术研发及产业化，安徽省科技厅，省部级项目，2022-2025，总经费:2000000，承担经费:1000000</li>
</ol>

</body>
</html>
"""

html = """
<html>
<head>
<style>
h1 {
    text-align: center;
}
h2 {
    border-bottom: 1px solid black;
    padding-bottom: 0.25em;
    margin-bottom: 1.0em;
}
table {
    border-collapse: collapse;
    margin: 0 auto;
}
th, td {
    border: 1px solid black;
    padding: 0.5em;
    text-align: center;
}
th {
    background-color: #eee;
}
</style>
</head>
<body>
<h1>教师教学科研工作统计</h1>

<h2>教师基本信息</h2>


<h2>教学情况</h2>
<table>
    <tr>
        <th>课程号</th>
        <th>课程名</th>
        <th>主讲学时</th>
        <th>学期</th>
    </tr>
    <tr>
        <td>CSCOMP001</td>
        <td>数据库系统及应用</td>
        <td>30</td>
        <td>2023春</td>
    </tr>
    <tr>
        <td>CSCOMPO11</td>
        <td>高级数据库系统</td>
        <td>60</td>
        <td>2023秋</td>
    </tr>
</table>

<h2>发表论文情况</h2>
<table>
    <tr>
        <th>论文标题</th>
        <th>期刊/会议名称</th>
        <th>发表年份</th>
        <th>CCF等级</th>
        <th>排名</th>
        <th>通讯作者</th>
    </tr>
    <tr>
        <td>ZB+tree:一种ZNS SSD感知的新型索引结构</td>
        <td>计算机研究与发展</td>
        <td>2023</td>
        <td>中文CCF-A</td>
        <td>第2</td>
        <td>是</td>
    </tr>
    <tr>
        <td>ZoneKV: A Space-Efficient Key-Value Store for ZNS SSDs</td>
        <td>DAC</td>
        <td>2023</td>
        <td>CCF-A</td>
        <td>第2</td>
        <td>是</td>
    </tr>
</table>

<h2>承担项目情况</h2>
<table>
    <tr>
        <th>项目名称</th>
        <th>项目级别</th>
        <th>起止年份</th>
        <th>总经费</th>
        <th>承担经费</th>
    </tr>
    <tr>
        <td>面向异构混合内存的NVM感知索引及自适应学习方法研究</td>
        <td>国家级</td>
        <td>2021-2024</td>
        <td>580000</td>
        <td>300000</td>
    </tr>
    <tr>
        <td>量子安全数据库系统关键技术研发及产业化</td>
        <td>省部级</td>
        <td>2022-2025</td>
        <td>2000000</td>
        <td>1000000</td>
    </tr>
</table>

</body>
</html>
"""

# 将 HTML 转换为 PDF 文件
options = {
    "page-size": "A4",
    "encoding": "UTF-8",
}
pdfkit.from_string(html, "output.pdf", options=options)
