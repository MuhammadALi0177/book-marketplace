<template>
  <div class="sheet-overlay" @click.self="$emit('close')">
    <div class="sheet">
      <div class="sheet-handle"></div>
      <div class="sheet-head">
        <h2>Filtrlar</h2>
        <button type="button" class="sheet-reset" @click="reset">Tozalash</button>
      </div>

      <div class="filter-label">Shahar</div>
      <div class="chip-grid">
        <button
          v-for="c in cities"
          :key="c"
          type="button"
          class="chip"
          :class="{ selected: local.city === c }"
          @click="local.city = local.city === c ? '' : c"
        >
          {{ c }}
        </button>
      </div>

      <div class="filter-label">Holat</div>
      <div class="chip-grid">
        <button
          v-for="s in statuses"
          :key="s.value"
          type="button"
          class="chip"
          :class="{ selected: local.status === s.value }"
          @click="local.status = local.status === s.value ? '' : s.value"
        >
          {{ s.label }}
        </button>
      </div>

      <button type="button" class="sheet-apply" @click="apply">Qo'llash</button>
    </div>
  </div>
</template>

<script setup>
import { reactive, watch } from "vue";

const props = defineProps({
  cities: { type: Array, default: () => [] },
  city: { type: String, default: "" },
  status: { type: String, default: "" },
});
const emit = defineEmits(["close", "apply"]);

const local = reactive({ city: props.city, status: props.status });
watch(
  () => [props.city, props.status],
  () => {
    local.city = props.city;
    local.status = props.status;
  }
);

const statuses = [
  { value: "sale", label: "Sotish" },
  { value: "rent", label: "Ijara" },
  { value: "barter", label: "Barter" },
];

function reset() {
  local.city = "";
  local.status = "";
}
function apply() {
  emit("apply", { city: local.city, status: local.status });
  emit("close");
}
</script>
