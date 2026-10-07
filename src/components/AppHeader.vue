<script setup>
import { ref, watch } from "vue";
import { useRoute } from "vue-router";

const links = [
  { to: "/", label: "Início" },
  { to: "/quem-somos", label: "Quem somos" },
  { to: "/sobre", label: "Sobre" },
  { to: "/aulas", label: "Aulas" },
  { to: "/contatos", label: "Contatos" },
];

const aberto = ref(false);
const route = useRoute();
watch(() => route.fullPath, () => (aberto.value = false));
</script>

<template>
  <header class="topbar">
    <div class="wrap topbar-inner">
      <RouterLink class="brand" to="/">
        <img src="img/logo-mini-s.jpg" alt="" width="40" height="40" />
        <span>Mini S</span>
      </RouterLink>

      <button
        class="menu-btn"
        :aria-expanded="aberto"
        aria-controls="menu-principal"
        :aria-label="aberto ? 'Fechar menu' : 'Abrir menu'"
        @click="aberto = !aberto"
      >
        <span aria-hidden="true">{{ aberto ? "✕" : "☰" }}</span>
      </button>

      <nav id="menu-principal" class="nav" :class="{ open: aberto }" aria-label="Menu principal">
        <RouterLink
          v-for="l in links"
          :key="l.to"
          :to="l.to"
          :class="{ ativo: l.to === '/' ? route.path === '/' : route.path.startsWith(l.to) }"
        >
          {{ l.label }}
        </RouterLink>
        <RouterLink class="btn btn-primary btn-small nav-cta" to="/aulas">Baixar aulas</RouterLink>
      </nav>
    </div>
  </header>
</template>
