#!/usr/bin/env node
/* Testa se alguma animação muda o tamanho da página (o bug que mais apareceu na Suzano:
   um bloco cresce durante o loop e empurra tudo abaixo). Também confere se a faixa de
   logos cobre a tela inteira o tempo todo e se a página estoura na lateral.

   Uso:  node estabilidade.js http://localhost:4321/<slug>/
   Saída: OK ou a lista do que se mexeu, por largura de tela. */
const path = require('path');
const os = require('os');
let chromium;
try { ({ chromium } = require('playwright')); }
catch { ({ chromium } = require(path.join(os.homedir(), '.cache/proposta-web/node_modules/playwright'))); }

(async () => {
  const url = process.argv[2];
  if (!url) { console.log('uso: node estabilidade.js <url>'); process.exit(1); }
  const b = await chromium.launch();
  let falhou = false;
  await Promise.all([390, 1100, 1440, 1920].map(async w => {
    const p = await b.newPage({ viewport: { width: w, height: 900 } });
    await p.goto(url, { waitUntil: 'networkidle' });
    const H = await p.evaluate(() => document.documentElement.scrollHeight);
    for (let y = 0; y < H; y += 500) { await p.evaluate(v => scrollTo(0, v), y); await p.waitForTimeout(120); }
    await p.evaluate(() => document.querySelector('#resumo').scrollIntoView());
    const sample = () => p.evaluate(() => {
      const o = {};
      document.querySelectorAll('main > section').forEach(s => { o[s.id || s.className] = s.offsetHeight; });
      const t = document.querySelector('.track');
      o.__marquee = t ? Math.round(t.getBoundingClientRect().right - innerWidth) : 9999;
      o.__overflow = document.documentElement.scrollWidth - innerWidth;
      return o;
    });
    const seen = {}; let minMarquee = 1e9, maxOverflow = 0;
    for (let i = 0; i < 50; i++) {            // ~20 s: mais de um ciclo da demonstração (3 itens)
      await p.waitForTimeout(400);
      const s = await sample();
      minMarquee = Math.min(minMarquee, s.__marquee); maxOverflow = Math.max(maxOverflow, s.__overflow);
      for (const [k, v] of Object.entries(s)) if (!k.startsWith('__')) (seen[k] ||= new Set()).add(v);
    }
    const mexeu = Object.entries(seen).filter(([, v]) => Math.max(...v) - Math.min(...v) > 2)
      .map(([k, v]) => `${k} variou ${Math.min(...v)}..${Math.max(...v)}px`);
    const probs = [...mexeu];
    if (minMarquee < 0) probs.push(`faixa de logos deixou ${-minMarquee}px vazios na direita`);
    if (maxOverflow > 0) probs.push(`página estoura ${maxOverflow}px na lateral`);
    if (probs.length) falhou = true;
    console.log(`${w}px: ${probs.length ? probs.join(' | ') : 'OK'}`);
    await p.close();
  }));
  await b.close();
  process.exit(falhou ? 1 : 0);
})();
