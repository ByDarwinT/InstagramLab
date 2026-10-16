// Toda la interfaz usa endpoints locales; no necesita cuenta adicional.
const form = document.querySelector('#jobForm');
const badge = document.querySelector('#badge');
const events = document.querySelector('#events');
const errorBox = document.querySelector('#error');
const download = document.querySelector('#download');
const submit = document.querySelector('#submit');
let interval = null;

async function refresh() {
  try {
    const response = await fetch('/api/jobs');
    if (!response.ok) throw new Error('No se pudo consultar el estado');
    const job = await response.json();
    badge.textContent = {idle:'Sin ejecutar',running:'Extrayendo…',complete:'Completado',error:'Error'}[job.status];
    events.replaceChildren(...(job.events.length ? job.events : ['Esperando inicio…']).map(message => {
      const li = document.createElement('li'); li.textContent = message; return li;
    }));
    errorBox.textContent = job.error || '';
    download.hidden = !job.file;
    if (job.file) download.href = '/downloads/' + encodeURIComponent(job.file);
    submit.disabled = job.status === 'running';
    if (job.status !== 'running' && interval) { clearInterval(interval); interval = null; }
  } catch (err) { errorBox.textContent = err.message; }
}

form.addEventListener('submit', async e => {
  e.preventDefault(); errorBox.textContent = ''; download.hidden = true;
  const response = await fetch('/api/jobs', {method:'POST', headers:{'Content-Type':'application/json'},
    body: JSON.stringify({profile:document.querySelector('#profile').value, posts:document.querySelector('#posts').value})});
  const data = await response.json();
  if (!response.ok) { errorBox.textContent = data.error; return; }
  submit.disabled = true;
  await refresh();
  if (interval) clearInterval(interval);
  interval = setInterval(refresh, 1500);
});
refresh();
