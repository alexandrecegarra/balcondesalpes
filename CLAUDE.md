# La Concorde · site de présentation (balcondesalpes)

Page publique de présentation de l'appartement La Concorde à Crans-Montana (commune de Lens, 1362 m), publiée sur GitHub Pages : https://alexandrecegarra.github.io/balcondesalpes/

Alexandre travaille uniquement depuis son iPhone et ne modifie pas le code : Claude construit, publie et maintient le site.

## Structure

- `index.html` : la page entière (HTML, CSS, JS), écrite à la main. Bilingue : chaque texte existe en `<span class="fr">` et `<span class="en">`, le bouton FR/EN bascule `data-lang` sur `<html>`. Français par défaut.
- `img/` : photos web en deux tailles (`-800.jpg`, `-1600.jpg`), produites par `src/photos.py` à partir des originaux placés dans `photos_src/` (non versionné, trop lourd). `hero-*.jpg` est le balcon recadré au-dessus du filigrane CosyHome (aussi produit par `src/photos.py`).
- Icônes `apple-touch-icon.png`, `icon-192.png`, `icon-512.png` : recadrage carré de la photo du balcon (avant-toit, sommets, garde-corps), produit par `src/icon.py`. Changer le suffixe `?v=` dans `index.html` et le manifeste à chaque nouvelle icône. `manifest.webmanifest`, `.nojekyll`.

## Règles de contenu

- Source de référence du texte : le dossier « La_Concorde_Crans_1968_last.pdf » (13 pages), dont le site reprend les chapitres I à VII en version resserrée. Ses images extraites sont dans `photos_src/pdf-*.jpg` ; plaques et passant floutés sur `immeuble-hiver` (voir `BLUR` dans `src/photos.py`).
- Écarts relevés avec le dossier : Lucca attribuée à Space Copenhagen (le dossier dit Niclas Hoflin) ; Grand Muveran 3051 m (le dossier répète 2968) ; Mont Blanc avant Pierre Avoi et Sommet de l'Ardève inclus, selon la capture PeakFinder.

- Ton factuel, sans vocabulaire de décoration ; ne jamais inventer de descriptions.
- Parentesi : câble tendu du sol au plafond. Prouvé : dessiné pour les lieux de travail et les espaces collectifs ; garder « Ce geste résume le projet » en cuisine. Casiers à skis surdimensionnés, aussi pour le golf.
- Pas d'adresse postale, pas de coordonnées GPS, pas de codes ni de numéros privés.
- Aucune mention CosyHome sur le site, ni filigrane ni texte (demande d'Alexandre). Ses propres photos (`photos_src/a-*`) remplacent celles de CosyHome ; les seules images CosyHome restantes (ouverture, chambre principale, salle de bain, balcon le long de la façade, String) sont recadrées au-dessus du filigrane (`keep` dans `src/photos.py`). Vérifier le bas de chaque image avant publication.
- Ne pas publier la photo de l'entrée côté rue (enseigne et numéro de la rue visibles) ni celle de la cage d'escalier (numéro de porte).
- Panorama : la liste des sommets vient de sa capture PeakFinder (cap 233°), dans l'ordre de gauche à droite.

## Vérifier puis publier

Playwright à 393 et 320 px : `scrollWidth` égal à la largeur, pas d'erreur JS, bascule de langue et visionneuse fonctionnelles. Commit au nom de `alexandrecegarra <alexandrecegarra@users.noreply.github.com>`, push sur `main`.
