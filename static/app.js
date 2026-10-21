// Estado independiente para el login manual y para el scraping.
const form = document.querySelector('#jobForm');
const authBadge = document.querySelector('#authBadge');
const loadBtn = document.querySelector('#loadCookies');
const confirmBtn = document.querySelector('#confirmCookies');
const authEvents = document.querySelector('#authEvents');
const authError = document.querySelector('#authError');
const fields = document.querySelector('#scrapingFields');
const hint = document.querySelector('#scrapingHint');
const badge = document.querySelector('#badge');
const jobBadge = document.querySelector('#jobBadge');
const events = document.querySelector('#events');
const errorBox = document.querySelector('#error');
const download = document.querySelector('#download');
const submit = document.querySelector('#submit');
let loggedIn = false;
let scraping = false;

function showEvents(element, messages, placeholder) {
  element.replaceChildren(...(messages.length ? messages : [placeholder]).map(message => {
    const li = document.createElement('li');
    li.textContent = message;
    return li;
  }));
}

async function post(url, body = {}) {
  const response = await fetch(url, {
    method: 'POST', headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(body)
  });
  const data = await response.json();
  if (!response.ok) throw new Error(data.error || 'Error de conexión');
  return data;
}

async function refresh() {
  try {
    const [authResponse, jobResponse] = await Promise.all([fetch('/api/auth'), fetch('/api/jobs')]);
    if (!authResponse.ok || !jobResponse.ok) throw new Error('Error consultando el servidor');
    const auth = await authResponse.json();
    const job = await jobResponse.json();
    loggedIn = auth.status === 'ready';
    scraping = job.status === 'running';
    const loggingIn = auth.status === 'running';
    authBadge.textContent = {idle:'Sin validar',running:'Esperando login',ready:'Cookies guardadas',error:'Error'}[auth.status] || auth.status;
    authError.textContent = auth.error || '';
    loadBtn.disabled = loggingIn || scraping;
    confirmBtn.disabled = !loggingIn;
    showEvents(authEvents, auth.events, 'Todavía no se inició la carga de cookies.');
    fields.disabled = !loggedIn || scraping;
    badge.textContent = loggedIn ? 'Habilitado' : 'Bloqueado';
    hint.textContent = loggedIn ? 'Sesión validada. Ya puedes extraer perfiles.' : 'Primero debes cargar y verificar las cookies.';
    jobBadge.textContent = {idle:'Sin ejecutar',running:'Extrayendo…',complete:'Completado',error:'Error'}[job.status] || job.status;
    showEvents(events, job.events, 'Esperando extracción…');
    errorBox.textContent = job.error || '';
    download.hidden = !job.file;
    if (job.file) download.href = '/downloads/' + encodeURIComponent(job.file);
  } catch (err) { authError.textContent = err.message; }
}

loadBtn.addEventListener('click', async () => {
  authError.textContent = '';
  try { await post('/api/auth/start'); await refresh(); }
  catch (err) { authError.textContent = err.message; }
});
confirmBtn.addEventListener('click', async () => {
  authError.textContent = '';
  try { await post('/api/auth/confirm'); await refresh(); }
  catch (err) { authError.textContent = err.message; }
});
form.addEventListener('submit', async event => {
  event.preventDefault();
  errorBox.textContent = '';
  download.hidden = true;
  try {
    await post('/api/jobs', {
      profile: document.querySelector('#profile').value,
      posts: document.querySelector('#posts').value
    });
    await refresh();
  } catch (err) { errorBox.textContent = err.message; }
});
refresh();
setInterval(refresh, 1800);
