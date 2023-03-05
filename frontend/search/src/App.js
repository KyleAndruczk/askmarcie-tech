import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [ingredient, setIngredient] = useState('');
  const [results, setResults] = useState([]);
  const [searchInProgress, setSearchInProgress] = useState(false);

  const handleInputChange = (event) => {
    setIngredient(event.target.value);
  };

  const handleSearch = async () => {
    try {
      setSearchInProgress(true); // set search in progress
      const response = await axios.get(`http://localhost:5000//ice_cream_shops?ingredient=${ingredient}`);
      setResults(response.data);
    } catch (error) {
      console.error(error);
    } finally {
      setSearchInProgress(false); // set search complete
    }
  };

  return (
    <div style={{display: 'flex', flexDirection: 'column', alignItems: 'center'}}>
      <h1 style={{fontSize: '3rem', marginBottom: '2rem'}}>Ice Cream Shops</h1>
      <div style={{display: 'flex', marginBottom: '2rem'}}>
        <input
          type="text"
          value={ingredient}
          onChange={handleInputChange}
          style={{padding: '1rem', marginRight: '1rem', flex: '1'}}
          placeholder="Enter an ingredient"
        />
        <button onClick={handleSearch} style={{padding: '1rem 2rem'}}>Search</button>
      </div>
      {searchInProgress ? (
        <>
        <p>Loading and generating chat GPT summaries...</p>
        <p>This should take about 5 seconds</p>
        </>
      ) : results.length > 0 ? (
        <ul style={{listStyle: 'none', marginLeft: 50, marginRight: 50 }}>
          {results.map((result) => (
            <li key={result.business_id} style={{marginBottom: '1rem'}}>
              <h2 style={{fontSize: '2rem', marginBottom: '0.5rem'}}>{result.name}</h2>
              <p style={{fontSize: '1.5rem', marginBottom: 0}}>{result.city}, {result.state}</p>
              <p style={{fontSize: '1.5rem', marginBottom: 0}}>{result.summary}</p>

            </li>
          ))}
        </ul>
      ) : (
        <p>No results found</p>
      )}
    </div>
  );
}

export default App;