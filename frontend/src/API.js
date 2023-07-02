import axios from 'axios';

export async function fetchInitialData(socket, setData) {
  const fetchData = async () => {
    const result = await axios('http://localhost:5000/');
    setData(result.data);
  };

  fetchData();
  socket.on('folder_updated', fetchData);

  // Clean up the effect
  return () => socket.off('folder_updated', fetchData);
}

export async function search(searchTerm, setData) {
  const result = await axios.post('http://localhost:5000/', {
    search: searchTerm,
  });

  setData(result.data);
}

export async function reset(setData, setSearchTerm) {
  const result = await axios.get('http://localhost:5000/');
  setData(result.data);
  setSearchTerm('');
}

export async function deleteFolder(folderId, setData) {
  await axios.post(`http://localhost:5000/delete/${folderId}`);
  const result = await axios.get('http://localhost:5000/');
  setData(result.data);
}
