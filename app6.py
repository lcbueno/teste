import pandas as pd
import streamlit as st
import seaborn as sns
import plotly.express as px
import matplotlib.pyplot as plt

# Carregar o dataset
df = pd.read_csv('/Users/luizbueno/Downloads/yamaha/dados/dataset.csv')  # Certifique-se de usar o caminho correto do seu arquivo CSV

# Converter a coluna "Date" para datetime
df['Date'] = pd.to_datetime(df['Date'], dayfirst=True, errors='coerce')

# Verificar se há datas inválidas
if df['Date'].isna().sum() > 0:
    st.warning("Algumas datas não puderam ser convertidas e foram definidas como NaT (Not a Time). Verifique o dataset.")

# Título do Dashboard
st.title('Dashboard de Vendas de Automóveis')

# Filtro por Região
regions = df['Dealer_Region'].unique()
selected_region = st.multiselect('Selecione a Região', regions, default=regions)

# Filtro por Data
min_date = df['Date'].min().date()  # Converter para datetime.date
max_date = df['Date'].max().date()  # Converter para datetime.date
selected_dates = st.date_input('Selecione o Período', [min_date, max_date])

# Converter as datas selecionadas para datetime64[ns]
selected_dates = [pd.to_datetime(date) for date in selected_dates]

# Filtrando o DataFrame
filtered_df = df[(df['Dealer_Region'].isin(selected_region)) & 
                 (df['Date'].between(selected_dates[0], selected_dates[1]))]

# Gráfico 1: Distribuição de vendas por Região
st.subheader('Distribuição de Vendas por Região')
sales_by_region = filtered_df['Dealer_Region'].value_counts().reset_index()
sales_by_region.columns = ['Dealer_Region', 'count']  # Renomear colunas
fig1 = px.pie(sales_by_region, names='Dealer_Region', values='count', title='Vendas por Região')
st.plotly_chart(fig1)

# Gráfico 2: Receita média por Tipo de Carro
st.subheader('Receita Média por Tipo de Carro')
avg_price_by_body = filtered_df.groupby('Body Style')['Price ($)'].mean().reset_index()
fig2 = px.bar(avg_price_by_body, x='Body Style', y='Price ($)', title='Receita Média por Tipo de Carro')
st.plotly_chart(fig2)

# Gráfico 3: Distribuição de Gênero por Região
st.subheader('Distribuição de Gênero por Região')
gender_distribution = filtered_df.groupby(['Dealer_Region', 'Gender']).size().reset_index(name='Counts')
fig3 = px.bar(gender_distribution, x='Dealer_Region', y='Counts', color='Gender', barmode='group', title='Distribuição de Gênero por Região')
st.plotly_chart(fig3)

# Gráfico 4: Evolução de Vendas ao Longo do Tempo
st.subheader('Evolução de Vendas ao Longo do Tempo')
sales_over_time = filtered_df.groupby('Date').size().reset_index(name='Counts')
fig4 = px.line(sales_over_time, x='Date', y='Counts', title='Evolução de Vendas')
st.plotly_chart(fig4)

# Gráfico 5: Top 10 Empresas com Maior Receita
st.subheader('Top 10 Empresas com Maior Receita')
top_companies = filtered_df.groupby('Company')['Price ($)'].sum().reset_index().sort_values(by='Price ($)', ascending=False).head(10)
fig5 = px.bar(top_companies, x='Company', y='Price ($)', title='Top 10 Empresas por Receita')
st.plotly_chart(fig5)

# Gráfico 6: Distribuição de Transmissão por Tipo de Motor
st.subheader('Distribuição de Transmissão por Tipo de Motor')
transmission_distribution = filtered_df.groupby(['Engine', 'Transmission']).size().reset_index(name='Counts')
fig6 = px.bar(transmission_distribution, x='Engine', y='Counts', color='Transmission', barmode='group', title='Distribuição de Transmissão por Tipo de Motor')
st.plotly_chart(fig6)

# Gráfico 7: Top 10 Modelos mais Comprados por Gênero
st.subheader('Top 10 Modelos mais Comprados por Gênero')
top_10_male_models = filtered_df[filtered_df['Gender'] == 'Male']['Model'].value_counts().head(10)
top_10_female_models = filtered_df[filtered_df['Gender'] == 'Female']['Model'].value_counts().head(10)

top_10_models_df = pd.DataFrame({
    'Male': top_10_male_models,
    'Female': top_10_female_models
}).fillna(0)

# Ordenando o DataFrame do maior para o menor baseado na soma das vendas de ambos os gêneros
top_10_models_df_sorted = top_10_models_df.sort_values(by=['Male', 'Female'], ascending=False)

