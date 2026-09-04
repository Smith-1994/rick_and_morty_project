/** Location or origin as returned by the Rick and Morty API. */
export type NamedPlace = {
  name: string
  url: string
}

/**
 * Character payload the frontend expects from the backend.
 * GET /api/character
 */
export type Character = {
  id: number
  name: string
  status: string
  species: string
  type: string
  gender: string
  origin: NamedPlace
  location: NamedPlace
  image: string
}
