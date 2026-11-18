# O que é fixo e o que muda, seção por seção

A proposta tem uma ordem fixa. Cada seção responde uma pergunta do leitor, e a ordem é a ordem
em que ele pergunta. Não reordene e não crie seção nova sem um motivo que o Victor aprove: a
força do formato vem de ser sempre a mesma estrutura bem executada.

| # | Seção (id) | Pergunta do leitor | Status |
|---|---|---|---|
| 1 | Capa (`capa`) | De quem é isto? | Fixa. Só o logo do cliente muda |
| 2 | Resumo (`resumo`) | O que vocês propõem, em uma frase? | Variável (texto + demonstração) |
| 3 | Prova social (`proof`) | Quem já confia em vocês? | Fixa |
| 4 | O problema (`problema`) | Vocês entenderam meu problema? | Variável |
| 5 | Solução proposta (`solucao`) | O que exatamente vocês vão fazer? | Variável |
| 6 | Como funciona (`fluxo`) | Como isso roda no dia a dia? | Variável |
| 7 | Cronograma (`cronograma`) | Quando fica pronto? | Variável |
| 8 | Investimento (`investimento`) | Quanto custa? | Variável |
| 9 | O que precisamos de vocês (`precisamos`) | O que eu preciso providenciar? | Variável |
| 10 | Quem somos (`quem-somos`) | Quem vai fazer? | Fixa, exceto o "quando" de cada papel |
| 11 | Fechamento (`aprovar`) | Como eu digo sim? | Fixo na estrutura, título e subtítulo mudam |

Títulos de seção são sempre curtos e literais: "O problema", "Solução proposta", "Como funciona",
"Cronograma", "Investimento", "O que precisamos de vocês", "Quem somos". O Victor pediu isso
explicitamente: a frase de efeito vai logo abaixo, em `.statement`, nunca no título.

---

## Sempre igual (não pergunte, não mude)

- **Visual inteiro:** fundo, superfícies, linhas, tipografia (Geist, Geist Mono e Inter Tight só na capa),
  espaçamentos, raios, botões, ícones Lucide. Só o grupo de acento muda (scripts/acento.py).
- **Capa:** "Proposta de projeto" em Inter Tight 700 com gradiente branco para cinza, padrão de pontos
  sutil atrás, logos Playbook Lab × cliente, a linha animada chamando para rolar.
- **Prova social:** legenda "Empresas que já automatizaram vendas com a gente" e a faixa de logos em loop contínuo.
  O pacote vem com 7 logos fictícias (Lumora, Novaterra, Kivo, Brightlane, Orbitta, Plenna, Vertexa) só para
  mostrar o formato: troque pelos logos dos seus clientes em `template/assets/logos/`, com autorização deles.
  Só adicione ou tire logo com autorização do Victor, e nunca coloque o próprio cliente na faixa.
- **Quem somos:** "A Playbook Lab é uma agência de automação com IA para áreas comerciais." +
  "Cada projeto tem três pessoas, para a solução funcionar na tecnologia e na operação." + logo + links
  (site, LinkedIn do Victor, YouTube do Victor). Os três papéis são sempre Especialista em vendas,
  Desenvolvedor de IA e Gestor de projeto. O gestor sempre "Cuida do prazo, do escopo e da comunicação com vocês."
- **Fechamento:** botões "Aprovar pelo WhatsApp" (`{{WHATSAPP}}`) e "Aprovar por e-mail" (`{{EMAIL}}`),
  assinatura "Victor Baggio · Fundador, Playbook Lab".
- **Rodapé:** "Playbook Lab · `{{RAZAO_SOCIAL}}` · CNPJ `{{CNPJ}}`" e "Proposta preparada para
  a/o {Cliente} · {Mês de Ano}".
- WhatsApp, e-mail, razão social e CNPJ vêm do `config.json` da skill: o `nova_proposta.py` preenche sozinho.
- **Nav:** lockup (aparece só depois da capa), 4 links curtos para as seções principais, botão Aprovar.
- **Técnico:** `noindex`, página única, sem framework, tudo que o JS faz já está no template.

## Muda por proposta (é aqui que está o trabalho)

### 2. Resumo
- **Promessa** (`.hero-t`): o resultado para o cliente, em duas partes. A primeira em branco afirma,
  a segunda em cinza qualifica. Até ~90 caracteres. Fala do que muda na operação, não da tecnologia.
  Ex.: "Cada lead do canal direto chega ao consultor / já pesquisado, qualificado e com dono."
- **Lede:** "Proposta de {o que é} para {cliente}, **{onde/como, em destaque}**." Uma frase.
- **Meta:** Duração · Investimento · 1 fato útil (Plataforma, Modelo, Canal, Início...).
- **Demonstração:** ver references/demo.md. É a peça que mais vende; capriche no conteúdo fictício.

### 4. O problema
- **Número grande (opcional):** só com número que o cliente disse (volume, tempo, custo). Sem número real,
  apague o bloco `.bignum` inteiro e deixe só a frase. Nunca estime número para ter o que mostrar.
  Número único (não faixa): apague o `<span class="a">a</span>` e o segundo span. Número com milhar:
  `<span data-roll="1200" data-fmt="br">1.200</span>` (o `data-fmt="br"` põe o ponto enquanto rola).
  Número com unidade ("4 horas"): o número no span e a unidade num `<span class="a">horas</span>` depois.
