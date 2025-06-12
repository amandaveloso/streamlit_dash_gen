import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# --------------------- CONFIGURAÇÃO DA PÁGINA ---------------------
st.set_page_config(
    page_title="ExcelViz: Gerador de Dashboards",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="auto"
)

# --------------------- TÍTULO E INSTRUÇÕES ---------------------
st.title("📊 ExcelViz: Gerador de Dashboards Automático")
st.markdown(
    "Que tal analisar rapidamente seu arquivo excel e obter insights relevantes? "
    "Faça o upload do seu arquivo Excel (.xlsx ou .xls) e visualize seus dados instantaneamente!"
)

# --------------------- UPLOAD DO ARQUIVO ---------------------
uploaded_file = st.file_uploader("Escolha um arquivo Excel", type=["xlsx", "xls"])

def plot_histogram(data, column, title, theme):
    try:
        fig = px.histogram(data, x=column, title=title, template=theme)
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Erro ao gerar histograma de {column}: {e}")

def plot_box(data, column, title, theme):
    try:
        fig = px.box(data, y=column, title=title, template=theme)
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Erro ao gerar box plot de {column}: {e}")

def plot_bar(data, x, y, title, theme):
    try:
        fig = px.bar(data, x=x, y=y, title=title, template=theme)
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Erro ao gerar gráfico de barras: {e}")

def plot_pie(data, names, title, theme):
    try:
        fig = px.pie(data, names=names, title=title, template=theme)
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Erro ao gerar gráfico de pizza: {e}")

def plot_scatter(data, x, y, title, theme):
    try:
        fig = px.scatter(data, x=x, y=y, title=title, template=theme)
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Erro ao gerar gráfico de dispersão: {e}")

def plot_corr_heatmap(data, num_cols, theme):
    try:
        corr_matrix = data[num_cols].corr()
        fig = px.imshow(corr_matrix, text_auto=True, title="Matriz de Correlação", template=theme)
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Erro ao gerar heatmap de correlação: {e}")

# --------------------- SIDEBAR CONFIGURAÇÕES ---------------------
st.sidebar.title("Configurações e Filtros")
theme = st.sidebar.selectbox(
    "Tema dos Gráficos:",
    ["plotly", "ggplot2", "seaborn", "simple_white", "presentation", "xgridoff", "ygridoff", "gridon", "none"],
    index=0
)

