# Frontend | Camadas

> Fonte: https://farmarcas.atlassian.net/wiki/spaces/SR/pages/3622797314/Frontend+Camadas · Última atualização no Confluence: nov. 27, 2025

## Camadas (Sources/Layers) no Órbita

* Cada camada é uma instância de `Source`, modelada em `shared/models/source.model.ts`. O modelo descreve o arquivo de origem, estrutura tabular, geometria disponível e dependências para cruzar atributos geográficos e estatísticos.

```294:367:webapp-orbita/src/app/shared/models/source.model.ts
@jsonObject
export class Source {
  @jsonMember({ name: '_id' }) id: string;
  @jsonMember name: string;
  @jsonMember({ constructor: Number }) fileType: SourceFileType;
  @jsonMember structure: SourceStructure;
  @jsonMember groupedBy: SourceGrouping;
  @jsonMember({ constructor: Number }) status: SourceStatus;
  @jsonMember({ constructor: Boolean }) active = false;
  @jsonMember({ constructor: Boolean }) checked = false;
  @jsonArrayMember(SourceReference) references: Array<SourceReference>;
  @jsonMember geometryType: SourceGeometryType;
  @jsonMember dataActive: string;
  ...
  get typeName(): string {
    switch (this.geometryType) {
      case 'Point': return 'Geográfica - Pontos';
      case 'LineString': return 'Geográfica - Linhas';
      case 'Polygon':
      case 'MultiPolygon': return 'Geográfica - Polígonos';
      default: return 'Estatística';
    }
  }
}
```

* `SourceStructure` lista as colunas e operações agregadas disponíveis; `SourceGrouping` define como uma coluna ativa colore a camada (grupos por intervalo, valores ou default). `SourceReference` relaciona uma camada “filha” (dados) ao pai (geometria).

## Onde cada camada é usada

* Estado global está em `MapModel` (`shared/models/map.model.ts`): `sources` armazena as camadas carregadas e `sourcesData` guarda os dados retornados pela API.

```88:130:webapp-orbita/src/app/shared/models/map.model.ts
@jsonObject
export class MapModel {
  @jsonArrayMember(Source) sources: Array<Source> = [];
  @jsonArrayMember(MapLayer) layers: Array<MapLayer> = [];
  get activeSources(): Array<Source> {
    return this.sources?.filter((source) => source.active);
  }
  sourcesData: { [sourceId: string]: SourceData } = {};
  ...
}
```

* `SourceService` (`shared/services/source.service.ts`) provê o backend:

    * `getSourcesAvailable()` lista camadas disponíveis.
    * `searchSources()` traz os dados renderizados considerando raio e posição selecionados, retornando `assets`, projeção de colunas e propriedades por geometria.
    * Atribuições e atualizações (delete/updateStructure/updateCoords) também passam por este serviço.
    

```31:74:webapp-orbita/src/app/shared/services/source.service.ts
public getSourcesAvailable(): Observable<Array<Source>> {
  const url = `${this.apiBase}/sources/available`;
  return this.getData(url);
}

private getData(url): Observable<Array<Source>> {
  return this._httpClient
    .get<HttpDataResponse<Array<Source>>>(url)
    .pipe(
      map((response) => {
        if (response?.data) {
          const parsedSources = response.data.map((source) =>
            this.sourceSerializer.parse(source)
          );
          ...
          return parsedSources
            .map((source) => { ... })
            .sort((a, b) => a.name.localeCompare(b.name))
            .sort((a, b) => a.groupBy.localeCompare(b.groupBy));
        }
        return [];
      })
    );
}
```

* `ViewManageComponent` (`modules/view/components/manage/manage.component.ts`) controla seleção/ativação:

    * Carrega camadas via `getSourcesAvailable`.
    * Mantém agrupamentos (`layerGroup`) com `groupBy`.
    * `addSource` garante que camadas filhas só entrem com a geometria pai ativa e define `dataActive` para indicar qual camada de dados alimenta a geometria.
    

