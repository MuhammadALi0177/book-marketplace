<template>
  <div class="page">
    <div class="subpage-head">
      <button type="button" class="back-btn" @click="$emit('back')">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M15 18l-6-6 6-6"/></svg>
      </button>
      <h1>Saqlangan kitoblar</h1>
    </div>

    <div v-if="!books.length" class="empty-state">
      <div class="empty-icon">❤️</div>
      <p>Saqlangan kitob yo'q</p>
    </div>
    <div v-else class="book-grid">
      <BookCard
        v-for="b in books"
        :key="b.id"
        :book="b"
        :favored="true"
        @select="$emit('select', b)"
        @toggle-fav="$emit('toggle-fav', b)"
      />
    </div>
  </div>
</template>

<script setup>
import BookCard from "./BookCard.vue";
defineProps({ books: { type: Array, default: () => [] } });
defineEmits(["back", "select", "toggle-fav"]);
</script>
