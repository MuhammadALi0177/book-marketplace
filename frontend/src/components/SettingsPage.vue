<template>
  <div class="page settings-page">
    <div class="subpage-head">
      <button type="button" class="back-btn" @click="$emit('back')">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M15 18l-6-6 6-6"/></svg>
      </button>
      <h1>Sozlamalar</h1>
    </div>

    <p class="page-sub" style="margin-bottom:18px">Ism, telefon, parol va ko'rinish</p>

    <div class="theme-row" @click="$emit('toggle-theme')">
      <div class="theme-row-left">
        <div class="menu-icon" style="width:40px;height:40px;border-radius:12px;background:var(--primary-soft);color:var(--primary);display:flex;align-items:center;justify-content:center">
          <svg v-if="dark" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M4.93 19.07l1.41-1.41M17.66 6.34l1.41-1.41"/>
          </svg>
          <svg v-else width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/>
          </svg>
        </div>
        <div>
          <div style="font-weight:700;font-size:15px">Ko'rinish</div>
          <div style="font-size:12.5px;color:var(--ink-3)">{{ dark ? "Qorong'u rejim" : "Yorug' rejim" }}</div>
        </div>
      </div>
      <div class="theme-switch" :class="{ on: dark }">
        <span class="theme-knob"></span>
      </div>
    </div>

    <div style="height:1px;background:var(--border);margin:20px 0"></div>

    <form @submit.prevent="saveProfile">
      <div class="form-field">
        <label>Ism-familiya</label>
        <input v-model="form.full_name" type="text" placeholder="Masalan: Aziz Karimov" />
      </div>
      <div class="form-field">
        <label>Telefon raqam</label>
        <input v-model="form.phone" type="tel" inputmode="tel" placeholder="+998 90 123 45 67" />
      </div>
      <div class="form-field">
        <label>Shahar</label>
        <input v-model="form.city" type="text" list="set-cities" placeholder="Toshkent, Andijon..." />
        <datalist id="set-cities">
          <option v-for="c in cities" :key="c" :value="c" />
        </datalist>
      </div>
      <p v-if="profileError" class="auth-error">{{ profileError }}</p>
      <button type="submit" class="submit-btn" :disabled="savingProfile">
        {{ savingProfile ? "Saqlanmoqda…" : "Profilni saqlash" }}
      </button>
    </form>

    <div style="height:1px;background:var(--border);margin:28px 0"></div>

    <h2 style="font-family:var(--font-display);font-size:18px;margin-bottom:12px">Parolni o'zgartirish</h2>
    <form @submit.prevent="savePassword">
      <div class="form-field">
        <label>Yangi parol</label>
        <input v-model="pass.password" type="password" minlength="4" placeholder="Kamida 4 belgi" required />
      </div>
      <div class="form-field">
        <label>Parolni tasdiqlang</label>
        <input v-model="pass.confirm" type="password" minlength="4" placeholder="Qayta kiriting" required />
      </div>
      <p v-if="passError" class="auth-error">{{ passError }}</p>
      <button type="submit" class="submit-btn" :disabled="savingPass">
        {{ savingPass ? "Saqlanmoqda…" : "Parolni saqlash" }}
      </button>
    </form>
  </div>
</template>

<script setup>
import { reactive, ref } from "vue";
import { apiAuthed } from "../api";

const props = defineProps({
  profile: { type: Object, default: null },
  cities: { type: Array, default: () => [] },
  dark: { type: Boolean, default: false },
});
const emit = defineEmits(["back", "saved", "error", "toggle-theme"]);

const form = reactive({
  full_name: props.profile?.full_name || "",
  phone: props.profile?.phone || "+998",
  city: props.profile?.city || "",
});
const pass = reactive({ password: "", confirm: "" });
const savingProfile = ref(false);
const savingPass = ref(false);
const profileError = ref("");
const passError = ref("");

async function saveProfile() {
  profileError.value = "";
  savingProfile.value = true;
  try {
    const updated = await apiAuthed("/api/profile/me", {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        full_name: form.full_name.trim(),
        phone: form.phone.trim(),
        city: form.city.trim(),
      }),
    });
    emit("saved", updated);
  } catch (e) {
    profileError.value = e.message || "Saqlanmadi";
    emit("error", profileError.value);
  } finally {
    savingProfile.value = false;
  }
}

async function savePassword() {
  passError.value = "";
  if (pass.password !== pass.confirm) {
    passError.value = "Parollar mos kelmadi";
    return;
  }
  if (pass.password.length < 4) {
    passError.value = "Parol kamida 4 belgi bo'lishi kerak";
    return;
  }
  savingPass.value = true;
  try {
    await apiAuthed("/api/profile/password", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ password: pass.password }),
    });
    pass.password = "";
    pass.confirm = "";
    emit("error", "Parol yangilandi ✅");
  } catch (e) {
    passError.value = e.message || "Parol saqlanmadi";
  } finally {
    savingPass.value = false;
  }
}
</script>