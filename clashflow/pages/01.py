import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import math

# 设置页面配置
st.set_page_config(page_title="富爸爸穷爸爸财务模拟器", layout="wide")

# 标题和介绍
st.title("富爸爸穷爸爸财务模拟器")
st.write("基于CASHFLOW游戏和《穷爸爸富爸爸》概念的交互式财务管理应用")

# 侧边栏：用户输入
with st.sidebar:
    st.header("输入你的财务数据")

    # 收入
    salary = st.number_input("工资收入", min_value=0, value=5000)
    business_income = st.number_input("事业收入", min_value=0, value=0)
    investment_income = st.number_input("投资收入", min_value=0, value=0)

    # 支出
    expenses = st.number_input("月度总支出", min_value=0, value=3000)

    # 资产
    savings = st.number_input("储蓄", min_value=0, value=10000)
    stocks = st.number_input("股票投资", min_value=0, value=5000)
    real_estate = st.number_input("房地产投资", min_value=0, value=0)
    business_value = st.number_input("事业价值", min_value=0, value=0)

    # 负债
    mortgage = st.number_input("房贷", min_value=0, value=0)
    car_loan = st.number_input("车贷", min_value=0, value=0)
    credit_card_debt = st.number_input("信用卡债务", min_value=0, value=0)
    other_debts = st.number_input("其他债务", min_value=0, value=0)

# 计算关键财务指标
total_income = salary + business_income + investment_income
passive_income = investment_income + business_income
net_income = total_income - expenses
total_assets = savings + stocks + real_estate + business_value
total_liabilities = mortgage + car_loan + credit_card_debt + other_debts
net_worth = total_assets - total_liabilities

# 创建财务报表
# 资产负债表
balance_sheet = pd.DataFrame({
    "项目": ["总资产", "总负债", "净资产"],
    "金额": [total_assets, total_liabilities, net_worth]
})

# 损益表
income_statement = pd.DataFrame({
    "项目": ["工资收入", "事业收入", "投资收入", "总收入", "总支出", "净收入"],
    "金额": [salary, business_income, investment_income, total_income, expenses, net_income]
})

# 现金流量表
cash_flow = pd.DataFrame({
    "项目": ["经营活动现金流", "投资活动现金流", "筹资活动现金流", "净现金流"],
    "金额": [net_income, investment_income, -total_liabilities, net_income + investment_income - total_liabilities]
})

# 显示财务报表
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("资产负债表")
    st.dataframe(balance_sheet)

with col2:
    st.subheader("损益表")
    st.dataframe(income_statement)

with col3:
    st.subheader("现金流量表")
    st.dataframe(cash_flow)

# 可视化
st.header("财务可视化")

# 收入构成饼图
fig_income = px.pie(
    values=[salary, business_income, investment_income],
    names=["工资收入", "事业收入", "投资收入"],
    title="收入构成"
)
st.plotly_chart(fig_income)

# 资产配置饼图
fig_assets = px.pie(
    values=[savings, stocks, real_estate, business_value],
    names=["储蓄", "股票", "房地产", "事业"],
    title="资产配置"
)
st.plotly_chart(fig_assets)

# 现金流象限图
def cash_flow_quadrant(employee, self_employed, business_owner, investor):
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=[0, 0, 1, 1, 0],
        y=[0, 1, 1, 0, 0],
        fill="toself",
        fillcolor="rgba(255, 0, 0, 0.2)",
        line_color="rgba(255, 0, 0, 0.2)",
        showlegend=False,
        hoverinfo="skip"
    ))

    fig.add_trace(go.Scatter(
        x=[0, 0, -1, -1, 0],
        y=[0, 1, 1, 0, 0],
        fill="toself",
        fillcolor="rgba(0, 255, 0, 0.2)",
        line_color="rgba(0, 255, 0, 0.2)",
        showlegend=False,
        hoverinfo="skip"
    ))

    fig.add_trace(go.Scatter(
        x=[0, 0, -1, -1, 0],
        y=[0, -1, -1, 0, 0],
        fill="toself",
        fillcolor="rgba(0, 0, 255, 0.2)",
        line_color="rgba(0, 0, 255, 0.2)",
        showlegend=False,
        hoverinfo="skip"
    ))

    fig.add_trace(go.Scatter(
        x=[0, 0, 1, 1, 0],
        y=[0, -1, -1, 0, 0],
        fill="toself",
        fillcolor="rgba(255, 255, 0, 0.2)",
        line_color="rgba(255, 255, 0, 0.2)",
        showlegend=False,
        hoverinfo="skip"
    ))

    fig.add_trace(go.Scatter(
        x=[0], y=[0],
        mode="markers+text",
        marker_size=20,
        text=["你"],
        textposition="top center"
    ))

    fig.add_annotation(x=0.5, y=0.5, text="雇员<br>Employee", showarrow=False)
    fig.add_annotation(x=-0.5, y=0.5, text="自由职业者<br>Self-employed", showarrow=False)
    fig.add_annotation(x=-0.5, y=-0.5, text="企业主<br>Business Owner", showarrow=False)
    fig.add_annotation(x=0.5, y=-0.5, text="投资人<br>Investor", showarrow=False)

    fig.update_layout(
        title="现金流象限",
        xaxis_range=[-1, 1],
        yaxis_range=[-1, 1],
        xaxis_visible=False,
        yaxis_visible=False,
        width=600,
        height=600
    )

    total = employee + self_employed + business_owner + investor
    x = (investor - self_employed) / total if total !=0 else 0
    y = (employee - business_owner) / total if total !=0 else 0

    fig.add_trace(go.Scatter(
        x=[x], y=[y],
        mode="markers",
        marker_size=15,
        marker_color="red",
        name="你的位置"
    ))

    return fig

