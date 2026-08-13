<template>
  <div class="page">
    <div class="subpage-head">
      <button type="button" class="back-btn" @click="$emit('back')">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M15 18l-6-6 6-6"/></svg>
      </button>
      <h1>Manzil</h1>
    </div>

    <p class="page-sub" style="margin-bottom:16px">Shaharingizni tanlang yoki o'zingiz yozing</p>

    <div class="form-field">
      <label>Shahar / tuman</label>
      <input
        v-model="city"
        list="city-list"
        placeholder="Masalan: Qo'qon, Andijon, Toshkent..."
      />
      <datalist id="city-list">
        <option v-for="c in cities" :key="c" :value="c" />
      </datalist>
    </div>

    <div class="chip-grid" style="margin-bottom:20px">
      <button
        v-for="c in popular"
        :key="c"
        type="button"
        class="chip"
        :class="{ selected: city === c }"
        @click="city = c"
      >
        {{ c }}
      </button>
    </div>

    <p v-if="error" class="auth-error">{{ error }}</p>
    <button type="button" class="submit-btn" :disabled="saving || !city.trim()" @click="save">
      {{ saving ? "Saqlanmoqda…" : "Saqlash" }}
    </button>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { apiAuthed } from "../api";

const props = defineProps({
  cities: { type: Array, default: () => [] },
  current: { type: String, default: "" },
});
const emit = defineEmits(["back", "saved", "error"]);

const city = ref(props.current || "");
const saving = ref(false);
const error = ref("");
const popular = ["Toshkent", "Andijon", "Samarqand", "Buxoro", "Namangan", "Farg'ona", "Qo'qon", "Nukus", "Qarshi", "Termiz"];

async function save() {
  error.value = "";
  saving.value = true;
  try {
    const updated = await apiAuthed("/api/profile/me", {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ city: city.value.trim() }),
    });
    emit("saved", updated);
  } catch (e) {
    error.value = e.message || "Saqlanmadi";
    emit("error", error.value);
  } finally {
    saving.value = false;
  }
}
</script>
