import React, { useState, useEffect, useMemo } from 'react';
import DashboardLayout from '../layouts/DashboardLayout';
import { getUserSignatures, downloadSignature } from '@api/stegoApi';
import { LoadingButton, Spinner, Input } from '@components';
import '@styles/pages/MySignatures.css';

const MySignatures = () => {
  const [signatures, setSignatures] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    loadSignatures();
  }, []);

  const loadSignatures = async () => {
    setLoading(true);
    setError('');
    try {
      const response = await getUserSignatures();
      setSignatures(response.data || []);
    } catch (err) {
      setError(err.response?.data?.detail || err.response?.data?.err || 'Une erreur est survenue lors du chargement des signatures');
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (dateString) => {
    if (!dateString) return 'N/A';
    return new Date(dateString).toLocaleString('fr-FR', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  // Filtrer les signatures en fonction du terme de recherche
  const filteredSignatures = useMemo(() => {
    if (!searchTerm.trim()) {
      return signatures;
    }
    
    const term = searchTerm.toLowerCase().trim();
    return signatures.filter((signature) => {
      const uuid = signature.signature_uuid?.toLowerCase() || '';
      const filename = signature.original_filename?.toLowerCase() || '';
      
      // Recherche dans l'UUID et le nom de fichier
      if (uuid.includes(term) || filename.includes(term)) {
        return true;
      }
      
      // Recherche dans la date formatée
      try {
        const date = formatDate(signature.signed_at).toLowerCase();
        if (date.includes(term)) {
          return true;
        }
      } catch (e) {
        // Ignore les erreurs de formatage de date
      }
      
      return false;
    });
  }, [signatures, searchTerm]);

  const handleDownload = async (signatureUuid, filename) => {
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
      a.download = filename || 'signed_image.png';
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
      title="My Signatures"
      titleDescription="Manage and track your steganographic signatures"
    >
      <div className="glassmorphic-card">
        <div className="signatures-header mb-4">
          <h2 className="text-xl font-semibold mb-2">Mes signatures</h2>
          <LoadingButton
            type="button"
            className="btn btn-secondary !py-2"
            defaultText="Actualiser"
            loadingText="Chargement..."
            loading={loading}
            onClick={loadSignatures}
          />
        </div>

        {error && (
          <div className="p-4 mb-4 text-sm text-red-500 border border-red-500 rounded-lg bg-red-50 dark:bg-gray-800 dark:text-red-400" role="alert">
            {error}
          </div>
        )}

        {loading && signatures.length === 0 ? (
          <div className="flex justify-center items-center py-8">
            <Spinner size={6} animate />
            <span className="ml-3">Chargement des signatures...</span>
          </div>
        ) : signatures.length === 0 ? (
          <div className="text-center py-8 text-gray-500">
            <p>Aucune signature trouvée.</p>
            <p className="text-sm mt-2">Créez votre première signature depuis la page "Sign Image".</p>
          </div>
        ) : (
          <div className="signatures-list">
            <div className="search-bar-container">
              <Input
                type="text"
                placeholder="Rechercher par UUID, nom de fichier ou date..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="search-input"
              />
              {searchTerm && (
                <span className="search-results-count">
                  {filteredSignatures.length} résultat{filteredSignatures.length > 1 ? 's' : ''}
                </span>
              )}
            </div>
            <div className="overflow-x-auto">
              <table>
                <thead>
                  <tr>
                    <th>UUID</th>
                    <th>Fichier original</th>
                    <th>Date de signature</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {filteredSignatures.length === 0 ? (
                    <tr>
                      <td colSpan="4" className="no-results">
                        <div className="text-center py-8 text-gray-500">
                          <p>Aucun résultat trouvé pour "{searchTerm}"</p>
                        </div>
                      </td>
                    </tr>
                  ) : (
                    filteredSignatures.map((signature) => (
                    <tr key={signature.id}>
                      <td>
                        <code>
                          {signature.signature_uuid}
                        </code>
                      </td>
                      <td>
                        {signature.original_filename || 'N/A'}
                      </td>
                      <td>
                        {formatDate(signature.signed_at)}
                      </td>
                      <td>
                        {signature.file_path && (
                          <button
                            className="btn btn-primary btn-sm"
                            onClick={() => handleDownload(signature.signature_uuid, signature.original_filename)}
                          >
                            Télécharger
                          </button>
                        )}
                      </td>
                    </tr>
                    ))
                  )}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </div>
    </DashboardLayout>
  );
};

export default React.memo(MySignatures);