```72:210:webapp-orbita/src/app/modules/view/components/manage/manage.component.ts
this._sourceService.getSourcesAvailable().subscribe((sources) => {
  this.allSources = sources.filter((s) => s.status > 1);
  this.getLayers();
  ...
});

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

* `SourceToggleComponent` (`source-toggle.component.ts`) atua no painel de gerenciamento: mostra o relacionamento pai/filho e chama `MapService.toggleDataSource` para alternar qual dataset está ativo por camada.

## Fluxo de dados das camadas

1. **Catálogo**: `ViewManageComponent` chama `SourceService.getSourcesAvailable()` e popula `allSources`, definindo `groupBy` (usado para exibir seções como “Geográfica - Pontos” ou o nome do dataset principal).
2. **Seleção**: Ao selecionar uma camada, `addSource`:

    * valida ponto central.
    * ativa a fonte pai (geometria) e associa a fonte filha (`dataActive`).
    * adiciona ambas em `MapModel.sources` com `active/checked`.
    
3. **Observabilidade**: `MapService` usa `on-change` para emitir `mapChanges` sempre que algo em `MapModel` muda. Componentes (`ViewMapComponent`, `LayerDetailsComponent`, `ViewManageComponent`) assinam `observeChanges` para reagir.

```28:115:webapp-orbita/src/app/shared/services/map.service.ts
private mapProxy: MapModel;
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

4. **Carga de dados**: `ViewMapComponent.getSourcesData()` reúne os IDs das camadas ativas (sempre a geometria ou seu `dataActive`), faz POST em `/sources/search` e popula `map.sourcesData[id] = { assets, geometries, projection }`. Cada `SourceData` guarda as features retornadas.

