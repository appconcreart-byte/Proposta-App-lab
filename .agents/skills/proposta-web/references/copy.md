# Texto da proposta

A proposta é lida por um decisor ocupado, sozinho, provavelmente no celular e mais de uma vez.
Cada frase precisa se sustentar sem o Victor explicando. O Victor pediu, depois da primeira versão:
"enxugar, tem muita coisa e algumas seções ficam poluídas com informação demais". Leve isso como a
regra principal: **na dúvida, corte.**

## Voz

- Consultiva e crível. Nunca guru, nunca hype. Fala de operação e de resultado, não de "IA revolucionária".
- Português do Brasil, frase curta, voz ativa, "vocês" para o cliente, "a gente" ou "nós" para a Playbook.
- Concreta: nomes das ferramentas do cliente, nomes dos passos, números que ele mesmo disse.
- **Nunca usar travessão** (o traço longo, caractere U+2014). Troque por vírgula, ponto, dois-pontos ou reescreva. O validar.py barra.
- Palavras que não entram: revolucionar, potencializar, alavancar, turbinar, jornada, robusto, disruptivo,
  sinergia, "soluções inovadoras", "de ponta a ponta" como enfeite, "no piloto automático".

## Uma ideia por bloco

| Bloco | Tamanho | Forma |
|---|---|---|
| Promessa do resumo | até ~90 caracteres | 2 partes: afirma (branco) + qualifica (cinza) |
| Lede | 1 frase | "Proposta de X para Y, **onde/como**." |
| Frase de seção (`.statement`) | até ~70 | 2 partes, final em cinza |
| Passo do fluxo | rótulo de 1 palavra + até ~60 | fato, sem adjetivo |
| Entrega | título até ~30 + texto até ~100 | o que o cliente recebe, não como é feito |
| Etapa do "como funciona" | título 2 a 3 palavras + até ~55 | verbo no presente |
| Fase | até ~80 | verbo no infinitivo ("Levantar...", "Montar...", "Testar...") |
| Item incluído | até ~55 | substantivo ("Mapeamento dos critérios...") |
| Título do fechamento | até ~50 | pergunta-convite ligada ao projeto |

O validar.py avisa quando um bloco passa do limite. Aviso não é erro, mas quase sempre é texto a cortar.

## O que cortar primeiro

1. Frases que repetem a promessa do topo em outra seção (a Suzano tinha "O consultor recebe o lead já
   pesquisado e qualificado" no fim da solução, repetindo o resumo; saiu).
2. Listas de três parágrafos que dizem a mesma dor de jeitos diferentes (viraram uma linha:
   "**A qualificação atrasa** e oportunidades se perdem.").
3. Painéis extras que duplicam a demonstração (um mini-registro na lateral da solução foi removido a pedido).
4. Chips de exemplo em toda entrega: deixe só onde ajudam.
5. Adjetivos. "Enriquecimento automático" já diz; "enriquecimento automático e inteligente" não diz mais nada.

## Exemplos da Suzano (aprovados)

- Promessa: "Cada lead do canal direto chega ao consultor" / "já pesquisado, qualificado e com dono."
- Problema: "Hoje, cada um deles é pesquisado" / "à mão."
- Solução: "O agente faz a pesquisa." / "O consultor faz a venda."
- Fechamento: "Vamos colocar o agente para trabalhar?" + "Com a aprovação e o acesso ao Salesforce, começamos pelo mapeamento."

Repare no padrão: a primeira parte é o fato, a segunda é a virada. Não copie as frases para outro
cliente; copie a mecânica.

## Antes de construir: o plano de conteúdo

Mostre ao Victor, no chat, a copy de cada seção em forma de lista curta (não o HTML), mais a ideia da
demonstração. É mais barato corrigir aqui do que depois de montado. Formato:

```
Resumo: "{parte 1}" / "{parte 2}" · Lede · Meta: {3 fatos}
Demo: {sistema} · {entidade} · campos base {..} · campos IA {..} · score {sim/não} · texto {..} · ação {..}
Problema: número {sim: X a Y / não} · "{frase}" · fluxo: {passo} → {passo} → {gargalo} · esteira {sim/não}
Solução: "{frase}" · {n} entregas: {títulos}
Como funciona: {etapas}
Cronograma: {períodos} · {fases com início e duração}
Investimento: {formato} · {números} · incluído: {itens} · terceiros: {..}
Precisamos: {itens}
Quem somos: especialista lidera {..} · dev lidera {..}
Fechamento: "{título}" · "{subtítulo}"
Supus: {lista do que foi suposição}
```
