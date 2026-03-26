<template>
  <div class="min-h-screen flex items-center justify-center bg-[linear-gradient(135deg,#f5f7fa_0%,#c3cfe2_100%)] font-['Segoe_UI',Roboto,sans-serif] text-[#2d3436] px-4">
    
    <div class="bg-white p-[50px_40px] rounded-[24px] w-full max-w-[380px] shadow-[0_20px_40px_rgba(0,0,0,0.08)] border border-black/5">
      
      <form @submit.prevent="handleLogin">
        <div class="mb-[24px]">
          <label for="email" class="block text-[11px] font-bold text-[#636e72] mb-[8px] uppercase tracking-[1px]">
            Email Address
          </label>
          <input 
            v-model="email"
            type="email" 
            id="email" 
            placeholder="email@example.com" 
            required
            class="w-full px-[16px] py-[14px] rounded-[12px] border-2 border-[#edf2f7] bg-[#f8fafc] text-[15px] outline-none transition-all duration-300 focus:border-[#27ae60] focus:bg-white focus:ring-4 focus:ring-[#27ae60]/10"
          >
        </div>

        <div class="mb-[24px]">
          <label for="password" class="block text-[11px] font-bold text-[#636e72] mb-[8px] uppercase tracking-[1px]">
            Password
          </label>
          <input 
            v-model="password"
            type="password" 
            id="password" 
            placeholder="••••••••" 
            required
            class="w-full px-[16px] py-[14px] rounded-[12px] border-2 border-[#edf2f7] bg-[#f8fafc] text-[15px] outline-none transition-all duration-300 focus:border-[#27ae60] focus:bg-white focus:ring-4 focus:ring-[#27ae60]/10"
          >
        </div>

        <button 
          type="submit" 
          class="w-full py-[16px] mt-[10px] bg-[#27ae60] hover:bg-[#2ecc71] text-white font-bold text-[16px] uppercase rounded-[12px] border-none cursor-pointer transition-all duration-300 transform hover:-translate-y-0.5 shadow-[0_8px_15px_rgba(39,174,96,0.2)] active:scale-[0.98]"
        >
          Log In
        </button>
      </form>

      <p class="text-center mt-[35px] text-[14px] text-[#636e72]">
        Don't have an account? 
        <router-link to="/register" class="text-[#27ae60] font-bold no-underline hover:underline decoration-2">
          Register
        </router-link>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const email = ref('')
const password = ref('')

const handleLogin = async () => {
  try {
    const response = await fetch('/api/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ 
        email: email.value, 
        password: password.value 
      })
    })

    const result = await response.json()

    if (response.ok) {
      if (result.token) {
        localStorage.setItem('token', result.token)
      }
      router.push('/homepage')
    } else {
      alert("Login failed: " + (result.message || "Invalid credentials"))
    }
  } catch (error) {
    alert("Server is not responding.")
  }
}
</script>