<script setup>
defineProps({ aula: { type: Object, required: true } });
</script>

<template>
  <RouterLink v-if="aula.status === 'disponivel'" class="card" :to="`/aulas/${aula.id}`">
    <div class="card-cover">
      <img v-if="aula.capa" :src="aula.capa" :alt="`Capa da aula ${aula.id}: ${aula.titulo}`" loading="lazy" />
      <div v-else class="card-cover-fallback" aria-hidden="true">
        <img src="img/logo-mini-s.jpg" alt="" />
        <strong>{{ aula.titulo }}</strong>
      </div>
      <span class="badge">Aula {{ aula.id }}</span>
    </div>
    <div class="card-body">
      <span class="card-serie">{{ aula.serie || "Mini S" }}</span>
      <h3>{{ aula.titulo }}</h3>
      <p>{{ aula.resumo }}</p>
      <span v-if="aula.equipe" class="card-equipe">Criada por {{ aula.equipe }}</span>
      <div class="card-meta">
        <span v-if="aula.idade">👧 {{ aula.idade }}</span>
        <span v-if="aula.tempo">⏱ {{ aula.tempo }}</span>
        <span class="card-link">Ver aula →</span>
      </div>
    </div>
  </RouterLink>

  <div v-else class="card soon" :aria-label="`Aula ${aula.id}, em breve`">
    <div class="card-cover"><span aria-hidden="true">{{ aula.id }}</span></div>
    <div class="card-body">
      <span class="card-serie">Aula {{ aula.id }}</span>
      <h3>Em breve</h3>
      <p>Material em produção pelas equipes.</p>
    </div>
  </div>
</template>
