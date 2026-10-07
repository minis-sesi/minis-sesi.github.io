<script setup>
import AppHeader from "./components/AppHeader.vue";
import AppFooter from "./components/AppFooter.vue";
</script>

<template>
  <a class="skip-link" href="#conteudo">Pular para o conteúdo</a>
  <AppHeader />
  <main id="conteudo" tabindex="-1">
    <RouterView v-slot="{ Component }">
      <Transition name="fade" mode="out-in">
        <component :is="Component" />
      </Transition>
    </RouterView>
  </main>
  <AppFooter />
</template>
