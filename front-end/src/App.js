import React, { useEffect, useState } from 'react';
import { io } from 'socket.io-client';
import { fetchInitialData, search, reset, deleteFolder } from './API';
import SearchForm from './components/SearchForm';
import ImagePreview from './components/ImagePreview';
import ImageTable from './components/ImageTable';

import './App.css';

const SOCKET_SERVER_URL = 'http://localhost:5000';

function App() {
  const [data, setData] = useState([]); 
  const [searchTerm, setSearchTerm] = useState(''); 
  const [previewImage, setPreviewImage] = useState(null); 

  useEffect(() => {
    // Establishing socket connection and fetching initial data
    const socket = io(SOCKET_SERVER_URL);
    fetchInitialData(socket, setData);
  }, []);

  return (
    <div className="App">
      <h1>Image Metadata Database</h1>

      {/* Search form component */}
      <SearchForm
        searchTerm={searchTerm}
        setSearchTerm={setSearchTerm}
        search={search}
        reset={reset}
        setData={setData}
      />

      {/* Image preview component */}
      <ImagePreview
        previewImage={previewImage}
        setPreviewImage={setPreviewImage}
      />

      {/* Image table component */}
      <ImageTable
        data={data}
        setPreviewImage={setPreviewImage}
        deleteFolder={deleteFolder}
        setData={setData}
      />
    </div>
  );
}

export default App;
