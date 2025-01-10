import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import json

# 设置页面配置
st.set_page_config(page_title="足彩投资记录与分析", layout="wide")

# 设置全局主题颜色
theme_colors = {
    "primary": "#1f77b4",
    "secondary": "#ff7f0e",
    "background": "#f0f2f6",
    "text": "#2c3e50"
}

# 初始化会话状态
if 'data' not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=["日期", "比赛", "投注类型", "赔率", "投注金额", "结果"])

# 辅助函数
def save_data():
    st.session_state.data.to_json("足彩投资记录.json", orient="records", date_format="iso")
    st.success("数据已保存")

def load_data():
    try:
        df = pd.read_json("足彩投资记录.json", orient="records")
        st.session_state.data = df
        st.success("数据已成功加载")
    except FileNotFoundError:
        st.error("未找到保存的数据文件")

def clear_data():
    st.session_state.data = pd.DataFrame(columns=["日期", "比赛", "投注类型", "赔率", "投注金额", "结果"])
    if st.button("确认清空数据"):
        save_data()
        st.success("所有数据已清空并保存")

def calculate_profit(row):
    if row['结果'] == '未开奖':
        return 0
    elif row['结果'] == row['投注类型']:
        return row['投注金额'] * (row['赔率'] - 1)
    else:
        return -row['投注金额']

# 标题和介绍
st.title("足彩投资记录与分析")
st.write("记录你的足彩投注，分析你的投资表现")

# 侧边栏：添加新的投注记录
with st.sidebar:
    st.header("数据管理")
    
    with st.form("new_record"):
        st.subheader("添加新的投注记录")
        date = st.date_input("日期", datetime.now())
        match = st.text_input("比赛", "主队 vs 客队")
        bet_type = st.selectbox("投注类型", ["胜", "平", "负"])
        odds = st.number_input("赔率", min_value=1.01, value=2.0, step=0.01)
        stake = st.number_input("投注金额", min_value=1, value=100)
        result = st.selectbox("比赛结果", ["未开奖", "胜", "平", "负"])
        
        submitted = st.form_submit_button("添加记录")
        if submitted:
            new_record = pd.DataFrame({
                "日期": [date],
                "比赛": [match],
                "投注类型": [bet_type],
                "赔率": [odds],
                "投注金额": [stake],
                "结果": [result]
            })
            st.session_state.data = pd.concat([st.session_state.data, new_record], ignore_index=True)
            st.success("记录已添加")

    if st.button("保存数据"):
        save_data()

    if st.button("加载保存的数据"):
        load_data()

    if st.button("清空数据"):
        clear_data()

