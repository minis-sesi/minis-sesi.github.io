<script setup>
import { computed, onBeforeUnmount, ref, watch } from "vue";
import VisualizadorImagens from "../components/VisualizadorImagens.vue";
import { aulasDisponiveis } from "../data/conteudo";
import { usePdfPaginas } from "../composables/usePdfPaginas";

const props = defineProps({ id: { type: String, required: true } });

const aula = computed(() => aulasDisponiveis.find((a) => a.id === Number(props.id)));
const indice = computed(() => aulasDisponiveis.indexOf(aula.value));
const anterior = computed(() => aulasDisponiveis[indice.value - 1]);
const proxima = computed(() => aulasDisponiveis[indice.value + 1]);

// Se a aula não tiver imagens das páginas, gera a prévia a partir do PDF
const pdf = usePdfPaginas();
const paginas = computed(() => (aula.value?.paginas.length ? aula.value.paginas : pdf.paginas.value));

watch(
  aula,
  (a) => {
    pdf.limpar();
    if (!a) return;
    document.title = `Aula ${a.id}: ${a.titulo} | Mini S`;
    if (!a.paginas.length) pdf.gerar(a.pdf);
  },
  { immediate: true }
);

const visualizador = ref(null);
const imagensVisualizador = computed(() =>
  paginas.value.map((src, i) => ({ src, alt: `Página ${i + 1} de ${paginas.value.length}` }))
);
onBeforeUnmount(() => pdf.limpar());
</script>

<template>
  <div v-if="!aula" class="section">
    <div class="wrap">
      <h1>Aula não encontrada</h1>
      <p>Esse material ainda não foi publicado.</p>
      <RouterLink class="btn btn-primary" to="/aulas">Ver todas as aulas</RouterLink>
    </div>
  </div>

  <div v-else>
    <section class="mission-hero">
      <div class="wrap mission-grid" :class="{ 'sem-capa': !aula.capa && !paginas[0] }">
        <div>
          <nav class="breadcrumb" aria-label="Você está em">
            <RouterLink to="/">Início</RouterLink> › <RouterLink to="/aulas">Aulas</RouterLink> › <span>Aula {{ aula.id }}</span>
          </nav>
          <span class="eyebrow">Aula {{ aula.id }}<template v-if="aula.serie"> · {{ aula.serie }}</template></span>
          <h1>{{ aula.titulo }}</h1>
          <p>{{ aula.resumo }}</p>
          <div class="facts">
            <span v-if="aula.equipe" class="fact">Equipe: {{ aula.equipe }}</span>
            <span v-if="aula.modulo" class="fact">Módulo: {{ aula.modulo }}</span>
            <span v-if="aula.idade" class="fact">Idade: {{ aula.idade }}</span>
            <span v-if="aula.tempo" class="fact">Tempo: {{ aula.tempo }}</span>
            <span v-if="paginas.length" class="fact">{{ paginas.length }} páginas</span>
          </div>
          <div class="hero-actions">
            <a class="btn btn-primary" :href="aula.pdf" download>⬇ Baixar PDF para imprimir</a>
            <a class="btn btn-ghost" :href="aula.pdf" target="_blank" rel="noopener">Abrir PDF</a>
          </div>
        </div>
        <img v-if="aula.capa || paginas[0]" class="mission-cover" :src="aula.capa || paginas[0]" :alt="`Capa da aula ${aula.titulo}`" />
      </div>
    </section>

    <section class="section">
      <div class="wrap mission-body">
        <div>
          <div class="panel">
            <h2>Páginas do material</h2>
            <p v-if="pdf.carregando.value && !paginas.length" class="muted">Carregando a prévia das páginas…</p>
            <p v-else-if="pdf.erro.value && !paginas.length" class="muted">
              Não foi possível mostrar a prévia aqui. Use o botão “Abrir PDF” para ver o material.
            </p>
            <p v-else class="muted">Clique numa página para ampliar.</p>
            <div class="pages">
              <button v-for="(src, i) in paginas" :key="src" type="button" :aria-label="`Ampliar página ${i + 1}`" @click="visualizador.abrir(i)">
                <img :src="src" :alt="`Página ${i + 1}`" loading="lazy" />
              </button>
            </div>
          </div>

          <div v-if="aula.roteiro.length" class="panel">
            <h2>Roteiro da aula</h2>
            <ol class="roteiro">
              <li v-for="r in aula.roteiro" :key="r">{{ r }}</li>
            </ol>
          </div>

          <div class="panel">
            <h2>Vídeo de apoio</h2>
            <iframe
              v-if="aula.video"
              class="video"
              :src="`https://www.youtube-nocookie.com/embed/${aula.video}`"
              :title="`Vídeo da aula ${aula.id}`"
              allowfullscreen
              loading="lazy"
            />
            <div v-else class="empty-video">🎬 O vídeo explicativo desta aula será publicado em breve.</div>
          </div>
        </div>

        <aside class="aside">
          <div v-if="aula.objetivos.length" class="panel">
            <h2>Objetivos</h2>
            <ul>
              <li v-for="o in aula.objetivos" :key="o">{{ o }}</li>
            </ul>
          </div>
          <div v-if="aula.habilidades.length" class="panel">
            <h2>Habilidades</h2>
            <div class="tags">
              <span v-for="h in aula.habilidades" :key="h" class="tag">{{ h }}</span>
            </div>
          </div>
          <div v-if="aula.materiais.length" class="panel">
            <h2>Materiais</h2>
            <ul>
              <li v-for="m in aula.materiais" :key="m">{{ m }}</li>
            </ul>
          </div>
          <div class="pager">
            <RouterLink v-if="anterior" class="btn btn-ghost btn-dark btn-small" :to="`/aulas/${anterior.id}`">← Aula {{ anterior.id }}</RouterLink>
            <span v-else />
            <RouterLink v-if="proxima" class="btn btn-primary btn-small" :to="`/aulas/${proxima.id}`">Aula {{ proxima.id }} →</RouterLink>
          </div>
        </aside>
      </div>
    </section>

    <VisualizadorImagens ref="visualizador" :imagens="imagensVisualizador" />
  </div>
</template>
