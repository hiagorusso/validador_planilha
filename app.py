import streamlit as st
import pandas as pd
from io import BytesIO

def main():
    st.title('Aplicação de Análise de Arquivos XLSX')
    st.write("Faça o upload dos dois arquivos XLSX para começar a análise.")

    # Upload dos dois arquivos
    file1 = st.file_uploader("Upload da base de dados XLSX", type="xlsx")
    file2 = st.file_uploader("Upload do arquivo para validar XLSX", type="xlsx")

    if file1 is not None and file2 is not None:
        try:
            # Leitura dos arquivos XLSX
            base_dados = pd.read_excel(file1)
            arquivo_validar = pd.read_excel(file2)

            # Exibir as primeiras linhas dos dataframes para o usuário
            st.write("Visualização do Primeiro Arquivo:")
            st.dataframe(base_dados.head())

            st.write("Visualização do Segundo Arquivo:")
            st.dataframe(arquivo_validar.head())

            # Verificar se ambas as planilhas têm as mesmas colunas
            if set(base_dados.columns) != set(arquivo_validar.columns):
                st.warning("As planilhas têm colunas diferentes. Certifique-se de que ambas têm as mesmas colunas.")
            else:
                # DataFrame para armazenar as diferenças
                diferencas = pd.DataFrame()

                # Comparar cada coluna, ignorando maiúsculas e minúsculas
                for coluna in base_dados.columns:
                    # Converter para minúsculas para a comparação
                    base_dados_lower = base_dados[coluna].astype(str).str.lower()
                    validar_lower = arquivo_validar[coluna].astype(str).str.lower()

                    # Identificar valores únicos na Planilha 2
                    valores_unicos = arquivo_validar[~validar_lower.isin(base_dados_lower)]

                    # Adicionar valores únicos ao DataFrame de diferenças
                    if not valores_unicos.empty:
                        diferencas = pd.concat([diferencas, valores_unicos[[coluna]]], axis=1)

                if not diferencas.empty:
                    # Salvar as diferenças em um buffer para download
                    output = BytesIO()
                    with pd.ExcelWriter(output, engine="openpyxl") as writer:
                        diferencas.to_excel(writer, index=False)
                    output.seek(0)

                    # Botão para baixar o arquivo de diferenças fora do loop
                    st.download_button(
                        label="Baixar arquivo de diferenças",
                        data=output,
                        file_name="diferencas_por_coluna.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        key="unique_download_button"  # chave única
                    )
                else:
                    st.success("Todas as informações da Planilha 2 já estão presentes na Planilha 1.")
        except Exception as e:
            st.error(f"Erro ao processar os arquivos: {e}")

if __name__ == "__main__":
    main()
