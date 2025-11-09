import { axiosInstance } from './axiosInstance';

/**
 * Upload une image avec un message caché (stéganographie LSB)
 * @param {File} file - Le fichier image à signer
 * @param {string} message - Le message à cacher dans l'image
 * @returns {Promise} Réponse avec signature_uuid, image_id et file_path
 */
export const uploadSignature = (file, message) => {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('message', message);

  return axiosInstance.post('/stego/upload-signature', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
};

/**
 * Vérifie une image signée pour extraire le message caché (stéganographie LSB)
 * @param {File} file - Le fichier image à vérifier
 * @returns {Promise} Réponse avec valid, signature_uuid, author_id, message, signed_at
 */
export const verifySignature = (file) => {
  const formData = new FormData();
  formData.append('file', file);

  return axiosInstance.post('/stego/verify', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
};

/**
 * Récupère toutes les signatures créées par l'utilisateur actuel
 * @returns {Promise} Liste des signatures avec id, signature_uuid, image_id, signer_id, signed_at, original_filename, file_path
 */
export const getUserSignatures = () => {
  return axiosInstance.get('/stego/signatures');
};

/**
 * Récupère toutes les vérifications effectuées par l'utilisateur actuel
 * @returns {Promise} Liste des vérifications avec id, signature_uuid, image_id, verifier_id, verified, timestamp, extracted_payload
 */
export const getUserVerifications = () => {
  return axiosInstance.get('/stego/verifications');
};

/**
 * Télécharge une image signée par son UUID
 * @param {string} signatureUuid - L'UUID de la signature à télécharger
 * @returns {Promise} Réponse avec les données du fichier en base64
 */
export const downloadSignature = (signatureUuid) => {
  return axiosInstance.get(`/stego/download/${signatureUuid}`);
};
