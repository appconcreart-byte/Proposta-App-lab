---
name: proposta-web
description: "Cria propostas comerciais da Playbook Lab como página web (HTML de uma página, estilo Linear, animada e enxuta) para publicar na Vercel e mandar como link ao cliente. Conduz o processo inteiro: puxa o contexto do cliente (mensagem do Victor, vault, Pipedrive, call no TLDV), entrevista só o que falta, monta o plano de conteúdo para aprovação, busca o logo e a cor da marca do cliente, constrói a partir do template aprovado (a proposta da Suzano), valida, testa desktop e celular e entrega o link local. ATIVE SEMPRE QUE o Victor pedir \"monta a proposta da [empresa]\", \"cria a proposta em HTML\", \"faz a página da proposta\", \"proposta web\", \"proposta bonita pro [cliente]\", \"transforma esse escopo em proposta\", \"proposta igual à da Suzano\", \"/proposta-web\", ou colar um rascunho de proposta (quem somos, desafio, solução, fases, investimento) pedindo para virar página. Para só escrever ou enviar o e-mail com a apresentação padrão, use proposta-comercial-email.\n"
---

# Proposta web

Uma proposta da Playbook Lab é uma página escura, silenciosa e bonita, em que o mecanismo vendido
aparece funcionando. O cliente abre o link, entende o problema dele descrito melhor do que ele mesmo
descreveria, vê o agente trabalhando, confere fases e preço e aprova pelo WhatsApp. O formato já foi
desenhado e aprovado na proposta da Suzano; seu trabalho é **aplicar o formato a um projeto novo com
conteúdo verdadeiro e enxuto**, não redesenhar.

**Antes de tudo, abra o exemplo:** `exemplos/suzano/index.html` (sirva com o preview, ver
references/publicacao.md). É a régua de qualidade e de quantidade de texto.

## Princípios (o porquê de cada regra)

- **A proposta vende sozinha.** O Victor não está na sala quando o cliente lê. Toda frase tem que fazer
  sentido sem explicação, e o preço e o escopo têm que estar claros sem letra miúda.
- **Menos é o padrão.** A primeira versão da Suzano foi enxugada a pedido: tiraram parágrafos repetidos e um
  painel extra. Se hesitar entre incluir e cortar, corte.
- **Mostrar, não listar.** A demonstração do topo, o fluxo de hoje com o gargalo e o pipeline em loop
  existem porque mostram o mecanismo. Benefício listado em card não convence ninguém.
- **Estrutura fixa, conteúdo novo.** Capa, prova social, quem somos, fechamento e todo o visual são
  iguais em toda proposta. O que muda está listado em references/fixo-vs-variavel.md.
- **Nada inventado.** Preço, prazo, números, clientes e resultados vêm de fonte ou do Victor. Só a
  demonstração tem dados fictícios, e ela diz isso na tela.
- **Nível Advisor.** Você prepara e mostra. Publicar e enviar são ações externas: só com confirmação explícita.

## Fluxo

Siga as fases em ordem. As fases 1 a 3 são conversa; não abra o template antes do plano aprovado.

**Antes da primeira proposta:** confira o `config.json` da skill. Se algum campo ainda estiver com
`PREENCHA_...`, peça os dados (WhatsApp com DDI e DDD, e-mail, razão social, CNPJ e a pasta onde as propostas
vão morar) e grave lá. Troque também os logos fictícios da faixa de prova social em `template/assets/logos/`.

### Fase 1: contexto
Leia references/entrevista.md e monte a **ficha da proposta** com o que já existe: a mensagem do Victor
(muitas vezes ele cola o rascunho inteiro), o hub do cliente no vault, o deal no Pipedrive (pipeline 02),
o transcript da call no TLDV e o site do cliente. Para cada item da ficha, anote a fonte ou marque que falta.

### Fase 2: entrevista
Pergunte só o que faltou nos itens obrigatórios e importantes da ficha: até 3 perguntas por rodada,
no máximo 2 rodadas, com opções concretas. Não pergunte nada de visual nem dados fixos da Playbook
(WhatsApp, e-mail, CNPJ, links). Se tudo está na ficha, pule para a fase 3.

