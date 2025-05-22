
# Diário de Bordo – Desafio Técnico de Web Scraping e Integração com API

O objetivo do script é extrair uma imagem de forma automatizada, processá-la com IA para obter uma descrição textual, e transmitir esse resultado a um sistema que valida ou registra a saída, o que é uma prática comum em sistemas de automação baseados em inteligência artificial.
---
## Parte 1: Web Scraping da Imagem

Realizar scraping da URL fornecida para obter e salvar localmente a imagem exibida na página:
```
https://intern.aiaxuropenings.com/scrape/407988b0-b245-4a8d-bde5-1a1bbaaf902a
```

### Estratégia
- foi utilizado `requests` para baixar o conteúdo da página.
- Com `BeautifulSoup`, para localiza a tag `<img>` que continha a imagem.
- Identificar que a imagem estava embutida em formato `base64`, ou seja, incorporada diretamente na página HTML.
- Foi decodificado o conteúdo base64 e salvamos a imagem localmente com extensão apropriada (`jpeg`, `png`, etc.).

### Dificuldades e Soluções
- A principal dificuldade foi perceber que não se tratava de uma URL tradicional de imagem, mas sim de uma string embutida com o prefixo `data:image/...;base64,...`.
- A solução envolveu fazer o split do conteúdo base64, identificar a extensão da imagem no cabeçalho e usar `base64.b64decode()` para salvar corretamente a imagem.

---

## Parte 2: Envio para Inferência com API

Enviar a imagem obtida para a API de inferência do modelo `microsoft-florence-2-large`, utilizando a seguinte URL:
```
https://intern.aiaxuropenings.com/v1/chat/completions
```

### Estratégia
- Ler a imagem salva e codificar novamente em base64.
- Criar o payload no formato semelhante ao da OpenAI API, com os campos `model`, `messages`, `images` e `temperature`.
- Utilizar o prompt `<DETAILED_CAPTION>`, conforme orientações.
- Enviar a requisição com autenticação via token no header (`Authorization: Bearer <token>`).

### Dificuldades e Soluções
- Como o endpoint se assemelha ao padrão OpenAI, segui o formato exato do campo `images`.
- Utilizi uma abordagem minimalista e validei experimentalmente até a resposta do modelo ser bem-sucedida.

---

## Parte 3: Submissão da Resposta para Avaliação

Submeter o JSON retornado pelo modelo para a plataforma de avaliação via API:
```
https://intern.aiaxuropenings.com/api/submit-response
```

### Estratégia
- Reutilizei os headers e o token de autenticação da etapa anterior.
- Submeti exatamente o JSON recebido do modelo, sem alterações, conforme exigido.
- A resposta foi verificada e o status de submissão foi exibido.

### Dificuldades e Soluções
- O maior cuidado foi garantir que o JSON não fosse modificado ou reestruturado antes do envio.
- Utilizamos diretamente o retorno de `response.json()` para manter a fidelidade da estrutura.

---

## Resultado Final

O script unificado executa as três etapas de forma sequencial:
1. Raspagem da imagem embutida em base64 e salvamento local;
2. Envio da imagem codificada para inferência com o modelo;
3. Submissão da resposta JSON retornada para validação na plataforma.

Todo o processo foi automatizado em um único arquivo `.py` e também disponibilizado como notebook `.ipynb` para uso em Google Colab/Jupyter Notebook.

---

## Instruções de Uso

### Requisitos
- Python 3.x
- Bibliotecas:
  - `requests`
  - `beautifulsoup4`
  - `base64` (nativa)

### Execução via terminal
```bash
pip install requests beautifulsoup4
python3 scraper.py
```

### Execução via Google Colab/Jupyter Notebook
- Faça o upload do arquivo `desafio_scraper_completo.ipynb`
- Clique em "Executar tudo"

---

## Estrutura de Arquivos

```
├── scraper_axur.py                 # Script completo com scraping, envio e submissão
├── scraper_notebook_axur.ipynb    # Versão notebook para uso no Google Colab/Jupyter notebook
├── imagem_scrape.jpeg                # Imagem salva localmente a partir do scraping
├── README.md           # Este documento com o diário de bordo
```

---

## Considerações Finais

Este desafio envolveu o domínio de scraping, manipulação de imagens em base64 e integração com APIs no padrão OpenAI. A execução em três etapas exigiu atenção à fidelidade de dados, controle de exceções e aderência ao formato esperado pelas APIs.
