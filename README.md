# Calendário Copa do Mundo 2026 → Google Agenda

Gera um arquivo `.ics` (iCalendar) com os jogos da Copa do Mundo FIFA 2026 (EUA, México e Canadá), pronto para importar no Google Agenda. **Os dados são puxados ao vivo da [football-data.org](https://www.football-data.org/)** a cada execução — quando a CBF derrotar a Argentina nas oitavas, é só rodar o script de novo e re-importar; o Google Agenda **atualiza** os eventos existentes em vez de duplicá-los, graças aos `UID`s estáveis.

## ✨ Recursos

- **Atualização 100% automática**: os jogos vêm da API ao vivo, sem edição manual de JSON
- **Bandeiras em emoji** nos títulos: `🇧🇷 Brasil vs Argentina 🇦🇷`
- **Placeholders** automáticos para confrontos ainda indefinidos: `🏳️ A definir vs A definir 🏳️`
- **UID estável** por partida (`match-{id}-worldcup-2026@calendariocopa`)
- **Fuso horário UTC** (Google Agenda converte automaticamente para o local do usuário)
- **Cache de resiliência**: se a API estiver fora, usa a última resposta com sucesso e avisa
- **Placar** e **status** (Agendado, Em andamento, Encerrado…) na descrição do evento

## 📦 Instalação

Pré-requisito: Python 3.10+.

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
```

## 🔑 Configurando a chave da API

A football-data.org oferece uma chave gratuita (cadastro de 1 minuto, sem cartão).

1. Crie a conta em [www.football-data.org/client/register](https://www.football-data.org/client/register).
2. Copie o token mostrado no painel.
3. Copie `.env.example` para `.env` e cole o token:

   ```env
   FOOTBALL_DATA_TOKEN=seu_token_aqui
   FOOTBALL_DATA_COMPETITION=WC
   FOOTBALL_DATA_SEASON=2026
   CALENDAR_NAMESPACE=worldcup-2026@calendariocopa
   ```

Limites do plano gratuito: 10 chamadas por minuto. O script faz **uma única** chamada por execução, então isso é mais que suficiente.

## ▶️ Como gerar o arquivo

```bash
python main.py
```

Saída padrão: `output/copa-2026.ics`. Para um caminho customizado:

```bash
python main.py --output ~/Downloads/copa-2026.ics
```

Para apenas inspecionar o que será gerado, sem escrever o arquivo:

```bash
python main.py --check
```

Saída típica:

```
🌐 API ao vivo • 104 jogos carregados
  • Fase de Grupos: 72
  • Oitavas de Final: 8
  • ...
  • Confrontos com ambos os times definidos: 84/104

✅ Arquivo gerado em: output/copa-2026.ics
```

## 📅 Como importar no Google Agenda (uso local)

1. Acesse [calendar.google.com](https://calendar.google.com) no navegador.
2. Clique na engrenagem ⚙️ no canto superior direito → **Configurações**.
3. Menu lateral → **Importar e exportar** → **Importar**.
4. Selecione o arquivo `output/copa-2026.ics`.
5. Escolha o calendário de destino (recomendo criar um chamado **Copa 2026**).
6. Clique em **Importar**. Pronto — os jogos aparecerão na sua agenda.

> 💡 **Dica**: crie um calendário separado para a Copa. Assim você pode mostrar/ocultar os jogos com um clique, mudar a cor e compartilhar com amigos.

## 🚀 Publicando para amigos (GitHub Pages, sem que ninguém precise da chave)

Quer compartilhar o calendário sem que cada amigo tenha que criar conta na API? O projeto já vem com um **GitHub Action** que regenera o `.ics` diariamente e publica numa página pública. Seus amigos só assinam a URL — atualização automática via Google Agenda.

### Passo a passo (uma vez só)

1. **Suba o projeto pra um repositório do GitHub** (público ou privado, tanto faz).
2. **Adicione sua chave da API como secret**:
   - Repositório → **Settings** → **Secrets and variables** → **Actions** → **New repository secret**
   - Nome: `FOOTBALL_DATA_TOKEN`
   - Valor: o token da football-data.org
3. **Habilite o GitHub Pages**:
   - Repositório → **Settings** → **Pages**
   - Em **Source**, selecione **GitHub Actions**
4. **Rode o workflow pela primeira vez**:
   - Aba **Actions** → **Build & Publish Calendar** → **Run workflow**
   - Em ~1 minuto, sua página estará no ar.
5. **Copie a URL pública** (aparece no resumo do workflow ou em Settings → Pages):
   ```
   https://SEU-USUARIO.github.io/calendariocopa/
   ```
   E a URL do `.ics`:
   ```
   https://SEU-USUARIO.github.io/calendariocopa/copa-2026.ics
   ```
6. **Mande a URL pros seus amigos.** A página tem botão de copiar e instruções prontas.

### Como seus amigos assinam (sem instalar nada)

1. Abre [calendar.google.com](https://calendar.google.com) no PC.
2. Barra lateral → ao lado de **Outros calendários**, clica em **+** → **Subscrever por URL**.
3. Cola a URL do `.ics`. Pronto — aparece no celular automaticamente.

A partir daí, conforme as oitavas/quartas/etc. forem sendo definidas, o GitHub Action regenera o `.ics` todo dia, e o Google Agenda atualiza os eventos sozinho na agenda dos seus amigos. Eles não precisam fazer nada nunca mais.

> ℹ️ O Google atualiza calendários assinados a cada 12-24h. Pra refrescos imediatos, eles podem remover e re-adicionar a URL.

## 🔄 Atualizando o calendário ao longo do torneio

Sempre que houver mudança (chaveamento, classificações, horários):

```bash
python main.py
```

E re-importe o `.ics` no Google Agenda. Os eventos existentes são **atualizados** com os novos times e bandeiras — sem duplicar.

> Você pode automatizar isso. No Linux/macOS, agende com `cron`:
>
> ```cron
> 0 6 * * * cd /caminho/para/CalendarioCopa && .venv/bin/python main.py
> ```
>
> No Windows, use o **Agendador de Tarefas** apontando para `python.exe main.py`.

## 🛠️ Estrutura do projeto

```
.
├── main.py                       # CLI principal
├── requirements.txt
├── .env.example                  # template de configuração
├── .github/workflows/
│   └── publish.yml               # CI: regenera + publica diariamente
├── web/
│   └── index.html                # landing page (instruções de assinatura)
├── data/
│   ├── flags.py                  # mapa TLA FIFA → (emoji, nome PT-BR)
│   └── cache/
│       └── matches.json          # cache automático (gerado)
├── src/
│   ├── api_client.py             # cliente da football-data.org
│   ├── loader.py                 # API → modelo interno + cache
│   └── ics_generator.py          # gera .ics com UIDs estáveis
└── output/
    └── copa-2026.ics             # arquivo gerado (uso local)
```

## 🧱 Detalhes técnicos

- **Fonte de dados**: `GET https://api.football-data.org/v4/competitions/WC/matches?season=2026`
- **UID**: `match-{api_id}-{namespace}` — `api_id` é o identificador imutável da partida na football-data.org
- **Cache**: `data/cache/matches.json` é regravado a cada execução bem-sucedida da API. Se a API falhar (rede caída, rate limit), o script usa o cache emitindo um aviso. **Não edite esse arquivo** — ele será sobrescrito.
- **Bandeiras**: Inglaterra, Escócia e País de Gales usam as bandeiras tag (subdivisões do Reino Unido) em vez do `🇬🇧` genérico.

### Adicionando uma seleção que falta

Se a API retornar um time cuja sigla TLA ainda não está mapeada, o evento usa o nome enviado pela API com bandeira genérica `🏳️`. Para adicionar tradução + emoji, edite [data/flags.py](data/flags.py):

```python
TEAMS["XYZ"] = ("🇽🇾", "Nome em português")
```

## 🤔 Por que `.ics` e não CSV?

O `.ics` é o formato nativo de calendário (iCalendar, RFC 5545). Diferente do CSV, ele:

- Suporta fuso horário corretamente.
- Tem o campo `UID` que permite **atualização idempotente** dos eventos.
- Funciona em Google Agenda, Apple Calendar, Outlook, etc., sem conversão.

## 📜 Licença

Uso livre — aproveite a Copa! 🏆
