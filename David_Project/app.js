// ---------- Shared ----------
const yearEl = document.getElementById('year');
if (yearEl) yearEl.textContent = new Date().getFullYear();

// Theme toggle (present on Support page)
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

// ---------- Pricing (Home + Order) ----------
(function pricingInit(){
  const COST_PER_BLOCK = 5;     // $5 per 250 words
  const BLOCK_SIZE = 250;

  const wordsInput = document.getElementById('wordCount'); // Home
  const words2 = document.getElementById('words2');        // Order
  const calcBtn = document.getElementById('calcBtn');      // Only on Order
  const totalCostEl = document.getElementById('totalCost');
  const blocksEl = document.getElementById('blocks');
  const payBtn = document.getElementById('payBtn');

  if (!totalCostEl || !blocksEl) return;

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

  // Auto-calc as user types
  [wordsInput, words2].forEach(el => el && el.addEventListener('input', updateQuote));
  if (calcBtn) calcBtn.addEventListener('click', updateQuote); // Order page "Recalculate"
  updateQuote();

  // Order quick actions
  const startBtn = document.getElementById('startBtn');
  const contactBtn = document.getElementById('contactBtn');
  if (startBtn) {
    startBtn.addEventListener('click', () => {
      const name = (document.getElementById('name')?.value || '').trim();
      const email = (document.getElementById('email')?.value || '').trim();
      const words = (document.getElementById('words2')?.value || '').trim();
      const { cost } = calculateCost(words);
      if (!name || !email || !words) return alert('Please fill your name, email, and word count.');
      alert(`Thanks ${name}! We'll email a quote of $${cost} to ${email}.`);
    });
  }
  if (contactBtn) contactBtn.addEventListener('click', () => { window.location.href = 'mailto:support@manualaiwrites.com'; });

  // PayPal
  if (payBtn) {
    let paypalRendered = false;
    payBtn.addEventListener('click', async () => {
      updateQuote();
      const total = parseFloat(totalCostEl.textContent || '0');
      if (!total || total <= 0) return alert('Please enter a valid word count to generate a total before paying.');
      const pc = document.getElementById('paypal-container');
      if (!pc) return;
      pc.style.display = 'block';

      if (window.paypal && !paypalRendered) {
        paypalRendered = true;
        paypal.Buttons({
          style: { layout: 'horizontal', height: 45 },
          createOrder: (data, actions) => actions.order.create({
            purchase_units: [{ amount: { value: total.toFixed(2) } }]
          }),
          onApprove: async (data, actions) => {
            const details = await actions.order.capture();
            alert(`Payment successful! Thank you, ${details.payer.name.given_name}.\nOrder ID: ${details.id}`);
          },
          onError: (err) => { console.error(err); alert('Payment could not be completed. Please try again.'); }
        }).render('#paypal-container');
      }
    });
  }
})();

// ---------- Blog detail (single template with slugs) ----------
(function blogDetail(){
  const root = document.getElementById('blogPost');
  if (!root) return;

  const POSTS = {
    'humanize-ai-drafts': {
      title: 'Five ways to humanize AI drafts',
      image: 'https://picsum.photos/seed/human/1200/700',
      author: 'Ava K.',
      date: 'Aug 2025',
      read: '6 min',
      body: `
        <p>AI is efficient, but raw output often lacks rhythm and intent. Here are five quick wins that make text feel written by a person:</p>
        <h3>1) Break the metronome</h3>
        <p>Vary sentence length deliberately. Follow a long line with a short punch. Let the paragraph breathe.</p>
        <h3>2) Purposeful transitions</h3>
        <p>Swap filler transitions (“Additionally…”) for connective logic: <em>because, therefore, so</em>.</p>
        <h3>3) Swap generic verbs</h3>
        <p>Pick verbs that carry the work: <em>prove, distill, surface, sharpen</em>.</p>
        <h3>4) Remove hedging</h3>
        <p>Limit “might, could, seems” unless you truly need uncertainty.</p>
        <h3>5) Read aloud</h3>
        <p>If it sounds robotic, it reads robotic. Edit with your ear.</p>
      `
    },
    'detector-myths': {
      title: 'Detector myths, explained',
      image: 'https://picsum.photos/seed/detector/1200/700',
      author: 'Sam R.',
      date: 'Aug 2025',
      read: '5 min',
      body: `
        <p>Detectors estimate patterns—not intent. We use tools like ZeroGPT and Turnitin as <em>signals</em>, then edit for natural cadence and originality.</p>
        <h3>Signals vs. decisions</h3>
        <p>Use multiple indicators and human review. Avoid treating a single score as a verdict.</p>
      `
    },
    'style-matching': {
      title: 'Style-matching in practice',
      image: 'https://picsum.photos/seed/style/1200/700',
      author: 'Lena M.',
      date: 'Aug 2025',
      read: '7 min',
      body: `
        <p>We mirror voice by sampling your writing for sentence music, idioms, and pacing. Then we rebuild your draft with that fingerprint intact.</p>
      `
    },
    'privacy-first': {
      title: 'Privacy-first editing',
      image: 'https://picsum.photos/seed/privacy/1200/700',
      author: 'Noah T.',
      date: 'Aug 2025',
      read: '4 min',
      body: `
        <p>We keep your content siloed, sign NDAs on request, and never reuse your text. Access is logged and time-boxed.</p>
      `
    },
    'zero-gpt-guide': {
      title: 'ZeroGPT: a practical guide',
      image: 'https://picsum.photos/seed/zerogpt/1200/700',
      author: 'Sam R.',
      date: 'Aug 2025',
      read: '6 min',
      body: `
        <p>ZeroGPT highlights statistical patterns. Treat it as an input to editing, not a compliance stamp.</p>
      `
    },
    'turnitin-tips': {
      title: 'Turnitin: similarity vs. plagiarism',
      image: 'https://picsum.photos/seed/turnitin/1200/700',
      author: 'Ava K.',
      date: 'Aug 2025',
      read: '6 min',
      body: `
        <p>Turnitin flags similarity, not guilt. We cut boilerplate, re-express ideas, and add original connective tissue.</p>
      `
    }
  };

  const params = new URLSearchParams(location.search);
  const slug = params.get('slug');
  const post = POSTS[slug] || POSTS['humanize-ai-drafts'];

  document.title = `${post.title} – manuaAIrewrites`;
  document.getElementById('bpTitle').textContent = post.title;
  document.getElementById('bpMeta').textContent = `${post.author} • ${post.date} • ${post.read} read`;
  const img = document.getElementById('bpImage'); img.src = post.image; img.alt = post.title;
  document.getElementById('bpBody').innerHTML = post.body;
})();

// ---------- Contact form (mailto handoff) ----------
(function contactForm(){
  const form = document.getElementById('contactForm');
  if (!form) return;
  const nameEl = document.getElementById('cName');
  const emailEl = document.getElementById('cEmail');
  const msgEl = document.getElementById('cMessage');
  const statusEl = document.getElementById('contactStatus');

  form.addEventListener('submit', (e) => {
    e.preventDefault();
    const name = nameEl.value.trim();
    const email = emailEl.value.trim();
    const message = msgEl.value.trim();
    if (!name || !email || !message) {
      statusEl.textContent = 'Please fill all fields.';
      return;
    }
    const subject = encodeURIComponent(`New inquiry from ${name}`);
    const body = encodeURIComponent(`Name: ${name}\nEmail: ${email}\n\nMessage:\n${message}`);
    window.location.href = `mailto:support@manualaiwrites.com?subject=${subject}&body=${body}`;
    statusEl.textContent = 'Opening your email app…';
  });
})();
