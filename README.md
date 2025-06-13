# 🏃🏻‍♂️ Rapidinho>

"Rapidinho" é um aplicativo web interativo construído no **Streamlit**, que permite aos usuários carregar seus arquivos Excel (`.xlsx`, `.xls`) ou CSV e obter gráficos automáticos para uma análise exploratória rápida dos dados. Ideal para quem precisa de insights visuais sem a necessidade de codificar.

# 📚 Bibliotecas utlizadas:
streamlit: A estrutura principal para construir o aplicativo web interativo.
pandas: Manipulação e análise de dados, incluindo leitura de arquivos (Excel/CSV), seleção de tipos de dados e cálculo de estatísticas descritivas.
plotly.express: Utilizada para a criação de todos os gráficos interativos
numpy: Apoia operações numéricas e a identificação de colunas de dados numéricos.

# 🎨 Funções do Streamlit (st.)
As funções do Streamlit são a base da interface do usuário e da interatividade do aplicativo:

st.set_page_config(): Configurações globais da página (título, ícone, layout).
st.title(): Exibe o título principal do aplicativo.
st.markdown(): Renderiza texto formatado com Markdown.
st.expander(): Cria seções de conteúdo expansíveis/colapsáveis.
st.file_uploader(): Permite o upload de arquivos pelo usuário.
st.success(), st.warning(), st.error(), st.info(): Exibem mensagens de feedback ao usuário.
st.stop(): Interrompe a execução do script.
st.dataframe(): Exibe DataFrames do Pandas em formato de tabela interativa.
st.tabs(): Organiza o conteúdo em múltiplas abas para melhor navegação.
st.columns(): Divide a interface em colunas para organização horizontal de elementos.
st.sidebar.*: Todas as funções prefixadas com sidebar. posicionam widgets e elementos na barra lateral.
st.multiselect(): Permite seleção de múltiplas opções de uma lista.
st.selectbox(): Permite seleção de uma única opção de uma lista.
st.plotly_chart(): Renderiza figuras Plotly no aplicativo Streamlit.
st.write(): Uma função genérica para exibir diversos tipos de conteúdo.

# 📊 Funções de plotagem (plotly.express)
As funções personalizadas no código (plot_histogram, plot_box, plot_bar, plot_pie, plot_scatter, plot_corr_heatmap) encapsulam chamadas específicas do Plotly Express para gerar os diferentes tipos de gráficos:

px.histogram(): Para distribuições de frequência.
px.box(): Para visualizar a distribuição e identificar outliers.
px.bar(): Para contagens e comparações categóricas.
px.pie(): Para distribuições proporcionais.
px.scatter(): Para explorar relações entre duas variáveis numéricas.
px.imshow(): Para criar heatmaps, neste caso, para a matriz de correlação.
