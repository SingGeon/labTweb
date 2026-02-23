function toggleForm() {
  const registerForm = document.getElementById('register-form');
  const loginForm = document.getElementById('login-form');
  const formTitle = document.getElementById('form-title');
  const formSubtitle = document.querySelector('.form-subtitle');

  registerForm.classList.toggle('active');
  loginForm.classList.toggle('active');

  if (registerForm.classList.contains('active')) {
    formTitle.innerHTML = 'Crează un cont <span>learnify</span>';
    formSubtitle.innerHTML = 'Ai deja un cont? <span class="toggle-link" onclick="toggleForm()">Log in</span>';
  } else {
    formTitle.innerHTML = 'Intră în contul tău <span>learnify</span>';
    formSubtitle.innerHTML = 'Nu ai încă un cont? <span class="toggle-link" onclick="toggleForm()">Înregistrează-te</span>';
  }
}

function nextStep() {
  const form = document.getElementById('step1Form');
  if (!form.checkValidity()) {
    alert('Completează toate câmpurile!');
    return;
  }

  const p1 = document.getElementById('password').value;
  const p2 = document.getElementById('confirmPassword').value;
  if (p1 !== p2) {
    alert("Parolele nu coincid!");
    return;
  }

  document.getElementById('step-1').classList.remove('active');
  document.getElementById('step-2').classList.add('active');
}

function prevStep() {
  document.getElementById('step-2').classList.remove('active');
  document.getElementById('step-1').classList.add('active');
}

// -------- REGISTER (Step 2 Submit) --------
document.addEventListener("DOMContentLoaded", () => {
  const step2Form = document.getElementById('step2Form');
  if (step2Form) {
    step2Form.addEventListener('submit', async (e) => {
      e.preventDefault();

      const payload = {
        nume: document.getElementById('name').value.trim(),
        email: document.getElementById('email').value.trim(),
        parola: document.getElementById('password').value,
        clasa: document.getElementById('clasa').value,
        liceul: document.getElementById('liceu').value,
        profil: "elev"
      };

      const res = await fetch('/api/register', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(payload)
      });

      const data = await res.json();

      if (!res.ok) {
        alert(data.error || "Eroare la înregistrare");
        return;
      }

      alert("Înregistrare reușită! Acum loghează-te.");
      // switch to login view
      if (document.getElementById('register-form').classList.contains('active')) {
        toggleForm();
      }
    });
  }

  // -------- LOGIN Submit --------
  const loginForm = document.getElementById('loginForm');
  if (loginForm) {
    loginForm.addEventListener('submit', async (e) => {
      e.preventDefault();

      const email = document.getElementById('loginEmail').value.trim();
      const parola = document.getElementById('loginPassword').value;

      const res = await fetch('/api/login', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ email, parola })
      });

      const data = await res.json();

      if (!res.ok) {
        alert(data.error || "Login failed");
        return;
      }

      window.location.href = data.redirect; // /dashboard
    });
  }
});