```168:213:webapp-orbita/src/app/modules/view/components/map/map.component.ts
const activeSources = this.map.activeSources
  .filter((source) => source.geometryType !== SourceGeometryType.NONE)
  .map((source) => source.dataActive || source.id);

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

5. **Renderização**: `ViewMapComponent.buildLayers()` chama `buildLayer()` para cada `Source` ativo:

    * `SourceService.buildGeoJsonLayer` (via `MapService`) cria `GeoJsonLayer` com [http://Deck.gl](http://Deck.gl)  usando os `assets` e `StyleHelper.polygonStyle` alimentado por `SourceGrouping`.
    * `buildIconLayer` gera `IconLayer` (pontos) aplicando ícones com `SourceGrouping` para cores.
    * `buildArcLayer` gera `ArcLayer` (linhas).
    * Eventos de `onClick` chamam `MapService.geometryClick` para sincronizar detalhes na área lateral.
    

```392:478:webapp-orbita/src/app/shared/services/map.service.ts
return forkJoin(
  sourceData.assets.map((asset) => this._geoJsonService.get(asset))
).pipe(
  map(
    (collections) =>
      new GeoJsonLayer({
        id: `geo-${dataSource?.id || source?.id}-${source.id}-${sourceData.id}`,
        data: { type: 'FeatureCollection', features: collections.flatMap((coll) => coll.features) },
        pickable: true,
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

6. **Detalhamento e tabelas**:

    * `LayerDetailsComponent` monta o painel lateral, recalculando colunas agregadas conforme `SourceStructure.columns` e operações (somatória, média etc.). Dados vêm de `map.sourcesData`.
    * `SourceToggleComponent` e `ViewManageComponent.openTable` exibem tabelas modais usando `map.sourcesData[source.id]`.
    
7. **Atualização e remoção**:

    * `MapService.removeSource` limpa dependências e o cache `sourcesData`.
    * `ViewManageComponent.removeSourceAndChildren` garante que remover um pai desligue os filhos (camadas de dados associadas).
    * `MapService.toggleDataSource` alterna qual camadas de dados alimenta a geometria, atualizando `activeSources` e disparando `geometryClick` para refrescar o foco.
    

## Padrão arquitetural

* **Service-centric state**: `MapService` age como um store reativo (sem NgRx). Ele encapsula o estado do mapa e difunde mudanças via `Subject`. Componentes ouvem `observeChanges` para detectar alterações específicas (ex.: `['sourcesData.']`).
* **Model-driven**: Modelos `Source`, `SourceData`, `MapModel` são serializados/deserializados com `TypedJSON`, garantindo tipos fortes e reuso tanto no cache local (`CoreStorage`) quanto no tráfego HTTP.
* **Camadas compostas**: Uma camada visível é resultado da composição `geometria + dataset`. `Source.references` dita o relacionamento; `dataActive` define qual dataset alimenta o pai. Este “link” é mantido em `MapModel` e respeitado por todos os componentes.
* **Renderização com** [http://Deck.gl](http://Deck.gl) : A própria renderização fica isolada em `MapService` e `ViewMapComponent`, utilizando `GeoJsonLayer`, `IconLayer` e `ArcLayer`. As cores e estilos dependem da `SourceGrouping`.

## Responsabilidades por camada

* **Geometria** (`geometryType` ≠ `NONE`): desenha shapes/pontos e captura cliques. Mantém `geometryFile`, `graphicSetup`, `customMarker`.
* **Dados** (`geometryType === NONE`): fornece colunas, agrupamentos, operações estatísticas e assets tabulares. Não é renderizada diretamente; alimenta sua referência geográfica via `dataActive`.
* **Agrupamentos**: configurados em `Source.groupedBy`. Usados tanto em renderização (`StyleHelper`) quanto em `LayerDetails` e gráficos.
* **Assets**: URLs retornadas pela API (`SourceAsset.geometryFile`). São pré-carregadas em `ViewComponent.loadSourcesAssets()` para reduzir latência quando uma camada é ativada.

## Implicações práticas para novas features

* Adicionar uma nova camada exige atualização apenas no catálogo backend; o frontend a exibirá automaticamente se `getSourcesAvailable()` retornar o `Source`. Porém, se houver interações especiais (ex.: operações personalizadas), ajuste `LayerDetailsComponent` e `StyleHelper`.
* Novas relações pai/filho (ex.: dataset estatístico associado a uma camada de polígonos) devem seguir o padrão `Source.references[].id` para ativação automática em `ViewManageComponent.addSource`.
* Alterar formato de dados retornados por `/sources/search` implica atualizar `SourceData` e todas as leituras (`MapService.geometryClick`, `LayerDetailsComponent.calculatedColumns`).
* Interações com cliques no mapa devem sempre passar por `MapService.geometryClick` para manter `MapModel.place` sincronizado com o painel lateral.
* Ao criar componentes que dependem de mudanças no mapa, sempre injete `MapService` e use `observeChanges` em vez de acessar diretamente as propriedades para manter consistência com o mecanismo de observabilidade.

## Boas práticas para manter/evoluir as camadas

* Use as classes de modelo existentes (`Source`, `SourceData`, `MapModel`) para tipar novos serviços ou componentes; evite objetos anônimos.
* Sempre atualize `MapService.map.sources` através dos métodos/utilitários existentes (`addSource`, `removeSourceAndChildren`, `toggleDataSource`) para preservar dependências e cache.
* Ao criar novas visualizações, centralize a lógica de renderização em `MapService` ou `ViewMapComponent`, mantendo componentes de UI (toggle, detalhes) livres de regras gráficas.
* Recarregue `map.sourcesData` apenas quando raio/ponto mudarem ou quando uma nova camada for ativada; reutilize dados em cache para evitar requisições redundantes.
* Documente qualquer alteração em `SourceStructure` (novas operações, colunas) e revise `LayerDetailsComponent` para garantir que agregações e formatações reflitam os novos campos.
