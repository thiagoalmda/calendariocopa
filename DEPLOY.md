# 🚀 Guia de Deploy — Publicar o calendário para os amigos

Este guia mostra como colocar seu calendário no ar via **GitHub Pages**, de forma 100% gratuita e automática. No final, você terá uma URL pública que seus amigos podem assinar no Google Agenda — sem precisar de chave de API, sem instalar nada, e com atualização automática.

---

## ✅ Checklist (uma vez só)

- [ ] Conta no GitHub
- [ ] Token gratuito da [football-data.org](https://www.football-data.org/client/register)
- [ ] Repositório no GitHub com este projeto
- [ ] Secret configurada
- [ ] GitHub Pages habilitado
- [ ] Workflow rodado pela primeira vez

---

## 1. Subir o projeto pro GitHub

Se ainda não tem o repositório criado:

1. Vá em [github.com/new](https://github.com/new).
2. Dê um nome (ex.: `calendariocopa`).
3. Pode deixar **público** (recomendado, simplifica o Pages) ou **privado** (também funciona).
4. **Não** marque para criar README/`.gitignore`/license — o projeto já tem.
5. Clique em **Create repository**.

Na sua máquina, dentro da pasta `CalendarioCopa`:

```bash
git init
git add .
git commit -m "primeiro commit do calendario da copa"
git branch -M main
git remote add origin https://github.com/SEU-USUARIO/calendariocopa.git
git push -u origin main
```

> 🔒 O `.gitignore` já protege seu `.env`. Confirme rodando `git status` antes do primeiro commit — o `.env` **não** deve aparecer na lista.

---

## 2. Adicionar a chave da API como secret

A chave fica guardada criptografada no GitHub. Apenas o workflow tem acesso, ninguém mais — nem mesmo quem clonar seu repo.

1. No repositório, abra **Settings** (aba do topo).
2. Menu lateral → **Secrets and variables** → **Actions**.
3. Clique em **New repository secret**.
4. Preencha:
   - **Name**: `FOOTBALL_DATA_TOKEN`
   - **Secret**: cole o token da football-data.org
5. **Add secret**.

---

## 3. Habilitar o GitHub Pages

1. Repositório → **Settings** → menu lateral **Pages**.
2. Em **Source**, selecione **GitHub Actions**.
3. Salvar (em alguns layouts não tem botão — basta selecionar).

> Não escolha "Deploy from a branch" — usamos o modo Actions, mais flexível.

---

## 4. Rodar o workflow pela primeira vez

O workflow está configurado para rodar:

- **Diariamente** às 06:00 UTC (03:00 BRT)
- **A cada push** na branch `main`
- **Manualmente**, sob demanda

Para o primeiro deploy, dispare manualmente:

1. Repositório → aba **Actions**.
2. No menu lateral, selecione **Build & Publish Calendar**.
3. Botão **Run workflow** → confirmar.
4. Aguarde ~1 minuto. Quando aparecer ✅ verde, está no ar.

> Se aparecer ❌ vermelho: clique no run que falhou e leia o log. Os erros mais comuns são (a) secret com nome errado e (b) Pages não habilitado em Settings.

---

## 5. Pegar a URL pública

Depois do primeiro deploy bem-sucedido:

- Repositório → **Settings** → **Pages**
- A URL aparece logo no topo, algo como:
  ```
  https://SEU-USUARIO.github.io/calendariocopa/
  ```

A URL do arquivo `.ics` é a mesma + `copa-2026.ics`:

```
https://SEU-USUARIO.github.io/calendariocopa/copa-2026.ics
```

---

## 6. Compartilhar com os amigos 🎉

Mande pros seus amigos **a URL da página** (não a do `.ics` direto). A página tem botão de copiar e instruções prontas:

```
https://SEU-USUARIO.github.io/calendariocopa/
```

### O que seus amigos fazem (passo a passo simples)

1. Abre a URL no computador.
2. Clica em **Copiar URL** (ou copia o link mostrado na página).
3. Vai em [calendar.google.com](https://calendar.google.com).
4. Na barra lateral esquerda, ao lado de **Outros calendários**, clica em **+**.
5. Escolhe **Subscrever por URL**.
6. Cola a URL e clica em **Adicionar calendário**.

Pronto — os jogos aparecem em todos os dispositivos do Google Agenda dele (PC, celular, tablet).

---

## 🔄 O que acontece a partir daí

- **Você não precisa fazer nada manual.** Todo dia o GitHub Action roda, busca os dados atualizados na API e atualiza o `.ics` no Pages.
- **Os amigos não precisam fazer nada.** O Google Agenda checa a URL assinada a cada 12-24 horas e atualiza os eventos automaticamente.
- Quando os times das oitavas forem definidos, os títulos dos eventos vão de `🏳️ A definir vs A definir 🏳️` para `🇧🇷 Brasil vs 🇦🇷 Argentina` sozinhos — sem novas importações, sem duplicação.

---

## 🛠️ Operações comuns

### Forçar uma atualização agora

- Aba **Actions** → **Build & Publish Calendar** → **Run workflow**.

### Mudar o horário automático

Edite [.github/workflows/publish.yml](.github/workflows/publish.yml), linha do `cron`:

```yaml
schedule:
  - cron: "0 6 * * *"   # diário 06:00 UTC
  # exemplos:
  # - cron: "0 */6 * * *"  # a cada 6 horas
  # - cron: "0 12 * * *"   # uma vez por dia ao meio-dia UTC
```

### Trocar o token

Settings → Secrets and variables → Actions → `FOOTBALL_DATA_TOKEN` → **Update**.

### Remover o calendário do ar

Settings → Pages → mude **Source** de "GitHub Actions" para "Disabled". Ou simplesmente delete o repositório.

---

## ❓ Problemas comuns

### "404 Not Found" ao abrir a URL

- O primeiro deploy ainda não rodou. Vá em **Actions** e dispare manualmente.
- Pages pode estar desabilitado. Confira **Settings → Pages → Source = GitHub Actions**.

### Workflow falha com "Token rejeitado"

- A secret está com nome errado ou valor incorreto. Refaça o passo 2.
- O nome **precisa** ser exatamente `FOOTBALL_DATA_TOKEN` (case-sensitive).

### Workflow falha com "Resource not accessible by integration"

- Pages não está como **GitHub Actions** em Settings → Pages. Mude e dispare o workflow de novo.

### Calendário do amigo não atualiza

- O Google atualiza calendários assinados a cada 12-24h. Pra forçar agora, ele pode remover e re-adicionar a URL.
- Confira que ele assinou pela **URL** (passo "Subscrever por URL"), não importou o `.ics` baixado.

---

Pronto. Boa Copa! 🏆
