<template>
  <nav class="bottom-nav">
    <button type="button" class="nav-item" :class="{ active: tab === 'catalog' }" @click="$emit('navigate', 'catalog')">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/>
      </svg>
      Katalog
    </button>

    <div class="nav-add-wrap">
      <button type="button" class="nav-add" aria-label="Qo'shish" @click="$emit('navigate', 'add')">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round">
          <path d="M12 5v14M5 12h14"/>
        </svg>
      </button>
      <span class="nav-add-label">Qo'shish</span>
    </div>

    <button type="button" class="nav-item" :class="{ active: tab === 'messages' }" @click="$emit('navigate', 'messages')">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
      </svg>
      <span v-if="msgCount" class="nav-badge">{{ msgCount }}</span>
      Xabarlar
    </button>

    <button type="button" class="nav-item" :class="{ active: tab === 'profile' }" @click="$emit('navigate', 'profile')">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/>
      </svg>
      Profil
    </button>
  </nav>
</template>

<script setup>
defineProps({
  tab: { type: String, default: "catalog" },
  msgCount: { type: Number, default: 0 },
});
defineEmits(["navigate"]);
</script>
