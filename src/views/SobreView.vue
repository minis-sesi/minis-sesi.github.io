<script setup>
import PageHeader from "../components/PageHeader.vue";
import GaleriaFotos from "../components/GaleriaFotos.vue";
import { site, galeria } from "../data/conteudo";

const estrutura = [
  { icone: "📖", titulo: "História em quadrinhos", texto: "Cada aula abre com uma aventura do Bolt que apresenta o desafio do dia." },
  { icone: "✏️", titulo: "Agora é a sua vez!", texto: "Atividades práticas com níveis de dificuldade que crescem aos poucos." },
  { icone: "🏅", titulo: "Conquistas", texto: "No fim de cada página a criança marca as conquistas e vê o próprio progresso." },
  { icone: "💡", titulo: "Cantinho da Sabedoria", texto: "Um fechamento com reflexão sobre o que foi aprendido e os valores trabalhados." },
];

const habilidades = ["Criatividade", "Raciocínio lógico", "Resolução de problemas", "Trabalho em equipe", "Curiosidade", "Visão espacial"];
</script>

<template>
  <div>
    <PageHeader
      eyebrow="Sobre o projeto"
      titulo="O que é o Mini S"
      texto="Um projeto educacional e social que aproxima crianças e adolescentes do universo da robótica, da ciência, da engenharia e da inovação."
    />

    <section class="section">
      <div class="wrap split">
        <div>
          <span class="eyebrow">A ideia</span>
          <h2>Um “drive com cara de site”</h2>
          <p>
            O Mini S reúne em um só lugar todos os materiais de um módulo de cerca de 3 meses: {{ site.totalEncontros }} encontros com
            histórias, desafios e brincadeiras, cada um criado por uma das equipes de robótica. Assim, qualquer professor pode aplicar o módulo sozinho, mesmo sem experiência em robótica.
          </p>
          <p>
            As aulas são aplicadas nas unidades do <strong>PEAL</strong>, presente em 14 cidades de Santa Catarina, e ficam
            abertas para qualquer escola ou projeto social que queira usar.
          </p>
        </div>
        <img class="split-img" src="img/paginas/p04.jpg" alt="Capa da Missão 1, Os Projetos Perdidos" loading="lazy" />
      </div>
    </section>

    <section class="section tinted">
      <div class="wrap">
        <span class="eyebrow">Como funciona</span>
        <h2>Toda aula segue o mesmo caminho</h2>
        <p class="lead">Uma estrutura previsível ajuda o professor a se preparar e as crianças a saberem o que vem a seguir.</p>
        <div class="feature-grid">
          <div v-for="e in estrutura" :key="e.titulo" class="feature">
            <span class="feature-icon" aria-hidden="true">{{ e.icone }}</span>
            <h3>{{ e.titulo }}</h3>
            <p>{{ e.texto }}</p>
          </div>
        </div>
      </div>
    </section>

    <section v-if="galeria.length" class="section">
      <div class="wrap">
        <span class="eyebrow">Registros do projeto</span>
        <h2>O Mini S na prática</h2>
        <p class="lead">Confira alguns momentos dos encontros e oficinas realizadas pelas equipes de robótica com as crianças.</p>
        <div class="gallery-wrap">
          <GaleriaFotos />
        </div>
      </div>
    </section>

    <section class="section tinted">
      <div class="wrap">
        <span class="eyebrow">O que desenvolvemos</span>
        <h2>Mais do que tecnologia</h2>
        <p class="lead">Mais do que ensinar tecnologia, o Mini S quer mostrar às crianças que elas também podem ser criadoras, inventoras e protagonistas.</p>
        <div class="tags tags-lg">
          <span v-for="h in habilidades" :key="h" class="tag">{{ h }}</span>
        </div>
        <div class="cta-box">
          <div>
            <h3>Pronto para aplicar?</h3>
            <p>Os materiais são gratuitos e prontos para imprimir.</p>
          </div>
          <RouterLink class="btn btn-primary" to="/aulas">Ver as aulas</RouterLink>
        </div>
      </div>
    </section>
  </div>
</template>
