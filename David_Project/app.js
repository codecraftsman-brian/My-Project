// --------- Utilities ---------
const clamp = (n, min, max) => Math.max(min, Math.min(max, n));

// Footer year
const yearEl = document.getElementById('year');
if (yearEl) yearEl.textContent = new Date().getFullYear();

// Theme toggle (only on support page or anywhere you include it)
(function themeInit(){
  const themeToggle = document.getElementById('themeToggle');
  if (!themeToggle) return;
  const LS_KEY = 'manua-theme';
  const applyTheme = (mode) => {
    document.documentElement.style.colorScheme = mode === 'light' ? 'light' : 'dark';
    localStorage.setItem(LS_KEY, mode);
  };
  const saved = localStorage.getItem(LS_KEY);
  if (saved) applyTheme(saved);
  const toggle = () => {
    const curr = localStorage.getItem(LS_KEY) || (matchMedia('(prefers-color-scheme: dark)').matches ? 'dark':'light');
    const next = curr === 'dark' ? 'light' : 'dark';
    applyTheme(next);
    themeToggle.setAttribute('aria-pressed', next === 'dark' ? 'true' : 'false');
  };
  themeToggle.addEventListener('click', toggle);
  themeToggle.addEventListener('keydown', (e)=>{ if(e.key==='Enter' || e.key===' '){ e.preventDefault(); toggle(); }});
})();

// --------- Pricing / PayPal (used on home & order pages) ---------
(function pricingInit(){
  const COST_PER_BLOCK = 5;      // $5
  const BLOCK_SIZE = 250;        // words per block

  const wordsInput = document.getElementById('wordCount'); // home
  const words2 = document.getElementById('words2');        // order page
  const calcBtn = document.getElementById('calcBtn');      // only on order page
  const totalCostEl = document.getElementById('totalCost');
  const blocksEl = document.getElementById('blocks');
  const payBtn = document.getElementById('payBtn');

  if (!totalCostEl || !blocksEl) return; // not on a pricing page

  const calculateCost = (words) => {
    const n = parseInt(words, 10);
    if (!isFinite(n) || n <= 0) return { blocks: 0, cost: 0 };
    const blocks = Math.ceil(n / BLOCK_SIZE);
    return { blocks, cost: blocks * COST_PER_BLOCK };
  };

  const updateQuote = () => {
    const value = (wordsInput && wordsInput.value) || (words2 && words2.value) || 0;
    const { blocks, cost } = calculateCost(value);
    totalCostEl.textContent = String(cost);
    blocksEl.textContent = String(blocks);
  };

  // Auto-calc on input on both pages
  [wordsInput, words2].forEach(el => el && el.addEventListener('input', updateQuote));

  // The Calculate button only exists on the order page—safe guard
  if (calcBtn) calcBtn.addEventListener('click', updateQuote);

  // Initialize display once
  updateQuote();

  // PayPal handler (unchanged)
  if (payBtn) {
    let paypalRendered = false;
    payBtn.addEventListener('click', async () => {
      updateQuote();
      const total = parseFloat(totalCostEl.textContent || '0');
      if (!total || total <= 0) {
        return alert('Please enter a valid word count to generate a total before paying.');
      }
      const pc = document.getElementById('paypal-container');
      if (!pc) return;
      pc.style.display = 'block';

      if (window.paypal && !paypalRendered) {
        paypalRendered = true;
        paypal.Buttons({
          style: { layout: 'horizontal', height: 45 },
          createOrder: (data, actions) =>
            actions.order.create({ purchase_units: [{ amount: { value: total.toFixed(2) } }] }),
          onApprove: async (data, actions) => {
            const details = await actions.order.capture();
            alert(`Payment successful! Thank you, ${details.payer.name.given_name}.\nOrder ID: ${details.id}`);
          },
          onError: (err) => {
            console.error(err);
            alert('Payment could not be completed. Please try again.');
          }
        }).render('#paypal-container');
      }
    });
  }
})();
