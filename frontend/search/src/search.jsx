import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [ingredient, setIngredient] = useState('');
  const [results, setResults] = useState([]);

  const handleInputChange = (event) => {
    setIngredient(event.target.value);
  };

  const handleSearch = async () => {
    try {
      const response = await axios.get(`/ice_cream_shops?ingredient=${ingredient}`);
      setResults(response.data);
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div>
      <input type="text" value={ingredient} onChange={handleInputChange} />
      <button onClick={handleSearch}>Search</button>
      <ul>
        {results.map((result) => (
          <li key={result.business_id}>
            {result.score[3]}, {result.city}, {result.state}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;