fig7 = px.bar(top_10_models_df_sorted, 
              x=top_10_models_df_sorted.index, 
              y=['Male', 'Female'], 
              title='Top 10 Modelos mais Comprados por Gênero',
              labels={'value': 'Número de Vendas', 'index': 'Modelos'},
              barmode='group')

st.plotly_chart(fig7)

# Gráfico 8: Renda Anual Média por Modelo de Carro (Top 15)
st.subheader('Renda Anual Média por Modelo de Carro (Top 15)')
average_income_by_model_top15 = df.groupby('Model')['Annual Income'].mean().loc[df['Model'].value_counts().index[:15]].sort_values(ascending=False)

fig8 = px.bar(average_income_by_model_top15, 
              x=average_income_by_model_top15.index, 
              y=average_income_by_model_top15.values, 
              title='Renda Anual Média por Modelo de Carro (Top 15)',
              labels={'x': 'Modelo', 'y': 'Renda Anual Média ($)'},
              color_discrete_sequence=['#1f77b4'])

st.plotly_chart(fig8)

# Gráfico 9: Evolução das Vendas ao Longo do Tempo por Região
st.subheader('Evolução das Vendas ao Longo do Tempo por Região')
sales_over_time_region = df.groupby([df['Date'].dt.to_period('M'), 'Dealer_Region']).size().unstack().fillna(0).reset_index()
sales_over_time_region['Date'] = sales_over_time_region['Date'].astype(str)  # Converter para string para ser compatível com Plotly

fig9 = px.line(sales_over_time_region, 
               x='Date', 
               y=sales_over_time_region.columns[1:], 
               title='Evolução das Vendas ao Longo do Tempo por Região',
               labels={'value': 'Número de Vendas', 'Date': 'Mês'},
               color_discrete_sequence=px.colors.qualitative.Set1)  # Substituindo por Set1

st.plotly_chart(fig9)

# Configurando o estilo do gráfico para ser mais elegante com fundo preto
plt.style.use('dark_background')
sns.set(style="whitegrid")

# Gráfico 10: Séries Temporais de Vendas por Região e Modelo
st.subheader('Séries Temporais de Vendas por Região e Modelo')

# Filtro para a série temporal
selected_region_time_series = st.selectbox('Selecione a Região para a Série Temporal', regions)
selected_model_time_series = st.selectbox('Selecione o Modelo para a Série Temporal', df['Model'].unique())

# Função para plotar as séries temporais de vendas por região e modelo
def plot_sales(region, model):
    sales_time = df[(df['Dealer_Region'] == region) & (df['Model'] == model)].groupby(df['Date'].dt.to_period('M')).size()
    plt.figure(figsize=(14, 8))
    sales_time.plot(kind='line', marker='o', color='#FF7F0E', linewidth=2, markersize=6)  # Linha laranja
    plt.title(f'Séries Temporais de Vendas Mensais - Região: {region}, Modelo: {model}', fontsize=16, color='white')
    plt.xlabel('Mês', fontsize=14, color='white')
    plt.ylabel('Número de Vendas', fontsize=14, color='white')
    plt.grid(True, color='gray', linestyle='--', linewidth=0.5)
    plt.xticks(fontsize=12, color='white')
    plt.yticks(fontsize=12, color='white')
    plt.gca().spines['top'].set_color('none')
    plt.gca().spines['right'].set_color('none')
    plt.gca().set_facecolor('black')  # Definindo o fundo como preto
    plt.gca().xaxis.label.set_color('white')  # Cor do eixo X
    plt.gca().yaxis.label.set_color('white')  # Cor do eixo Y
    plt.gca().title.set_color('white')        # Cor do título
    plt.gca().tick_params(axis='x', colors='white')  # Cor dos ticks do eixo X
    plt.gca().tick_params(axis='y', colors='white')  # Cor dos ticks do eixo Y
    st.pyplot(plt)

# Plotando a série temporal
plot_sales(selected_region_time_series, selected_model_time_series)

# Gráfico 11: Heatmap do Mix de Produtos por Região (Body Style)
st.subheader('Heatmap do Mix de Produtos por Região (Body Style)')

# Agrupando por região e estilo de carroceria
mix_product_region = df.groupby(['Dealer_Region', 'Body Style']).size().unstack().fillna(0)

# Criando o heatmap
plt.figure(figsize=(12, 8))
sns.heatmap(mix_product_region, annot=True, cmap='coolwarm', fmt='g')
plt.title('Mix de Produtos por Região (Body Style)', fontsize=16, color='white')
plt.xlabel('Estilo de Carroceria', fontsize=14, color='white')
plt.ylabel('Região do Revendedor', fontsize=14, color='white')
plt.xticks(fontsize=12, color='white')
plt.yticks(fontsize=12, color='white')
st.pyplot(plt)
