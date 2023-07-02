import React from 'react';

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
  );
}

export default ImageTable;