### Fase 3: plano de conteúdo
Escreva no chat o plano no formato de references/copy.md (a copy de cada seção em linhas curtas, a ideia
da demonstração, quais blocos opcionais entram e o que foi suposição). Siga references/fixo-vs-variavel.md
para cada seção e references/demo.md para a demonstração. **Espere o ok do Victor** antes de construir.
Ajustes de texto aqui custam segundos; depois de montado custam uma rodada inteira.

### Fase 4: materiais visuais
1. **Logo do cliente.** Busque no site oficial: `firecrawl_scrape` com `formats: ["branding"]` devolve a URL do
   logo e as cores. Baixe com `curl -sL -A "Mozilla/5.0"`. Prefira SVG; PNG só com fundo transparente
   (recorte a margem com PIL se sobrar). Confira que é o logo da empresa (o scraper às vezes pega o logo de
   um cliente dela) abrindo o arquivo. Se o site só tiver o logo embutido no HTML (SVG inline), extraia o
   `<svg>` do cabeçalho. Sem logo bom, pergunte ao Victor.
   O logo é desenhado por máscara (só o alfa conta): logo com disco ou fundo colorido e traços brancos vira
   um círculo chapado. Nesse caso monte um SVG com `<mask>` que vaza os traços (foi o caso da G&L Construir).
2. **Cor da marca.** A fonte mais confiável é o próprio logo: `python3 scripts/cores_logo.py <logo>` lista as
   cores dele, da mais presente para a menos. O `branding` do firecrawl às vezes devolve cor de fundo ou de
   link como "primária" (aconteceu no teste com a Solfácil). Logo monocromático: use a cor do botão principal
   do site. O acento sai da cor pelo script; não escolha à mão.
   **Marca verde** (o acento.py avisa): o acento se confundiria com o verde de "concluído" da página. Use a
   cor secundária da marca, se houver, ou `--neutro`, e diga ao Victor qual escolheu e por quê.
3. **Nada de fotos.** O formato não usa fotos nem ilustração.

### Fase 5: construir
1. Crie a pasta a partir do template:
   ```bash
   python3 scripts/nova_proposta.py --slug <slug> --cliente "<Nome>" --artigo a|o --cor "#hex" --logo <arquivo>
   ```
   Ele copia o template para `<PROPOSTAS>/<slug>/` (a `pasta_propostas` do `config.json` da skill), copia o logo, embute todos os logos no
   HTML como data URI (o Victor abre o `index.html` por `file://`, e aí logo externo por mask some), calcula
   proporção e alturas, deriva o acento e troca os placeholders globais. No fim lista o que falta.
   Se ele imprimir AVISO sobre a cor, resolva antes de seguir (ver fase 4). `--neutro` força o acento neutro.
2. Edite `index.html` trocando cada `{{PLACEHOLDER}}` pelo conteúdo do plano aprovado. Blocos marcados
   REPETÍVEL podem ganhar ou perder itens (ajuste `--steps`, `--n`, `--k`, `--cols`, `--from`, `--span`,
   `--r`); blocos OPCIONAL saem inteiros quando não há conteúdo verdadeiro.
3. Preencha o objeto `DEMO` no script (references/demo.md): mesmas chaves em todos os itens, 3 itens
   com histórias diferentes (alto, médio, e um que o agente não empurra).
4. Confira os 4 links da nav contra as seções que existem.

Não mexa no CSS nem no JS abaixo de "DAQUI PARA BAIXO É FIXO". Se precisar de algo que o template não faz,
pergunte primeiro: quase sempre a resposta é menos, não mais.

### Fase 6: verificar
```bash
python3 scripts/validar.py <PROPOSTAS>/<slug>/index.html
node scripts/estabilidade.js http://localhost:4321/<slug>/
node scripts/capturar.js http://localhost:4321/<slug>/ /tmp/proposta-<slug>
```
(Suba o preview antes: references/publicacao.md. Playwright, uma vez só:
`npm i --prefix ~/.cache/proposta-web playwright@1.58`.)

