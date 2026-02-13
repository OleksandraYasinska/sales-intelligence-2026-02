import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from src.data_loader import load_and_clean_data

# 1. КОНФІГУРАЦІЯ СТОРІНКИ
st.set_page_config(
    page_title="Sales Intelligence 2026",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 2. КЕШУВАННЯ ТА ОБРОБКА ДАНИХ
@st.cache_data
def get_clean_data():
    df = load_and_clean_data("data/sales_data.csv")
    if df is not None:
        df['Margin_Perc'] = (df['Profit'] / df['Sales']) * 100
        return df
    return None

# 3. ЕЛІТНИЙ ДИЗАЙН (CSS)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background-color: #FBFBFE;
    }

    /* Метрики */
    div[data-testid="stMetric"] {
        background-color: white;
        border-radius: 12px;
        padding: 20px !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        border: 1px solid #F1F5F9;
    }

    /* Контейнер для графіків без рамок */
    .viz-box {
        background-color: white;
        padding: 25px;
        border-radius: 16px;
        border: 1px solid #F1F5F9;
        margin-bottom: 25px;
    }

    /* Чисті заголовки */
    .clean-header {
        color: #1E293B;
        font-size: 1.15rem;
        font-weight: 700;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        gap: 10px;
    }

    /* Стилізація табів */
    .stTabs [data-baseweb="tab-list"] { gap: 15px; }
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        color: #94A3B8;
        border: none;
        padding: 10px 20px;
        font-weight: 500;
    }
    .stTabs [aria-selected="true"] {
        color: #2563EB !important;
        border-bottom: 3px solid #2563EB !important;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #FFFFFF;
        border-right: 1px solid #F1F5F9;
    }
    </style>
    """, unsafe_allow_html=True)

# Глобальний стиль графіків
BRAND_COLORS = ["#0F172A", "#2563EB", "#60A5FA", "#93C5FD", "#BFDBFE"]

def apply_pro_theme(fig, is_map=False):
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Inter", size=12, color="#64748B"),
        margin=dict(l=0, r=0, t=10, b=10),
        legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5),
        colorway=BRAND_COLORS
    )
    if not is_map:
        fig.update_xaxes(showgrid=False, linecolor='#F1F5F9')
        fig.update_yaxes(gridcolor='#F1F5F9', zeroline=False)
    return fig

# 4. ЛОГІКА ДОДАТКУ
df = get_clean_data()

if df is not None:
    # --- SIDEBAR (Фільтри) ---
    with st.sidebar:
        st.markdown("<h2 style='color:#1E293B;'>📊 Аналітика</h2>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        
        with st.container():
            st.markdown("**📅 Період**")
            date_range = st.date_input("Оберіть дати", value=(df["Date"].min(), df["Date"].max()), label_visibility="collapsed")

        st.markdown("<br>", unsafe_allow_html=True)
        with st.expander("🌍 Локація", expanded=True):
            selected_countries = st.multiselect("Країни", options=sorted(df["Country"].unique()), default=df["Country"].unique())
        
        with st.expander("💼 Бізнес-сегменти", expanded=True):
            selected_segments = st.multiselect("Сегментація", options=sorted(df["Segment"].unique()), default=df["Segment"].unique())

        st.markdown("---")
        # Feature: Quick Stats in Sidebar
        top_country = df.groupby("Country")["Sales"].sum().idxmax()
        st.info(f"🏆 **Лідери ринку:** {top_country}")
        
        if st.button("🔄 Скинути фільтри", use_container_width=True):
            st.rerun()

        st.markdown("<br>"*3, unsafe_allow_html=True)
        csv_data = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Завантажити звіт CSV", data=csv_data, file_name='sales_report_2026.csv', use_container_width=True)

    # Фільтрація
    df_f = df[
        (df["Date"].dt.date >= date_range[0]) &
        (df["Date"].dt.date <= date_range[1]) &
        (df["Country"].isin(selected_countries)) &
        (df["Segment"].isin(selected_segments))
    ]

    # --- ГОЛОВНИЙ ЕКРАН ---
    st.title("📈 Стратегічний звіт із продажів")
    
    if not df_f.empty:
        # KPI МЕТРИКИ
        k1, k2, k3, k4 = st.columns(4)
        
        t_sales = df_f["Sales"].sum()
        t_profit = df_f["Profit"].sum()
        margin = (t_profit / t_sales) * 100
        aov = df_f["Sales"].mean()
        customers = df_f["Customer_ID"].nunique()

        k1.metric("Загальний виторг", f"${t_sales:,.0f}")
        k2.metric("Чистий прибуток", f"${t_profit:,.0f}", f"{margin:.1f}% Маржа")
        k3.metric("Середній чек (AOV)", f"${aov:,.0f}")
        k4.metric("Активні клієнти", f"{customers:,}")

        st.markdown("<br>", unsafe_allow_html=True)

        # ТАБИ
        tab_trends, tab_geo, tab_table = st.tabs([
            "📉 Аналітика трендів та часток", 
            "🌍 Географія та Продукти", 
            "📋 Реєстр транзакцій"
        ])

        with tab_trends:
            c1, c2 = st.columns([1.7, 1])
            
            with c1:
                st.markdown('<div class="clean-header">📈 Динаміка доходів та прибутковості</div>', unsafe_allow_html=True)
                df_m = df_f.groupby(pd.Grouper(key='Date', freq='M')).sum(numeric_only=True).reset_index()
                fig_t = go.Figure()
                fig_t.add_trace(go.Scatter(x=df_m['Date'], y=df_m['Sales'], name='Виторг', line=dict(color='#2563EB', width=4), fill='tozeroy'))
                fig_t.add_trace(go.Bar(x=df_m['Date'], y=df_m['Profit'], name='Прибуток', marker_color='#0F172A', opacity=0.8))
                st.plotly_chart(apply_pro_theme(fig_t), use_container_width=True)
            
            with c2:
                st.markdown('<div class="clean-header">🥧 Продажі за сегментами</div>', unsafe_allow_html=True)
                fig_p = px.pie(df_f, values='Sales', names='Segment', hole=0.6)
                fig_p.update_traces(textinfo='percent+label', marker=dict(line=dict(color='#FFFFFF', width=2)))
                st.plotly_chart(apply_pro_theme(fig_p), use_container_width=True)

        with tab_geo:
            st.markdown('<div class="clean-header">🌍 Глобальне охоплення ринку</div>', unsafe_allow_html=True)
            g_data = df_f.groupby("Country")["Sales"].sum().reset_index()
            fig_m = px.choropleth(g_data, locations="Country", locationmode='country names', color="Sales", color_continuous_scale="Blues")
            fig_m.update_geos(showcoastlines=True, coastlinecolor="#E2E8F0", showland=True, landcolor="#F8FAFC")
            st.plotly_chart(apply_pro_theme(fig_m, is_map=True), use_container_width=True)
            
            st.markdown("---")
            c3, c4 = st.columns(2)
            with c3:
                st.markdown('<div class="clean-header">🏆 ТОП-5 Продуктів за прибутком</div>', unsafe_allow_html=True)
                top = df_f.groupby("Product_Name")["Profit"].sum().nlargest(5).reset_index().sort_values("Profit")
                fig_b = px.bar(top, x="Profit", y="Product_Name", orientation='h', color_discrete_sequence=['#2563EB'])
                st.plotly_chart(apply_pro_theme(fig_b), use_container_width=True)
            
            with c4:
                st.markdown('<div class="clean-header">⚖️ Матриця: Продажі vs Прибуток</div>', unsafe_allow_html=True)
                fig_s = px.scatter(df_f, x="Sales", y="Profit", size="Units Sold", color="Segment", opacity=0.7)
                st.plotly_chart(apply_pro_theme(fig_s), use_container_width=True)

        with tab_table:
            st.markdown('<div class="clean-header">🔍 Детальний перегляд операцій</div>', unsafe_allow_html=True)
            
            # Feature: Search
            search = st.text_input("Пошук за назвою продукту або клієнтом", placeholder="Введіть запит...")
            
            disp_df = df_f.copy()
            if search:
                disp_df = disp_df[disp_df.astype(str).apply(lambda x: x.str.contains(search, case=False)).any(axis=1)]
            
            st.dataframe(
                disp_df.style.format({"Sales": "${:,.2f}", "Profit": "${:,.2f}", "Margin_Perc": "{:.1f}%"})
                .background_gradient(cmap='Blues', subset=['Profit']),
                use_container_width=True, height=550
            )
            st.caption("ℹ️ *Примітка: Інтенсивність синього кольору в колонці 'Profit' вказує на вищу прибутковість транзакції.*")

    else:
        st.warning("☝️ Оберіть параметри на панелі зліва для відображення даних.")
else:
    st.error("🚨 Помилка: Файл `data/sales_data.csv` не знайдено.")