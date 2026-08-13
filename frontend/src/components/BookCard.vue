<template>
  <article class="book-card" @click="$emit('select', book)">
    <div class="book-cover">
      <img v-if="book.photo_url" :src="photoSrc" :alt="book.title" />
      <div v-else class="book-cover-placeholder">📖</div>
      <span class="card-badge" :class="book.status">{{ statusLabel }}</span>
      <button type="button" class="card-fav" :class="{ active: favored }" @click.stop="$emit('toggle-fav', book)">
        <svg width="16" height="16" viewBox="0 0 24 24" :fill="favored ? 'currentColor' : 'none'" stroke="currentColor" stroke-width="2">
          <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/>
        </svg>
      </button>
    </div>
    <div class="book-info">
      <div class="book-title">{{ book.title }}</div>
      <div class="book-author">{{ book.author }}</div>
      <div class="book-meta-row">
        <svg class="loc-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>
        <span>{{ book.city }}</span>
        <span class="price" v-if="book.status === 'barter'">Barter</span>
        <span class="price" v-else>{{ formatPrice(book.price) }}</span>
      </div>
    </div>
  </article>
</template>

<script setup>
import { computed } from "vue";
import { API_BASE } from "../api";

const props = defineProps({
  book: { type: Object, required: true },
  favored: { type: Boolean, default: false },
});
defineEmits(["select", "toggle-fav"]);

const photoSrc = computed(() => {
  const u = props.book.photo_url || "";
  if (u.startsWith("http")) return u;
  return `${API_BASE}${u}`;
});

const statusLabel = computed(() =>
  ({ sale: "SOTISH", rent: "IJARA", barter: "BARTER" }[props.book.status] || props.book.status)
);

function formatPrice(n) {
  if (n == null || n === "") return "—";
  return Number(n).toLocaleString("uz-UZ") + " so'm";
}
</script>
