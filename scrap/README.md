# Cunha Visível

Responsabilidade de fazer scrap, e criação dos dados para front-end

## Instalação

Para instalar as dependências e configurar o ambiente, siga os passos abaixo:

1. Clone o repositório:
    ```sh
    git clone https://github.com/fabiojcp/cunha-visivel.git
    cd cunha-visivel
    cd scrap
    ```

2. Instale o Poetry, se ainda não estiver instalado:
    ```sh
    pip install poetry
    ```

3. Instale as dependências do projeto:
    ```sh
    poetry install
    ```

4. Inicie o shell:
    ```sh
    poetry shell
    ```

5. Instale Pyenv (Opcional):
    ```sh
    curl https://pyenv.run | bash
    ```

    Edite seu bash ```vim ~/.bashrc``` ou ```code ~/.bashrc```, adicione no final do arquivo:
    ```sh
    export PYENV_ROOT="$HOME/.pyenv"
    [[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"
    eval "$(pyenv init -)"
    ```
    
    Adicione localmente a versão de python:
    ```sh
    pyenv local 3.12
    ```

    O pyenv é uma ferramenta de gerenciamento de versões do Python que permite alternar entre diferentes versões do Python de forma fácil. Ele pode instalar várias versões do Python e definir versões globais ou específicas por projeto. Usando um arquivo .python-version, pyenv garante que o projeto utilize a versão exata do Python especificada. Isso é especialmente útil para trabalhar com múltiplos projetos que requerem diferentes versões do Python.

    Para mais informações, visite o repositório pyenv no [GitHub](https://github.com/pyenv/pyenv).

## Como Usar

- `cunha`: Comando CLI de scraper do site do diário oficial da cidade de Cunha/SP [link](https://www.imprensaoficialmunicipal.com.br/cunha)

### Parâmetros obrigatórios:

  - **`nome_da_pasta`** 
    - **Tipo:** String
    - **Descrição:** destino dos arquivos, exemplo: `cunha scrap` ou `cunha cunha.workdir`, o sufixo `.workdir` será adicionado automaticamente caso não seja indicado

### Parâmetros opcionais:
  - **`--at-most`**
    - **Tipo:** Inteiro
    - **Padrão:** 10
    - **Descrição:** Define o número máximo de arquivos PDF a serem baixados durante a execução.

  - **`--url`**
    - **Tipo:** String
    - **Padrão:** `"https://www.imprensaoficialmunicipal.com.br/cunha"`
    - **Descrição:** Especifica a URL completa de onde os arquivos PDF serão raspados.
    - **Exceção:** Não pode ser usado junto do parâmetro `--city`

  - **`--city`**
    - **Tipo:** String
    - **Padrão:** `"cunha"`
    - **Descrição:** Especifica o caminho da cidade na URL de onde os arquivos PDF serão raspados.
    - **Exceção:** Não pode ser usado junto do parâmetro `--url`

  - **`--href`**
    - **Tipo:** String
    - **Padrão:** `'a[href^="https://dosp.com.br/impressao.php?i="]'`
    - **Descrição:** Selector CSS para identificar os botões que abrem os PDFs durante a raspagem.

  - **`--next-btn`**
    - **Tipo:** String
    - **Padrão:** "a.next"
    - **Descrição:** Selector CSS para identificar o botão de "próximo" que avança para a próxima página durante a raspagem.

  - **`--count-existing`**
    - **Tipo:** Flag
    - **Descrição:** Se habilitado, ignora o download de PDFs que já existem no destino na contagem de máximo de arquivos em `--at-most`.

  

## Dependências

- **certifi**: 2023.5.7
  - Descrição: Pacote de CA (Certificate Authority) Bundle no formato PEM.

- **charset-normalizer**: 3.1.0
  - Descrição: Decodificador de texto que detecta automaticamente a codificação e garante a conversão precisa de qualquer texto em Unicode.

- **idna**: 3.4
  - Descrição: Implementação do mecanismo de codificação IDNA (Internationalized Domain Names in Applications).

- **numpy**: 1.24.3
  - Descrição: Biblioteca fundamental para computação científica em Python, com suporte a arrays e matrizes multidimensionais.

- **pandas**: 2.0.2
  - Descrição: Biblioteca poderosa e flexível para análise e manipulação de dados.

- **Pillow**: 9.5.0
  - Descrição: Biblioteca de manipulação de imagens que suporta muitos formatos de arquivo e funcionalidades de processamento de imagem.

- **python-dateutil**: 2.8.2
  - Descrição: Extensões para a biblioteca datetime do Python, oferecendo suporte a parsing, operações e manipulação de datas e horários.

- **pytz**: 2023.3
  - Descrição: Biblioteca que suporta fusos horários baseados no banco de dados da IANA.

- **requests**: 2.31.0
  - Descrição: Biblioteca simples e elegante para fazer requisições HTTP em Python.

- **six**: 1.16.0
  - Descrição: Biblioteca de compatibilidade entre Python 2 e Python 3.

- **tqdm**: 4.65.0
  - Descrição: Biblioteca para criar barra de progresso em loops e iterações.

- **urllib3**: 2.0.2
  - Descrição: Biblioteca com um cliente HTTP robusto e funcionalidades avançadas.

## Contribuição

1. Faça um fork do projeto.
2. Crie uma branch para sua feature (`git checkout -b feature/nome-da-feature`).
3. Commit suas mudanças (`git commit -am 'Adiciona nova feature'`).
4. Faça o push para a branch (`git push origin feature/nome-da-feature`).
5. Abra um Pull Request.