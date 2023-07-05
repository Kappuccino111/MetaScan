import React from 'react';

const BASE_URL = process.env.REACT_APP_BASE_URL || 'http://localhost:5000';

// Component function for generating Table Rows
function TableRow({ item, handlePreview, handleDelete }) {
  
  // Constructing the image URL for preview
  const imageUrl = `${BASE_URL}/image/${item.folder_name}/image.jpg`;

  return (
    <tr key={item.id}>
      <td>{item.id}</td>
      <td>{item.folder_name}</td>
      <td>
        <img
          className='previewImage'
          src={imageUrl}
          alt={`Preview of ${item.folder_name}`}
        />
      </td>
      <td>
        <div className='action'>
          <button onClick={() => handlePreview(imageUrl)}>Preview</button>
          <button onClick={() => handleDelete(item.id)}>Delete</button>
        </div>
      </td>
    </tr>
  );
}

// Component Function for displaying final set of images
function ImageTable({ data, setPreviewImage, deleteFolder, setData }) {
  const handlePreview = (imageUrl) => {
    setPreviewImage(imageUrl);
  };

  const handleDelete = (folderId) => {
    deleteFolder(folderId, setData);
  };

  return (
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
          <TableRow
            key={item.id}
            item={item}
            handlePreview={handlePreview}
            handleDelete={handleDelete}
          />
        ))}
      </tbody>
    </table>
  );
}

export default ImageTable;
