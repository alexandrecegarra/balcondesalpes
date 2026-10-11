# La Concorde · site de présentation (balcondesalpes)

Page publique de présentation de l'appartement La Concorde à Crans-Montana (commune de Lens, 1362 m), publiée sur GitHub Pages : https://alexandrecegarra.github.io/balcondesalpes/

Alexandre travaille uniquement depuis son iPhone et ne modifie pas le code : Claude construit, publie et maintient le site.

## Structure

- `index.html` : la page entière (HTML, CSS, JS), écrite à la main. Bilingue : chaque texte existe en `<span class="fr">` et `<span class="en">`, le bouton FR/EN bascule `data-lang` sur `<html>`. Français par défaut.
- `img/` : photos web en deux tailles (`-800.jpg`, `-1600.jpg`), produites par `src/photos.py` à partir des originaux placés dans `photos_src/` (non versionné, trop lourd). `hero-*.jpg` est le balcon recadré au-dessus du filigrane CosyHome.
- Icônes `apple-touch-icon.png`, `icon-192.png`, `icon-512.png`, `manifest.webmanifest`, `.nojekyll`.

## Règles de contenu

- Ton factuel, sans vocabulaire de décoration ; ne jamais inventer de descriptions.
- Parentesi : câble tendu du sol au plafond. Prouvé : dessiné pour les lieux de travail et les espaces collectifs ; garder « Ce geste résume le projet » en cuisine. Casiers à skis surdimensionnés, aussi pour le golf.
- Pas d'adresse postale, pas de coordonnées GPS, pas de codes ni de numéros privés.
- Photos CosyHome : filigrane conservé tant qu'Alexandre n'a pas fourni de versions sans filigrane.
- Panorama : la liste des sommets vient de sa capture PeakFinder (cap 233°), dans l'ordre de gauche à droite.

## Vérifier puis publier

Playwright à 393 et 320 px : `scrollWidth` égal à la largeur, pas d'erreur JS, bascule de langue et visionneuse fonctionnelles. Commit au nom de `alexandrecegarra <alexandrecegarra@users.noreply.github.com>`, push sur `main`.
