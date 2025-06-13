import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from streamlit_cloud import cloud_resource

# --------------------- CONFIGURAÇÃO DA PÁGINA ---------------------
st.set_page_config(
    page_title="Rapidinho: Gerador de Dashboards",
    page_icon="🏃🏻‍♂️",
    layout="wide",
    initial_sidebar_state="auto"
)

# --------------------- TÍTULO E INSTRUÇÕES ---------------------
st.title("🏃🏻‍♂️ Rapidinho: Gerador de Dashboards Automático")
with st.expander("Instruções: Como usar o Rapidinho?"):
    st.markdown(
        "Que tal analisar rapidamente seu arquivo Excel e obter insights relevantes? \n"
        "Faça o **upload do seu arquivo Excel (.xlsx ou .xls) ou CSV** e visualize seus dados instantaneamente! "
        "O Rapidinho irá gerar automaticamente tabelas descritivas, gráficos de distribuição, "
        "e até um heatmap de correlação para te ajudar a entender seus dados."
    )

# --------------------- FUNÇÕES DE PLOTAGEM ---------------------
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
st.sidebar.title("⚙️ Configurações e Filtros")
theme = st.sidebar.selectbox(
    "🎨 Tema dos Gráficos:",
    ["plotly", "ggplot2", "seaborn", "simple_white", "presentation", "xgridoff", "ygridoff", "gridon", "none"],
    index=0
)

# --------------------- UPLOAD DO ARQUIVO ---------------------
uploaded_file = st.file_uploader("📤 Escolha um arquivo Excel ou CSV", type=["xlsx", "xls", "csv"])

