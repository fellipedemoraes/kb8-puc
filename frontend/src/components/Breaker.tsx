import React, { useState, ChangeEvent, FormEvent } from 'react';

const Breaker: React.FC = () => {
    const [gameId, setGameId] = useState<string>('');
    const [guess, setGuess] = useState<string>('');
    const [result, setResult] = useState<string>('');
    const [error, setError] = useState<string>('');

    const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
        event.preventDefault();
        try {
            const backendUrl = process.env.REACT_APP_BACKEND_URL; // Use the environment variable
            const response = await fetch(`${backendUrl}/guess/${gameId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ guess }),
            });

            if (response.status === 404) {
                throw new Error('Game not found');
            }

            const data = await response.json();
            setResult(`Result: ${data.result}`);
            setError('');
        } catch (error) {
            console.error('Error submitting guess:', error);
            // setResult('');
            setError('Game not found');
        }
    };

    const handleGameIdChange = (event: ChangeEvent<HTMLInputElement>) => {
        setGameId(event.target.value);
    };

    const handleGuessChange = (event: ChangeEvent<HTMLInputElement>) => {
        setGuess(event.target.value);
    };

    return (
        <div>
            <h1>Guess the Word</h1>
            <form onSubmit={handleSubmit}>
                <label>
                    Game ID:
                    <input type="text" value={gameId} onChange={handleGameIdChange} />
                </label>
                <label>
                    Your Guess:
                    <input type="text" value={guess} onChange={handleGuessChange} />
                </label>
                <button type="submit">Submit Guess</button>
            </form>
            {error && <p className="error">{error}</p>}
            {result && <p className={result.startsWith('Result: Incorrect') ? 'incorrect' : ''}>{result}</p>}
        </div>
    );
};

export default Breaker;
