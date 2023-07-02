import React from 'react';

function ImagePreview({ previewImage, setPreviewImage }) {
  return (
    previewImage && (
      <div className="modal">
        <div className="modal-content">
          <img src={previewImage} alt="Preview" />
          <button onClick={() => setPreviewImage(null)}>Close Preview</button>
        </div>
      </div>
    )
  );
}

export default ImagePreview;
