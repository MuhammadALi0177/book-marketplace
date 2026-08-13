<template>
  <div class="page">
    <h1 class="page-title">Xabarlar</h1>

    <div v-if="!loggedIn" class="auth-gate">
      <p>Xabarlarni ko'rish uchun tizimga kiring</p>
      <button type="button" class="submit-btn" @click="$emit('need-auth')">Kirish</button>
    </div>

    <div v-else-if="loading" class="empty-state" style="padding-top:48px">
      <p>Yuklanmoqda…</p>
    </div>

    <div v-else-if="!conversations.length" class="empty-state" style="padding-top:48px">
      <div class="empty-icon">💬</div>
      <p>Hali xabar yo'q</p>
      <p style="font-size:13px;margin-top:6px;color:var(--ink-3)">Kitob sahifasidan «Egasi bilan bog'lanish» bosing</p>
    </div>

    <div v-else class="msg-list">
      <div
        v-for="c in conversations"
        :key="c.id"
        class="msg-item"
        @click="$emit('open-chat', c)"
      >
        <div class="msg-avatar">{{ initials(c) }}</div>
        <div class="msg-body">
          <div class="msg-top">
            <span class="msg-name">{{ otherName(c) }}</span>
            <span class="msg-time">{{ formatTime(c.last_message?.created_at || c.updated_at) }}</span>
          </div>
          <div class="msg-book">{{ c.book?.title || "Kitob" }}</div>
          <div class="msg-preview">{{ c.last_message?.text || "Suhbat boshlandi" }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  loggedIn: { type: Boolean, default: false },
  conversations: { type: Array, default: () => [] },
  loading: { type: Boolean, default: false },
});
defineEmits(["need-auth", "open-chat"]);

function otherName(c) {
  return c.other_user?.full_name || c.other_user?.username || c.other_user?.phone || "Foydalanuvchi";
}
function initials(c) {
  return otherName(c)
    .split(" ")
    .map((w) => w[0])
    .join("")
    .slice(0, 2)
    .toUpperCase();
}
function formatTime(iso) {
  if (!iso) return "";
  const d = new Date(iso);
  const now = new Date();
  const sameDay = d.toDateString() === now.toDateString();
  if (sameDay) {
    return `${String(d.getHours()).padStart(2, "0")}:${String(d.getMinutes()).padStart(2, "0")}`;
  }
  const yesterday = new Date(now);
  yesterday.setDate(now.getDate() - 1);
  if (d.toDateString() === yesterday.toDateString()) return "Kecha";
  return `${d.getDate()}.${d.getMonth() + 1}`;
}
</script>
