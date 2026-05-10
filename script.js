document.getElementById('year').textContent = new Date().getFullYear();

const form = document.querySelector('.lead-form');
form?.addEventListener('submit', () => {
  const button = form.querySelector('button[type="submit"]');
  if (button) button.textContent = 'Opening email...';
});