cf_quadrant = cash_flow_quadrant(salary, 0, business_income, investment_income)
st.plotly_chart(cf_quadrant)

# 财务健康指标
st.header("财务健康指标")

col1, col2, col3 = st.columns(3)

with col1:
    savings_rate = (total_income - expenses) / total_income * 100 if total_income != 0 else 0
    st.metric("储蓄率", f"{savings_rate:.2f}%")

with col2:
    debt_to_income = total_liabilities / (total_income * 12) * 100 if total_income != 0 else 0
    st.metric("债务收入比", f"{debt_to_income:.2f}%")

with col3:
    passive_income_ratio = passive_income / total_income * 100 if total_income != 0 else 0
    st.metric("被动收入比例", f"{passive_income_ratio:.2f}%")

# 财务建议
st.header("财务建议")

if savings_rate < 20:
    st.warning("你的储蓄率偏低，建议增加储蓄以应对紧急情况和投资机会。")
else:
    st.success("你有不错的储蓄习惯，继续保持！考虑将多余的储蓄投入到能产生现金流的资产中。")

if debt_to_income > 40:
    st.warning("你的债务收入比偏高，可能面临财务风险。考虑制定还债计划，并避免产生新的不良负债。")
else:
    st.success("你的债务水平在可控范围内。记住，并非所有负债都是坏的，关键是要区分好负债和坏负债。")

if passive_income_ratio < 10:
    st.info("考虑增加被动收入来源，如投资或创业，以提高财务自由度。目标是让被动收入超过支出。")
else:
    st.success("你有不错的被动收入比例，这有助于提高财务自由度。继续努力提高这个比例！")

# 资产负债比较
st.header("资产与负债比较")

assets_liabilities = pd.DataFrame({
    "类型": ["资产", "负债"],
    "金额": [total_assets, total_liabilities]
})

fig_assets_liabilities = px.bar(
    assets_liabilities,
    x="类型",
    y="金额",
    title="资产与负债比较",
    color="类型",
    color_discrete_map={"资产": "green", "负债": "red"}
)
st.plotly_chart(fig_assets_liabilities)

# 现金流游戏模拟器
st.header("现金流游戏模拟器")

st.write("模拟增加被动收入和减少支出对你财务状况的影响")

col1, col2 = st.columns(2)

with col1:
    additional_passive_income = st.number_input("增加的月被动收入", min_value=0, value=0)
    reduced_expenses = st.number_input("减少的月支出", min_value=0, max_value=expenses, value=0)

with col2:
    months = st.slider("模拟月数", min_value=1, max_value=120, value=12)

new_passive_income = passive_income + additional_passive_income
new_expenses = expenses - reduced_expenses
new_net_income = total_income + additional_passive_income - new_expenses

months_to_freedom = 0
if new_passive_income > new_expenses:
    months_to_freedom = math.ceil((total_liabilities) / (new_passive_income - new_expenses)) if (new_passive_income - new_expenses) != 0 else 0

st.write(f"新的月净收入: ${new_net_income}")
if months_to_freedom > 0:
    st.write(f"预计达到财务自由所需时间: {months_to_freedom} 个月")
else:
    st.write("被动收入尚未超过支出，继续努力增加被动收入或减少支出！")

# 财务自由进度条
financial_freedom_ratio = min(new_passive_income / new_expenses * 100, 100) if new_expenses != 0 else 0
st.progress(financial_freedom_ratio / 100)
st.write(f"财务自由进度: {financial_freedom_ratio:.2f}%")

# 教育资源
st.header("财务教育资源")
st.write("以下是一些帮助你提高财务知识的资源：")
st.markdown("""
- [穷爸爸富爸爸](https://www.richdad.com/)
- [现金流游戏](https://www.richdad.com/products/cashflow-classic)
- [投资基础知识](https://www.investopedia.com/investing-essentials-4689754)
- [被动收入ideas](https://www.entrepreneur.com/article/435909)
""")

# 财务知识小测验
st.header("财务知识小测验")
q1 = st.radio(
    "根据《穷爸爸富爸爸》，以下哪项不是资产？",
    ("股票", "自住房", "租金收入", "版税")
)

if q1 == "自住房":
    st.success("正确！根据Robert Kiyosaki的定义，资产是能给你口袋带来现金的东西。自住房虽然可能升值，但每月会产生支出，因此不算是资产。")
else:
    st.error("不正确。自住房虽然可能升值，但每月会产生支出（如房贷、物业费等），因此根据Robert Kiyosaki的定义，它不算是资产。资产应该是能给你带来现金流入的东西。")

# 结语
st.markdown("---")
st.write("记住，财务自由是一段旅程，而不是终点。持续学习、明智决策，并定期审视你的财务状况。")
st.write("关注现金流，而不仅仅是净资产。努力将被动收入提高到超过支出的水平，这才是真正的财务自由。")
st.write("本应用仅供教育目的，不构成专业财务建议。对于具体的财务决策，请咨询专业的财务顾问。")