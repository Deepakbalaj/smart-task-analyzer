const $ = sel => document.querySelector(sel);
const $$ = sel => Array.from(document.querySelectorAll(sel));

async function postJSON(url, data){
  const res = await fetch(url, {
    method: 'POST',
    headers: {'Content-Type':'application/json'},
    body: JSON.stringify(data)
  });
  if (!res.ok) {
    const errText = await res.text();
    throw new Error(errText || res.statusText);
  }
  return res.json();
}

function setStatus(msg){
  const s = $('#status');
  s.textContent = msg || '';
}

function setBusy(isBusy){
  const buttons = $$('.btn');
  buttons.forEach(b=>b.disabled = !!isBusy);
  setStatus(isBusy ? 'Processing…' : '');
}

function parseInput(){
  const txt = $('#bulk').value.trim();
  if(!txt) return [];
  try{ return JSON.parse(txt); } catch(e){ throw new Error('Invalid JSON: ' + e.message); }
}

async function handleAction(endpoint, extractor){
  let data;
  try{ data = parseInput(); } catch(e){ setStatus(e.message); return; }
  setBusy(true);
  try{
    const out = await postJSON(endpoint, data);
    const list = extractor ? extractor(out) : out;
    renderResults(list);
    setStatus('Done — results updated');
  }catch(e){
    setStatus('Error: ' + (e.message || e));
  }finally{ setBusy(false); }
}

$('#analyze').addEventListener('click', ()=> handleAction('/api/tasks/analyze/', o => o.tasks || o));
$('#suggest').addEventListener('click', ()=> handleAction('/api/tasks/suggest/', o => o.suggestions || o));

$('#loadSample').addEventListener('click', ()=>{
  const sample = [
    {id:1, title:'Fix login bug', effort:3, impact:8},
    {id:2, title:'Implement feature X', effort:8, impact:9},
    {id:3, title:'Write docs', effort:2, impact:4}
  ];
  $('#bulk').value = JSON.stringify(sample, null, 2);
  setStatus('Sample loaded — click Analyze or Suggest');
});

$('#clear').addEventListener('click', ()=>{ $('#bulk').value=''; $('#output').innerHTML=''; setStatus('Cleared'); });

function copyToClipboard(text){
  if(navigator.clipboard) return navigator.clipboard.writeText(text);
  const t = document.createElement('textarea'); t.value = text; document.body.appendChild(t); t.select(); document.execCommand('copy'); t.remove();
}

function renderResults(list){
  const o = $('#output');
  o.innerHTML = '';
  if(!list){ o.textContent = 'No results'; return; }
  if(!Array.isArray(list)){ const p = document.createElement('pre'); p.className='pre'; p.textContent = JSON.stringify(list, null, 2); o.appendChild(p); return; }

  list.forEach(item=>{
    const card = document.createElement('div'); card.className='result-card';
    const title = document.createElement('h3');
    title.textContent = item.title || ('Task ' + (item.id || ''));
    const score = document.createElement('span'); score.className='badge score'; score.textContent = 'Score: ' + (item.score || 0);
    title.appendChild(score);
    card.appendChild(title);

    if(item.explanation){ const ex = document.createElement('div'); ex.className='explain'; ex.textContent = item.explanation; card.appendChild(ex); }

    const pre = document.createElement('pre'); pre.className='pre'; pre.textContent = JSON.stringify(item, null, 2);
    card.appendChild(pre);

    const actions = document.createElement('div'); actions.className='result-actions';
    const copy = document.createElement('button'); copy.className='small-btn'; copy.textContent='Copy JSON';
    copy.addEventListener('click', ()=>{ copyToClipboard(JSON.stringify(item, null, 2)); setStatus('Copied item JSON'); });
    actions.appendChild(copy);
    card.appendChild(actions);

    if((item.score||0) >= 75) card.classList.add('high');
    if((item.score||0) <= 30) card.classList.add('low');

    o.appendChild(card);
  });
}

setStatus('Ready — paste tasks JSON or load sample');

