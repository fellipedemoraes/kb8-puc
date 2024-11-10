import React, { useState, ChangeEvent, FormEvent } from 'react';

const Maker: React.FC = () => {
    const [password, setPassword] = useState<string>('');
    const [gameId, setGameId] = useState<string>('');

    const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
        event.preventDefault();
        
        // Criando um AbortController
        const controller = new AbortController();
        const signal = controller.signal;

        // Definindo um timeout para a requisição
        const timeoutId = setTimeout(() => controller.abort(), 5000); // Timeout de 5000ms (5 segundos)

        try {
            const backendUrl = process.env.REACT_APP_BACKEND_URL; // Use the environment variable
            const response = await fetch(`${backendUrl}/create`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ password }),
                signal: signal, // Passando o sinal para a requisição fetch
            });

            clearTimeout(timeoutId); // Cancela o timeout se a requisição for bem sucedida antes do tempo

            const data = await response.json();
            setGameId(data.game_id);
        } catch (error) {
    // Verificando se error é uma instância de Error
    if (error instanceof Error) {
        console.error('Error creating game:', error.message);

        // Agora podemos verificar com segurança a propriedade name do error
        if (error.name === 'AbortError') {
            console.error('Fetch aborted due to timeout');
        }
    } else {
        // Caso o erro capturado não seja uma instância de Error,
        // você pode decidir como lidar com esse caso.
        console.error('An unexpected error occurred');
    }
        }
    };

    const handlePasswordChange = (event: ChangeEvent<HTMLInputElement>) => {
        setPassword(event.target.value);
    };

    return (
        <div>
            <h1>Create a New Game</h1>
            <form onSubmit={handleSubmit}>
                <label>
                    Password:
                    <input name="passcode" type="text" value={password} onChange={handlePasswordChange} />
                </label>
                <button type="submit">Create Game</button>
            </form>
            {gameId && <p>Game ID: {gameId}</p>}
        </div>
    );
};

export default Maker;
