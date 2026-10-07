import { createRouter, createWebHashHistory } from "vue-router";
import HomeView from "./views/HomeView.vue";

// Hash history (#/aulas) evita página 404 ao recarregar no GitHub Pages.
const routes = [
  { path: "/", name: "home", component: HomeView, meta: { title: "Início" } },
  { path: "/quem-somos", name: "quem-somos", component: () => import("./views/QuemSomosView.vue"), meta: { title: "Quem somos" } },
  { path: "/sobre", name: "sobre", component: () => import("./views/SobreView.vue"), meta: { title: "Sobre o projeto" } },
  { path: "/aulas", name: "aulas", component: () => import("./views/AulasView.vue"), meta: { title: "Aulas" } },
  { path: "/aulas/:id", name: "aula", component: () => import("./views/AulaView.vue"), props: true, meta: { title: "Aula" } },
  { path: "/contatos", name: "contatos", component: () => import("./views/ContatosView.vue"), meta: { title: "Contatos" } },
  { path: "/:pathMatch(.*)*", name: "404", component: () => import("./views/NotFoundView.vue"), meta: { title: "Página não encontrada" } },
];

const router = createRouter({
  history: createWebHashHistory(),
  routes,
  scrollBehavior: () => ({ top: 0 }),
});

router.afterEach((to) => {
  document.title = `${to.meta.title} | Mini S`;
});

export default router;
