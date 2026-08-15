<template>
  <AuthPage v-if="view === 'auth'" @back="view = 'main'" @success="onAuthSuccess" />

  <BookDetail
    v-else-if="view === 'detail' && selectedBook"
    :book="selectedBook"
    :favored="favIds.has(selectedBook.id)"
    @close="view = 'main'"
    @toggle-fav="toggleFav"
    @contact="onContact"
  />

  <ChatPage
    v-else-if="view === 'chat' && activeConv"
    :conversation="activeConv"
    :my-id="profile?.id"
    @back="view = 'main'; tab = 'messages'; loadConversations()"
  />

  <div v-else class="app-shell">
    <BottomNav :tab="tab" :msg-count="conversations.length" @navigate="onNavigate" />

    <div class="main-content">
      <CatalogPage
        v-show="tab === 'catalog' && !subPage"
        :books="books"
        :search="filters.search"
        :city="filters.city"
        :status="filters.status"
        :favs="favIds"
        @update:search="filters.search = $event"
        @update:city="filters.city = $event"
        @update:status="filters.status = $event"
        @select="openDetail"
        @toggle-fav="toggleFav"
        @open-filters="showFilters = true"
      />

      <AddBookPage
        v-show="tab === 'add' && !subPage"
        :cities="cities"
        :logged-in="loggedIn"
        @need-auth="view = 'auth'"
        @added="onBookAdded"
        @error="showToast"
      />

      <MessagesPage
        v-show="tab === 'messages' && !subPage"
        :logged-in="loggedIn"
        :conversations="conversations"
        :loading="convLoading"
        @need-auth="view = 'auth'"
        @open-chat="openChat"
      />

      <ProfilePage
        v-show="tab === 'profile' && !subPage"
        :logged-in="loggedIn"
        :profile="profile"
        :my-count="myCount"
        :sold-count="0"
        :fav-count="favIds.size"
        @need-auth="view = 'auth'"
        @logout="handleLogout"
        @open-my-books="subPage = 'my-books'"
        @open-favorites="subPage = 'favorites'"
        @open-address="subPage = 'address'"
        @open-settings="subPage = 'settings'"
      />

      <MyBooksPage
        v-if="subPage === 'my-books'"
        @back="subPage = null; refreshMyCount()"
        @deleted="onBookDeleted"
        @error="showToast"
      />

      <FavoritesPage
        v-if="subPage === 'favorites'"
        :books="favBooks"
        @back="subPage = null"
        @select="openDetail"
        @toggle-fav="toggleFav"
      />

      <AddressPage
        v-if="subPage === 'address'"
        :cities="cities"
        :current="profile?.city || ''"
        @back="subPage = null"
        @saved="onAddressSaved"
        @error="showToast"
      />

      <SettingsPage
        v-if="subPage === 'settings'"
        :profile="profile"
        :cities="cities"
        :dark="dark"
        @back="subPage = null"
        @saved="onSettingsSaved"
        @error="showToast"
        @toggle-theme="toggleTheme"
      />
    </div>

    <FilterSheet
      v-if="showFilters"
      :cities="cities"
      :city="filters.city"
      :status="filters.status"
      @close="showFilters = false"
      @apply="onFilterApply"
    />

    <Toast :message="toastMsg" />
  </div>
</template>

<script setup>
import { computed, onMounted, reactive, ref, watch } from "vue";
import CatalogPage from "./components/CatalogPage.vue";
import AddBookPage from "./components/AddBookPage.vue";
import MessagesPage from "./components/MessagesPage.vue";
import ProfilePage from "./components/ProfilePage.vue";
import MyBooksPage from "./components/MyBooksPage.vue";
import FavoritesPage from "./components/FavoritesPage.vue";
import AddressPage from "./components/AddressPage.vue";
import SettingsPage from "./components/SettingsPage.vue";
import BookDetail from "./components/BookDetail.vue";
import ChatPage from "./components/ChatPage.vue";
import AuthPage from "./components/AuthPage.vue";
import BottomNav from "./components/BottomNav.vue";
import FilterSheet from "./components/FilterSheet.vue";
import Toast from "./components/Toast.vue";
import { apiAuthed, apiGet, apiLogout, isLoggedIn } from "./api";

const view = ref("main");
const tab = ref("catalog");
const subPage = ref(null);
const books = ref([]);
const myCount = ref(0);
const cities = ref([]);
const filters = reactive({ city: "", status: "", search: "" });
const selectedBook = ref(null);
const profile = ref(null);
const loggedIn = ref(isLoggedIn());
const showFilters = ref(false);
const toastMsg = ref("");
const favIds = ref(new Set(JSON.parse(localStorage.getItem("kj_favs") || "[]")));
const conversations = ref([]);
const convLoading = ref(false);
const activeConv = ref(null);
const dark = ref(localStorage.getItem("kj_theme") === "dark");
let toastTimer;

