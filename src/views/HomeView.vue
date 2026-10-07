<script setup>
import AulaCard from "../components/AulaCard.vue";
import GaleriaFotos from "../components/GaleriaFotos.vue";
import { aulasDisponiveis, equipes, galeria, site } from "../data/conteudo";

const passos = [
  { titulo: "Escolha a aula", texto: "Siga a ordem da trilha. Cada aula é uma nova missão do Bolt." },
  { titulo: "Baixe e imprima", texto: "Baixe o PDF da aula e imprima uma cópia por criança." },
  { titulo: "Conte a história", texto: "Comece lendo os quadrinhos com a turma para apresentar o desafio." },
  { titulo: "Mão na massa", texto: "As crianças fazem as atividades e marcam suas conquistas." },
];
</script>

<template>
  <div>
    <section class="hero">
      <div class="wrap hero-grid">
        <div>
          <div class="tagline"><span>Aprender</span><span>Criar</span><span>Transformar</span></div>
          <h1>Robótica e tecnologia ao alcance de <span>toda criança</span></h1>
          <p>
            Aulas prontas, criadas pelas equipes de robótica da Escola SESI de Jaraguá do Sul, para qualquer professor
            baixar, imprimir e aplicar com a sua turma. De graça.
          </p>
          <div class="hero-actions">
            <RouterLink class="btn btn-primary" to="/aulas">Ver as aulas</RouterLink>
            <RouterLink class="btn btn-ghost" to="/sobre">Conhecer o projeto</RouterLink>
          </div>
        </div>
        <div class="hero-logo">
          <img src="img/logo-mini-s.jpg" alt="Logo do Mini S: o robô Bolt pintando o nome do projeto" />
        </div>
      </div>
    </section>

    <section class="stats" aria-label="O projeto em números">
      <div class="wrap stats-grid">
        <div class="stat"><strong>{{ site.totalEncontros }}</strong><span>encontros planejados</span></div>
        <div class="stat"><strong>{{ aulasDisponiveis.length }}</strong><span>já disponíveis</span></div>
        <div class="stat"><strong>{{ equipes.length }}</strong><span>equipes criando</span></div>
        <div class="stat"><strong>100%</strong><span>gratuito</span></div>
      </div>
    </section>

    <section class="section">
      <div class="wrap">
        <div class="section-head">
          <div>
            <span class="eyebrow">Comece por aqui</span>
            <h2>Aulas disponíveis</h2>
          </div>
          <RouterLink class="btn btn-ghost btn-dark" to="/aulas">Ver todas as aulas →</RouterLink>
        </div>
        <div class="grid">
          <AulaCard v-for="a in aulasDisponiveis" :key="a.id" :aula="a" />
        </div>
      </div>
    </section>

    <section class="section how">
      <div class="wrap">
        <span class="eyebrow">Para professores</span>
        <h2>Aplique uma aula em 4 passos</h2>
        <p class="lead">Você não precisa saber robótica. Cada aula já vem com história, atividades e fechamento prontos.</p>
        <ol class="steps">
          <li v-for="p in passos" :key="p.titulo">
            <h3>{{ p.titulo }}</h3>
            <p>{{ p.texto }}</p>
          </li>
        </ol>
      </div>
    </section>

    <section v-if="galeria.length" class="section tinted">
      <div class="wrap">
        <div class="section-head">
          <div>
            <span class="eyebrow">Na prática</span>
            <h2>O Mini S acontecendo</h2>
            <p class="lead">Registros dos encontros com as crianças.</p>
          </div>
          <RouterLink class="btn btn-ghost btn-dark" to="/quem-somos">Ver mais fotos →</RouterLink>
        </div>
        <GaleriaFotos :limite="6" />
      </div>
    </section>

    <section class="section">
      <div class="wrap split">
        <img class="split-img" src="img/fotos/equipes.jpg" alt="Integrantes das equipes de robótica com a bandeira da S ROBOTS" loading="lazy" />
        <div>
          <span class="eyebrow">Quem somos</span>
          <h2>Feito por estudantes, para crianças</h2>
          <p>
            O Mini S nasceu da vontade das equipes de robótica da Escola SESI de Jaraguá do Sul de levar para a comunidade o
            que aprendem nas competições, mostrando que tecnologia pode ser acessível e divertida. Cada equipe cria um
            conjunto de aulas com a sua identidade.
          </p>
          <RouterLink class="btn btn-primary" to="/quem-somos">Conheça as equipes</RouterLink>
        </div>
      </div>
    </section>
  </div>
</template>
