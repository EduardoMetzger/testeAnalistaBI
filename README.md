# Apresentação do case: Panorama de ações.pbix

### 1️. Processamento

Optei em realizar todo o processo de **ETL com Python**, incluindo a orquestração das etapas no arquivo [run_all.py](./scripts/run_all.py).  
Outra escolha foi de manter em `.csv` todos os outputs dos scripts. Estas duas escolhas foram tomadas apenas para simplificar o processo de leitura e análise deste case.

Iniciei pela extração e replicação dos arquivos localizados em [spreadsheets](./spreadsheets) para [raw](./files/raw).  
Depois disso, realizei processos de limpeza de campos que não seriam utilizados e renomeei conforme a necessidade na camada *clean*.

Em uma análise prévia dos dados, identifiquei que são comuns os casos de falta de dados históricos para algumas empresas.  
De modo a possibilitar o comparativo dos indicadores escolhidos (descrevo-os abaixo), mantive somente empresas que possuem 9 meses ou mais de histórico no arquivo [bolsa_cotacoes.csv](./files/raw/bolsa_cotacoes.csv).  
Também identifiquei que alguns valores estavam omitindo o separador decimal, portanto apliquei na etapa [enrich_f_cotacoes.py](./scripts/load/enrich_f_cotacoes.py) uma validação e ajuste destas situações.  
Por fim, mantive apenas cotações no período de 01/01/2021 à 31/12/2022 para dar sentido à análise.

###  1.1. Representação do processo de ETL

Esta é uma representação do processo de ETL deste case.  
Todos os scripts são chamados pelo arquivo [run_all.py](./scripts/run_all.py).

![Screenshot_1](https://github.com/user-attachments/assets/79c663e1-b0cf-44ad-a3c8-e3652d6ec162)

---

## 2️. Modelagem de dados

Todo o processo de ETL foi feito pensando em obter um star schema no painel do Power BI.  
De modo a simplificar a estrutura final, unifiquei os dados de empresa e empresas da bolsa em uma única tabela.  
Deste modo, todos os dados referentes às empresas ficam centralizados.  
Há uma ressalva nesta metodologia a depender do volume de dados, mas para este case o cenário é aplicável.

---

## 3️. Análises propostas

O objetivo das visões é permitir ao usuário explorar ações com potencial de crescimento e analisar suas variações de movimento diário, sempre buscando personalização de perfil de investimento.  
Com isso, as visões disponibilizadas não só indicam as principais métricas, como também permitem apersonalização de acordo com o perfil de investimento do usuário.  
Utilizei como base de comparativo histórico o valor das ações no fechamento do pregão, mas aqui há espaço para discussão da melhor regra de negócio a ser adotada.

---

## 4. Usabilidade

O relatório possui controladores (slicers, hyperlinks, botões, etc.) pensados para uso na web.  
Caso este relatório seja utilizado no **Power BI Desktop**, utilize `CTRL + Clique` para executar a ação dos botões.

---

## 5. Visões

### 5.1. Início

Apresenta o objetivo do painel e um resumo das regras utilizadas.  
Também direciona para a documentação oficial do painel com o descritivo de todas as tratativas aplicadas.

---

### 5.2. Potencial

Esta visão foi desenvolvida com base nas perguntas:

- “Quais ações estão valorizando mais?”
- “Esse crescimento é constante ou irregular?”

O quadro Histórico de Crescimento vs. Mês Anterior apresenta uma evolução histórica da valorização das ações ao mesmo tempo que indica se esta valorização é estável ou irregular.  
Logo ao lado, é possível analisar uma associação entre o valor da ação e o seu percentual de crescimento.  
O objetivo é permitir ao usuário avaliar um crescimento acelerado de ações pequenas ou um crescimento vagaroso de ações maiores.

Alguns recursos de usabilidade foram aplicados para melhorar a experiência do usuário:

![image](https://github.com/user-attachments/assets/a3d93845-64b5-46cc-b4c4-cc91e0cbb4d0)

---

### 5.3. Calendário de variação

Na visão anterior, entendemos o que está valorizando mais e a estabilidade dessa valorização.  
Aqui no Calendário de Variação, podemos analisar em que momento do dia é melhor comprar uma ação — abertura ou fechamento.  
Também é possível visualizar o detalhamento dos pregões e todas as movimentações por ação.

---

### 5.4. Analítico

Self-service de dados: nesta visão o usuário pode construir sua própria visualização de resumo dos dados do painel.
