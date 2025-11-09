import React, { useState, useCallback } from 'react';
import DashboardLayout from '@layouts/DashboardLayout';
import { FileUpload, Input, LoadingButton } from '@components';
import { uploadSignature, downloadSignature } from '@api/stegoApi';
import '@styles/pages/SignImage.css';

const SignImage = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');
  const [signedImageUrl, setSignedImageUrl] = useState(null);
  const [signatureUuid, setSignatureUuid] = useState(null);

  // Fonction appelée quand un fichier est sélectionné
  const handleFileSelect = useCallback((file) => {
    setError('');
    setSuccess('');
    setSignedImageUrl(null);
    setSignatureUuid(null);
    setSelectedFile(file);

    // Créer un aperçu de l'image
    const reader = new FileReader();
    reader.onload = () => {
      setPreviewUrl(reader.result);
    };
    reader.readAsDataURL(file);
  }, []);

  // Fonction appelée en cas d'erreur
  const handleError = useCallback((errorMessage) => {
    setError(errorMessage);
  }, []);

  // Fonction pour supprimer le fichier sélectionné
  const removeFile = () => {
    setSelectedFile(null);
    setPreviewUrl(null);
    setError('');
    setSuccess('');
    setSignedImageUrl(null);
    setSignatureUuid(null);
    setMessage('');
  };

  // Fonction pour traiter l'image
  const handleProcessImage = async () => {
    if (!selectedFile) {
      setError('Veuillez d\'abord sélectionner une image');
      return;
    }

    if (!message.trim()) {
      setError('Veuillez entrer un message à cacher dans l\'image');
      return;
    }

    setError('');
    setSuccess('');
    setLoading(true);

    try {
      const response = await uploadSignature(
        selectedFile,
        message
      );

      setSuccess('Image signée avec succès !');
      
      // Store the signature UUID for download
      setSignatureUuid(response.data.signature_uuid);
      
      // Construire l'URL de l'image signée (à adapter selon votre configuration backend)
      // Le backend retourne file_path, mais il faut construire l'URL complète
      const signedPath = response.data.file_path;
      // Si votre backend sert les fichiers statiques, construire l'URL complète
      const baseUrl = import.meta.env.VITE_API_BASE_URL || '';
      setSignedImageUrl(`${baseUrl}${signedPath.replace(/^.*media\//, '/media/')}`);

      // Réinitialiser les champs
      setMessage('');
    } catch (err) {
      setError(err.response?.data?.detail || err.response?.data?.err || 'Une erreur est survenue lors de la signature de l\'image');
    } finally {
      setLoading(false);
    }
  };

  const handleDownload = async () => {
    if (!signatureUuid) {
      setError('UUID de signature non disponible');
      return;
    }

    try {
      const response = await downloadSignature(signatureUuid);
      
      if (!response.data?.base64_data) {
        throw new Error('Données de fichier non trouvées');
      }

      // Convert base64 to blob
      const byteCharacters = atob(response.data.base64_data);
      const byteNumbers = new Array(byteCharacters.length);
      for (let i = 0; i < byteCharacters.length; i++) {
        byteNumbers[i] = byteCharacters.charCodeAt(i);
      }
      const byteArray = new Uint8Array(byteNumbers);
      const blob = new Blob([byteArray], { type: 'image/png' });

      // Create download link
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.style.display = 'none';
      a.href = url;
      a.download = `signed_${selectedFile?.name || 'image.png'}`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (error) {
      console.error('Erreur téléchargement:', error);
      setError('Erreur lors du téléchargement du fichier');
    }
  };

  return (
    <DashboardLayout
      title="Image Signing"
      titleDescription="Hide your secret messages in images with steganography"
    >
      <div className="glassmorphic-card">
        {/* Composant de l'upload de fichier */}
        {!selectedFile && (
          <FileUpload
            enableGlobalDrop={true}
            onFileSelect={handleFileSelect}
            onError={handleError}
            acceptedTypes={{
              'image/bmp': ['.bmp'],
              'image/png': ['.png'],
              'image/jpeg': ['.jpg', '.jpeg']
            }}
            maxFiles={1}
          />
        )}

        {/* Affichage de l'erreur si elle existe */}
        {error && (
          <div className="text-red-500" role="alert">
            {error}
          </div>
        )}

        {/* Affichage du succès si elle existe */}
        {success && (
          <div className="text-green-500" role="alert">
            {success}
          </div>
        )}

        {/* Affichage de l'aperçu de l'image */}
        {previewUrl && (
          <div className="preview-container">
            <div className="preview-header">
              <h3>Aperçu de l'image</h3>
              <button
                onClick={removeFile}
                type="button"
              >
                Supprimer
              </button>
            </div>
            <img 
              src={previewUrl} 
              alt="Aperçu" 
              className="preview-image"
            />
          </div>
        )}

        {/* Formulaire pour le message et les options */}
        {selectedFile && (
          <div className="form-container">
            <Input
              type="textarea"
              label="Message à cacher"
              placeholder="Entrez le message que vous souhaitez cacher dans l'image (stéganographie LSB)"
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              required
              rows={4}
            />

            <LoadingButton
              type="button"
              className="btn btn-primary"
              defaultText="Signer l'image"
              loadingText="Signature en cours..."
              loading={loading}
              onClick={handleProcessImage}
              disabled={!selectedFile || !message.trim()}
            />
          </div>
        )}

        {/* Affichage de l'image signée */}
        {signedImageUrl && (
          <div className="signed-image-container">
            <h3>Image signée</h3>
            <div className="download-container">
              <button
                onClick={handleDownload}
                className="btn btn-primary"
                disabled={!signatureUuid}
              >
                Télécharger l'image signée
              </button>
            </div>
          </div>
        )}
      </div>
    </DashboardLayout>
  );
};

export default React.memo(SignImage);
