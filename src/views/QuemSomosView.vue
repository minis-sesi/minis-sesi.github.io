<script setup>
import PageHeader from "../components/PageHeader.vue";
import GaleriaFotos from "../components/GaleriaFotos.vue";
import { equipes, galeria, site, aulasDisponiveis } from "../data/conteudo";

const aulasDaEquipe = (nome) => aulasDisponiveis.filter((a) => a.equipe === nome).length;
</script>

<template>
  <div>
    <PageHeader
      eyebrow="Quem somos"
      titulo="Estudantes que constroem robôs e agora constroem aulas"
      texto="O Mini S é criado pelas equipes de robótica da Escola SESI de Jaraguá do Sul. Cada equipe monta um conjunto de aulas com a sua identidade, transformando o que vive nas competições em atividades para crianças."
    />

    <section class="section">
      <div class="wrap">
        <img class="banner-img" src="img/fotos/equipes.jpg" alt="Integrantes das equipes de robótica reunidos com a bandeira da S ROBOTS" />

        <div class="section-head">
          <div>
            <span class="eyebrow">As equipes</span>
            <h2>Quem cria as aulas</h2>
          </div>
        </div>
        <div class="team-grid">
          <article v-for="e in equipes" :key="e.nome" class="panel team">
            <img v-if="e.logo" class="team-logo" :src="e.logo" :alt="`Logo da equipe ${e.nome}`" />
            <span v-if="e.categoria" class="eyebrow">{{ e.categoria }}</span>
            <h3>{{ e.nome }}</h3>
            <p>{{ e.descricao }}</p>
            <div class="team-foot">
              <RouterLink v-if="aulasDaEquipe(e.nome)" to="/aulas" class="tag">
                {{ aulasDaEquipe(e.nome) }} {{ aulasDaEquipe(e.nome) === 1 ? "aula publicada" : "aulas publicadas" }}
              </RouterLink>
              <a v-if="e.instagram" :href="`https://www.instagram.com/${e.instagram.replace(/^@/, '')}/`" target="_blank" rel="noopener">
                @{{ e.instagram.replace(/^@/, "") }}
              </a>
            </div>
          </article>
        </div>
      </div>
    </section>

    <section class="section tinted">
      <div class="wrap">
        <span class="eyebrow">Nossa motivação</span>
        <h2>Da competição para a comunidade</h2>
        <p class="lead">
          Nas competições aprendemos engenharia, programação, design e, principalmente, a trabalhar em equipe. Queremos que
          mais crianças tenham contato com esse universo desde cedo e descubram que também podem ser criadoras, inventoras e
          protagonistas.
        </p>
        <div v-if="galeria.length" class="gallery-wrap">
          <GaleriaFotos />
        </div>
      </div>
    </section>

    <section class="section">
      <div class="wrap">
        <span class="eyebrow">Créditos</span>
        <h2>Quem torna o Mini S possível</h2>
        <div class="credit-groups">
          <div class="credit-box">
            <h3>Idealização e criação</h3>
            <div class="chips">
              <span v-for="e in equipes" :key="e.nome" class="chip">{{ e.nome }}<small>{{ e.categoria }}</small></span>
              <span class="chip">Escola SESI<small>Jaraguá do Sul / SC</small></span>
            </div>
          </div>
          <div class="credit-box">
            <h3>Parceiros e apoiadores</h3>
            <div class="chips">
              <span v-for="a in site.apoiadores" :key="a.nome" class="chip" :class="{ 'chip-logo': a.logo }">
                <img v-if="a.logo" :src="a.logo" :alt="a.nome" />
                <template v-else>{{ a.nome }}<small>{{ a.detalhe }}</small></template>
              </span>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>
