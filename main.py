# app_analise_mileage.py

import streamlit as st
import numpy as np
import math
from reliability.Datasets import mileage # Importa a classe mileage

# --- Configurações da Página Streamlit ---
st.set_page_config(layout="wide", page_title="Análise Estatística - Mileage")

# --- Título Principal ---
st.title("📊 Análise Estatística do Dataset 'Mileage'")
st.markdown("Este aplicativo carrega o dataset 'mileage', realiza cálculos estatísticos e exibe os resultados.")

# --- Passo 1: Carregar os Dados ---
st.header("1. Carregamento dos Dados")
dados_array = None # Inicializa para o caso de falha no carregamento
tamanho_N0 = 0

try:
    # Criar uma instância da classe mileage
    instancia_mileage = mileage()
    # Acessar o atributo 'failures'
    lista_de_falhas = instancia_mileage.failures

    if isinstance(lista_de_falhas, list) and len(lista_de_falhas) > 0:
        dados_array = np.array(lista_de_falhas)
        tamanho_N0 = len(dados_array)
        st.success(f"Dataset 'mileage' carregado com sucesso! Contém {tamanho_N0} observações.")

        # Opcional: Mostrar informações do dataset (do atributo .info)
        if hasattr(instancia_mileage, 'info'):
            with st.expander("Informações do Dataset (do atributo .info)"):
                st.text_area("Detalhes:", value=str(instancia_mileage.info), height=150)

        # Mostrar uma amostra dos dados
        with st.expander("Ver Amostra dos Dados Carregados"):
            st.markdown(f"**Primeiras 10 observações:** `{dados_array[:10].tolist()}`")
            st.markdown(f"**Últimas 10 observações:** `{dados_array[-10:].tolist()}`")
            st.dataframe(dados_array, column_config={"value": "Milhagem"})

    else:
        st.error("Os dados de 'failures' não são uma lista válida ou estão vazios.")
        st.stop() # Interrompe a execução se os dados não puderem ser carregados

except Exception as e:
    st.error(f"Ocorreu um erro ao carregar os dados do dataset 'mileage': {e}")
    st.exception(e) # Mostra o traceback completo no app para depuração
    st.stop() # Interrompe a execução

# --- Passo 2: Cálculos Estatísticos ---
# Esta seção só executa se dados_array for válido e tiver tamanho > 0
if dados_array is not None and tamanho_N0 > 0:
    st.header("2. Cálculos Estatísticos Descritivos")

    # 1. Valor Mínimo
    valor_minimo = np.min(dados_array)

    # 2. Valor Máximo
    valor_maximo = np.max(dados_array)

    # 3. Amplitude do Rol (R)
    amplitude_R = valor_maximo - valor_minimo

    # (tamanho_N0 já foi calculado)

    # 5. Número de Classes Calculado (K_sqrt) - Raiz de N0
    K_sqrt = np.sqrt(tamanho_N0)

    # 6. Número de Classes Ajustado (K_sturges) - Regra de Sturges
    if tamanho_N0 > 1:
        K_sturges_calculado = 1 + (3.322 * math.log10(tamanho_N0))
    elif tamanho_N0 == 1:
        K_sturges_calculado = 1.0
    else: # Caso improvável aqui, pois já verificamos tamanho_N0 > 0
        K_sturges_calculado = 0.0
    
    K_sturges_ajustado = round(K_sturges_calculado)
    if tamanho_N0 > 0 and K_sturges_ajustado == 0: # Garante pelo menos 1 classe se houver dados
        K_sturges_ajustado = 1

    # 7. Incremento (h) - Amplitude dividido pelo número de classes ajustado
    if K_sturges_ajustado > 0:
        incremento_h = amplitude_R / K_sturges_ajustado
    else:
        incremento_h = np.nan # Ou 0, ou "Indefinido"

    # --- Exibição dos Resultados dos Cálculos ---
    col1, col2 = st.columns(2)

    with col1:
        st.metric(label="Valor Mínimo", value=f"{valor_minimo:.2f}")
        st.metric(label="Valor Máximo", value=f"{valor_maximo:.2f}")
        st.metric(label="Amplitude do Rol (R)", value=f"{amplitude_R:.2f}")
        st.metric(label="Tamanho da Amostra (N0)", value=int(tamanho_N0))

    with col2:
        st.metric(label="Nº de Classes (K) - Raiz de N0", value=f"{K_sqrt:.2f}")
        st.metric(label="Nº de Classes (K) - Sturges (calculado)", value=f"{K_sturges_calculado:.2f}")
        st.metric(label="Nº de Classes (K) - Sturges (ajustado)", value=int(K_sturges_ajustado))
        if np.isnan(incremento_h):
            st.metric(label="Incremento (h)", value="Indefinido")
        else:
            st.metric(label="Incremento (h)", value=f"{incremento_h:.2f}")
    
    st.markdown("---") # Linha divisória
    st.caption("Nota: O 'Número de Classes Ajustado' pela regra de Sturges é arredondado para o inteiro mais próximo. O incremento (h) é a amplitude dividida por este número ajustado de classes.")

else:
    # Esta mensagem será mostrada se o carregamento de dados falhar e o st.stop() for atingido antes.
    # Mas é uma boa prática ter um fallback.
    if tamanho_N0 == 0 and dados_array is None: # Se falhou bem no início
        st.warning("Não foi possível prosseguir com os cálculos pois os dados não foram carregados.")


# --- Rodapé (Opcional) ---
st.markdown("---")
st.markdown("")