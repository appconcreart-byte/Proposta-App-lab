# Design e movimento

O sistema visual é fixo e já está inteiro no template. Esta referência existe para você **não
precisar inventar nada** e para saber o que não fazer quando for adaptar um bloco.

Origem: o Victor pediu propostas "extremamente bonitas, modernas e tecnológicas", inspiradas no site
da Linear, e **proibiu o brandbook da Playbook Lab** (verde escuro, verde neon, Syne, Poppins) nas
propostas. A referência completa da Linear está em `~/.claude/skills/design-referencias/marcas/linear.app.md`.

## O sistema em 8 linhas

1. Fundo quase preto `#08090a`, superfícies `#0f1011` / `#141516` / `#191a1b`, linhas de 1px `#23252a`.
   Profundidade por degrau de superfície e linha, não por sombra (uma única sombra: o painel da demonstração).
2. Tintas: `#f7f8f8` (afirma), `#d0d6e0` (dados), `#8a8f98` (qualifica), `#80848d` (rótulos). Todas passam AA.
3. **Um acento**, derivado da marca do cliente por `scripts/acento.py`. Só em: botão Aprovar, barra de progresso,
   foco, score, item ativo, pacote do pipeline, fase destacada, selo "IA". Nunca em texto corrido ou fundo de seção.
   Sempre via `var(--accent)` ou `color-mix(...)`; o validar.py barra cor escrita à mão.
4. Verde `#4cb782` só para estado concluído/positivo. Coral `#e2725b` só para o que se perde hoje no cliente.
5. Geist 400/500/600 com tracking negativo nos títulos; Geist Mono só em dado de sistema (campos, códigos, chips).
   Inter Tight 700 só no "Proposta de projeto" da capa.
6. Títulos em duas tintas (branco afirma, cinza qualifica). Sem negrito, itálico ou cor de acento em título.
7. Logos sempre monocromáticos por máscara CSS (`.logo` com `--src`, `--ar`, `--h`), incluindo o do cliente.
8. Raios: 6 chips, 8 botões, 10 caixas internas, 12 a 16 painéis, 20 fechamento. Tudo com borda de 1px.

**Marca do cliente verde ou sem cor:** verde fica perto do verde de "concluído" e confunde (no teste da
Solfácil, a barra do score e o selo "Prioridade alta" ficaram da mesma cor); cinza não gera acento.
O acento.py avisa nos dois casos. Saídas: a cor secundária da marca (veja `cores_logo.py`) ou `--neutro`
(azul-acinzentado). Diga ao Victor qual usou; não troque o verde de "concluído" da página.

## Inventário de movimento (e só isso)

| Onde | Movimento | Tipo |
|---|---|---|
| Página toda | entrada no scroll: opacidade + 14px + desfoque de 6px, 0.9s, escalonado 90ms | uma vez |
| Capa | linha que desce chamando para rolar | loop sutil |
| Resumo | demonstração do registro (references/demo.md) | loop, pausa fora da tela |
| Prova social | faixa de logos contínua (clona o conjunto até cobrir 2x a tela) | loop, pausa no hover |
| Problema | número rolando até o valor; esteira de itens que se perdem (opcional) | uma vez / loop |
| Solução | a entrega no meio da tela acende (título e ícone) | ligado ao scroll |
| Como funciona | pacote percorre a trilha, cada etapa acende | loop |
| Cronograma | barras crescem da esquerda, escalonadas | uma vez |
| Investimento | total rola até o valor | uma vez |
| Nav | barra de progresso de 1px | ligado ao scroll |

Uma curva de easing só: `cubic-bezier(.16,1,.3,1)`. Não adicione movimento novo: se um bloco novo
parece precisar de animação, provavelmente precisa de menos texto. Hover é só troca de cor, borda ou
fundo em 0.2 a 0.3s, nunca mover, escalar ou elevar. Tudo respeita `prefers-reduced-motion` (já está no template).

## O que não fazer

- Cards iguais de ícone + título + texto como estrutura de seção. Listas com linha de 1px, sim.
- Rótulo pequeno acima do título (eyebrow/kicker). O título fala sozinho.
- Numeração 01/02/03 em seções.
- Gradiente como atmosfera, glow, halo, vidro decorativo. Gradiente só tem função: o título da capa,
  as bordas esmaecidas da faixa e da esteira, o rastro do pacote, a linha no topo do fechamento.
- Emoji ou caractere como ícone. Ícones são Lucide em SVG (o template tem os mais comuns; para um novo,
  copie o path de lucide.dev no mesmo formato de `<symbol>`).
- Fotos de banco de imagem, mockups genéricos, ilustração de "robô". Não há fotos no formato.
- Segunda cor de destaque.

## Bugs que já aconteceram (não repita)

1. **Bloco que muda de altura durante uma animação empurra a página inteira.** Aconteceu na fila de leads
   (chips entrando no fluxo) e no painel da demonstração (texto com mais linhas). Correção: altura fixa
   para tudo que anima, elementos em loop com `position:absolute` dentro de uma faixa de altura fixa.
   Teste: `scripts/estabilidade.js`.
2. **Faixa de logos com buraco preto em tela larga.** Duas cópias fixas não cobrem 1850px. O template
   clona até cobrir 2x a largura e recalcula no resize. Não volte para "2 cópias + translateX(-50%)".
3. **Troca de texto com esmaecimento sobreposto** ("L-2042" e "perdido" um em cima do outro). Troca de
   palavra em animação é instantânea (keyframe em 69.9% / 70%).
4. **Contraste baixo** no cinza de rótulo (`#62666d` não passa AA). Use as tintas do template.
5. **Cor do acento escrita à mão** em 12 lugares quebrava a troca de cliente. Só via token.
6. **`overflow-x:hidden` no body** quebra o `position:sticky` da solução. O template usa `overflow-x:clip`.
7. **Placeholder de número rolando para negativo** quando o relógio da página atrasa. O template limita o progresso entre 0 e 1.

8. **Logos sumindo quando o Victor abre o `index.html` direto (`file://`).** O logo é CSS `mask` e o Chrome
   bloqueia máscara de arquivo externo em `file://`: some sem erro. O `nova_proposta.py` embute os logos como data
   URI; o `validar.py` acusa `url(assets/logos/...)` que sobrar. Teste também abrindo por `file://`.

## Revisão visual (depois das capturas)

Olhe desktop e celular e responda sim/não:
- A capa tem só título, logos e a linha? Os dois logos parecem do mesmo "peso"? (ajuste `LOGO_CLIENTE_ALTURA_*` se não)
- O título do resumo cabe em até 5 linhas no desktop e o painel não está vazio ou cortado?
- Alguma seção tem mais de um bloco de texto corrido? Alguma frase repete outra?
- Os chips mono aparecem em no máximo 2 entregas?
- O cronograma tem as barras nas colunas certas? A fase destacada faz sentido?
- O total do investimento é o número certo, com o formato certo?
- No celular, algum texto quebrou feio, algum botão ficou torto, algo estoura na lateral?
- Nenhum texto com travessão, nenhum placeholder, nenhum "lorem"?
