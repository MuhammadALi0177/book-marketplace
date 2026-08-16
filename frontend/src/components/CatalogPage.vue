<template>
  <div class="page">
    <div class="brand-bar">
      <img class="brand-logo" src="/logo.svg" alt="KitobJavon" @error="($e)=>$e.target.style.display='none'" />
      <div class="brand-text">Kitob<span>Javon</span></div>
    </div>
    <div class="page-head">
      <div>
        <h1 class="page-title">Kitoblar</h1>
        <p class="page-sub">{{ loading ? 'Yuklanmoqda…' : (books.length + ' ta kitob topildi') }}</p>
      </div>
      <button type="button" class="filter-btn" @click="$emit('open-filters')">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"/>
        </svg>
        Filtr
        <span v-if="hasFilters" class="badge-dot"></span>
      </button>
    </div>

    <div class="search-wrap">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2">
        <circle cx="11" cy="11" r="7"/><path d="M21 21l-4.3-4.3"/>
      </svg>
      <input
        class="search-input"
        type="search"
        placeholder="Kitob nomi yoki muallif..."
        :value="search"
        @input="onSearch"
      />
    </div>

    <div v-if="city || status" class="active-filters">
      <span v-if="city" class="chip-active">
        {{ city }}
        <button type="button" @click="$emit('update:city', '')">×</button>
      </span>
      <span v-if="status" class="chip-active">
        {{ statusLabel }}
        <button type="button" @click="$emit('update:status', '')">×</button>
      </span>
    </div>

    <div class="book-grid">
      <template v-if="books.length">
        <BookCard
          v-for="b in books"
          :key="b.id"
          :book="b"
          :favored="favs.has(b.id)"
          @select="$emit('select', b)"
          @toggle-fav="$emit('toggle-fav', b)"
        />
      </template>
      <div v-else-if="loading" class="empty-state">
        <div class="empty-icon">⏳</div>
        <p>Yuklanmoqda…</p>
      </div>
      <div v-else class="empty-state">
        <div class="empty-icon">📖</div>
        <p>Kitob topilmadi</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from "vue";
import BookCard from "./BookCard.vue";

const props = defineProps({
  books: { type: Array, default: () => [] },
  search: { type: String, default: "" },
  city: { type: String, default: "" },
  status: { type: String, default: "" },
  favs: { type: Object, default: () => new Set() },
  loading: { type: Boolean, default: false },
});
const emit = defineEmits(["update:search", "update:city", "update:status", "select", "toggle-fav", "open-filters"]);

const hasFilters = computed(() => Boolean(props.city || props.status));
const statusLabel = computed(() => ({ sale: "Sotish", rent: "Ijara", barter: "Barter" }[props.status] || props.status));

let t;
function onSearch(e) {
  clearTimeout(t);
  t = setTimeout(() => emit("update:search", e.target.value.trim()), 350);
}
</script>