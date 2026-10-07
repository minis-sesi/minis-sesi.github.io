<script setup>
import { computed, ref } from "vue";
import PageHeader from "../components/PageHeader.vue";
import AulaCard from "../components/AulaCard.vue";
import { aulas, aulasDisponiveis, equipesComAula, site } from "../data/conteudo";

const filtro = ref("todas");
const opcoes = [
  { id: "todas", label: "Todas" },
  { id: "disponiveis", label: "Disponíveis" },
  ...equipesComAula.map((e) => ({ id: e, label: e })),
];

const visiveis = computed(() => {
  if (filtro.value === "todas") return aulas;
  if (filtro.value === "disponiveis") return aulasDisponiveis;
  return aulasDisponiveis.filter((a) => a.equipe === filtro.value);
});
</script>

<template>
  <div>
    <PageHeader
      eyebrow="Aulas"
      titulo="Trilha de aulas do Mini S"
      :texto="`${site.totalEncontros} encontros planejados, cada um criado por uma das equipes de robótica. Siga a ordem, baixe o PDF e aplique com a sua turma.`"
    >
      <a v-if="site.materialCompleto" class="btn btn-primary" :href="site.materialCompleto" download>⬇ Baixar todo o material (PDF)</a>
    </PageHeader>

    <section class="section">
      <div class="wrap">
        <div class="filters" role="group" aria-label="Filtrar aulas">
          <button
            v-for="o in opcoes"
            :key="o.id"
            type="button"
            class="filter"
            :aria-pressed="filtro === o.id"
            @click="filtro = o.id"
          >
            {{ o.label }}
          </button>
        </div>

        <TransitionGroup name="list" tag="div" class="grid">
          <AulaCard v-for="a in visiveis" :key="a.id" :aula="a" />
        </TransitionGroup>
      </div>
    </section>
  </div>
</template>