- **Frase** (`.statement`): o problema em uma linha, com o final em cinza. Ex.: "Hoje, cada um deles é
  pesquisado / à mão."
- **Fluxo de hoje:** 2 a 4 passos curtos do processo atual (rótulo de 1 palavra + frase de até ~60 caracteres)
  e o gargalo no fim, destacado. Ajuste `--steps` para o número de passos antes do gargalo.
- **Esteira (opcional):** só quando existe uma "fila" real que se perde (leads, tickets, pedidos, propostas).
  Troque os códigos (L-2041, T-1180, #4471...) e a palavra final (perdido, parado, atrasado, sem resposta).
- **Consequência** (`.conclusion`): uma linha, com o começo em destaque. Ex.: "**A qualificação atrasa** e
  oportunidades se perdem."

### 5. Solução proposta
- **Frase** (`.statement`): a divisão de trabalho entre o agente e a pessoa, quando couber
  ("O agente faz a pesquisa. / O consultor faz a venda.").
- **Explicação** (`.sub`): quando dispara e o que faz, em uma frase.
- **Selo "onde roda" (opcional):** quando o cliente se importa com isso (restrição de TI, ferramenta que já usa).
  Cor do sistema em `--sys`.
- **Entregas:** 3 a 5 itens. Título de até ~30 caracteres, texto de até ~100. Para mais itens, copie um `<li>`
  inteiro; o destaque no scroll pega todos sozinho. Os chips em mono (`.ex`) são opcionais: use em 1 ou 2 itens,
  onde um exemplo concreto explica melhor que a frase. Nunca em todos. Ícones disponíveis no template:
  i-building, i-gauge, i-message, i-map-pin, i-sparkles, i-bot, i-send, i-chart, i-users, i-clock, i-calendar,
  i-file, i-database, i-inbox, i-check-square.

### 6. Como funciona
3 a 5 etapas, na ordem em que acontecem, cada uma com título de 2 a 3 palavras (nunca uma palavra só) e uma frase curta.
É o mesmo processo do problema, agora com o agente. Ajuste `--n` e os `--k`.

### 7. Cronograma
- Períodos em `--cols` (semanas, sprints ou meses) e rótulos no cabeçalho.
- Uma linha por fase, com `--from` (início) e `--span` (duração em períodos). Fases podem se sobrepor.
- A última fase, ou a mais importante para o cliente, recebe `.cur`.
- Para contrato recorrente, o cronograma é do primeiro projeto dentro das horas, ou dos
  primeiros meses. Não invente fases que ninguém combinou; se o escopo não tem fases, pergunte.

### 8. Investimento: três formatos
1. **Projeto por horas** (ex.: Suzano): calc "**{N} horas** × R$ {valor} por hora", total formatado, nota "Valor único do projeto, em 3 semanas."
2. **Recorrente mensal:** calc "**{Nome do plano}** · {N} horas por mês", total com sufixo
   `<span class="per">/mês</span>` depois do número, nota "Sem fidelidade. Horas compartilhadas entre projetos."
   Use os seus planos e preços. Confirme o plano com o Victor, nunca escolha sozinho.
3. **Valor fechado:** calc com o que está incluído ("4 semanas · implantação completa"),
   total, nota de pagamento se o Victor disser.
- Lista "incluído": 3 a 5 itens que espelham as fases ou entregas.
- Custo de terceiros (API, licença, créditos) em `.extra`, só se existir. Sempre dizendo quem paga.
  Rótulo: "**Custo à parte, se for preciso:**" quando talvez exista; "**Custo à parte:**" quando é certo.
- `data-roll` recebe o número sem pontuação (12500); o texto visível vem formatado (12.500).

### 9. O que precisamos de vocês
1 a 3 itens concretos (acessos, pessoa de contato, dados, aprovação de TI). Selo "Talvez" só no que
ainda não é certo, com a condição dita no texto.

### 10. Quem somos
Só o `.when` (qual fase cada papel lidera, com a fase em `<b>`) e a frase do especialista e do dev
se adaptam ao projeto. O resto fica como está.

### 11. Fechamento
- Título (`h2`, até ~50 caracteres): convite para começar, ligado ao projeto. Ex.: "Vamos colocar o agente para trabalhar?"
- Subtítulo: o primeiro passo depois do sim. Ex.: "Com a aprovação e o acesso ao Salesforce, começamos pelo mapeamento."
- `CFG.projeto`: como o projeto aparece na mensagem pronta de aprovação ("para o {projeto} ({cliente})").

---

## Quando tirar um bloco

Blocos marcados OPCIONAL no template saem inteiros (HTML), sem deixar buraco. Tire quando não houver
conteúdo verdadeiro para ele. Uma seção variável inteira só sai com o ok do Victor (ex.: proposta sem
cronograma porque é recorrente pura). Se sair, tire também o link dela na nav.
