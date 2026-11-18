# Contexto e entrevista

O objetivo desta fase é preencher a **ficha da proposta** com fatos verdadeiros, perguntando ao
Victor só o que não dá para descobrir. Ele não gosta de repetir o que já está no vault ou numa call.

## 1. Onde buscar, nesta ordem

1. **O que o Victor mandou na mensagem.** Muitas vezes ele cola o rascunho da proposta (quem somos,
   desafio, solução, fases, investimento, o que precisamos). Isso é a fonte principal: use como modelo,
   pode enxugar e reorganizar, mas não invente fatos além dele.
2. **Vault do cliente:** `clientes/{Nome}/{Nome}.md` (hub) e a parte acima do `---` de
   `clientes/{Nome}/contexto/projeto.md`. Para lead novo, não existe pasta: siga.
3. **Pipedrive (pipeline 02, o real):** deal do cliente, valor, fase, notas, contato (nome, e-mail, telefone).
4. **TLDV:** transcript da call de vendas com o cliente (`search-meetings` pelo nome da empresa ou do contato).
   É onde aparecem os números reais (volume, time, ferramenta), a dor nas palavras do cliente e as restrições
   (ex.: "tem que rodar dentro do Salesforce"). Leia o transcript, não só o resumo.
5. **Gmail:** thread com o contato, se houver troca depois da call.
6. **Site do cliente:** o que a empresa faz, para quem vende, e o logo (fase de materiais).

Referências fixas da Playbook, se precisar: `comercial/ofertas/ai-partner.md`, `comercial/ofertas/founders-os.md`,
`comercial/ofertas/posicionamento-ai-partner.md`.

## 2. A ficha da proposta

Monte isto antes de perguntar qualquer coisa. Marque cada item como ✅ (fonte encontrada, diga qual),
❓ (falta) ou ➖ (não se aplica).

**Obrigatórios (sem eles não dá para construir):**
- Cliente: nome como deve aparecer, artigo (a/o), site
- Contato: quem vai ler e aprovar (nome, cargo)
- Problema: o processo de hoje em passos, onde trava, o que se perde
- Solução: o que o agente/automação faz, quando dispara, em qual ferramenta roda
- Entregas: 3 a 5 coisas concretas que o cliente recebe
- Fases e duração
- Investimento: formato (horas × valor, mensal, fechado), números exatos
- O que o cliente precisa providenciar

**Importantes (melhoram muito a proposta):**
- Números reais do problema (volume, tempo gasto, tamanho do time)
- Restrições técnicas (ferramenta obrigatória, TI, segurança, LGPD)
- Custos de terceiros e quem paga
- Mercado do cliente (para a demonstração ficar plausível: quem são os clientes dele?)

**Opcionais:**
- Fato para o 3º campo da meta (plataforma, canal, início previsto)
- Palavra de perda para a esteira (se houver fila)

## 3. Entrevista

Use a ferramenta de perguntas (AskUserQuestion) quando disponível. Regras:

- Pergunte **só o que ficou ❓ nos obrigatórios e nos importantes**. Se está tudo ✅, pule direto para
  confirmar o plano de conteúdo.
- Até 3 perguntas por rodada, no máximo 2 rodadas. Se ainda faltar algo, siga com uma suposição
  explícita e liste no fim ("Supus X; confirma?").
- Ofereça opções concretas tiradas do contexto (ex.: "40h/mês no plano mensal" ou "34h fechadas"), não
  perguntas abertas genéricas.
- Não pergunte nada do visual: o estilo é fixo. A única decisão visual que pode surgir é sobre o logo
  (quando não se acha um bom) ou sobre a cor (marca verde ou sem cor, ver references/design.md).
- Não pergunte o WhatsApp, o e-mail, o CNPJ ou os links do Victor: são fixos (vêm do `config.json` da skill).
  Se o `config.json` ainda estiver com `PREENCHA_...`, peça esses dados uma vez e grave lá.

## 4. O que nunca inventar

Preço, horas, prazo, número de clientes, métricas de resultado, nomes de clientes da Playbook fora da
lista da faixa, depoimentos, garantias, integrações que ninguém confirmou, datas de início. Se a
proposta ficaria melhor com um desses e ele não existe, **pergunte**. A demonstração do topo é a única
parte com dados inventados, e ela é rotulada como fictícia.