# 主页面：数据展示和分析
if not st.session_state.data.empty:
    df = st.session_state.data.copy()
    
    # Ensure all numeric columns are properly typed
    df['赔率'] = pd.to_numeric(df['赔率'], errors='coerce')
    df['投注金额'] = pd.to_numeric(df['投注金额'], errors='coerce')
    
    df['盈亏'] = df.apply(calculate_profit, axis=1)
    df['是否盈利'] = df['盈亏'] > 0

    # 总体统计
    total_bets = len(df)
    total_stake = df['投注金额'].sum()
    total_profit = df['盈亏'].sum()
    win_rate = (df['是否盈利'].sum() / total_bets) * 100
    roi = (total_profit / total_stake) * 100 if total_stake > 0 else 0

    st.header("总体统计")
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("总投注次数", f"{total_bets:,}")
    col2.metric("总投注金额", f"¥{total_stake:,.2f}")
    col3.metric("总盈亏", f"¥{total_profit:,.2f}", delta=f"{roi:.2f}%")
    col4.metric("胜率", f"{win_rate:.2f}%")
    col5.metric("ROI", f"{roi:.2f}%")

    # 数据可视化
    st.header("数据可视化")
    tab1, tab2, tab3 = st.tabs(["盈亏趋势", "投注分析", "赔率分析"])

    with tab1:
        fig_profit_trend = go.Figure()
        fig_profit_trend.add_trace(go.Scatter(
            x=df['日期'], 
            y=df['盈亏'].cumsum(), 
            mode='lines+markers',
            name='累计盈亏',
            line=dict(color=theme_colors['primary'], width=2),
            marker=dict(size=6, color=theme_colors['secondary'])
        ))
        fig_profit_trend.update_layout(
            title='累计盈亏趋势',
            xaxis_title='日期',
            yaxis_title='累计盈亏 (¥)',
            plot_bgcolor=theme_colors['background'],
            paper_bgcolor=theme_colors['background'],
            font=dict(color=theme_colors['text'])
        )
        st.plotly_chart(fig_profit_trend, use_container_width=True)

    with tab2:
        col1, col2 = st.columns(2)
        with col1:
            fig_bet_type = px.pie(
                df, 
                names='投注类型', 
                values='投注金额',
                title='投注类型分布',
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            fig_bet_type.update_traces(textposition='inside', textinfo='percent+label')
            fig_bet_type.update_layout(
                plot_bgcolor=theme_colors['background'],
                paper_bgcolor=theme_colors['background'],
                font=dict(color=theme_colors['text'])
            )
            st.plotly_chart(fig_bet_type, use_container_width=True)
        
        with col2:
            fig_stake_dist = px.histogram(
                df, 
                x='投注金额', 
                title='投注金额分布',
                color_discrete_sequence=[theme_colors['primary']]
            )
            fig_stake_dist.update_layout(
                xaxis_title='投注金额 (¥)',
                yaxis_title='频次',
                plot_bgcolor=theme_colors['background'],
                paper_bgcolor=theme_colors['background'],
                font=dict(color=theme_colors['text'])
            )
            st.plotly_chart(fig_stake_dist, use_container_width=True)

    with tab3:
        # Ensure '投注金额' is numeric
        df['投注金额'] = pd.to_numeric(df['投注金额'], errors='coerce')
        
        fig_odds_profit = px.scatter(
            df, 
            x='赔率', 
            y='盈亏', 
            color='是否盈利',
            size='投注金额',
            hover_data=['比赛', '投注类型', '结果'],
            title='赔率与盈亏关系',
            color_discrete_map={True: theme_colors['primary'], False: theme_colors['secondary']}
        )
        fig_odds_profit.update_layout(
            xaxis_title='赔率',
            yaxis_title='盈亏 (¥)',
            plot_bgcolor=theme_colors['background'],
            paper_bgcolor=theme_colors['background'],
            font=dict(color=theme_colors['text'])
        )
        st.plotly_chart(fig_odds_profit, use_container_width=True)

    # 投注策略分析
    st.header("投注策略分析")
    tab1, tab2 = st.tabs(["投注类型分析", "赔率区间分析"])

    with tab1:
        performance_by_type = df.groupby('投注类型').agg({
            '投注金额': 'sum',
            '盈亏': 'sum',
            '是否盈利': 'mean'
        }).reset_index()
        performance_by_type['ROI'] = performance_by_type.apply(
            lambda row: (row['盈亏'] / row['投注金额'] * 100) if row['投注金额'] != 0 else 0, axis=1
        )
        performance_by_type['胜率'] = performance_by_type['是否盈利'] * 100
        
        fig_performance_by_type = go.Figure()
        fig_performance_by_type.add_trace(go.Bar(
            x=performance_by_type['投注类型'],
            y=performance_by_type['ROI'],
            name='ROI (%)',
            marker_color=theme_colors['primary']
        ))
        fig_performance_by_type.add_trace(go.Bar(
            x=performance_by_type['投注类型'],
            y=performance_by_type['胜率'],
            name='胜率 (%)',
            marker_color=theme_colors['secondary']
        ))
        fig_performance_by_type.update_layout(
            title='各投注类型表现',
            barmode='group',
            xaxis_title='投注类型',
            yaxis_title='百分比 (%)',
            plot_bgcolor=theme_colors['background'],
            paper_bgcolor=theme_colors['background'],
            font=dict(color=theme_colors['text'])
        )
        st.plotly_chart(fig_performance_by_type, use_container_width=True)
        st.dataframe(performance_by_type)

    with tab2:
        df['赔率区间'] = pd.cut(df['赔率'], bins=[1, 1.5, 2, 2.5, 3, float('inf')], labels=['1.0-1.5', '1.5-2.0', '2.0-2.5', '2.5-3.0', '3.0+'])
        performance_by_odds = df.groupby('赔率区间').agg({
            '投注金额': 'sum',
            '盈亏': 'sum',
            '是否盈利': 'mean'
        }).reset_index()
        performance_by_odds['ROI'] = performance_by_odds.apply(
            lambda row: (row['盈亏'] / row['投注金额'] * 100) if row['投注金额'] != 0 else 0, axis=1
        )
        performance_by_odds['胜率'] = performance_by_odds['是否盈利'] * 100
        
        fig_performance_by_odds = go.Figure()
        fig_performance_by_odds.add_trace(go.Bar(
            x=performance_by_odds['赔率区间'],
            y=performance_by_odds['ROI'],
            name='ROI (%)',
            marker_color=theme_colors['primary']
        ))
        fig_performance_by_odds.add_trace(go.Bar(
            x=performance_by_odds['赔率区间'],
            y=performance_by_odds['胜率'],
            name='胜率 (%)',
            marker_color=theme_colors['secondary']
        ))
        fig_performance_by_odds.update_layout(
            title='各赔率区间表现',
            barmode='group',
            xaxis_title='赔率区间',
            yaxis_title='百分比 (%)',
            plot_bgcolor=theme_colors['background'],
            paper_bgcolor=theme_colors['background'],
            font=dict(color=theme_colors['text'])
        )
        st.plotly_chart(fig_performance_by_odds, use_container_width=True)
        st.dataframe(performance_by_odds)

    # 投注建议
    st.header("投注建议")
    if not performance_by_type.empty and not performance_by_odds.empty:
        best_type = performance_by_type.loc[performance_by_type['ROI'].idxmax()]
        worst_type = performance_by_type.loc[performance_by_type['ROI'].idxmin()]
        best_odds_range = performance_by_odds.loc[performance_by_odds['ROI'].idxmax()]

        advice = [
            f"1. 考虑增加 '{best_type['投注类型']}' 类型的投注，它的表现最好（ROI: {best_type['ROI']:.2f}%）。",
            f"2. 赔率在 {best_odds_range['赔率区间']} 范围内的投注表现最好，可以多关注这个赔率区间（ROI: {best_odds_range['ROI']:.2f}%）。",
            f"3. 谨慎考虑 '{worst_type['投注类型']}' 类型的投注，它的表现最差（ROI: {worst_type['ROI']:.2f}%）。",
            "4. 持续记录和分析你的投注数据，定期调整你的投注策略。",
            f"5. 当前整体ROI为 {roi:.2f}%，努力保持正收益并逐步提高。"
        ]
        for item in advice:
            st.info(item)
    else:
        st.info("需要更多的投注数据来生成建议。")

    # 数据表格
    st.header("投注记录")
    st.dataframe(df.style.highlight_max(axis=0, subset=['盈亏'], color='lightgreen')
                   .highlight_min(axis=0, subset=['盈亏'], color='lightcoral'))

    # 导出数据
    if st.button("导出数据"):
        df.to_csv("足彩投资记录.csv", index=False)
        st.success("数据已导出到 '足彩投资记录.csv'")

else:
    st.info("还没有投注记录，请在左侧添加新的记录")

