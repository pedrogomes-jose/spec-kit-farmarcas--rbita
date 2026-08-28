# Frontend | Mapa

> Fonte: https://farmarcas.atlassian.net/wiki/spaces/SR/pages/3622600726/Frontend+Mapa · Última atualização no Confluence: nov. 27, 2025

## Visão Geral

O mapa do Órbita vive no módulo `ViewModule` (`src/app/modules/view/view.module.ts`), que agrega `ViewComponent`, `ViewMapComponent`, `ViewManageComponent`, `ViewSearchComponent`, `LayerDetailsComponent` e os serviços compartilhados `GeoJsonService`, `SourceService` e `MapService`. A renderização usa `@angular/google-maps` como wrapper do Google Maps JS API e `deck.gl` (`GeoJsonLayer`, `IconLayer`, `ArcLayer`) para desenhar camadas personalizadas sobre o mapa. O estado global fica em `MapService`, declarado como provider `providedIn: 'root'`, funcionando como um store observável compartilhado com toda a aplicação.

## Arquitetura e Montagem

* **Bootstrap**: ao entrar em `/view`, `CommonHomeComponent` garante que `MapService.map` tenha um `MapModel` inicial e, se o usuário escolheu um endereço na home, já preenche `map.main` (`src/app/modules/common/pages/home/home.component.ts`).
* **Store**: `MapService` serializa/deserializa `MapModel` usando `TypedJSON` e salva no `CoreStorage` sempre que `mapChanges` detecta alterações (via `on-change`). O setter de `map` injeta um proxy que dispara eventos de mudança e executa `localSave`.  

```66:105:webapp-orbita/src/app/shared/services/map.service.ts
public set map(map: MapModel) {
  this.internalMap = map;
  this.mapProxy = onChange(this.internalMap, (path, value, previousValue) => {
    if ((!value && !previousValue) || isEqual(value, previousValue)) {
      return;
    }
    if (this.changesSubjectLock) {
      this.changesSubjectPaths.push(path);
      return;
    }
    this.mapChanges.next(path);
  });
  this.localSave();
}
```

* **Composição de componentes**: `ViewComponent` monta a árvore: `<app-view-map>` para o canvas, `<app-view-manage>` para gerenciamento de camadas, `<app-view-search>` para busca e `<app-layer-details>`/`<app-location-details>` para os painéis informativos. O template mostra o mapa sempre dentro de `div#map`.  

```9:34:webapp-orbita/src/app/modules/view/view.component.html
<div id="map">
  <app-view-map [centralize]="mapCentralize"></app-view-map>
</div>
<div id="manage" *ngIf="dataViewEnabled && !map.placeEdit">
  <app-view-manage></app-view-manage>
</div>
<div id="tools">
  <button rdsTooltip="Centralizar" (click)="centralizeMap()"></button>
  <button rdsTooltip="Régua" [class.active]="map.measureEnabled" (click)="measureToggle()"></button>
  ...
</div>
```

