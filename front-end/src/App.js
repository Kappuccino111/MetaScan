if (typeof setImmediate === 'undefined') {
   var setImmediate = function(callback) {
      setTimeout(callback, 0);
   };
}

import React, { useEffect, useState} from 'react';
import { io } from 'socket.io-client';
import './App.css';
import { fetchInitialData, search, reset, deleteFolder } from './API';
import SearchForm from './SearchForm';
import ImagePreview from './ImagePreview';
import ImageTable from './ImageTable';

const socket = io('http://localhost:5000');

function App() {
  const [data, setData] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [previewImage, setPreviewImage] = useState(null); 

  useEffect(() => {
    fetchInitialData(socket, setData);
  }, []);

  return (
    <div className="App">
      <h1>Image Metadata Database</h1>

      <SearchForm 
        searchTerm={searchTerm} 
        setSearchTerm={setSearchTerm}
        search={search}
        reset={reset}
        setData={setData}
      />

      <ImagePreview 
        previewImage={previewImage}
        setPreviewImage={setPreviewImage}
      />

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
