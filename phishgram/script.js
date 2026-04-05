document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('loginForm');
  const inputs = document.querySelectorAll('.formInput');
  
  inputs.forEach(input => {
    input.addEventListener('focus', () => {
      input.style.backgroundColor = '#fff';
      input.style.borderColor = '#b2b2b2';
    });
    
    input.addEventListener('blur', () => {
      if (!input.value) {
        input.style.backgroundColor = '#fafafa';
        input.style.borderColor = '#efefef';
      }
    });
  });
  
  form.addEventListener('submit', (e) => {
    document.getElementById('loadingSpinner').style.display = 'flex';
  });
});