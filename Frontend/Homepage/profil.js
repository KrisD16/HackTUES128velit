function safeJsonParse(s, fallback) {
  try { return JSON.parse(s) } catch { return fallback }
}

function init() {
  const form = document.getElementById('profileForm')
  const clearBtn = document.getElementById('pfClear')
  if (!form) return

  const existing = safeJsonParse(localStorage.getItem('mp_profile'), null)
  if (existing) {
    const set = (id, v) => {
      const el = document.getElementById(id)
      if (el && v) el.value = v
    }
    set('pfName', existing.name)
    set('pfPhone', existing.phone)
    set('pfRegion', existing.region)
    set('pfProduct', existing.product)
  }

  form.addEventListener('submit', (e) => {
    e.preventDefault()
    const fd = new FormData(form)
    const photo = document.getElementById('pfPhoto')
    const file = photo?.files?.[0]

    const profile = {
      name: String(fd.get('name') || '').trim(),
      phone: String(fd.get('phone') || '').trim(),
      region: String(fd.get('region') || '').trim(),
      product: String(fd.get('product') || '').trim(),
      photoName: file ? file.name : '',
      updatedAt: new Date().toISOString(),
    }

    localStorage.setItem('mp_profile', JSON.stringify(profile))
    window.location.href = 'Homepage.html'
  })

  if (clearBtn) {
    clearBtn.addEventListener('click', () => {
      form.reset()
      localStorage.removeItem('mp_profile')
    })
  }
}

init()
