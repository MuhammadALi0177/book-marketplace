<template>
  <div class="chat-page">
    <div class="chat-header">
      <button type="button" class="back" @click="$emit('back')">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M15 18l-6-6 6-6"/></svg>
      </button>
      <div class="msg-avatar" style="width:40px;height:40px;font-size:14px">{{ initials }}</div>
      <div class="info">
        <div class="name">{{ name }}</div>
        <div class="sub">{{ bookTitle }}</div>
      </div>
    </div>

    <div class="chat-messages" ref="box">
      <div v-if="loading" style="text-align:center;color:var(--ink-3);padding:20px">Yuklanmoqda…</div>
      <div
        v-for="m in messages"
        :key="m.id"
        class="bubble"
        :class="m.sender_id === myId ? 'me' : 'them'"
      >
        {{ m.text }}
        <div class="time">{{ formatTime(m.created_at) }}</div>
      </div>
    </div>

    <form class="chat-input-bar" @submit.prevent="send">
      <input style="color: white;" v-model="text" placeholder="Xabar yozing..." :disabled="sending" />
      <button type="submit" class="chat-send" :disabled="!text.trim() || sending">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M22 2L11 13"/><path d="M22 2l-7 20-4-9-9-4 20-7z"/></svg>
      </button>
    </form>
  </div>
</template>

<script setup>
import { computed, nextTick, onMounted, onUnmounted, ref, watch } from "vue";
import { apiAuthed } from "../api";

const props = defineProps({
  conversation: { type: Object, required: true },
  myId: { type: Number, default: null },
});
defineEmits(["back"]);

const messages = ref([]);
const text = ref("");
const box = ref(null);
const loading = ref(true);
const sending = ref(false);
let pollTimer;

const name = computed(
  () =>
    props.conversation.other_user?.full_name ||
    props.conversation.other_user?.username ||
    props.conversation.other_user?.phone ||
    "Foydalanuvchi"
);
const initials = computed(() =>
  name.value
    .split(" ")
    .map((w) => w[0])
    .join("")
    .slice(0, 2)
    .toUpperCase()
);
const bookTitle = computed(() => props.conversation.book?.title || "");

onMounted(async () => {
  await loadMessages();
  pollTimer = setInterval(loadMessages, 4000);
});
onUnmounted(() => clearInterval(pollTimer));

watch(
  () => props.conversation.id,
  async () => {
    messages.value = [];
    await loadMessages();
  }
);

async function loadMessages() {
  try {
    const data = await apiAuthed(`/api/conversations/${props.conversation.id}/messages`);
    const prevLen = messages.value.length;
    messages.value = data;
    if (data.length !== prevLen) scrollBottom();
  } catch (e) {
    console.error(e);
  } finally {
    loading.value = false;
  }
}

function scrollBottom() {
  nextTick(() => {
    if (box.value) box.value.scrollTop = box.value.scrollHeight;
  });
}

async function send() {
  const t = text.value.trim();
  if (!t || sending.value) return;
  sending.value = true;
  try {
    const msg = await apiAuthed(`/api/conversations/${props.conversation.id}/messages`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text: t }),
    });
    messages.value.push(msg);
    text.value = "";
    scrollBottom();
  } catch (e) {
    alert(e.message || "Xabar yuborilmadi");
  } finally {
    sending.value = false;
  }
}

function formatTime(iso) {
  if (!iso) return "";
  const d = new Date(iso);
  return `${String(d.getHours()).padStart(2, "0")}:${String(d.getMinutes()).padStart(2, "0")}`;
}
</script>
