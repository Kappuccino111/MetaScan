import React from 'react';

function SearchForm({ searchTerm, setSearchTerm, search, reset, setData }) {
  const handleSearchChange = (event) => {
    setSearchTerm(event.target.value);
  };

  const handleSearchSubmit = (event) => {
    event.preventDefault();
    search(searchTerm, setData);
  };

  const handleReset = () => {
    reset(setData, setSearchTerm);
  };

  return (
    <form className="search-container" onSubmit={handleSearchSubmit}>
      <input
        type="text"
        value={searchTerm}
        onChange={handleSearchChange}
        placeholder="Enter Metadata to Search"
      />
      <div className="button-container">
        <button type="submit">Search</button>
        <button type="button" onClick={handleReset}>Reset</button>
      </div>
    </form>
  );
}

export default SearchForm;
