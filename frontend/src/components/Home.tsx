import React from 'react';
import { Link } from 'react-router-dom';

const Home: React.FC = () => {
    return (
        <div>
            <h1>Welcome to the Guess Word Game</h1>
            <Link to="/maker">Create a Game</Link>
            <br />
            <Link to="/breaker">Join a Game</Link>
        </div>
    );
};

export default Home;
