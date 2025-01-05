import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta

# 设置页面配置
st.set_page_config(page_title="Optimized CASHFLOW Simulator", layout="wide")
st.title("Optimized CASHFLOW Simulator: 掌握财务自由之道")

# 初始化会话状态
if 'salary' not in st.session_state:
    st.session_state.salary = 10000
if 'passive_income' not in st.session_state:
    st.session_state.passive_income = 1000
if 'expenses' not in st.session_state:
    st.session_state.expenses = 8000
if 'cash' not in st.session_state:
    st.session_state.cash = 20000
if 'liabilities' not in st.session_state:
    st.session_state.liabilities = 2000  # 初始化负债
if 'investment_return' not in st.session_state:
    st.session_state.investment_return = 0.07
if 'simulation_years' not in st.session_state:
    st.session_state.simulation_years = 10
if 'monthly_investment' not in st.session_state:
    st.session_state.monthly_investment = 1000

# 侧边栏 - 财务目标设置
st.sidebar.header("设置你的财务目标")
target_passive_income = st.sidebar.number_input("目标月被动收入", min_value=0, value=10000, step=500)

# 主要内容区域
tab1, tab2, tab3 = st.tabs(["当前财务状况", "财务模拟", "学习资源"])

with tab1:
    col1, col2, col3 = st.columns(3)

    # 收入支出表
    with col1:
        st.subheader("收入支出表")
        salary = st.number_input("工资收入", min_value=0, value=st.session_state.salary, step=100, key="salary_input")
        passive_income = st.number_input("被动收入", min_value=0, value=st.session_state.passive_income, step=100, key="passive_income_input")
        expenses = st.number_input("总支出", min_value=0, value=st.session_state.expenses, step=100, key="expenses_input")
        liabilities = st.number_input("每月债务还款总额", min_value=0, value=st.session_state.liabilities, step=1000, key="liabilities_input")  # 添加负债输入框
        
        total_income = salary + passive_income
        cash_flow = total_income - expenses
        
        st.metric("总收入", f"${total_income}")
        st.metric("现金流", f"${cash_flow}", delta=cash_flow)
        
        if passive_income > expenses:
            st.success("恭喜！你已经实现财务自由！")
        elif cash_flow > 0:
            st.info(f"你每月有${cash_flow}的正现金流，继续努力增加被动收入！")
        else:
            st.error(f"注意！你每月有${-cash_flow}的负现金流。")

    # 应急基金
    with col2:
        st.subheader("应急基金")
        cash = st.number_input("现金", min_value=0, value=st.session_state.cash, step=1000, key="cash_input")
        
        months_of_expenses = cash / expenses if expenses > 0 else float('inf')
        st.metric("应急基金", f"{months_of_expenses:.1f} 个月", delta=months_of_expenses - 6)
        
        if months_of_expenses >= 6:
            st.success("你有充足的应急基金！")
        elif months_of_expenses >= 3:
            st.info("你的应急基金接近建议水平，继续增加！")
        else:
            st.warning("你的应急基金不足，建议增加到3-6个月的支出。")

    # 财务健康指标
    with col3:
        st.subheader("财务健康指标")
        debt_to_income_ratio = liabilities / total_income if total_income > 0 else float('inf')
        st.metric("债务收入比", f"{debt_to_income_ratio:.2f}", delta=-debt_to_income_ratio, delta_color="inverse")
        if debt_to_income_ratio < 0.36:
            st.success("你的债务收入比在健康范围内。")
        else:
            st.warning("你的债务收入比过高，考虑减少负债。")
        
        savings_rate = (total_income - expenses) / total_income if total_income > 0 else 0
        st.metric("储蓄率", f"{savings_rate:.2%}", delta=savings_rate - 0.2)
        if savings_rate > 0.2:
            st.success("你有很好的储蓄习惯！")
        else:
            st.info("考虑增加你的储蓄率以加速实现财务自由。")
        
        passive_income_ratio = passive_income / expenses if expenses > 0 else float('inf')
        st.metric("被动收入比", f"{passive_income_ratio:.2%}", delta=passive_income_ratio - 1)
        if passive_income_ratio >= 1:
            st.success("你的被动收入已经覆盖了所有支出！")
        else:
            st.info(f"你还需要增加 ${expenses - passive_income:.2f} 的月被动收入来实现财务自由。")

    # 财务健康指标界定注释
    st.markdown("---")
    st.write("**财务健康指标界定注释**:")
    st.write("""
    - **债务收入比**: 低于0.36（36%）为健康范围，高于0.43（43%）可能存在财务风险。
    - **储蓄率**: 建议至少20%，高于50%为非常优秀。
    - **被动收入比**: 达到1.0（100%）表示被动收入覆盖所有支出，实现财务自由。
    - **应急基金**: 建议储备3-6个月的生活支出。
    """)

    # 可视化
    st.subheader("财务状况可视化")

    col4, col5 = st.columns(2)

    with col4:
        # 收入构成饼图
        income_df = pd.DataFrame({
            'Category': ['工资收入', '被动收入'],
            'Amount': [salary, passive_income]
        })
        fig_income = px.pie(income_df, values='Amount', names='Category', title='收入构成')
        st.plotly_chart(fig_income, use_container_width=True)

    with col5:
        # 现金流瀑布图
        fig_cash_flow = go.Figure(go.Waterfall(
            name = "现金流", orientation = "v",
            measure = ["relative", "relative", "total"],
            x = ["总收入", "总支出", "现金流"],
            textposition = "outside",
            text = [f"+${total_income}", f"-${expenses}", f"${cash_flow}"],
            y = [total_income, -expenses, cash_flow],
            connector = {"line":{"color":"rgb(63, 63, 63)"}},
        ))
        fig_cash_flow.update_layout(title="现金流瀑布图")
        st.plotly_chart(fig_cash_flow, use_container_width=True)

    # 财务自由进度
    financial_freedom_progress = passive_income / expenses if expenses > 0 else 0
    st.subheader("财务自由进度")
    st.progress(financial_freedom_progress)
    st.write(f"你的被动收入已经覆盖了 {financial_freedom_progress:.2%} 的支出")

