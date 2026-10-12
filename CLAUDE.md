# La Concorde · site de présentation (balcondesalpes)

Page publique de présentation de l'appartement La Concorde à Crans-Montana (commune de Lens), publiée sur GitHub Pages : https://alexandrecegarra.github.io/balcondesalpes/

Alexandre travaille uniquement depuis son iPhone et ne modifie pas le code : Claude construit, publie et maintient le site.

## Structure

- `index.html` : la page entière (HTML, CSS, JS), écrite à la main. Bilingue : chaque texte existe en `<span class="fr">` et `<span class="en">`, le bouton FR/EN bascule `data-lang` sur `<html>`. Français par défaut.
- `img/` : photos web en deux tailles (`-800.jpg`, `-1600.jpg`), produites par `src/photos.py` à partir des originaux placés dans `photos_src/` (non versionné, trop lourd). `hero-*.jpg` : photo CosyHome du balcon (IMG_1977), choisie par Alexandre car elle valorise davantage la vue, recadrée au-dessus du filigrane (`keep` 0.77). Les « plates » (`PLATES` dans `src/photos.py`, export 2400 px) sont les grandes photos pleine largeur entre les chapitres ; sur téléphone la première photo de chaque pièce va aussi bord à bord.
- Icônes `apple-touch-icon.png`, `icon-192.png`, `icon-512.png` : recadrage carré de la photo du balcon d'Alexandre (poutres, sommets enneigés), produit par `src/icon.py`. Changer le suffixe `?v=` dans `index.html` et le manifeste à chaque nouvelle icône. `manifest.webmanifest`, `.nojekyll`.

## Règles de contenu

- Source de référence du texte : le dossier « La_Concorde_Crans_1968_last.pdf » (13 pages), dont le site reprend les chapitres I à VII en version resserrée. Ses images extraites sont dans `photos_src/pdf-*.jpg` ; plaques et passant floutés sur `immeuble-hiver` (voir `BLUR` dans `src/photos.py`).
- Écarts relevés avec le dossier : Lucca attribuée à Space Copenhagen (le dossier dit Niclas Hoflin) ; Grand Muveran 3051 m (le dossier répète 2968) ; Mont Blanc avant Pierre Avoi et Sommet de l'Ardève inclus, selon la capture PeakFinder.

- Ton factuel, sans vocabulaire de décoration ; ne jamais inventer de descriptions.
- Parentesi : câble tendu du sol au plafond. Prouvé : dessiné pour les lieux de travail et les espaces collectifs ; garder « Ce geste résume le projet » en cuisine. Casiers à skis surdimensionnés, aussi pour le golf.
- Altitude : ne jamais afficher 1362 m (altitude exacte de l'appartement) ; dire « le haut plateau de Crans‑Montana, à 1500 m », formule générique voulue par Alexandre. Plaine du Rhône : « près de mille mètres plus bas ».
- Pas d'adresse postale, pas de coordonnées GPS, pas de codes ni de numéros privés.
- Aucune mention CosyHome sur le site, ni filigrane ni texte. Photos d'Alexandre partout, sauf là où il a choisi de garder celles de CosyHome (photo d'ouverture du balcon ; salle de bain : trois photos ; chambre principale : tête de lit complète avec la table en verre, `photos_src/c-tete-de-lit.png`, logo effacé par retouche `delogo`), recadrées au-dessus du filigrane ou retouchées. Vérifier le bas de ces images avant publication.
- Retouches dans `src/photos.py` : redressement des verticales (`persp`), débruitage des photos de nuit (`denoise`), recadrage (`crop`, ex. téléphone au sol dans la chambre). Alexandre tient aux photos de la cuisine (bar, bouilloire) et des lits superposés.
- Ne pas publier la photo de l'entrée côté rue (enseigne et numéro de la rue visibles) ni celle de la cage d'escalier (numéro de porte).
- Panorama : image annotée `img/panorama-*.jpg` produite par `src/panorama.py` à partir de sa capture PeakFinder (`photos_src/a-peakfinder.png`, cap 233°) : bande de paysage réelle nettoyée (boutons de l'appli, soleil, coordonnées GPS retirés) et étiquettes redessinées aux positions mesurées. Grand Combin est juste hors cadre à gauche (mention en tête). Défilement horizontal sur téléphone.
- Photo du clair de lune : reflet du visage d'Alexandre dans la vitre effacé (`smooth` dans `src/photos.py`).

## Vérifier puis publier

Playwright à 393 et 320 px : `scrollWidth` égal à la largeur, pas d'erreur JS, bascule de langue et visionneuse fonctionnelles. Commit au nom de `alexandrecegarra <alexandrecegarra@users.noreply.github.com>`, push sur `main`.

- Ne pas publier la photo du séjour avec l'œuvre de Basquiat affichée sur le cadre (reproduction d'une œuvre protégée en sujet principal).
- Photos golf et station de nuit (`photos_src/w-*`) : fournies par Alexandre, d'origine publique ; il a décidé de les publier. Ne pas rendre le site invisible aux moteurs (pas de noindex ni de robots.txt), à sa demande.
