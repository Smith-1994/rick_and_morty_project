import type { Character } from '../types/character'
import './CharacterCard.css'

type CharacterCardProps = {
  character: Character
}

function statusClass(status: string): string {
  const value = status.toLowerCase()
  if (value === 'alive') return 'status-alive'
  if (value === 'dead') return 'status-dead'
  return 'status-unknown'
}

function displayValue(value: string): string {
  return value.trim() === '' ? 'Unknown' : value
}

function CharacterCard({ character }: CharacterCardProps) {
  return (
    <article className="character-card">
      <div className="character-card-image-wrap">
        <img
          className="character-card-image"
          src={character.image}
          alt={character.name}
        />
        <span className={`character-card-status ${statusClass(character.status)}`}>
          <span className="status-dot" aria-hidden="true" />
          {character.status}
        </span>
      </div>

      <div className="character-card-body">
        <p className="character-card-id">#{character.id}</p>
        <h2 className="character-card-name">{character.name}</h2>

        <dl className="character-card-fields">
          <div>
            <dt>Species</dt>
            <dd>{displayValue(character.species)}</dd>
          </div>
          <div>
            <dt>Type</dt>
            <dd>{displayValue(character.type)}</dd>
          </div>
          <div>
            <dt>Gender</dt>
            <dd>{displayValue(character.gender)}</dd>
          </div>
          <div>
            <dt>Origin</dt>
            <dd>{displayValue(character.origin.name)}</dd>
          </div>
          <div className="character-card-location">
            <dt>Location</dt>
            <dd>{displayValue(character.location.name)}</dd>
          </div>
        </dl>
      </div>
    </article>
  )
}

export default CharacterCard