const favBooks = computed(() => books.value.filter((b) => favIds.value.has(b.id)));

function applyTheme() {
  document.documentElement.classList.toggle("dark", dark.value);
  localStorage.setItem("kj_theme", dark.value ? "dark" : "light");
  const meta = document.querySelector('meta[name="theme-color"]');
  if (meta) meta.content = dark.value ? "#0B1220" : "#2563EB";
}

function toggleTheme() {
  dark.value = !dark.value;
  applyTheme();
}

onMounted(async () => {
  applyTheme();
  await loadCities();
  await loadBooks();
 if (loggedIn.value) {
  try {
    profile.value = await apiAuthed("/api/profile/me");
    await refreshMyCount();
    await loadConversations();
  } catch {
    apiLogout();
    loggedIn.value = false;
    profile.value = null;
  }
}
});

watch(filters, () => loadBooks(), { deep: true });
watch(tab, (t) => {
  subPage.value = null;
  if (t === "messages" && loggedIn.value) loadConversations();
});

async function loadCities() {
  try {
    cities.value = await apiGet("/api/cities");
  } catch {
    cities.value = [
      "Toshkent", "Andijon", "Samarqand", "Buxoro", "Namangan", "Farg'ona",
      "Qo'qon", "Nukus", "Qarshi", "Termiz", "Jizzax", "Navoiy",
    ];
  }
}

async function loadBooks() {
  const params = new URLSearchParams();
  if (filters.city) params.set("city", filters.city);
  if (filters.status) params.set("status", filters.status);
  if (filters.search) params.set("search", filters.search);
  try {
    books.value = await apiGet(`/api/books?${params.toString()}`);
  } catch {
    showToast("Kitoblarni yuklashda xatolik");
  }
}

async function refreshMyCount() {
  if (!loggedIn.value) return;
  try {
    const list = await apiAuthed("/api/books/mine/list");
    myCount.value = list.length;
  } catch {
    myCount.value = 0;
  }
}

async function loadConversations() {
  if (!loggedIn.value) return;
  convLoading.value = true;
  try {
    conversations.value = await apiAuthed("/api/conversations");
  } catch {
    conversations.value = [];
  } finally {
    convLoading.value = false;
  }
}

function onNavigate(t) {
  tab.value = t;
  view.value = "main";
  subPage.value = null;
}

function onFilterApply({ city, status }) {
  filters.city = city;
  filters.status = status;
}

function openDetail(book) {
  selectedBook.value = book;
  view.value = "detail";
  window.scrollTo(0, 0);
}

function toggleFav(book) {
  const s = new Set(favIds.value);
  if (s.has(book.id)) s.delete(book.id);
  else s.add(book.id);
  favIds.value = s;
  localStorage.setItem("kj_favs", JSON.stringify([...s]));
}

async function onContact(book) {
  if (!loggedIn.value) {
    view.value = "auth";
    return;
  }
  try {
    const conv = await apiAuthed("/api/conversations", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ book_id: book.id }),
    });
    activeConv.value = conv;
    view.value = "chat";
  } catch (e) {
    showToast(e.message || "Suhbat ochilmadi");
  }
}

function openChat(conv) {
  activeConv.value = conv;
  view.value = "chat";
}

function onAuthSuccess(data) {
  loggedIn.value = true;
  profile.value = data.user;
  view.value = "main";
  showToast("Xush kelibsiz!");
  refreshMyCount();
  loadConversations();
}

function handleLogout() {
  apiLogout();
  loggedIn.value = false;
  profile.value = null;
  myCount.value = 0;
  conversations.value = [];
  showToast("Tizimdan chiqdingiz");
}

function onBookAdded() {
  showToast("Kitob qo'shildi ✅");
  tab.value = "catalog";
  loadBooks();
  refreshMyCount();
}

function onBookDeleted() {
  showToast("E'lon o'chirildi");
  loadBooks();
  refreshMyCount();
}

function onAddressSaved(updated) {
  profile.value = updated;
  subPage.value = null;
  showToast("Manzil saqlandi ✅");
}

function onSettingsSaved(updated) {
  profile.value = updated;
  showToast("Profil saqlandi ✅");
}

function showToast(msg) {
  toastMsg.value = msg;
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => (toastMsg.value = ""), 2500);
}
</script>