- **validar.py:** ERRO bloqueia; AVISO de tamanho de texto quase sempre significa cortar.
- **estabilidade.js:** qualquer seção que muda de altura é bug (references/design.md, "Bugs que já aconteceram").
- **capturar.js:** imprime AVISOs de layout que só aparecem renderizados (título do resumo com mais de 4
  linhas, meta quebrando, campo da demonstração cortado, código que não cabe na esteira). Trate como o
  validar.py. Depois abra `desktop.png`, `mobile.png`, `*-capa.png` e `*-resumo.png` (a demonstração já no
  estado final) e passe a revisão visual de references/design.md. Imagem cheia é alta: fatie com PIL antes de olhar.

Corrija em lote e rode de novo. Duas rodadas é o teto; o que sobrar vai como pendência na entrega.

### Fase 7: entregar
Diga ao Victor, curto:
- o link clicável `http://localhost:4321/<slug>/` (e que só abre neste computador);
- o que você supôs ou adaptou do rascunho dele, para ele conferir;
- o que ficou pendente, se algo ficou.
Ajuste o que ele pedir, sempre re-rodando validar.py e estabilidade.js depois de mexer em algo que anima.
Quando ele aprovar a página, ofereça publicar (references/publicacao.md) e só publique com o sim dele.
Depois de publicado, ofereça mandar o link pela proposta-comercial-email.

## Mapa do pacote

| Arquivo | Quando ler |
|---|---|
| `references/entrevista.md` | Fases 1 e 2: onde buscar, a ficha, o que perguntar, o que nunca inventar |
| `references/fixo-vs-variavel.md` | Fase 3 e 5: seção por seção, o que é fixo e como preencher o variável, formatos de investimento |
| `references/copy.md` | Fase 3: voz, tamanho de cada bloco, o que cortar, formato do plano de conteúdo |
| `references/demo.md` | Fase 3 e 5: como montar a demonstração para outros tipos de projeto |
| `references/design.md` | Fase 6 e sempre que for tocar em layout: sistema, movimento permitido, bugs conhecidos, revisão visual |
| `references/publicacao.md` | Preview local e publicação na Vercel |
| `config.json` | Dados fixos (WhatsApp, e-mail, razão social, CNPJ) e a pasta onde as propostas são criadas. Preencha antes da 1ª proposta |
| `template/` | A base de toda proposta nova (não edite para um cliente; copie com o script). A faixa de prova social vem com logos fictícias |
| `exemplos/` | Propostas reais com valores, números e contatos trocados por fictícios: servem de régua de formato, não de preço |
| `exemplos/suzano/` | Proposta real construída pelo template: régua de tom, tamanho e acabamento |
| `exemplos/enuve/` | Proposta real: agente SDR e aplicação de gestão |
| `exemplos/gl-construir/` | Proposta real: atendimento com IA no WhatsApp (traz imagem do cliente em `assets/img`) |
| `exemplos/trinus/` | Proposta real: atendimento e qualificação de leads com IA |
| `scripts/nova_proposta.py` | Cria a pasta da proposta e preenche o mecânico |
| `scripts/acento.py` | Deriva o acento da cor da marca (o nova_proposta.py já chama) |
| `scripts/cores_logo.py` | Lista as cores do logo, para achar a cor real da marca |
| `scripts/validar.py` · `estabilidade.js` · `capturar.js` | Verificação da fase 6 |

## Autoaperfeiçoamento
Esta skill aprende com o uso. Em sessão interativa, quando o Victor **corrigir** a saída com uma regra que vale além deste caso ("sempre", "nunca", "prefiro", ou a mesma correção de novo), acrescente uma linha datada em **Aprendizados** abaixo, e quando ele **aprovar** um resultado muito bom, guarde entrada e saída em `exemplos/` (crie se não existir; 3 a 5 exemplos, mais para copy) e avise numa linha ("salvei na skill: …"). Antes de escrever, leia `exemplos/` (se existir) e Aprendizados. Ajuste de um caso só não grava. **Rotina autônoma não edita a skill**: põe a sugestão no relatório final. Regra que se repetir sobe para o corpo da skill; Aprendizados fica abaixo de ~15 linhas.

### Aprendizados
- _(nenhum ainda)_
