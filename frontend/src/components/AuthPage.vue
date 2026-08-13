<template>
  <div class="auth-page">
    <button type="button" class="auth-back" @click="$emit('back')">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M15 18l-6-6 6-6"/></svg>
      Orqaga
    </button>

    <div class="auth-logo-row">
      <div class="auth-logo">KJ</div>
      <div>
        <div style="font-family:var(--font-display);font-weight:700;font-size:18px">KitobJavon</div>
        <div style="font-size:12.5px;color:var(--ink-3)">Kitob bozori</div>
      </div>
    </div>

    <h1 class="auth-title">{{ mode === 'login' ? 'Xush kelibsiz' : 'Hisob ochish' }}</h1>
    <p class="auth-sub">{{ mode === 'login' ? 'Telefon va parol bilan kiring' : 'Bir necha soniyada ro\'yxatdan o\'ting' }}</p>

    <div class="auth-tabs">
      <button type="button" class="auth-tab" :class="{ active: mode === 'login' }" @click="mode = 'login'; error = ''">Kirish</button>
      <button type="button" class="auth-tab" :class="{ active: mode === 'register' }" @click="mode = 'register'; error = ''">Ro'yxat</button>
    </div>

    <form @submit.prevent="submit">
      <div class="form-field" v-if="mode === 'register'">
        <label>Ism-familiya</label>
        <input v-model="form.full_name" placeholder="Aziz Karimov" />
      </div>
      <div class="form-field">
        <label>Telefon raqam</label>
        <input
          v-model="form.phone"
          type="tel"
          required
          inputmode="tel"
          placeholder="+998 90 123 45 67"
          @focus="onPhoneFocus"
        />
      </div>
      <div class="form-field">
        <label>Parol</label>
        <input v-model="form.password" type="password" required minlength="4" placeholder="Kamida 4 belgi" />
      </div>
      <p v-if="error" class="auth-error">{{ error }}</p>
      <button type="submit" class="submit-btn" :disabled="loading">
        {{ loading ? 'Kuting…' : (mode === 'login' ? 'Kirish' : "Ro'yxatdan o'tish") }}
      </button>
    </form>
  </div>
</template>

<script setup>
import { reactive, ref } from "vue";
import { apiLogin, apiRegister } from "../api";

const emit = defineEmits(["back", "success"]);
const mode = ref("login");
const form = reactive({ full_name: "", phone: "+998", password: "" });
const loading = ref(false);
const error = ref("");

async function submit() {
  error.value = "";
  loading.value = true;
  try {
    const data =
      mode.value === "login"
        ? await apiLogin({ phone: form.phone, password: form.password })
        : await apiRegister({ phone: form.phone, password: form.password, full_name: form.full_name });
    emit("success", data);
  } catch (e) {
    error.value = e.message || "Xatolik";
  } finally {
    loading.value = false;
  }
}
</script>
