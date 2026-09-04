import type { Character } from '../types/character'

export async function fetchCharacter(): Promise<Character> {
  const response = await fetch('/api/character')

  if (!response.ok) {
    throw new Error(`Backend returned ${response.status}`)
  }

  return (await response.json()) as Character
}
