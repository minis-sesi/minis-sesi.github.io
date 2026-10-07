<script setup>
defineProps({
  eyebrow: String,
  titulo: { type: String, required: true },
  texto: String,
});
</script>

<template>
  <section class="page-header">
    <div class="wrap">
      <span v-if="eyebrow" class="eyebrow">{{ eyebrow }}</span>
      <h1>{{ titulo }}</h1>
      <p v-if="texto" class="lead">{{ texto }}</p>
      <slot />
    </div>
  </section>
</template>
