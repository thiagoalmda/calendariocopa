# Projeto: Gerador de Calendário da Copa do Mundo para Google Agenda

## Objetivo
Criar um script (em Python ou Node.js) que busque os dados atualizados da Copa do Mundo e gere um arquivo de calendário (`.ics`) pronto para ser importado no Google Agenda. O sistema deve ser desenhado para atualizar os eventos automaticamente conforme as fases da Copa avançam (ex: substituindo "Vencedor Grupo A" pela seleção classificada), sem criar eventos duplicados.

## Instruções de Implementação para o Claude Code

Por favor, atue como um Engenheiro de Software Sênior e construa a solução seguindo rigorosamente os requisitos abaixo:

### 1. Formato de Saída (Arquivo `.ics`)
- O script deve gerar um arquivo no formato `.ics` (iCalendar). Diferente de um CSV, o `.ics` é o formato nativo para calendários e lida melhor com fusos horários e atualizações.

### 2. Títulos, Nomes e Bandeiras (Emojis)
- Os títulos dos eventos na agenda devem conter obrigatoriamente as **bandeiras em emoji** e o nome das seleções.
- Exemplo de título de evento final: `🇧🇷 Brasil vs Argentina 🇦🇷`
- Para jogos onde os times ainda não estão definidos (fases eliminatórias futuras), use placeholders indicativos, por exemplo: `🏳️ 1º Grupo A vs 2º Grupo B 🏳️`.
- **Tarefa**: Crie um dicionário/mapeamento de dados interno no código que relacione o nome do país com o seu respectivo emoji de bandeira.

### 3. Mecanismo Auto-Incremental (Crucial para o Google Agenda)
Para que o calendário se atualize quando importado novamente (em vez de duplicar todos os jogos), o Google Agenda depende do campo **`UID`** (Unique Identifier) do iCalendar.
- **Regra**: Cada partida deve ter um `UID` fixo e estático. Você deve gerar esse UID baseando-se em um identificador único imutável da partida (como o ID da partida na API ou o número do jogo, ex: `match-01-worldcup-2026@seuprojeto.com`).
- Dessa forma, quando as oitavas de final forem definidas, o usuário roda o script de novo, gera o `.ics` atualizado e o Google Agenda apenas sobrescreve o evento existente, preenchendo os times classificados.

### 4. Fonte de Dados Totalmente Automática (API)
- **ATENÇÃO:** O sistema **NÃO DEVE** depender de edição manual de arquivos locais (como editar um `teams.json` na mão) para atualizar quem passou de fase. A atualização deve ser 100% automática.
- Programe a extração de dados utilizando exclusivamente uma API pública/gratuita e viva de futebol (como *football-data.org*, *API-Football*, ou uma API específica da Copa) que retorne os jogos já atualizados com os times classificados.
- Quando o usuário rodar o script (ex: `python main.py` ou `node index.js`), o script deve bater nessa API, ler os dados mais recentes e gerar o novo `.ics`.
- Caso a API exija chave, deixe o suporte via variável de ambiente (ex: `.env`) e documente onde o usuário pode gerar a chave gratuita.

### 5. Detalhes Adicionais do Evento no Calendário
- **Fuso Horário**: Todas as datas e horas devem ser passadas preferencialmente em UTC no `.ics`, para que o Google Agenda converta automaticamente para o horário local de quem visualizar.
- **Local/Location**: Inserir o estádio e cidade da partida.
- **Descrição/Description**: Inclua o nome da fase (ex: "Fase de Grupos - Rodada 1", "Oitavas de Final").

### 6. Linguagem e Stack
- Utilize **Python** (com bibliotecas como `icalendar` e `requests`) ou **Node.js** (com `ics` e `axios`). Escolha a que fornecer a solução mais simples, elegante e de fácil execução para o usuário final.

## Plano de Ação para o Claude
1. **Configuração**: Inicialize o ambiente (crie `package.json` ou `requirements.txt`).
2. **Integração Automática (Real-Time)**: Implemente o consumo da API ao vivo. **É estritamente proibido** criar um fluxo onde o usuário atualize o chaveamento manualmente editando arquivos JSON de configuração.
3. **Mapeamento de Bandeiras**: Crie o arquivo ou objeto de mapa de países -> emojis.
4. **Geração do ICS**: Programe a lógica de criação do calendário, prestando **máxima atenção na regra do UID**.
5. **Documentação (README)**: Crie um `README.md` detalhado explicando:
   - Como instalar as dependências.
   - Como configurar chaves de API (se necessário).
   - Como rodar o script para gerar o arquivo.
   - Instruções exatas de como subir o arquivo `.ics` no Google Agenda.

Por favor, gere todo o código necessário em arquivos separados, estruturando o projeto com boas práticas.
