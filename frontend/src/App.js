import React, { useEffect, useState} from 'react';
import axios from 'axios';
import { io } from 'socket.io-client';
import './App.css';

const socket = io('http://localhost:5000');

function App() {
  const [data, setData] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [previewImage, setPreviewImage] = useState(null); 
  

  useEffect(() => {
    const fetchData = async () => {
      const result = await axios(
        'http://localhost:5000/',
      );
      setData(result.data);
    };

    fetchData();
    socket.on('folder_updated', fetchData);

    // Clean up the effect
    return () => socket.off('folder_updated', fetchData);

  }, []);


  const handleSearchChange = (event) => {
    setSearchTerm(event.target.value);
  };

  const handleSearchSubmit = async (event) => {
    event.preventDefault();
    
    const result = await axios.post('http://localhost:5000/', {
      search: searchTerm,
    });

    setData(result.data);
  };
  
  const handleReset = async () => {
    const result = await axios.get('http://localhost:5000/');
    setData(result.data);
    setSearchTerm('');
  };

  const handleDelete = async (folderId) => {
    await axios.post(`http://localhost:5000/delete/${folderId}`);
    const result = await axios.get('http://localhost:5000/');
    setData(result.data);
  };

  const handlePreview = (imageUrl) => {
    setPreviewImage(imageUrl);  
  };


  return (
    <div className="App">
      <h1>Image Metadata Database</h1>

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

      {previewImage && (
  <div className="modal">
    <div className="modal-content">
      <img src={previewImage} alt="Preview" />
      <button onClick={() => setPreviewImage(null)}>Close Preview</button>
    </div>
  </div>
)}

      <table className="table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Folder Name</th>
            <th>Image Preview</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {data.map((item) => (
          <tr key={item.id}>
          <td>{item.id}</td>
          <td>{item.folder_name}</td>
          <td>
            <img className='previewImage'
              src={`http://localhost:5000/image/${item.folder_name}/image.jpg`}
              alt="Preview Not Available"
            />
          </td>
          <td>
             <div className='action'>
               <button onClick={() => handlePreview(`http://localhost:5000/image/${item.folder_name}/image.jpg`)}>Preview</button>
                <button onClick={() => handleDelete(item.id)}>Delete</button>
             </div>
          </td>
        </tr>
))}
        </tbody>
      </table>
    </div>
  );
}

export default App;
