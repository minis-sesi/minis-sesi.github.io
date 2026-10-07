<script setup>
import { computed, ref } from "vue";
import VisualizadorImagens from "./VisualizadorImagens.vue";
import { galeria } from "../data/conteudo";

const props = defineProps({ limite: { type: Number, default: 0 } });

const fotos = computed(() => (props.limite ? galeria.slice(0, props.limite) : galeria));
const imagens = computed(() =>
  fotos.value.map((f) => ({ src: f.imagem, alt: f.legenda || "Foto de um encontro do Mini S", legenda: f.legenda }))
);
const visualizador = ref(null);
</script>

<template>
  <div v-if="galeria.length" class="gallery">
    <button
      v-for="(f, i) in fotos"
      :key="f.imagem"
      type="button"
      class="gallery-item"
      :aria-label="`Ampliar foto: ${f.legenda || 'Mini S'}`"
      @click="visualizador.abrir(i)"
    >
      <img :src="f.imagem" :alt="f.legenda || 'Foto de um encontro do Mini S'" loading="lazy" />
      <span v-if="f.legenda" class="gallery-caption">{{ f.legenda }}</span>
    </button>
  </div>

  <VisualizadorImagens ref="visualizador" :imagens="imagens" />
</template>
