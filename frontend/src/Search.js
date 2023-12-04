import React, { useState } from 'react';

const Search = ({ onSearch }) => {
    const [artistName, setArtistName] = useState('');

    const handleSubmit = (event) => {
        event.preventDefault();
        onSearch(artistName);
    };

    return (
        <div className="search">
            <input
                type="text"
                value={artistName}
                onChange={(e) => setArtistName(e.target.value)}
                placeholder="Enter artist name"
            />
            <button onClick={handleSubmit}>Search</button>
        </div>
    );
};


export default Search;