* **Inicialização do mapa**: `ViewMapComponent` utiliza `<google-map>` para criar a instância do Google Maps e aplica configurações padrão (controles básicos habilitados/desabilitados conforme necessário). O evento `(mapInitialized)` chama `onMapReady`, onde as variantes de mapa (`SimpleAtlasMapType`, `WhiteWaterMapType`) são registradas, o zoom/centro inicial é definido e os overlays do [http://deck.gl](http://deck.gl)  são conectados.  

```1:22:webapp-orbita/src/app/modules/view/components/map/map.component.html
<google-map height="100vh" width="100vw"
  (mapInitialized)="onMapReady($event)"
  [options]="{zoomControl:true,...}"
  (mapClick)="mapClick($event)">
  <map-circle *ngIf="map.radiusEnabled && map.radius <= 6500" ...></map-circle>
  <map-marker *ngIf="!!map.main && !map.placeEdit" ...></map-marker>
</google-map>
```

## Fluxo de Dados e Camadas

1. **Catálogo de fontes**: `ViewManageComponent` carrega todas as `Source` disponíveis via `SourceService.getSourcesAvailable()`, filtrando apenas as com `status > 1`. Elas são agrupadas por `source.groupBy` para exibição.  
2. **Seleção e estado**: ao selecionar uma camada, `addSource` garante que a geometria principal entre no mapa, configura `checked/active` e, se houver `references`, seta `dataActive` para ligar uma camada de dados à geometria.  

```117:209:webapp-orbita/src/app/modules/view/components/manage/manage.component.ts
addSource(layer: Source, active?: boolean, checked?: boolean): void {
  ...
  if (selectedSource.references?.length) {
    dependencySource = this.allSources.find((source) =>
      selectedSource.references.some((reference) => reference.name === source.name)
    );
  }
  if (dependencySource) {
    dependencySource.checked = true;
    dependencySource.active = true;
    dependencySource.dataActive = selectedSource.id;
  }
}
```

3. **Carregamento de assets**: `ViewComponent` faz `SourceService.getAssets()` e usa `GeoJsonService.get` para baixar todos os GeoJSON necessários antes de liberar a UI (progress bar em `assetProgress`).  

```272:329:webapp-orbita/src/app/modules/view/view.component.ts
this.sourcesAssetSubscription = this._sourceService.getAssets().subscribe(
  (sourceAssets) => {
    const assetsUrls = sourceAssets
      .map((asset) => asset.geometryFile)
      .filter((url) => !!url);
    this.assetFiles = sourceAssets
      .filter((asset) => assetsUrls.includes(asset.geometryFile))
      .map((asset) => new AssetFile({ url: asset.geometryFile }));
    this.loadAssets();
  }
);
```

4. **Busca de dados geográficos**: `ViewMapComponent.getSourcesData()` observa mudanças em `radius`, `main`, `sources` e `dataActive`. Quando algum deles muda, ele reseta `map.sourcesData` (se necessário) e solicita `/sources/search`, enviando `latitude`, `longitude`, `range` e a lista de IDs de camadas ativas.  

```168:213:webapp-orbita/src/app/modules/view/components/map/map.component.ts
const activeSources = this.map.activeSources
  .filter((source) => source.geometryType !== SourceGeometryType.NONE)
  .map((source) => source.dataActive || source.id);
...
this.sourceDataSub = this._sourceService
  .searchSources(this.map, sourcesToLoad)
  .subscribe((res) => {
    res.data.source?.forEach((sourceData) => {
      const sourceGeometries = {};
      sourceData.geometries.forEach((geometry) => {
        sourceGeometries[geometry._id] = geometry.properties;
      });
      this.map.sourcesData[sourceData.id] = {
        id: sourceData.id,
        assets: sourceData.assets,
        geometries: sourceGeometries,
        projection: sourceData.projection,
      };
    });
  });
```

5. **Renderização via** [http://deck.gl](http://deck.gl) :

    * `MapService.buildGeoJsonLayer` combina todos os `assets` de uma camada, aplica estilos com base em `SourceGrouping` e registra `onClick` para repassar a seleção para `MapService.geometryClick`.
    * `ViewMapComponent.buildIconLayer` e `buildArcLayer` tratam pontos e linhas, respectivamente.  
    

```392:474:webapp-orbita/src/app/shared/services/map.service.ts
return forkJoin(sourceData.assets.map((asset) => this._geoJsonService.get(asset))).pipe(
  map((collections) =>
    new GeoJsonLayer({
      id: `geo-${dataSource?.id || source?.id}-${source.id}-${sourceData.id}`,
      data: { type: 'FeatureCollection', features: collections.flatMap((coll) => coll.features) },
      getLineColor: (feature) => {
        const properties = sourceData.geometries[feature._id];
        const style = StyleHelper.polygonStyle(
          feature._id,
          properties[sourceData.projection[grouping.column]],
          grouping
        );
        return [...style.strokeColor, style.fillOpacity * 255];
      },
      onClick: (info): void => {
        if (info?.object) {
          const feature = info.object as GeoJsonFeature;
          this.geometryClick(source.dataActive || source.id, feature._id);
        }
      },
    })
  )
);
```

6. **Painel lateral**: `LayerDetailsComponent` ouve `MapService.observeChanges(['sources','activeSources','placeDetails'])` e recalcula estatísticas usando `Source.structure.columns`, exibindo propriedades agregadas do `SourceData` ativo.  

## Interações e Controles

* **Zoom/Pan**: `mapCentralize()` é exposto em `ViewComponent` e chama `googleMap.panTo` e `setZoom`. O usuário também pode arrastar manualmente; o Google Maps nativo gerencia o evento.
* **Círculo de raio**: baseado em `map.radiusEnabled` e `map.radius`. O slider (`ngx-slider`) atualiza `map.radius`, disparando uma nova consulta via `observeChanges`.
* **Definição de ponto central**: o marcador principal é arrastável (`map-marker` com `mapDragend`). `mainMarkerDragEnd` chama `updateMainLocation`, que geocodifica a posição via `PlaceService`.
* **Cliques em features**: `GeoJsonLayer`, `ArcLayer` e `IconLayer` chamam `MapService.geometryClick`, que sincroniza `map.place` e `mapProperties`. `LayerDetailsComponent` reage e mostra os atributos da geometria selecionada.
* **Marcadores de busca e favoritos**: `ViewSearchComponent.getNearbyPlaces` cria `Marker` objetos e os adiciona a `map.searchMarkers`. `MapService.buildMarkers` transforma esses dados em `IconLayer`s dedicados, com destaque para o item selecionado.

```232:285:webapp-orbita/src/app/shared/services/map.service.ts
const layers = [
  new IconLayer({ id: 'markers-base', data: baseFeatures, onClick: (info) => this.onMarkerClick(info) }),
  new IconLayer({ id: 'markers-highlighted', data: highlighted, onClick: (info) => this.onMarkerClick(info) })
];
this.deckglMarkersOverlay?.setProps({ layers });
```

* **Seleção/Hover**: o hover é tratado nativamente pelo [http://deck.gl](http://deck.gl)  (ex.: `pickable: true`); o código atual foca em `onClick`. O `MapService.selectedMarker` guarda o marcador ativo e força rebuild dos layers para alterar o destaque.
* **Edição de local**: `togglePlaceEdit` desanexa os overlays para mostrar apenas o Google Maps puro e abre um modal de confirmação (`rds-modal`) em `map.component.html`. O arraste dispara `placeUpdateDragEnd`, e `updateMarker` decide se atualiza um marcador local ou dispara `SourceService.updateCoordinates`.
* **Medida de distância**: o botão “Régua” liga/desliga `map.measureEnabled`. `MapService.observeChanges(['type','measureEnabled'])` notifica `ViewMapComponent`, que delega ao `PolylineService` (adiciona pontos com `addPath` e limpa com `clearPath`).  
* **Filtros e busca**:

    * `SearchLayerComponent` filtra os grupos de camadas via regex normalizado.
    * `ViewManageComponent.applyFilter` manipula `map.sources`, garantindo que apenas camadas selecionadas continuem carregadas.
    * `ViewComponent.checkNearbyAnalysis()` chama `SourceService.searchWarnings` sempre que ponto central ou raio mudam, mostrando um toast se já houver análise próxima.
    

## Integração com Backend e Serviços Externos

* **Endpoints primários** (todos definidos em `SourceService`):

    * `GET /sources` e `/sources/available`: catálogo completo ou filtrado.
    * `POST /sources/search`: recebe `dataSources[]`, `latitude`, `longitude`, `range`. Resposta contém `SearchSourceResponse` com `assets`, `projection`, `geometries`.
    * `POST /sources/search/warnings`: usa query `analysisId` + body com lat/lng para alertas.
    * `PUT /sources/{id}/structure` e `PUT /sources/{id}/{geometryId}/coords`: atualizações estruturais e geográficas.
    * `GET /sources/{id}/download`: exportação.
    
* **Serviços Google**: `GoogleMapsService` carrega as bibliotecas `places`, `geometry`, `drawing`. `PlaceService` encapsula `AutocompleteService`, `PlacesService`, `Geocoder`, garantindo chamadas assíncronas com `Observable`.
* **Persistência e análises**: `AnalysisService.updateMap` envia o `MapModel` completo (`map.analysisId`) para a API expansion. `MapService.localSave` grava o estado parcial no `CoreStorage` para restaurar a sessão.
* **Erro e loading**: `ViewMapComponent` mantém `map.loading` true enquanto busca dados; `ViewComponent` exibe overlay de carregamento em `view.component.html`. `ToastrService` mostra mensagens em falhas (`searchSources`, `updateCoordinates`, `searchWarnings` etc.).

## Performance e Estado

* Debounce generalizado: `MapService.mapChanges` usa `debounceTime(500)` antes de salvar no storage; `ViewComponent` e `ViewMapComponent` também aplicam `debounceTime` nos observers (`observeChanges(['loading','placeEdit'], 25)`, `observeChanges(['radius','main','sources','dataActive'], 100)`), reduzindo rebuilds.
* `MapService.lockChangesSubject` evita rajadas de eventos quando o usuário abre modais ou executa mutações em lote. Ao desbloquear, apenas caminhos únicos acumulados são notificados.
* [http://Deck.gl](http://Deck.gl)  overlays renderizam tudo em GPU e separam layers por tipo (`GeoJsonLayer`, `IconLayer`, `ArcLayer`), o que evita reprocessamento completo. `forkJoin` carrega assets em paralelo, mas só aplica `setProps` quando todos estão prontos.
* `ViewComponent.loadSourcesAssets()` pré-carrega os arquivos GeoJSON do `SourceAsset`, eliminando requisições repetidas durante a exploração interativa.
* `MapService.buildMarkers` diferencia camada base e destaque, evitando re-renderização completa quando apenas o marcador ativo muda.

## Pontos de Extensão

1. **Adicionar uma nova camada (source)**:

    * Backend: disponibilize a nova `Source` em `/sources/available` com `groupBy`, `structure`, `geometryType` e `references` adequadas.
    * Frontend:
    
        1. Nenhuma alteração estrutural é necessária; `ViewManageComponent` a exibirá automaticamente no grupo correto.
        2. Se precisar de estilo próprio, ajuste `StyleHelper.polygonStyle` ou `IconHelper.marker`.
        3. Para operações agregadas específicas, confira `LayerDetailsComponent.calculateColumns`.
        4. Teste ativando a camada pela UI, verificando se `map.sourcesData` recebe `assets` e `geometries`.
        
    
2. **Conectar uma nova fonte de dados sem geometria**:

    * Certifique-se de que `Source.geometryType === SourceGeometryType.NONE` e que `references` aponte para a geometria pai.
    * Garanta que o backend envie a projeção correta (`projection[col.name]`), pois `MapService.geometryClick` usa esse mapa para exibir valores.
    
3. **Criar nova interação**:

    * Use `MapService.observeChanges` para reagir a trechos específicos do estado sem polling. Ex.: `observeChanges(['place'])`.
    * Para eventos do Google Maps, adicione listeners dentro de `ViewMapComponent.onMapReady`.
    * Para overlays específicos, crie novos builders (similar a `buildArcLayer`) e registre-os em `buildLayers`.
    
4. **Integrar novo controle**:

    * Adicione o botão em `view.component.html`, vincule a métodos de `ViewComponent` e atualize `MapModel` ou `MapService` via injeção direta.
    

## Boas Práticas para Trabalhar com o Mapa

* Sempre manipule `MapModel` através de `MapService` para preservar a serialização e o disparo de eventos (`mapChanges`).
* Prefira `MapService.observeChanges` com caminhos específicos e `debounceTime` curto para evitar ciclos de renderização desnecessários.
* Ao adicionar camadas, garanta que `Source.references` e `groupBy` estejam corretos para que `ViewManageComponent` e `LayerDetailsComponent` mantenham o comportamento esperado.
* Reaproveite os serviços existentes (`SourceService`, `GeoJsonService`, `PlaceService`) em vez de criar chamadas HTTP diretas, preservando o padrão de error handling com `ToastrService`.
* Teste novas features com o loader de assets habilitado (usar `ViewComponent.loadSourcesAssets`) para certificar-se de que os GeoJSON ficam disponíveis antes da renderização.
* Quando criar novas interações, mantenha a lógica de mutação no serviço (MapService) e deixe os componentes apenas como orquestradores de UI, garantindo consistência e reutilização em todo o módulo View.
* Evite recalcular dados agregados manualmente; use `LayerDetailsComponent.recalculate` como referência e estenda os helpers (`ValueHelper`, `StyleHelper`) quando necessário.
* Para performance, agregue mudanças (usar `lockChangesSubject(true)` durante operações batch) e só libere os eventos quando todo o estado estiver consistente.
