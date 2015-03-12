## In admin ##
> Fill in Required Fields (in bold) + square footage and year (otherwise a bunch of errors occur)
> Use GIMP to get coordinates for map, fill in the field

## Outside of Admin ##
> Edit campusmap image (PSD in /site-media/) to highlight building
> Add picutres, description etc.

## Checks ##
> Make sure building appears on campusmap and building list
> Make sure building appears in API


## How queryids work in the DB ##

QUERY\_ID is placed into the page by Django (used in the old query format)
> It is either --> queryid if defined, building longname otherwise

NEW\_QUERY\_ID is also placed into the page by Django (used for the new query format)
> It is either --> sumQueryid if defined, QUERY\_ID otherwise