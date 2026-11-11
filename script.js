'use strict';
// Quinze paradigmes, une seule réponse : 2.
const MODES = [
 ['Impératif', 'let s = 1;\ns = s + 1;', () => { let s = 1; s = s + 1; return s; }],
 ['Procédural', 'function add(a,b){return a+b}', () => { function add(a, b) { return a + b; } return add(1, 1); }],
 ['Fonctionnel', '[1,1].reduce((a,b)=>a+b)', () => [1, 1].reduce((a, b) => a + b)],
 ['Orienté objet', 'new Addition(1,1).valeur()', () => { class Addition { constructor(a, b) { this.a = a; this.b = b; } valeur() { return this.a + this.b; } } return new Addition(1, 1).valeur(); }],
 ['Prototypal', 'Object.create(base).somme()', () => { const base = { somme() { return this.a + this.b; } }; return Object.assign(Object.create(base), { a: 1, b: 1 }).somme(); }],
 ['Déclaratif', 'règles = { "1+1": 2 }', () => ({ '1+1': 2 })['1+1']],
 ['Événementiel', 'addEventListener("somme", …)', () => { const t = new EventTarget(); let r; t.addEventListener('somme', e => { r = e.detail[0] + e.detail[1]; }); t.dispatchEvent(new CustomEvent('somme', { detail: [1, 1] })); return r; }],
 ['Réactif', 'new Proxy(état, { set })', () => { let r = 0; const etat = new Proxy({ a: 1, b: 1 }, { set(o, k, v) { o[k] = v; r = o.a + o.b; return true; } }); etat.b = 1; return r; }],
 ['Récursif', 'add(a,b) = b? add(a+1,b-1) : a', () => { const add = (a, b) => b === 0 ? a : add(a + 1, b - 1); return add(1, 1); }],
 ['Asynchrone', 'await Promise.resolve(1) + 1', async () => (await Promise.resolve(1)) + 1],
 ['Générateur', 'function* un(){ yield 1; yield 1 }', () => { function* un() { yield 1; yield 1; } let s = 0; for (const x of un()) s += x; return s; }],
 ['Métaprogrammation', 'new Function("return 1+1")()', () => new Function('return 1+1')()],
 ['Par contraintes', 'chercher x tel que x - 1 = 1', () => { for (let x = 0; x < 100; x++) if (x - 1 === 1) return x; }],
 ['Concurrent', 'Promise.all([1,1]) puis somme', async () => (await Promise.all([Promise.resolve(1), Promise.resolve(1)])).reduce((a, b) => a + b)],
 ['Bit à bit', '(a^b) + ((a&b)<<1) en boucle', () => { let a = 1, b = 1; while (b) { [a, b] = [a ^ b, (a & b) << 1]; } return a; }]
];

const $ = id => document.getElementById(id);
const list = $('modes');
const rows = MODES.map(([nom, code]) => {
  const li = document.createElement('li');
  li.innerHTML = '<h3></h3><pre></pre><span class="res">en attente…</span>';
  li.querySelector('h3').textContent = nom;
  li.querySelector('pre').textContent = code;
  list.append(li);
  return li.querySelector('.res');
});

let total = 0;
$('go').addEventListener('click', async () => {
  const resultats = [];
  for (let i = 0; i < MODES.length; i++) {
    const t0 = performance.now();
    const r = await MODES[i][2]();
    rows[i].textContent = `= ${r} (${(performance.now() - t0).toFixed(2)} ms)`;
    rows[i].classList.toggle('ok', r === 2);
    resultats.push(r);
  }
  const big = $('big');
  big.textContent = resultats.every(r => r === 2) ? '2' : '¯\\_(ツ)_/¯';
  big.classList.remove('shake'); void big.offsetWidth; big.classList.add('shake');
  $('verdict').textContent = `${MODES.length} paradigmes, ${new Set(resultats).size} résultat. Mission inutilement accomplie.`;
  $('count').textContent = ++total;
});

// Python et Kotlin : appel au serveur, avec repli si on ouvre le fichier à la main.
const FALLBACK = { py: 'Python dort : lance ./run.sh pour le réveiller.', kt: 'Kotlin n’a rien généré : lance ./run.sh.' };
document.querySelectorAll('[data-api]').forEach(b => b.addEventListener('click', async () => {
  const k = b.dataset.api, out = $(k);
  try {
    const r = await fetch(`/api/${k}`);
    if (!r.ok) throw new Error(r.status);
    out.textContent = (await r.json()).message;
  } catch { out.textContent = FALLBACK[k]; }
}));

// Le relais : le navigateur donne le départ, le serveur fait circuler 1+1 dans tous les langages.
$('relais').addEventListener('click', async () => {
  const ol = $('chaine'), retour = $('retour'), ign = $('ignores'), btn = $('relais');
  ol.innerHTML = ''; ign.innerHTML = ''; retour.textContent = 'Le relais est lancé (la première fois, il compile)…';
  btn.disabled = true;
  try {
    const r = await fetch('/api/relais?depart=' + encodeURIComponent('HTML>CSS>JavaScript'));
    if (!r.ok) throw new Error(r.status);
    const d = await r.json();
    for (const nom of d.chemin) {
      const li = document.createElement('li'); li.textContent = nom; ol.append(li);
      await new Promise(ok => setTimeout(ok, 150));
    }
    retour.textContent = `Retour au navigateur : ${d.valeur}. ${d.chemin.length} étapes pour une addition.`;
    for (const i of d.ignores) {
      const li = document.createElement('li'); li.textContent = `${i.nom} ignoré : ${i.raison}`; ign.append(li);
    }
    $('count').textContent = ++total;
  } catch { retour.textContent = 'Le relais a besoin du serveur : lance ./run.sh.'; }
  btn.disabled = false;
});
