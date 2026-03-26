<template>
  <div class="min-h-screen flex items-center justify-center bg-[linear-gradient(135deg,#f5f7fa_0%,#c3cfe2_100%)] font-['Segoe_UI',Roboto,sans-serif] text-[#2d3436] px-4">
    
    <div class="bg-white p-[50px_40px] rounded-[24px] w-full max-w-[380px] shadow-[0_20px_40px_rgba(0,0,0,0.08)] border border-black/5">
      
      <form @submit.prevent="handleRegister">
        <div class="mb-[20px]">
          <label for="reg-email" class="block text-[11px] font-bold text-[#636e72] mb-[6px] uppercase tracking-[1px]">
            Email Address
          </label>
          <div class="relative">
            <input 
              v-model="email"
              type="email" 
              id="reg-email" 
              placeholder="email@example.com" 
              required
              class="w-full px-[16px] py-[12px] rounded-[12px] border-2 border-[#edf2f7] bg-[#f8fafc] text-[#2d3436] font-['Segoe_UI'] text-[15px] outline-none transition-all duration-300 ease-in-out focus:border-[#27ae60] focus:bg-white focus:ring-4 focus:ring-[#27ae60]/10"
            >
          </div>
        </div>

        <div class="mb-[20px]">
          <label for="reg-password" class="block text-[11px] font-bold text-[#636e72] mb-[6px] uppercase tracking-[1px]">
            Password
          </label>
          <div class="relative">
            <input 
              v-model="password"
              type="password" 
              id="reg-password" 
              placeholder="Create password" 
              required
              class="w-full px-[16px] py-[12px] rounded-[12px] border-2 border-[#edf2f7] bg-[#f8fafc] text-[#2d3436] font-['Segoe_UI'] text-[15px] outline-none transition-all duration-300 ease-in-out focus:border-[#27ae60] focus:bg-white focus:ring-4 focus:ring-[#27ae60]/10"
            >
          </div>
        </div>

        <div class="mb-[20px]">
          <label for="confirm-password" class="block text-[11px] font-bold text-[#636e72] mb-[6px] uppercase tracking-[1px]">
            Confirm Password
          </label>
          <div class="relative">
            <input 
              v-model="confirmPassword"
              type="password" 
              id="confirm-password" 
              placeholder="Repeat password" 
              required
              class="w-full px-[16px] py-[12px] rounded-[12px] border-2 border-[#edf2f7] bg-[#f8fafc] text-[#2d3436] font-['Segoe_UI'] text-[15px] outline-none transition-all duration-300 ease-in-out focus:border-[#27ae60] focus:bg-white focus:ring-4 focus:ring-[#27ae60]/10"
            >
          </div>
        </div>

        <button 
          type="submit" 
          class="w-full py-[16px] mt-[15px] bg-[#27ae60] hover:bg-[#2ecc71] text-white font-bold text-[16px] uppercase rounded-[12px] border-none cursor-pointer transition-all duration-300 ease-in-out hover:-translate-y-0.5 active:scale-[0.98] shadow-[0_8px_15px_rgba(39,174,96,0.2)]"
        >
          Create Account
        </button>
      </form>

      <p class="text-center mt-[25px] text-[14px] text-[#636e72]">
        Already have an account? 
        <router-link to="/login" class="text-[#27ae60] font-bold no-underline hover:underline decoration-2">
          Log In
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
const confirmPassword = ref('')

const handleRegister = async () => {
  if (password.value !== confirmPassword.value) {
    alert("Passwords do not match!")
    return
  }

  if (password.value.length < 6) {
    alert("Password must be at least 6 characters long.")
    return
  }

  try {
    const response = await fetch('/api/auth/register', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ 
        email: email.value, 
        password: password.value 
      })
    })

    const result = await response.json()

    if (response.ok) {
      alert("Registration successful! Now you can log in.")
      router.push('/login')
    } else {
      alert("Registration failed: " + (result.message || "Unknown error"))
    }
  } catch (error) {
    alert("Could not connect to the server.")
  }
}
</script>