# --------------------- PROCESSAMENTO DO ARQUIVO ---------------------
if uploaded_file is not None:
    try:
        file_extension = uploaded_file.name.split(".")[-1]
        if file_extension in ["xlsx", "xls"]:
            df = pd.read_excel(uploaded_file)
        elif file_extension == "csv":
            df = pd.read_csv(uploaded_file)
        else:
            st.error("Formato inválido. Apenas arquivos Excel (.xlsx, .xls) ou CSV são suportados.")
            st.stop()

        if df.empty:
            st.error("O arquivo está vazio ou não contém dados legíveis.")
            st.stop()

        # Limitar para arquivos muito grandes
        if len(df) > 10000:
            st.warning("⚠️ O arquivo contém muitos dados. Uma amostra de 10.000 linhas será exibida para melhor desempenho.")
            df = df.sample(10000, random_state=42)

        st.success("✅ Arquivo carregado com sucesso!")

        # TABS PARA MELHOR EXPERIÊNCIA DO USUÁRIO
        tab1, tab2, tab3, tab4 = st.tabs([
            "📊 Prévia dos Dados",
            "📈 Estatísticas Descritivas",
            "📉 Gráficos",
            "🔗 Correlação"
        ])

        # --------------------- IDENTIFICAÇÃO DE TIPOS ---------------------
        numerical_cols = df.select_dtypes(include=np.number).columns.tolist()
        categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
        datetime_cols = df.select_dtypes(include=['datetime64[ns]']).columns.tolist()

        # --------------------- TAB 1: PRÉVIA ---------------------
        with tab1:
            st.markdown("### Primeiras Linhas do Seu Dataset")
            st.dataframe(df.head())
            st.markdown(f"**Dimensões do Dataset:** {df.shape[0]} linhas, {df.shape[1]} colunas")
            st.markdown("### Tipos de Dados por Coluna")
            st.dataframe(df.dtypes.rename('Tipo de Dado').to_frame())

        # --------------------- TAB 2: ESTATÍSTICAS ---------------------
        with tab2:
            if numerical_cols:
                st.markdown("### Estatísticas Descritivas para Colunas Numéricas")
                st.dataframe(df[numerical_cols].describe().T)
            else:
                st.info("Nenhuma coluna numérica encontrada no arquivo para estatísticas descritivas.")

            if categorical_cols:
                st.markdown("### Contagem de Valores para Colunas Categóricas (Top 10)")
                for col in categorical_cols:
                    st.write(f"**{col}:**")
                    st.dataframe(df[col].value_counts().head(10).to_frame())
            else:
                st.info("Nenhuma coluna categórica encontrada no arquivo para contagem de valores.")

        # --------------------- TAB 3: GRÁFICOS ---------------------
        with tab3:
            col1, col2 = st.columns(2)

            # Gráficos Numéricos
            with col1:
                st.markdown("#### Distribuição de Variáveis Numéricas")
                if numerical_cols:
                    num_cols_to_plot = st.multiselect(
                        "Selecione colunas numéricas para Histograma/Box Plot:",
                        numerical_cols,
                        default=numerical_cols[:min(2, len(numerical_cols))],
                        key="num_plots_multiselect"
                    )
                    for col in num_cols_to_plot:
                        plot_histogram(df, col, f"Distribuição de {col}", theme)
                        plot_box(df, col, f"Box Plot de {col}", theme)
                else:
                    st.info("Nenhuma coluna numérica disponível para gráficos de distribuição.")

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
                elif not datetime_cols:
                    st.info("Nenhuma coluna de data/hora encontrada para gráficos de tendência temporal.")
                elif not numerical_cols:
                     st.info("Nenhuma coluna numérica encontrada para gráficos de tendência temporal.")


            # Gráficos Categóricos e Dispersão
            with col2:
                # Categóricas
                st.markdown("#### Distribuição de Variáveis Categóricas")
                if categorical_cols:
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
                        if 1 < df[col].nunique() < 15: # Plot pie chart only for categories with reasonable number of unique values
                            plot_pie(df, col, f"Distribuição de {col}", theme)
                else:
                    st.info("Nenhuma coluna categórica disponível para gráficos.")

                # Dispersão
                if len(numerical_cols) >= 2:
                    st.markdown("#### Dispersão entre Variáveis Numéricas")
                    x_scatter = st.selectbox("Selecione o Eixo X:", numerical_cols, key="scatter_x_select")
                    y_options = [col for col in numerical_cols if col != x_scatter]
                    if y_options: # Ensure there's a Y option after selecting X
                        y_scatter = st.selectbox("Selecione o Eixo Y:", y_options, key="scatter_y_select")
                        if x_scatter and y_scatter and x_scatter != y_scatter:
                            plot_scatter(df, x_scatter, y_scatter, f"Dispersão de {x_scatter} vs {y_scatter}", theme)
                    else:
                        st.info("Selecione pelo menos duas colunas numéricas para um gráfico de dispersão.")
                else:
                    st.info("São necessárias pelo menos duas colunas numéricas para o gráfico de dispersão.")

        # --------------------- TAB 4: HEATMAP DE CORRELAÇÃO ---------------------
        with tab4:
            st.markdown("### Matriz de Correlação entre Variáveis Numéricas")
            if len(numerical_cols) > 1:
                plot_corr_heatmap(df, numerical_cols, theme)
            else:
                st.info("São necessárias pelo menos duas colunas numéricas para a matriz de correlação.")

    except Exception as e:
        st.error(f"❌ Erro ao processar o arquivo. Certifique-se de que é um arquivo Excel ou CSV válido e bem formatado. Detalhes do erro: {e}")
else:
    st.info("⬆️ Aguardando o upload de um arquivo Excel ou CSV para gerar o dashboard...")


# --------------------- CONTADOR DE VISITAS E FOOTER ---------------------
@st.cache_data(ttl=600)  # Cache for 10 minutes to reduce reads
def get_visits():
    with cloud_resource(name="visit_counter.txt", type="text") as visits_file:
        try:
            count = int(visits_file.getvalue())
        except ValueError:
            count = 0
        return count

def increment_visits():
    with cloud_resource(name="visit_counter.txt", type="text") as visits_file:
        current_visits = get_visits() + 1
        visits_file.write(str(current_visits))
        return current_visits

visits = increment_visits()

st.markdown("---")
col_footer1, col_footer2 = st.columns([0.7, 0.3])
with col_footer1:
    st.markdown("Desenvolvido para portfólio por [@amandaveloso](https://github.com/amandaveloso)")
with col_footer2:
    st.markdown(f"**Visitas à página:** {visits} 🚀")
