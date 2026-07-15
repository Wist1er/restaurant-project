const header = document.querySelector('.header');
if (header) {
  window.addEventListener('scroll', () => {
    header.classList.toggle('is-scrolled', window.scrollY > 40);
  });
}

const navToggle = document.querySelector('.header__toggle');
const nav = document.querySelector('.nav');
if (navToggle && nav) {
  navToggle.addEventListener('click', () => nav.classList.toggle('is-open'));
  nav.querySelectorAll('.nav__link').forEach(link => {
    link.addEventListener('click', () => nav.classList.remove('is-open'));
  });
}

const sliderTrack = document.querySelector('.slider__track');
const sliderPrev = document.querySelector('[data-slider-prev]');
const sliderNext = document.querySelector('[data-slider-next]');
if (sliderTrack && sliderPrev && sliderNext) {
  const scrollStep = () => sliderTrack.querySelector('.slider__item').offsetWidth + 24;
  sliderPrev.addEventListener('click', () => sliderTrack.scrollBy({ left: -scrollStep(), behavior: 'smooth' }));
  sliderNext.addEventListener('click', () => sliderTrack.scrollBy({ left: scrollStep(), behavior: 'smooth' }));
}

const filterButtons = document.querySelectorAll('.menu__filter');
const menuItems = document.querySelectorAll('.menu__item');
filterButtons.forEach(btn => {
  btn.addEventListener('click', () => {
    filterButtons.forEach(b => b.classList.remove('menu__filter--active'));
    btn.classList.add('menu__filter--active');

    const category = btn.dataset.category;
    menuItems.forEach(item => {
      const show = category === 'all' || item.dataset.category === category;
      item.classList.toggle('is-hidden', !show);
    });
  });
});

function handleAjaxForm(formId, onSuccess) {
  const form = document.getElementById(formId);
  if (!form) return;

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const msgBox = form.querySelector('.form__message');

    try {
      const response = await fetch(form.action, {
        method: 'POST',
        body: new FormData(form),
        headers: { 'X-Requested-With': 'XMLHttpRequest' },
      });

      let data;
      try {
        data = await response.json();
      } catch (parseErr) {
        throw new Error('server');
      }

      if (msgBox) {
        msgBox.textContent = data.message;
        msgBox.classList.toggle('form__message--success', data.ok);
        msgBox.classList.toggle('form__message--error', !data.ok);
      }

      if (data.ok) {
        form.reset();
        if (onSuccess) onSuccess();
      }
    } catch (err) {
      if (msgBox) {
        msgBox.textContent = err.message === 'server'
          ? 'Ошибка на сервере, проверьте консоль python run.py'
          : 'Ошибка сети, попробуйте позже';
        msgBox.classList.add('form__message--error');
      }
    }
  });
}

handleAjaxForm('login-form', () => window.location.reload());
handleAjaxForm('register-form', () => window.location.reload());
handleAjaxForm('booking-form');
handleAjaxForm('contact-form');
