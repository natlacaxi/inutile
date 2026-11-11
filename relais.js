const [v, ...r] = require('fs').readFileSync(0, 'utf8').replace(/[\r\n]+$/, '').split('\t');
console.log(`${v}\t${r.join('\t')}>Node.js`);