with tab2:
    st.header("财务模拟")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("模拟参数")
        investment_return = st.slider("年投资回报率", min_value=0.0, max_value=0.20, value=st.session_state.investment_return, step=0.01, format="%.2f")
        simulation_years = st.slider("模拟年数", min_value=1, max_value=50, value=st.session_state.simulation_years)
        monthly_investment = st.number_input("每月投资金额", min_value=0, value=st.session_state.monthly_investment, step=100)

    with col2:
        st.subheader("模拟结果")
        
        # 使用财务终值公式（FV）计算未来价值
        total_investment = monthly_investment * 12 * simulation_years
        rate_monthly = investment_return / 12  # 月利率
        nper = simulation_years * 12  # 总期数（月数）
        
        # 计算每月定投的未来价值
        future_value = -((monthly_investment * (1 + rate_monthly)**nper - monthly_investment) / rate_monthly + monthly_investment * (1 + rate_monthly)**nper)

        
        st.metric("总投资金额", f"${total_investment:,.2f}")
        st.metric("预计未来价值", f"${future_value:,.2f}")
        st.metric("投资回报", f"${future_value - total_investment:,.2f}")

    # 投资增长曲线
    years = list(range(simulation_years + 1))
    values = []
    current_value = 0
    for year in years:
        for month in range(12):
          current_value = current_value * (1 + rate_monthly) + monthly_investment

        values.append(current_value)
    
    
    fig_growth = go.Figure()
    fig_growth.add_trace(go.Scatter(x=years, y=values, mode='lines', name='投资价值'))
    fig_growth.add_trace(go.Scatter(x=years, y=[monthly_investment * 12 * year for year in years], mode='lines', name='总投资金额'))
    fig_growth.update_layout(title="投资增长曲线", xaxis_title="年数", yaxis_title="价值")
    st.plotly_chart(fig_growth, use_container_width=True)

    # 计算实现财务目标所需时间
    years_to_passive_income = 0
    total_investment_value = 0
    monthly_rate = investment_return / 12

    for year in range(1, 101):  # 最多模拟100年
        for month in range(12):
            total_investment_value = (total_investment_value + monthly_investment) * (1 + monthly_rate)
        
        annual_passive_income = total_investment_value * investment_return
        monthly_passive_income = annual_passive_income / 12

        if monthly_passive_income >= target_passive_income and years_to_passive_income == 0:
            years_to_passive_income = year
            break

    st.subheader("实现财务目标所需时间")
    if years_to_passive_income > 0:
        st.metric("达到目标被动收入", f"{years_to_passive_income} 年")
    else:
        st.write("以当前增长率，无法在100年内达到目标被动收入")

