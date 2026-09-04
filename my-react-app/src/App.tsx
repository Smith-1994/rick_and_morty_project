import { useCallback, useEffect, useState } from 'react'
import { fetchCharacter } from './api/character'
import CharacterCard from './components/CharacterCard'
import type { Character } from './types/character'
import './App.css'

function App() {
  const [character, setCharacter] = useState<Character | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(true)

  const loadCharacter = useCallback(async () => {
    setLoading(true)
    setError(null)

    try {
      const data = await fetchCharacter()
      setCharacter(data)
    } catch {
      setCharacter(null)
      setError('Could not load a character from the backend.')
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    void loadCharacter()
  }, [loadCharacter])

  return (
    <main className="app">
      <header className="app-header">
        <p className="app-kicker">Rick and Morty</p>
        <h1>Character Card</h1>
        <p className="app-subtitle">
          Data comes from your backend at <code>GET /api/character</code>
        </p>
      </header>

      {loading && <p className="app-status">Loading character…</p>}
      {error && <p className="app-status app-error">{error}</p>}
      {!loading && character && <CharacterCard character={character} />}

      <button type="button" className="app-refresh" onClick={() => void loadCharacter()}>
        Load another character
      </button>
    </main>
  )
}

export default App
