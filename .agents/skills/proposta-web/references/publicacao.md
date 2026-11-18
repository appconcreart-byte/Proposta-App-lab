# Preview e publicação

## Preview local

As propostas moram em `<PROPOSTAS>/<slug>/`, onde `<PROPOSTAS>` é a `pasta_propostas` do `config.json` da
skill (padrão `~/propostas-web`; a variável de ambiente `PROPOSTAS_DIR` tem precedência). Vale manter essa
pasta como um repo git próprio, porque é código.

- No app: crie (uma vez) uma configuração no `.claude/launch.json` do projeto chamada `propostas`, que serve
  essa pasta na porta 4321 (`python3 -m http.server 4321 --directory <PROPOSTAS>`). Depois `preview_start`
  com name `propostas` e abra `http://localhost:4321/<slug>/`.
- Fora do app: `python3 -m http.server 4321 --directory <PROPOSTAS>`.

O link para o Victor clicar é sempre `http://localhost:4321/<slug>/`, dito com todas as letras.
Lembre que ele só abre neste computador.

Atenção: o painel do navegador do app **pausa animações quando está oculto**, e aí a página parece
travada no estado inicial. Para conferir de verdade, use `scripts/capturar.js` (Playwright).

## Publicar (só depois do Victor aprovar a página)

Publicar é ação externa: confirme com o Victor antes, sempre, mesmo que ele já tenha aprovado outra proposta.

**Como montar (uma vez):**
- Um projeto na Vercel ligado à pasta `<PROPOSTAS>` (rode `npx vercel link` dentro dela; isso cria `.vercel/`).
- Opcional: um repo privado no GitHub para versionar as propostas.
- Endereço: `https://<seu-projeto>.vercel.app/<slug>/` (domínio padrão) ou um domínio próprio.
- Recomendado na raiz da pasta:
  - `vercel.json` forçando barra final (`"trailingSlash": true`) e mandando o header `X-Robots-Tag: noindex`
    (proposta não deve aparecer no Google);
  - `.vercelignore` tirando `*.md`, `.impeccable` e `_teste-*` do site; `.gitignore` tirando `_teste-*` do repo;
  - opcional: redirecionar a raiz para o seu site.

**Passo a passo:**
```bash
cd <PROPOSTAS>
git add <slug> && git commit -m "Proposta <cliente>" && git push      # versiona (se usar git)
npx vercel deploy --prod --yes [--scope <seu-time>]                    # publica
```
Se o CLI disser que não há login, peça ao Victor para rodar `npx vercel login` (é com ele: abre o navegador).

**O MCP da Vercel não serve bem para isto:** ele só aceita arquivos colados na chamada, inviável com ~150KB de
página e logos. Use o CLI.

Pasta de teste deve começar com `_teste-` para nunca ir ao ar nem ao repo.

Depois de publicar:
- Confira com `curl -s -o /dev/null -w "%{http_code}"` que a página e um logo devolvem 200, e abra o link no
  navegador. O link a mandar é sempre com a barra final.
- Ofereça mandar o link pela skill `proposta-comercial-email` (e-mail) ou montar a mensagem de WhatsApp.
  Nunca envie sem o Victor confirmar texto e destinatário.
