import colors from "vuetify/es5/util/colors";

export default {
  // Global page headers (https://go.nuxtjs.dev/config-head)
  head: {
    // titleTemplate: "%s - EssayShares",
    title: "EssayShares",
    meta: [
      { charset: "utf-8" },
      { name: "viewport", content: "width=device-width, initial-scale=1" },
      { hid: "description", name: "description", content: "英語ライティング・英語エッセイ共有ウェブアプリ" },
      { name: "google-site-verification", content: "04zYgkBTBKgaqj1CPZTCM0XlxGwBizdRDxW9arXFhtw" }
    ],
    link: [{
      rel: "shortcut icon",
      type: "image/x-icon",
      href: "favicon2.ico"
    },
      {
        rel: "apple-touch-icon",
        href: "apple-touch-icon.png",
        sizes: "180x180"
      },
      {
        rel: "icon",
        type: "image/png",
        href: "android-touch-icon.png", sizes: "192x192"
    }
    ]
  },

  // Global CSS (https://go.nuxtjs.dev/config-css)
  css: [
     '@/assets/css/common.css',
  ],

  // Plugins to run before rendering page (https://go.nuxtjs.dev/config-plugins)
  plugins: [
    // '@/plugins/utils'
  ],

  // Auto import components (https://go.nuxtjs.dev/config-components)
  components: true,

  // Modules for dev and build (recommended) (https://go.nuxtjs.dev/config-modules)
  buildModules: [
    // https://go.nuxtjs.dev/vuetify
    "@nuxtjs/vuetify"
  ],

  // Modules (https://go.nuxtjs.dev/config-modules)
  modules: [
  ],

  // Vuetify module configuration (https://go.nuxtjs.dev/config-vuetify)
  vuetify: {
    customVariables: ["~/assets/variables.scss"],
    theme: {
      // dark: true,
      themes: {
        dark: {
          primary: colors.blue.darken2,
          accent: colors.grey.darken3,
          secondary: colors.amber.darken3,
          info: colors.teal.lighten1,
          warning: colors.amber.base,
          error: colors.deepOrange.accent4,
          success: colors.green.accent3
        }
      }
    }
  },

  // Routing configuration
  router: {
    extendRoutes (routes, resolve) {
      routes.push({
        name: 'custom',
        path: '*',
        // component: resolve(__dirname, 'pages/errors/404.vue')
        component: resolve(__dirname, 'pages/404.vue')
      })
    }
  },
  // Build Configuration (https://go.nuxtjs.dev/config-build)
  build: {},
};