with tab3:
    st.header("学习资源")
    
    st.subheader("财务知识小贴士")
    tips = [
        "增加被动收入是实现财务自由的关键。",
        "控制支出，特别是非必要支出，可以加速你实现财务自由的进程。",
        "优先偿还高利息负债，如信用卡债务，可以显著改善你的财务状况。",
        "保持3-6个月支出的现金储备作为应急基金，以应对突发情况。",
        "长期投资策略通常优于频繁交易。考虑定期投资指数基金或ETF。",
        "分散投资于不同的资产类别，如股票、债券、房地产等，以降低风险。",
        "持续学习投资和理财知识，提高自己的财务决策能力。",
        "定期检查你的财务状况，确保你在朝着财务自由的目标稳步前进。",
        "记住，真正的资产会把钱放进你的口袋，而不是从你的口袋里拿走。",
        "财务自由不仅仅是关于金钱，也是关于时间和选择的自由。"
    ]
    for tip in tips:
        st.info(tip)
    
    st.subheader("推荐阅读")
    books = [
        "《富爸爸穷爸爸》 - 罗伯特·清崎",
        "《小狗钱钱》 - 博多·舍费尔",
        "《投资最重要的事》 - 霍华德·马克斯",
        "《巴菲特之道》 - 罗伯特·哈格斯特朗",
        "《聪明的投资者》 - 本杰明·格雷厄姆",
        "《指数基金投资指南》 - 约翰·博格",
        "《随机漫步的傻瓜》 - 纳西姆·塔勒布",
        "《金钱心理学》 - 摩根·豪塞尔",
    ]
    for book in books:
        st.write(f"- {book}")

# Educational content
st.subheader("财务知识")
st.write("""
1. **现金流的重要性**: 保持正现金流是财务健康的关键。努力增加收入（特别是被动收入）并控制支出。

2. **资产vs负债**: 购买能给你带来收入的资产，而不是增加支出的负债。记住：资产往你口袋里放钱，负债从你口袋里拿钱。

3. **被动收入**: 建立多元化的被动收入来源，如股息、租金收入、版税等，是实现财务自由的关键。

4. **长期投资**: 专注于长期投资策略，避免频繁交易。市场波动是正常的，保持耐心和纪律。

5. **风险管理**: 分散投资，不要把所有鸡蛋放在一个篮子里。建立应急基金以应对意外情况。

6. **持续学习**: 不断提高你的财务知识和技能。了解不同的投资工具和策略，但也要认识到自己的局限性。

7. **生活方式设计**: 财务自由不仅仅是关于金钱，也是关于设计你想要的生活方式。平衡当前的生活质量和未来的财务安全。
""")

# 更新会话状态
st.session_state.salary = salary
st.session_state.passive_income = passive_income
st.session_state.expenses = expenses
st.session_state.cash = cash
st.session_state.liabilities = liabilities  # 更新负债值
st.session_state.investment_return = investment_return
st.session_state.simulation_years = simulation_years
st.session_state.monthly_investment = monthly_investment

# 添加页脚
st.markdown("---")
st.write("注意：这个模拟器仅用于教育目的。请在做出任何重大财务决策之前咨询专业的财务顾问。")