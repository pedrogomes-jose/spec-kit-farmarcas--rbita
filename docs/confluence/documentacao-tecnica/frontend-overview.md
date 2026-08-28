# Frontend | Overview

> Fonte: https://farmarcas.atlassian.net/wiki/spaces/SR/pages/3622666241/Frontend+Overview · Última atualização no Confluence: nov. 27, 2025

## Documentação Frontend Órbita

### Visão geral

* Aplicação Angular 18 modularizada que entrega um cockpit geoespacial e painéis de análise para o ecossistema Farmarcas.
* Interface em português/BR focada em gestão de dados (marcadores, fontes, camadas), visualização em mapas e acompanhamento de análises/contratos.
* Usa o design system Aurora e o core corporativo Farmarcas para autenticação, autorização e instrumentação.

### Stack principal

* Angular CLI 18 + Typescript 5.4; Node LTS Hydrogen (`.nvmrc`) e Yarn.
* Bibliotecas chave: `@farmarcas/angular-core`, `@farmarcas/aurora-angular`, Google Maps + [http://Deck.gl](http://Deck.gl) , Lucide Icons, ngx-toastr, ngx-charts, ngx-slider, color-picker.
* Testes com Karma/Jasmine e E2E com Protractor; lint com Angular ESLint e Prettier.

### Arquitetura

`app.routes.ts`

```typescript
  {
    path: '',
    canActivateChild: [AuthenticatedGuard, PermissionGuard],
    data: {
      permission: [
        {
          role: PermissionRole.ADMIN,
          product: PermissionProduct.ORBITA,
          permission: 'AccessOrbita',
        },
        {
          role: PermissionRole.ANGEL,
          product: PermissionProduct.ORBITA,
          permission: 'AccessOrbita',
        },
      ] as PermissionRouteData,
    },
    children: [
      {
        path: 'view',
        loadChildren: (): Promise<any> =>
          import('./modules/view/view.module').then(
            (module) => module.ViewModule
          ),
      },
      ...
```

* Rotas raiz exigem autenticação + permissão via guards providos pelo core corporativo.
* Navegação hierárquica: `view` (lazy), `manage`, `analysis`, `contracts`, além da home comum.

      
    `app.module.ts`



    ```typescript
        FarmarcasCoreModule.forRoot(
          () =>
            ({
              application: {
                  name: enviro  nment.app`     lication.name,
                release: environment.application.release,
                environment: environment.environment,
              },
              services: {
                common: { apiBase: environment.api.common },
                authentication: {
                  requestUrl: environment.webapp.authentication,
                  tokenInterceptorBaseUrls: [
                    environment.api.base,
                    environment.api.common,
                    environment.api.expansion,
                  ],
                },
              },
              external: {
                googleAnalytics: { trackingCode: 'G-F1Z1LRSVEL' },
                posthog: { prefix: environment.lib.posthog.prefix },
                appCues: { appId: '218891', enabled: false },
                clarity: { appId: 'tjd3w9to9e', enabled: true },
                sentry: { enabled: false },
                usersnap: { apiKey: '7d4df069-2410-474c-b388-113ec335ac77', enabled: false }
              },
              interceptors: {},
            }) as unknown as FarmarcasCoreConfig
        ),
        ToastrModule.forRoot({
          positionClass: 'toast-bottom-left',
          preventDuplicates: true,
          timeOut: 7500,
          closeButton: true,
          toastComponent: OrbitaToastComponent,
        }),
    ```
* `AppModule` centraliza configuração de libs corporativas, interceptadores HTTP, Toastr customizado e registro de serviços compartilhados (Analysis, Brand, Map, Place, GeoJson, Source).
* Localização padrão `pt-BR` e timezone ajustada via Dayjs.

**Módulos funcionais**

* `modules/common`: layout, navegação, componentes compartilhados (menu lateral, home, breadcrumbs).
* `modules/view`: experiência principal de mapa geoespacial; integra Google Maps, [http://Deck.gl](http://Deck.gl)  e componentes de gerenciamento de camadas/marcadores, filtros, detalhamento de localizações e categorias.
* `modules/manage`: workflow administrativo, hoje focado em `database` (upload/importação de bases, gerenciamento de catálogos).
* `modules/analysis`: CRUD de análises, anexos, comentários, histórico; fornece pipes utilitárias (`TruncatePipe`, `FileSizePipe`) e componentes modais reutilizáveis.
* `modules/contracts`: telas dedicadas ao ciclo de contratos (rotas e componentes próprios).
* `shared`: fornece componentes genéricos (modal-action, toast), services (API, mapas, análises), helpers, directives e models. Serve como base para cross-cutting concerns.

### Configuração e ambientes

`environment.ts`

```typescript
export const environment = {
  environment: ApplicationEnvironment.DEVELOPMENT,
  application: {
    name: 'ORBITA',
    release: '%APP_VERSION%',
  },
  lib: {
    googlemaps: { apiKey: 'AIzaSyBZYwCXEuT9dgcGIXwDUDBOFQaRvu8zjGI' },
    posthog: { prefix: 'Órbita' },
    sentry: { dsn: 'https://c42ece0fef6041fb9776e91a253db695@o453111.ingest.sentry.io/5466477', tracesSampleRate: 0.0 },
  },
  api: {
    domain: 'localhost:8080',
    base: 'http://localhost:8080',
    expansion: 'https://expansion.api.dev.radar.farmarcas.com.br',
    common: 'https://management.api.dev.radar.farmarcas.com.br',
  },
  webapp: {
    authentication: 'https://dev.radar.farmarcas.com.br/authentication',
    radar: 'https://dev.radar.farmarcas.com.br',
  },
};
```

* Existem variantes `environment.develop.ts`, `environment.staging.ts`, `environment.production.ts` usadas pelos `fileReplacements` de build.
* `%APP_VERSION%` é substituído no pipeline para rastrear releases.
* APIs segmentadas: `base` (gateway principal), `common` (gestão), `expansion` (camadas geoespaciais). As URLs alimentam interceptadores e serviços.

### Pré-requisitos locais

1. Node LTS Hydrogen (`nvm install lts/hydrogen && nvm use`).
2. AWS CLI configurado + CodeArtifact (ver README): necessário para baixar pacotes privados.
3. `yarn install` após configurar `aws codeartifact login`.
4. `ng serve` padrão ou `ng serve -c local-staging`/`local-production` usando scripts `start-*`.

### Scripts relevantes (`package.json`)

* `start`, `start-local-staging`, `start-local-production`: servem a aplicação com diferentes configs.
* `build`: gera artefatos em `dist/`.
* `test`, `e2e`, `lint`.
* `start-farmarcas/aurora-yalc`: fluxo para testar versões locais do Aurora design system via `yalc`.

### Estrutura de diretórios (resumo)

* `src/app/core`: helpers de ambiente, wrappers para libs corporativas.
* `src/app/modules`: módulos funcionais descritos acima.
* `src/app/shared`: UI genérica, models, services, pipes e helpers.
* `src/assets`: ícones, mapas (SVG por UF), imagens e favicons.
* `src/environments`: configurações por ambiente.
* `e2e`: suíte Protractor.
* `styles.scss` + `aurora.scss`: estilos globais, overrides do Aurora.
* `webpack.config.ts`: customizações (quando necessário) via `@angular-builders/custom-webpack`.

### Fluxo de dados e integrações

* Todas as chamadas HTTP passam pelos interceptores do `FarmarcasCoreModule`, garantindo injeção de tokens e manipulação de erros global.
* Módulos específicos (p.ex. `view`) consomem `Shared` services (`GeoJsonService`, `SourceService`) para carregar camadas, markers e tabelas.
* Gestão de arquivos (upload/download, conversões) utilizam pipes e utilitários (`FileSizePipe`, helpers em `shared/helpers`).
* Autorização é declarativa nas rotas: cada feature exige permissões (`ManageData`, `ManagamentAnalysis`) e o guard só deixa prosseguir se o token contiver o escopo adequado.

### Build & Deploy

`bitbucket-pipelines.yml`

```yaml
definitions:
  steps:
    - step: &build-angular
        image: sleavely/node-awscli:18.x
        name: Build - Angular Assets
        ...
        script:
          - export APP_RELEASE="$RELEASE_PREFIX-$BITBUCKET_BUILD_NUMBER"
          - sed -ri "s|%APP_VERSION%|$APP_RELEASE|" src/environments/environment.${BITBUCKET_DEPLOYMENT_ENVIRONMENT}.ts
          - yarn install --frozen-lockfile
          - yarn build --configuration ${BITBUCKET_DEPLOYMENT_ENVIRONMENT} --base-href $PUBLIC_BASE
          - printenv > enviroment_variables
    - step: &release-sentry
        image: getsentry/sentry-cli
        ...
          - sentry-cli releases files $APP_RELEASE upload-sourcemaps ./dist ...
    - step: &release-aws
        ...
          - pipe: atlassian/aws-s3-deploy:1.2.0
            variables:
              S3_BUCKET: "${AWS_S3_BUCKET}"
              ...
pipelines:
  branches:
    develop/staging: build → sentry release → deploy S3/CloudFront
    main: tag release + build + sentry + deploy
```

* Builds usam imagem Node+AWS CLI para empacotar e publicar em buckets S3 específicos por ambiente, com invalidação CloudFront.

* Sentry release automatizado (criação, upload de sourcemaps).

* Branch `main` adiciona etapa de tagging.
