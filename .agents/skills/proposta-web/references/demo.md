# A demonstração do resumo

É o painel à direita do resumo: um registro na ferramenta do cliente sendo processado pelo agente,
em loop, com 3 exemplos fictícios. É a parte que faz a proposta parecer produto e não PowerPoint:
o cliente **vê** a solução funcionando antes de ler qualquer coisa. Vale gastar tempo aqui.

## Como o componente funciona

Tudo vem do objeto `DEMO` no script do template. O JavaScript monta o painel e roda o ciclo:

1. Registro aparece com os campos **base** preenchidos (o que já existe na ferramenta hoje).
2. O ponto do agente pulsa no acento ("Enriquecendo", "Analisando", "Classificando"...).
3. Cada campo **IA** passa por um carregamento curto e ganha o valor, com o selo "IA".
4. O score conta até o número e a barra cresce (se `score` não for `null`).
5. O texto do agente é digitado (se `texto` não for `null`).
6. A ação final fica verde e sólida ("Tarefa criada", "Respondido", "Encaminhado").
7. Espera, some com um desfoque e entra o próximo item. Pausa quando sai da tela.

```js
const DEMO = {
  sistema: { nome: 'HubSpot', cor: '#ff7a59', icone: 'i-database' },   // cor e ícone do selo da barra
  entidade: 'Contatos',                                                  // "Contatos / Nome do item"
  status: { novo: 'Novo', espera: 'Agente aguardando', rodando: 'Qualificando', feito: 'Qualificado' },
  campos: [                                   // mesmas chaves em todos os itens; 4 ou 6 no total
    { k: 'a', rotulo: 'Origem', base: true, mobile: false },   // base = já existe; mobile:false some no celular
    { k: 'b', rotulo: 'Cidade', base: true },
    { k: 'c', rotulo: 'Faturamento' },                         // sem base = preenchido pelo agente
    { k: 'd', rotulo: 'Nº de lojas' },
    { k: 'e', rotulo: 'Decisor' },
    { k: 'f', rotulo: 'Fit com o ICP' }
  ],
  score: { rotulo: 'Score de fit', max: 100 },     // ou null
  texto: { rotulo: 'Resumo para o SDR', icone: 'i-sparkles' },   // ou null
  acaoPendente: 'Reunião será sugerida pelo agente',
  itens: [ /* 3 itens: titulo, iniciais, subtitulo, valores{a..f}, score, selo, texto, acao */ ]
};
```

Os três itens contam uma pequena história: um de prioridade alta (score ~85), um médio (~70) e um
que o agente decide **não** empurrar para o vendedor (score ~40, ação diferente: encaminhar, nutrir,
descartar). Isso mostra julgamento, não só automação.

## Como adaptar a outros tipos de projeto

| Projeto | sistema / entidade | campos base | campos IA | score | texto | ação |
|---|---|---|---|---|---|---|
| Enriquecimento e roteamento de leads (Suzano) | Salesforce / Leads | E-mail, CEP | Porte, Segmento, Cargo, Site | Qualificação | Sugestão de abordagem | Tarefa para o consultor do CEP |
| SDR de IA no WhatsApp | WhatsApp / Conversas | Telefone, Origem | Interesse, Orçamento, Prazo, Decisor | Intenção de compra | Última resposta do agente | Reunião agendada |
| Triagem de tickets / pós-venda | Zendesk / Tickets | Cliente, Canal | Categoria, Urgência, Produto, Sentimento | Prioridade | Resposta sugerida | Encaminhado para o time X |
| Follow-up de propostas paradas | Pipedrive / Negócios | Valor, Fase | Dias parado, Último contato, Risco, Próximo passo | Chance de fechar | Mensagem de follow-up | Tarefa criada para o vendedor |
| Prospecção outbound | LinkedIn / Prospects | Cargo, Empresa | Porte, Tecnologia, Gatilho, Contato | Fit com o ICP | Primeira mensagem | Adicionado à cadência |

Regras para os dados fictícios:
- Plausíveis para o mercado do cliente (a Suzano vende papel e celulose: os leads eram gráfica,
  fábrica de embalagens e revenda de papel). Pesquise o mercado se precisar.
- Nomes de pessoas e empresas inventados, nunca clientes reais do cliente.
- Valores curtos o bastante para caber numa linha (o campo corta com reticências; não force).
- O texto do agente tem até ~130 caracteres (a caixa reserva 3 linhas; mais que isso é cortado).
- A ação cabe em uma linha no desktop: "<b>verbo + objeto</b> · detalhe".

## Variante: conversa de WhatsApp

Para projetos de atendimento/SDR no WhatsApp, o painel do registro pode ser trocado por uma conversa animada em
loop (balões do lead claros à esquerda, da IA verdes à direita, digitando, foto e PDF, aviso final de atribuição ao
time). Referência pronta, com CSS (`.wa*`, `.msg*`) e o motor no objeto `CHAT`:
`exemplos/gl-construir/index.html` (na pasta da skill). Mantém as mesmas regras: altura fixa, um loop só,
pausa fora da tela, estado final em `prefers-reduced-motion`, rótulo de dados fictícios. Afirmações sobre o produto
nas falas têm que vir do site ou da call do cliente.

## Quando o registro não serve

Se o projeto não é "um item entra e o agente processa" (ex.: um dashboard, uma base de conhecimento),
não force o registro. Mantenha o mesmo painel (`.record`, barra, corpo) e troque o conteúdo por algo
que mostre o mecanismo com a mesma disciplina: um número que atualiza, uma lista que se ordena, uma
resposta que é gerada. Três condições valem para qualquer versão:

1. **Altura fixa.** Nada no painel pode mudar de tamanho durante o loop. Reserve a altura máxima
   (linha com altura fixa, texto com `height` em `em`, `min-height` nos blocos). Foi o bug mais recorrente.
2. **Um loop só**, pausando fora da tela, com estado final pintado em `prefers-reduced-motion`.
3. **Rótulo "Demonstração com dados fictícios"** embaixo.

Rode `scripts/estabilidade.js` depois de mexer: ele acusa qualquer seção que mude de altura.
