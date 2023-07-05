import axios from 'axios';

const FRONTEND_URL = 'http://localhost:5000/';

// Function for updating data and state
const fetchDataAndUpdate = async (url, setData) => {
  try {
    const result = await axios.get(url);
    setData(result.data, null); 
  } catch (error) {
    setData(null, error);
  }
};

// Function for setting up socket event 
export async function fetchInitialData(socket, setData) {
  const fetchData = () => fetchDataAndUpdate(FRONTEND_URL, setData);

  fetchData();
  socket.on('folder_updated', fetchData);

  return () => socket.off('folder_updated', fetchData);
}

// Function for performing search operation
export async function search(searchTerm, setData) {
  try {
    const result = await axios.post(FRONTEND_URL, { search: searchTerm });
    setData(result.data, null);
  } catch (error) {
    setData(null, error);
  }
}

// Function for resetting search operation
export async function reset(setData, setSearchTerm) {
  fetchDataAndUpdate(FRONTEND_URL, setData);
  setSearchTerm('');
}

// Function for deleting folders through frontend
export async function deleteFolder(folderId, setData) {
  try {
    await axios.post(`${FRONTEND_URL}/delete/${folderId}`);
    fetchDataAndUpdate(FRONTEND_URL, setData);
  } catch (error) {
    setData(null, error);
  }
}
