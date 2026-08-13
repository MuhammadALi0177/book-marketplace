<template>
  <div class="page">
    <h1 class="page-title">Profil</h1>

    <div v-if="!loggedIn" class="auth-gate">
      <p>Profilni ko'rish uchun tizimga kiring</p>
      <button type="button" class="submit-btn" @click="$emit('need-auth')">Kirish</button>
    </div>

    <template v-else>
      <div class="profile-card">
        <div class="profile-avatar">
          {{ initials }}
          <span class="online"></span>
        </div>
        <div class="profile-meta">
          <div class="name">{{ displayName }}</div>
          <div class="loc" v-if="profile?.city">📍 {{ profile.city }}</div>
          <div class="handle" v-if="profile?.phone">{{ profile.phone }}</div>
        </div>
      </div>

      <div class="profile-stats">
        <div class="stat-box">
          <div class="num">{{ myCount }}</div>
          <div class="lbl">E'lonlar</div>
        </div>
        <div class="stat-box">
          <div class="num">{{ soldCount }}</div>
          <div class="lbl">Sotilgan</div>
        </div>
        <div class="stat-box">
          <div class="num">4.8 ★</div>
          <div class="lbl">Reyting</div>
        </div>
      </div>

      <div class="menu-list">
        <div class="menu-item" @click="$emit('open-my-books')">
          <div class="menu-icon">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg>
          </div>
          <div class="menu-text">
            <div class="t">Mening kitoblarim</div>
            <div class="s">{{ myCount }} ta e'lon</div>
          </div>
          <svg class="menu-arrow" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 18l6-6-6-6"/></svg>
        </div>

        <div class="menu-item" @click="$emit('open-favorites')">
          <div class="menu-icon">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/></svg>
          </div>
          <div class="menu-text">
            <div class="t">Saqlangan kitoblar</div>
            <div class="s">{{ favCount }} ta kitob</div>
          </div>
          <svg class="menu-arrow" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 18l6-6-6-6"/></svg>
        </div>

        <div class="menu-item" @click="$emit('open-address')">
          <div class="menu-icon">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>
          </div>
          <div class="menu-text">
            <div class="t">Manzil</div>
            <div class="s">{{ profile?.city || "Qo'shish" }}</div>
          </div>
          <svg class="menu-arrow" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 18l6-6-6-6"/></svg>
        </div>

        <div class="menu-item" @click="$emit('open-settings')">
          <div class="menu-icon">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="3"/><path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"/></svg>
          </div>
          <div class="menu-text">
            <div class="t">Sozlamalar</div>
            <div class="s">Ism, nomer, parol</div>
          </div>
          <svg class="menu-arrow" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 18l6-6-6-6"/></svg>
        </div>
      </div>

      <button type="button" class="submit-btn" style="margin-top:20px;background:transparent;color:var(--primary);border:1.5px solid var(--primary);box-shadow:none" @click="$emit('logout')">
        Chiqish
      </button>
    </template>
  </div>
</template>

<script setup>
import { computed } from "vue";

const props = defineProps({
  loggedIn: { type: Boolean, default: false },
  profile: { type: Object, default: null },
  myCount: { type: Number, default: 0 },
  soldCount: { type: Number, default: 0 },
  favCount: { type: Number, default: 0 },
});
defineEmits(["need-auth", "logout", "open-my-books", "open-favorites", "open-address", "open-settings"]);

const displayName = computed(() => props.profile?.full_name || props.profile?.username || "Foydalanuvchi");
const initials = computed(() =>
  displayName.value.split(" ").map((w) => w[0]).join("").slice(0, 2).toUpperCase()
);
</script>
