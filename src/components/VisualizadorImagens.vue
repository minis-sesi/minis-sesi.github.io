<script setup>
import { computed, onBeforeUnmount, onMounted, ref } from "vue";

/*
 * Visualizador em tela cheia (páginas das aulas e fotos da galeria).
 * A imagem sempre cabe inteira na tela; clicar nela amplia para leitura.
 */
const props = defineProps({
  // [{ src, alt, legenda? }]
  imagens: { type: Array, required: true },
});

const dialogo = ref(null);
const atual = ref(0);
const zoom = ref(false);
const imagem = computed(() => props.imagens[atual.value]);
const varias = computed(() => props.imagens.length > 1);

function abrir(i = 0) {
  atual.value = i;
  zoom.value = false;
  dialogo.value.showModal();
}
function fechar() {
  dialogo.value.close();
}
function mover(passo) {
  const total = props.imagens.length;
  atual.value = (atual.value + passo + total) % total;
  zoom.value = false;
}
function teclas(ev) {
  if (!dialogo.value?.open || !varias.value) return;
  if (ev.key === "ArrowRight") mover(1);
  if (ev.key === "ArrowLeft") mover(-1);
}
onMounted(() => document.addEventListener("keydown", teclas));
onBeforeUnmount(() => document.removeEventListener("keydown", teclas));

defineExpose({ abrir });
</script>

<template>
  <dialog ref="dialogo" class="viewer" aria-label="Visualizador de imagens">
    <template v-if="imagem">
      <div class="viewer-bar">
        <span class="viewer-info">
          <template v-if="varias">{{ atual + 1 }} / {{ imagens.length }}</template>
          <template v-if="imagem.legenda"> · {{ imagem.legenda }}</template>
        </span>
        <div class="viewer-actions">
          <button type="button" :aria-pressed="zoom" @click="zoom = !zoom">{{ zoom ? "Ajustar à tela" : "🔍 Ampliar" }}</button>
          <button type="button" aria-label="Fechar" @click="fechar">✕</button>
        </div>
      </div>

      <div class="viewer-stage" :class="{ zoom }" @click.self="fechar">
        <img :key="imagem.src" :src="imagem.src" :alt="imagem.alt" @click="zoom = !zoom" />
      </div>

      <div v-if="varias" class="viewer-nav">
        <button type="button" @click="mover(-1)">← Anterior</button>
        <button type="button" @click="mover(1)">Próxima →</button>
      </div>
    </template>
  </dialog>
</template>
