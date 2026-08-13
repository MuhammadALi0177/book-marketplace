<template>
  <div class="detail-page">
    <div class="detail-hero">
      <img v-if="photoSrc" :src="photoSrc" :alt="book.title" />
      <div v-else style="width:100%;height:100%;display:flex;align-items:center;justify-content:center;font-size:64px;background:linear-gradient(145deg,#E8D9C4,#D4C0A0)">📖</div>
      <div class="detail-top-btns">
        <button type="button" class="circle-btn" @click="$emit('close')">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M15 18l-6-6 6-6"/></svg>
        </button>
        <button type="button" class="circle-btn" @click="$emit('toggle-fav', book)">
          <svg width="18" height="18" viewBox="0 0 24 24" :fill="favored ? 'var(--primary)' : 'none'" stroke="currentColor" stroke-width="2" :style="{ color: favored ? 'var(--primary)' : undefined }">
            <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/>
          </svg>
        </button>
      </div>
    </div>

    <div class="detail-body">
      <span class="detail-badge" :class="book.status" :style="badgeStyle">{{ statusLabel }}</span>
      <h1 class="detail-title">{{ book.title }}</h1>
      <p class="detail-author">{{ book.author }}</p>

      <div class="detail-price-row">
        <div class="price-box">
          <div class="label">Narx</div>
          <div class="value">{{ priceText }}</div>
        </div>
        <div class="loc-box">
          <div class="label">Joylashuv</div>
          <div class="value">📍 {{ book.city }}</div>
        </div>
      </div>

      <div class="meta-chips">
        <div class="meta-chip">
          <div class="ml">Yil</div>
          <div class="mv">{{ year }}</div>
        </div>
        <div class="meta-chip">
          <div class="ml">Til</div>
          <div class="mv">O'zbek</div>
        </div>
        <div class="meta-chip">
          <div class="ml">Reyting</div>
          <div class="mv">4.8 ★</div>
        </div>
      </div>

      <div class="section-label">Tavsif</div>
      <p class="detail-desc">{{ book.description || "Tavsif kiritilmagan." }}</p>

      <div class="owner-card" v-if="book.owner">
        <div class="owner-avatar">{{ initials }}</div>
        <div class="owner-info">
          <div class="owner-role">Kitob egasi</div>
          <div class="owner-name">{{ ownerName }}</div>
        </div>
        <div class="owner-rating">★ 4.8</div>
      </div>
    </div>

    <div class="detail-cta">
      <button type="button" @click="$emit('contact', book)">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>
        Egasi bilan bog'lanish
      </button>
    </div>
  </div>
</template>

<script setup>
import { computed } from "vue";
import { API_BASE } from "../api";

const props = defineProps({
  book: { type: Object, required: true },
  favored: { type: Boolean, default: false },
});
defineEmits(["close", "toggle-fav", "contact"]);

const photoSrc = computed(() => {
  const u = props.book.photo_url || "";
  if (!u) return "";
  return u.startsWith("http") ? u : `${API_BASE}${u}`;
});
const statusLabel = computed(() => ({ sale: "SOTISH", rent: "IJARA", barter: "BARTER" }[props.book.status] || ""));
const badgeStyle = computed(() => {
  const map = { sale: "var(--sale)", rent: "var(--rent)", barter: "var(--barter)" };
  return { background: map[props.book.status] || "var(--primary)" };
});
const priceText = computed(() => {
  if (props.book.status === "barter") return "Barter";
  if (props.book.price == null) return "—";
  return Number(props.book.price).toLocaleString("uz-UZ") + " so'm";
});
const year = computed(() => {
  if (!props.book.created_at) return "—";
  return new Date(props.book.created_at).getFullYear();
});
const ownerName = computed(() => props.book.owner?.full_name || props.book.owner?.username || "Sotuvchi");
const initials = computed(() => {
  const n = ownerName.value;
  return n.split(" ").map((w) => w[0]).join("").slice(0, 2).toUpperCase();
});
</script>