# --------------------- PROCESSAMENTO DO ARQUIVO ---------------------
if uploaded_file is not None:
    try:
        if uploaded_file.name.split(".")[-1] not in ["xlsx", "xls"]:
            st.error("Formato inválido. Apenas arquivos Excel (.xlsx, .xls) são suportados.")
            st.stop()

        df = pd.read_excel(uploaded_file)
        if df.empty:
            st.error("O arquivo está vazio ou não contém dados legíveis.")
            st.stop()

        # Limitar para arquivos muito grandes
        if len(df) > 10000:
            st.warning("O arquivo contém muitos dados. Apenas uma amostra de 10.000 linhas será exibida para melhor desempenho.")
            df = df.sample(10000, random_state=42)

        st.success("Arquivo carregado com sucesso!")

        # TABS PARA MELHOR EXPERIÊNCIA DO USUÁRIO
        tab1, tab2, tab3, tab4 = st.tabs([
            "Prévia dos Dados",
            "Estatísticas Descritivas",
            "Gráficos",
            "Correlação"
        ])

        # --------------------- TAB 1: PRÉVIA ---------------------
        with tab1:
            st.dataframe(df.head())

        # --------------------- IDENTIFICAÇÃO DE TIPOS ---------------------
        numerical_cols = df.select_dtypes(include=np.number).columns.tolist()
        categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
        datetime_cols = df.select_dtypes(include=['datetime64[ns]']).columns.tolist()

        # --------------------- TAB 2: ESTATÍSTICAS ---------------------
        with tab2:
            if numerical_cols:
                st.markdown("### Estatísticas Descritivas")
                st.dataframe(df[numerical_cols].describe().T)
            else:
                st.info("Nenhuma coluna numérica encontrada no arquivo.")

        # --------------------- TAB 3: GRÁFICOS ---------------------
        with tab3:
            col1, col2 = st.columns(2)

            # Gráficos Numéricos
            with col1:
                if numerical_cols:
                    st.markdown("#### Variáveis Numéricas")
                    num_cols_to_plot = st.multiselect(
                        "Selecione colunas numéricas para Histograma/Box Plot:",
                        numerical_cols,
                        default=numerical_cols[:min(2, len(numerical_cols))],
                        key="num_plots_multiselect"
                    )
                    for col in num_cols_to_plot:
                        plot_histogram(df, col, f"Distribuição de {col}", theme)
                        plot_box(df, col, f"Box Plot de {col}", theme)

                    # Tendências Temporais
                    if datetime_cols and numerical_cols:
                        st.markdown("#### Tendências Temporais")
                        date_col_selected = st.selectbox("Selecione a coluna de Data:", datetime_cols, key="date_col_select")
                        num_col_for_trend = st.selectbox("Selecione a Variável Numérica para a Tendência:", numerical_cols, key="trend_num_select")
                        if date_col_selected and num_col_for_trend:
                            df_agg = df.groupby(date_col_selected)[num_col_for_trend].sum().reset_index()
                            fig_line = px.line(df_agg, x=date_col_selected, y=num_col_for_trend, 
                                               title=f"Tendência de {num_col_for_trend} por {date_col_selected}", template=theme)
                            st.plotly_chart(fig_line, use_container_width=True)
                else:
                    st.info("Nenhuma coluna numérica disponível para gráficos.")

            # Gráficos Categóricos e Dispersão
            with col2:
                # Categóricas
                if categorical_cols:
                    st.markdown("#### Variáveis Categóricas")
                    cat_cols_to_plot = st.multiselect(
                        "Selecione colunas categóricas para Contagem/Distribuição:",
                        categorical_cols,
                        default=categorical_cols[:min(2, len(categorical_cols))],
                        key="cat_plots_multiselect"
                    )
                    for col in cat_cols_to_plot:
                        counts = df[col].value_counts().reset_index()
                        counts.columns = [col, 'Contagem']
                        plot_bar(counts, col, 'Contagem', f"Contagem de {col}", theme)
                        if 1 < df[col].nunique() < 15:
                            plot_pie(df, col, f"Distribuição de {col}", theme)
                else:
                    st.info("Nenhuma coluna categórica disponível para gráficos.")

                # Dispersão
                if len(numerical_cols) >= 2:
                    st.markdown("#### Dispersão entre Variáveis Numéricas")
                    x_scatter = st.selectbox("Selecione o Eixo X:", numerical_cols, key="scatter_x_select")
                    y_options = [col for col in numerical_cols if col != x_scatter]
                    y_scatter = st.selectbox("Selecione o Eixo Y:", y_options, key="scatter_y_select")
                    if x_scatter and y_scatter and x_scatter != y_scatter:
                        plot_scatter(df, x_scatter, y_scatter, f"Dispersão de {x_scatter} vs {y_scatter}", theme)

        # --------------------- TAB 4: HEATMAP DE CORRELAÇÃO ---------------------
        with tab4:
            if len(numerical_cols) > 1:
                plot_corr_heatmap(df, numerical_cols, theme)
            else:
                st.info("São necessárias pelo menos duas colunas numéricas para a matriz de correlação.")

    except Exception as e:
        st.error(f"Erro ao processar o arquivo. Certifique-se de que é um arquivo Excel válido e bem formatado. Detalhes do erro: {e}")
else:
    st.info("Aguardando o upload de um arquivo Excel para gerar o dashboard...")

st.markdown("---")
st.markdown("Desenvolvido para portfólio [@amandaveloso](https://github.com/amandaveloso)")
