function safeJsonParse(s, fallback) {
  try { return JSON.parse(s) } catch { return fallback }
}

function loadProfile() {
  return safeJsonParse(localStorage.getItem('mp_profile'), null)
}

function saveOffer(offer) {
  const arr = safeJsonParse(localStorage.getItem('mp_offers'), [])
  arr.unshift(offer)
  localStorage.setItem('mp_offers', JSON.stringify(arr.slice(0, 50)))
}

function init() {
  const form = document.getElementById('offerForm')
  const saveBtn = document.getElementById('offerSaveBtn')
  const profile = loadProfile()

  if (!form || !saveBtn) return

  form.addEventListener('submit', (e) => {
    e.preventDefault()
    const fd = new FormData(form)
    const offer = {
      id: crypto?.randomUUID?.() || String(Date.now()),
      product: String(fd.get('product') || '').trim(),
      region: String(fd.get('region') || '').trim(),
      quantity: String(fd.get('quantity') || '').trim(),
      price: String(fd.get('price') || '').trim(),
      createdAt: new Date().toISOString(),
      sellerName: profile?.name || '',
      sellerPhone: profile?.phone || '',
    }

    saveOffer(offer)
    window.location.href = 'Homepage.html'
  })
}

init()
