### set up nuxt, github, firebase

- create a nuxt project
  - \$ yarn create nuxt-app EssayShares-github
  - choose all of the default settings except vuetify
    - ? Project name: EssayShares-github
    - ? Programming language: JavaScript
    - ? Package manager: Yarn
    - ? UI framework: Vuetify.js
    - ? Nuxt.js modules: (Press <space> to select, <a> to toggle all, <i> to invert - selection)
    - ? Linting tools: (Press <space> to select, <a> to toggle all, <i> to invert selection)
    - ? Testing framework: None
    - ? Rendering mode: Universal (SSR / SSG)
    - ? Deployment target: Server (Node.js hosting)
    - ? Development tools: (Press <space> to select, <a> to toggle all, <i> to invert - selection)
    - ? What is your GitHub username? masaki
    - ? Version control system: Git
- create a GitHub repositorie named EssayShares on Chrome
  - choose all of the default settings
- execute an first commit
  - \$ git init
  - \$ git add .
  - \$ git commit -m "first commit"
  - \$ git branch -M main
  - \$ git remote add origin https://github.com/maasa22/EssayShares.git
  - \$ git push -u origin main
- set up a firebase project and hosting
  - \$ yarn dev
  - create a project at firebase console named EssayShares on Chrome
    - add firebase to a web app //ウェブアプリに Firebase を追加
    - set firebase hosting //このアプリの Firebse Hosting も設定します。
  - \$ yarn add firebase
  - \$ yarn add firebase-tools
  - \$ yarn generate
  - \$ firebase login
  - \$ firebase init
    - check only hosting, set public folder as "dist"
      - ? Which Firebase CLI features do you want to set up for this folder? Press Space to select features, then Ent
        er to confirm your choices. Hosting: Configure and deploy Firebase Hosting sites
      - ? Please select an option: Use an existing project
      - ? Select a default Firebase project for this directory: essayshares (EssayShares)
      - ? What do you want to use as your public directory? dist
      - ? Configure as a single-page app (rewrite all urls to /index.html)? No
      - ? File dist/index.html already exists. Overwrite? No
  - \$ firebase deploy

### add database

- create a database with test mode //データベースの作成
- create plugins/firebase.js //プロジェクトを設定 > 全般 > Firebase SDK snippet > CDN
- create a python script

  - https://qiita.com/yusukeito58/items/c77feaa25fbbe37e9953

- http://toefl-scores.blogspot.com/2015/12/toefl-writing-topic-185-vol1.html
- http://toefl-scores.blogspot.com/2015/12/toefl-writing-topic-185-vol2.html

### develop
