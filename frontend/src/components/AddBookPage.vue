<template>
  <div class="page add-page">
    <h1 class="page-title">Kitob qo'shish</h1>
    <p class="page-sub">Kitobingizni boshqalarga taklif qiling</p>

    <div v-if="!loggedIn" class="auth-gate">
      <p>Kitob qo'shish uchun tizimga kiring</p>
      <button type="button" class="submit-btn" @click="$emit('need-auth')">Kirish</button>
    </div>

    <form v-else @submit.prevent="submit">
      <div class="photo-upload" @click="fileRef?.click()">
        <img v-if="preview" :src="preview" alt="" />
        <template v-else>
          <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
            <path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"/>
            <circle cx="12" cy="13" r="4"/>
          </svg>
          Rasm yuklash
        </template>
        <input
          ref="fileRef"
          type="file"
          accept="image/*,image/jpeg,image/png,image/webp"
          @change="onFile"
        />
      </div>

      <div class="form-field">
        <label>Kitob nomi *</label>
        <input v-model="form.title" required placeholder="Masalan: O'tkan kunlar" />
      </div>
      <div class="form-field">
        <label>Muallif *</label>
        <input v-model="form.author" required placeholder="Masalan: Abdulla Qodiriy" />
      </div>
      <div class="form-field">
        <label>Shahar</label>
        <select v-model="form.city" required>
          <option value="" disabled>Tanlang</option>
          <option v-for="c in cities" :key="c" :value="c">{{ c }}</option>
        </select>
      </div>
      <div class="form-field">
        <label>Taklif turi</label>
        <div class="type-pills">
          <button type="button" class="type-pill" :class="{ active: form.status === 'sale' }" @click="form.status = 'sale'">Sotish</button>
          <button type="button" class="type-pill" :class="{ active: form.status === 'rent' }" @click="form.status = 'rent'">Ijara</button>
          <button type="button" class="type-pill" :class="{ active: form.status === 'barter' }" @click="form.status = 'barter'">Barter</button>
        </div>
      </div>
      <div class="form-field" v-if="form.status !== 'barter'">
        <label>Narx (so'm)</label>
        <input v-model.number="form.price" type="number" min="0" placeholder="0" />
      </div>
      <div class="form-field">
        <label>Tavsif</label>
        <textarea v-model="form.description" placeholder="Kitob holati, xususiyatlari haqida..."></textarea>
      </div>

      <p v-if="error" class="auth-error">{{ error }}</p>
      <button type="submit" class="submit-btn" :disabled="loading">
        {{ loading ? "Yuklanmoqda…" : "Qo'shish" }}
      </button>
    </form>
  </div>
</template>

<script setup>
import { reactive, ref } from "vue";
import { apiAuthed, API_BASE, getToken } from "../api";

defineProps({
  cities: { type: Array, default: () => [] },
  loggedIn: { type: Boolean, default: false },
});
const emit = defineEmits(["need-auth", "added", "error"]);

const form = reactive({
  title: "",
  author: "",
  city: "",
  status: "sale",
  price: 0,
  description: "",
  photo_url: "",
});
const fileRef = ref(null);
const preview = ref("");
const file = ref(null);
const loading = ref(false);
const error = ref("");

function compressToJpeg(f, maxSide = 1280, quality = 0.8) {
  return new Promise((resolve, reject) => {
    const url = URL.createObjectURL(f);
    const img = new Image();
    img.onload = () => {
      URL.revokeObjectURL(url);
      let { width, height } = img;
      if (width > maxSide || height > maxSide) {
        if (width > height) {
          height = Math.round((height * maxSide) / width);
          width = maxSide;
        } else {
          width = Math.round((width * maxSide) / height);
          height = maxSide;
        }
      }
      const canvas = document.createElement("canvas");
      canvas.width = width;
      canvas.height = height;
      const ctx = canvas.getContext("2d");
      ctx.drawImage(img, 0, 0, width, height);
      canvas.toBlob(
        (blob) => {
          if (!blob) {
            reject(new Error("Rasm qayta ishlanmadi"));
            return;
          }
          resolve(new File([blob], "photo.jpg", { type: "image/jpeg" }));
        },
        "image/jpeg",
        quality
      );
    };
    img.onerror = () => {
      URL.revokeObjectURL(url);
      reject(new Error("Rasm ochilmadi. JPG/PNG tanlang"));
    };
    img.src = url;
  });
}

async function onFile(e) {
  const f = e.target.files?.[0];
  if (!f) return;
  error.value = "";
  try {
    preview.value = URL.createObjectURL(f);
    file.value = await compressToJpeg(f);
  } catch (err) {
    file.value = f;
    if (!preview.value) preview.value = URL.createObjectURL(f);
  }
}

async function submit() {
  error.value = "";
  loading.value = true;
  try {
    if (file.value) {
      const fd = new FormData();
      fd.append("file", file.value, file.value.name || "photo.jpg");
      const token = getToken();
      if (!token) throw new Error("Avval tizimga kiring");
      const upRes = await fetch(`${API_BASE}/api/upload`, {
        method: "POST",
        headers: { Authorization: `Bearer ${token}` },
        body: fd,
      });
      const up = await upRes.json().catch(() => ({}));
      if (!upRes.ok) {
        throw new Error(up.detail || `Rasm yuklanmadi (${upRes.status})`);
      }
      if (!up.photo_url) throw new Error("Rasm URL qaytmadi");
      form.photo_url = up.photo_url;
    }
    const payload = {
      title: form.title,
      author: form.author,
      city: form.city,
      status: form.status,
      price: form.status === "barter" ? null : form.price,
      description: form.description,
      photo_url: form.photo_url || null,
    };
    await apiAuthed("/api/books", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    emit("added");
    Object.assign(form, {
      title: "",
      author: "",
      city: "",
      status: "sale",
      price: 0,
      description: "",
      photo_url: "",
    });
    preview.value = "";
    file.value = null;
  } catch (e) {
    error.value = e.message || "Xatolik";
    emit("error", error.value);
  } finally {
    loading.value = false;
  }
}
</script>