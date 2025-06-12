# app.py

import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# Configuração da página do Streamlit
st.set_page_config(
    page_title="ExcelViz: Gerador de Dashboards",
    page_icon="📊",
    layout="wide", # Layout mais amplo para o dashboard
    initial_sidebar_state="auto" # Define o estado inicial da sidebar
)

st.title("📊 ExcelViz: Gerador de Dashboards Automático")
st.markdown("Faça o upload do seu arquivo Excel (.xlsx ou .xls) e visualize seus dados instantaneamente!")

# --- 1. Upload do Arquivo ---
uploaded_file = st.file_uploader("Escolha um arquivo Excel", type=["xlsx", "xls"])

if uploaded_file is not None:
    try:
        # Carregar o Excel
        df = pd.read_excel(uploaded_file)
        st.success("Arquivo carregado com sucesso!")

        # Exibir as primeiras linhas da tabela para o usuário verificar
        st.subheader("Prévia dos Dados:")
        st.dataframe(df.head())

        # --- 2. Análise e Geração de Dashboard ---
        st.subheader("Dashboard Automatizado")

        # Separar colunas por tipo para análise
        numerical_cols = df.select_dtypes(include=np.number).columns.tolist()
        # CORREÇÃO AQUI: Removido o "= df" indevido
        categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
        datetime_cols = df.select_dtypes(include=['datetime64[ns]']).columns.tolist()

        # Adicionar uma sidebar para configurações e filtros (opcional, mas bom para usabilidade)
        st.sidebar.title("Configurações e Filtros")

        # --- Seção de Métricas Descritivas ---
        if numerical_cols:
            st.markdown("### Estatísticas Descritivas")
            st.dataframe(df[numerical_cols].describe().T) # Transpor para melhor visualização

        # --- Seção de Gráficos ---
        # Usando colunas para organizar o layout
        col1, col2 = st.columns(2)

        # Gráficos para variáveis numéricas
        if numerical_cols:
            with col1: # Colocar gráficos numéricos na primeira coluna
                st.markdown("### Análise de Variáveis Numéricas")
                num_cols_to_plot = st.multiselect(
                    "Selecione colunas numéricas para Histograma/Box Plot:",
                    numerical_cols,
                    default=numerical_cols[:min(2, len(numerical_cols))] if numerical_cols else [],
                    key="num_plots_multiselect" # Chave única para o widget
                )
                for col in num_cols_to_plot:
                    if col:
                        # Histograma
                        fig_hist = px.histogram(df, x=col, title=f"Distribuição de {col}")
                        st.plotly_chart(fig_hist, use_container_width=True)

                        # Box Plot
                        fig_box = px.box(df, y=col, title=f"Box Plot de {col}")
                        st.plotly_chart(fig_box, use_container_width=True)
            
            # Gráficos de tendências (se houver data e ao menos uma numérica)
            with col2: # Colocar tendências na segunda coluna
                if datetime_cols and numerical_cols:
                    st.markdown(f"### Tendências Temporais")
                    date_col_selected = st.selectbox("Selecione a coluna de Data:", datetime_cols, key="date_col_select")
                    num_col_for_trend = st.selectbox("Selecione a Variável Numérica para a Tendência:", numerical_cols, key="trend_num_select")
                    
                    if date_col_selected and num_col_for_trend:
                        # Agrupa por data para séries temporais (soma os valores para a mesma data)
                        df_agg = df.groupby(date_col_selected)[num_col_for_trend].sum().reset_index()
                        fig_line = px.line(df_agg, x=date_col_selected, y=num_col_for_trend, 
                                           title=f"Tendência de {num_col_for_trend} por {date_col_selected}")
                        st.plotly_chart(fig_line, use_container_width=True)


        # Usando colunas novamente para organizar categóricas e dispersão
        col3, col4 = st.columns(2)

        # Gráficos para variáveis categóricas
        if categorical_cols:
            with col3: # Colocar gráficos categóricos na terceira coluna
                st.markdown("### Análise de Variáveis Categóricas")
                cat_cols_to_plot = st.multiselect(
                    "Selecione colunas categóricas para Contagem/Distribuição:",
                    categorical_cols,
                    default=categorical_cols[:min(2, len(categorical_cols))] if categorical_cols else [],
                    key="cat_plots_multiselect" # Chave única para o widget
                )
                for col in cat_cols_to_plot:
                    if col:
                        # Contagem de valores (Gráfico de Barras)
                        counts = df[col].value_counts().reset_index()
                        counts.columns = [col, 'Contagem']
                        fig_bar = px.bar(counts, x=col, y='Contagem', title=f"Contagem de {col}")
                        st.plotly_chart(fig_bar, use_container_width=True)

                        # Distribuição (Gráfico de Pizza - para poucas categorias)
                        if df[col].nunique() < 15 and df[col].nunique() > 1:
                            fig_pie = px.pie(df, names=col, title=f"Distribuição de {col}")
                            st.plotly_chart(fig_pie, use_container_width=True)

        # Gráfico de dispersão entre duas variáveis numéricas
        if len(numerical_cols) >= 2:
            with col4: # Colocar gráfico de dispersão na quarta coluna
                st.markdown("### Relação entre Variáveis Numéricas")
                x_scatter = st.selectbox("Selecione o Eixo X (Dispersão):", numerical_cols, key="scatter_x_select")
                # Garante que o y_scatter não seja o mesmo que x_scatter
                remaining_cols_for_y = [col for col in numerical_cols if col != x_scatter]
                y_scatter = st.selectbox("Selecione o Eixo Y (Dispersão):", remaining_cols_for_y, key="scatter_y_select")
                
                if x_scatter and y_scatter and x_scatter != y_scatter:
                    fig_scatter = px.scatter(df, x=x_scatter, y=y_scatter, 
                                             title=f"Dispersão de {x_scatter} vs {y_scatter}")
                    st.plotly_chart(fig_scatter, use_container_width=True)
            

    except Exception as e:
        st.error(f"Erro ao processar o arquivo. Certifique-se de que é um arquivo Excel válido e bem formatado. Detalhes do erro: {e}")

else:
    st.info("Aguardando o upload de um arquivo Excel para gerar o dashboard...")

st.markdown("---")
st.markdown("Desenvolvido para portfólio de Analista de Dados - [@SeuNome ou SeuGitHub](https://github.com/seu-usuario)")
