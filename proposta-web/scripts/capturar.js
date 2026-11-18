#!/usr/bin/env node
/* Captura a proposta em desktop (1440) e celular (390), página inteira, com as animações
   de entrada já disparadas. Também salva a capa, o resumo com a demonstração no estado final
   e imprime avisos de layout (título com linhas demais, meta quebrando, campo cortado).

   Uso:
     node capturar.js http://localhost:4321/<slug>/ <pasta-de-saida>

   Precisa do Playwright (uma vez só):
     npm i --prefix ~/.cache/proposta-web playwright@1.58
   Por que Playwright e não o Chrome headless da linha de comando: o Chrome headless tem largura
   mínima de janela (~500px) e corta a captura de 390px, parecendo que a página estoura na lateral.
   E o painel do navegador do app pausa animações quando está oculto; aqui elas rodam de verdade. */
const path = require('path');
const os = require('os');
let chromium;
try { ({ chromium } = require('playwright')); }
catch { ({ chromium } = require(path.join(os.homedir(), '.cache/proposta-web/node_modules/playwright'))); }

(async () => {
  const [url, out = '.'] = process.argv.slice(2);
  if (!url) { console.log('uso: node capturar.js <url> <pasta>'); process.exit(1); }
  const fs = require('fs'); fs.mkdirSync(out, { recursive: true });
  const b = await chromium.launch();
  for (const [nome, w, h] of [['desktop', 1440, 900], ['mobile', 390, 844]]) {
    const p = await b.newPage({ viewport: { width: w, height: h }, isMobile: w < 700, hasTouch: w < 700 });
    await p.goto(url, { waitUntil: 'networkidle' });
    await p.waitForTimeout(1200);
    await p.screenshot({ path: path.join(out, `${nome}-capa.png`) });
    // rola a página inteira para disparar as entradas e os números
    const H = await p.evaluate(() => document.documentElement.scrollHeight);
    for (let y = 0; y < H; y += Math.round(h * 0.6)) { await p.evaluate(v => scrollTo(0, v), y); await p.waitForTimeout(300); }
    // resumo (hero) com a demonstração no estado final (tarefa criada), para ver o painel cheio
    await p.evaluate(() => document.querySelector('#resumo').scrollIntoView());
    try { await p.waitForSelector('#r-task.on', { timeout: 25000 }); await p.waitForTimeout(600); }
    catch { console.log(`${nome}: ATENÇÃO a demonstração não chegou ao estado final em 25 s`); }
    await p.screenshot({ path: path.join(out, `${nome}-resumo.png`) });
    // checagens de layout que o validar.py não consegue ver (dependem da renderização)
    const alertas = await p.evaluate((w) => {
      const a = [];
      const lh = el => parseFloat(getComputedStyle(el).lineHeight) || 1;
      const linhas = el => Math.round(el.getBoundingClientRect().height / lh(el));
      const t = document.querySelector('.hero-t');
      if (t) { const n = linhas(t); if (n > (w > 700 ? 4 : 6)) a.push(`título do resumo com ${n} linhas (ideal: até ${w > 700 ? 4 : 6}); encurte a promessa`); }
      document.querySelectorAll('.meta dd').forEach(el => { if (linhas(el) > 1) a.push(`meta "${el.textContent.trim()}" quebra em ${linhas(el)} linhas; encurte`); });
      document.querySelectorAll('.f .v').forEach(el => { if (el.scrollWidth > el.clientWidth + 1) a.push(`campo da demonstração cortado: "${el.textContent.trim()}"`); });
      document.querySelectorAll('.chip b').forEach(el => { if (el.getBoundingClientRect().right > el.parentElement.getBoundingClientRect().right + 1) a.push(`código da esteira não cabe no chip: "${el.textContent.trim()}" (use até 7 caracteres)`); });
      document.querySelectorAll('.node h3, .deliv h3, .roles h3').forEach(el => { if (linhas(el) > 2) a.push(`título "${el.textContent.trim()}" com ${linhas(el)} linhas`); });
      return a;
    }, w);
    alertas.forEach(x => console.log(`${nome}: AVISO ${x}`));
    await p.evaluate(() => scrollTo(0, 0));
    await p.waitForTimeout(800);
    await p.screenshot({ path: path.join(out, `${nome}.png`), fullPage: true });
    const overflow = await p.evaluate(() => document.documentElement.scrollWidth - innerWidth);
    console.log(`${nome}: ${path.join(out, nome + '.png')}${overflow > 0 ? `  ATENÇÃO: estoura ${overflow}px na lateral` : ''}`);
    await p.close();
  }
  await b.close();
})();
