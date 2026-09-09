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
  origin: string
  location: string
  image: string
}
