import React, { useState, useCallback } from 'react';
import DashboardLayout from '../layouts/DashboardLayout';
import { FileUpload, Input, LoadingButton } from '@components';
import { verifySignature } from '@api/stegoApi';
import '@styles/pages/VerifyImage.css';

const VerifyImage = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [verificationResult, setVerificationResult] = useState(null);

  // Fonction appelée quand un fichier est sélectionné
  const handleFileSelect = useCallback((file) => {
    setError('');
    setVerificationResult(null);
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
    setVerificationResult(null);
  };

  // Fonction pour vérifier l'image
  const handleVerifyImage = async () => {
    if (!selectedFile) {
      setError('Veuillez d\'abord sélectionner une image');
      return;
    }

    setError('');
    setVerificationResult(null);
    setLoading(true);

    try {
      const response = await verifySignature(selectedFile);

      setVerificationResult(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || err.response?.data?.err || 'Une erreur est survenue lors de la vérification de l\'image');
    } finally {
      setLoading(false);
    }
  };
  
  return (
    <DashboardLayout
      title="Verify Image"
      titleDescription="Detect and extract hidden messages from images"
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

        {/* Bouton pour vérifier l'image */}
        {selectedFile && (
          <div className="form-container">
            <LoadingButton
              type="button"
              className="btn btn-primary"
              defaultText="Vérifier l'image"
              loadingText="Vérification en cours..."
              loading={loading}
              onClick={handleVerifyImage}
              disabled={!selectedFile}
            />
          </div>
        )}

        {/* Affichage du résultat de vérification */}
        {verificationResult && (
          <div className={`verification-result ${verificationResult.valid ? 'valid' : 'invalid'}`}>
            <h3>
              {verificationResult.valid ? '✓ Vérification réussie' : '✗ Vérification échouée'}
            </h3>
            
            {verificationResult.valid ? (
              <div className="verification-details">
                {verificationResult.signature_uuid && (
                  <p><strong>UUID de la signature:</strong> {verificationResult.signature_uuid}</p>
                )}
                {verificationResult.author_id && (
                  <p><strong>ID de l'auteur:</strong> {verificationResult.author_id}</p>
                )}
                {verificationResult.message && (
                  <div>
                    <strong>Message extrait:</strong>
                    <div>
                      {verificationResult.message}
                    </div>
                  </div>
                )}
                {verificationResult.signed_at && (
                  <p>
                    <strong>Date de signature:</strong> {new Date(verificationResult.signed_at).toLocaleString('fr-FR')}
                  </p>
                )}
              </div>
            ) : (
              <div className="verification-details">
                <p>{verificationResult.message || 'La vérification a échoué. L\'image ne contient peut-être pas de message caché (stéganographie LSB).'}</p>
              </div>
            )}
          </div>
        )}
      </div>
    </DashboardLayout>
  );
};

export default React.memo(VerifyImage);
