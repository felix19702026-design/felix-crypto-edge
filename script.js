document.getElementById('year').textContent = new Date().getFullYear();

const form = document.querySelector('.lead-form');
form?.addEventListener('submit', () => {
  const btn = form.querySelector('button[type="submit"]');
  if (btn) btn.textContent = 'Opening email...';
});
