<template>
  <div class="page">
    <div class="subpage-head">
      <button type="button" class="back-btn" @click="$emit('back')">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M15 18l-6-6 6-6"/></svg>
      </button>
      <h1>Mening kitoblarim</h1>
    </div>

    <div v-if="loading" class="empty-state"><p>Yuklanmoqda…</p></div>
    <div v-else-if="!books.length" class="empty-state">
      <div class="empty-icon">📖</div>
      <p>Hali e'lon yo'q</p>
    </div>
    <div v-else>
      <div v-for="b in books" :key="b.id" class="my-book-row">
        <img
          v-if="b.photo_url"
          class="my-book-thumb"
          :src="photo(b)"
          alt=""
        />
        <div v-else class="my-book-thumb" style="display:flex;align-items:center;justify-content:center;font-size:24px">📖</div>
        <div class="my-book-info">
          <div class="t">{{ b.title }}</div>
          <div class="s">{{ b.author }} · {{ statusLabel(b.status) }} · {{ b.city }}</div>
        </div>
        <button type="button" class="btn-delete" :disabled="deleting === b.id" @click="remove(b)">
          {{ deleting === b.id ? "…" : "O'chirish" }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from "vue";
import { apiAuthed, API_BASE } from "../api";

const emit = defineEmits(["back", "deleted", "error"]);
const books = ref([]);
const loading = ref(true);
const deleting = ref(null);

onMounted(load);

async function load() {
  loading.value = true;
  try {
    books.value = await apiAuthed("/api/books/mine/list");
  } catch (e) {
    emit("error", e.message);
  } finally {
    loading.value = false;
  }
}

function photo(b) {
  const u = b.photo_url || "";
  return u.startsWith("http") ? u : `${API_BASE}${u}`;
}
function statusLabel(s) {
  return { sale: "Sotish", rent: "Ijara", barter: "Barter" }[s] || s;
}

async function remove(b) {
  if (!confirm(`"${b.title}" e'lonini o'chirasizmi?`)) return;
  deleting.value = b.id;
  try {
    await apiAuthed(`/api/books/${b.id}`, { method: "DELETE" });
    books.value = books.value.filter((x) => x.id !== b.id);
    emit("deleted");
  } catch (e) {
    emit("error", e.message || "O'chirib bo'lmadi");
  } finally {
    deleting.value = null;
  }
}
</script>
