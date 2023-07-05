import React from 'react';
import PropTypes from 'prop-types';

const ImagePreview = ({ previewImage, setPreviewImage }) => {
  
  if (!previewImage) return null;

  // Handler for closing image preview
  const handleClosePreview = () => setPreviewImage(null);

  return (
    <div className="modal">
      <div className="modal-content">
        <img src={previewImage} alt="Preview" />
        <button onClick={handleClosePreview}>Close Preview</button>
      </div>
    </div>
  );
}

ImagePreview.propTypes = {
  previewImage: PropTypes.string, 
  setPreviewImage: PropTypes.func.isRequired, 
};

export default ImagePreview;
