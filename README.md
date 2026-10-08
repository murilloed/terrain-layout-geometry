# Geometria computacional para implantação em terrenos

Protótipo independente com terreno sintético em coordenadas locais métricas.

## Objetivo e entrega
Aplicar recuo uniforme, gerar edifícios retangulares sem sobreposição e com afastamento mínimo, comparar três ordens de busca e exportar SVG, GeoJSON, CSV e JSON.

## Técnicas
Python, Shapely/GEOS, offset interno de polígonos, predicados de contenção, distância, interseção e busca gulosa em grade. Região admissível pode ser vazia ou multipolígono. Critérios: maior quantidade de edifícios e menor distância média ao centro entre alternativas geradas. Não há rede neural nem treinamento.

## Reproduzir
```bash
python -m pip install -r requirements.txt
python demo.py
python demo.py --setback 6 --output output/setback6
python -m unittest discover -s tests -v
```

A função `generate` aceita coordenadas, dimensões, afastamento, passo de busca, taxa máxima de ocupação e limite de edifícios. Use coordenadas planas em metros; longitude/latitude requer reprojeção antes do cálculo. `layout.geojson` usa coordenadas locais e não deve ser sobreposto diretamente a um mapa geográfico.

## Resultados e limites
Busca gulosa determinística, não ótimo global. Nenhuma conformidade legal ou aprovação técnica é afirmada. Não modela vias, rampas, acessibilidade, incêndio, topografia, recuos diferenciados por face ou BIM. Nenhum dado de cliente ou implementação da Arqgen foi utilizado.

## Próximas etapas
Adicionar vias e acessos, recuos por face, solver com restrições e fronteira de Pareto; comparar qualidade e tempo com o baseline; importar formatos CAD/GIS e avaliar terrenos autorizados.
