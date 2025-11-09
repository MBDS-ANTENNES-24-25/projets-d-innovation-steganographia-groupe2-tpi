import React, { useState, useEffect, useMemo } from 'react';
import DashboardLayout from '../layouts/DashboardLayout';
import { getUserVerifications } from '@api/stegoApi';
import { LoadingButton, Spinner, Input } from '@components';
import '@styles/pages/MyVerifications.css';

const MyVerifications = () => {
  const [verifications, setVerifications] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    loadVerifications();
  }, []);

  const loadVerifications = async () => {
    setLoading(true);
    setError('');
    try {
      const response = await getUserVerifications();
      setVerifications(response.data || []);
    } catch (err) {
      setError(err.response?.data?.detail || err.response?.data?.err || 'Une erreur est survenue lors du chargement des vérifications');
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

  const parseExtractedPayload = (payload) => {
    if (!payload) return null;
    try {
      return JSON.parse(payload);
    } catch {
      return payload;
    }
  };

  // Filtrer les vérifications en fonction du terme de recherche
  const filteredVerifications = useMemo(() => {
    if (!searchTerm.trim()) {
      return verifications;
    }
    
    const term = searchTerm.toLowerCase().trim();
    return verifications.filter((verification) => {
      const uuid = verification.signature_uuid?.toLowerCase() || '';
      
      // Recherche dans l'UUID
      if (uuid.includes(term)) {
        return true;
      }
      
      // Recherche dans le statut
      const status = verification.verified ? 'validée' : 'échouée';
      if (status.includes(term)) {
        return true;
      }
      
      // Recherche dans la date formatée
      try {
        const date = formatDate(verification.timestamp).toLowerCase();
        if (date.includes(term)) {
          return true;
        }
      } catch (e) {
        // Ignore les erreurs de formatage de date
      }
      
      // Recherche dans le payload extrait
      const payload = parseExtractedPayload(verification.extracted_payload);
      if (payload && typeof payload === 'object' && payload.message) {
        if (payload.message.toLowerCase().includes(term)) {
          return true;
        }
      } else if (verification.extracted_payload && verification.extracted_payload.toLowerCase().includes(term)) {
        return true;
      }
      
      return false;
    });
  }, [verifications, searchTerm]);

  return (
    <DashboardLayout
      title="My Verifications"
      titleDescription="Track and manage your image verification history"
    >
      <div className="glassmorphic-card">
        <div className="verifications-header mb-4">
          <h2 className="text-xl font-semibold mb-2">Mes vérifications</h2>
          <LoadingButton
            type="button"
            className="btn btn-secondary !py-2"
            defaultText="Actualiser"
            loadingText="Chargement..."
            loading={loading}
            onClick={loadVerifications}
          />
        </div>

        {error && (
          <div className="p-4 mb-4 text-sm text-red-500 border border-red-500 rounded-lg bg-red-50 dark:bg-gray-800 dark:text-red-400" role="alert">
            {error}
          </div>
        )}

        {loading && verifications.length === 0 ? (
          <div className="flex justify-center items-center py-8">
            <Spinner size={6} animate />
            <span className="ml-3">Chargement des vérifications...</span>
          </div>
        ) : verifications.length === 0 ? (
          <div className="text-center py-8 text-gray-500">
            <p>Aucune vérification trouvée.</p>
            <p className="text-sm mt-2">Vérifiez votre première image depuis la page "Verify Image".</p>
          </div>
        ) : (
          <div className="verifications-list">
            <div className="search-bar-container">
              <Input
                type="text"
                placeholder="Rechercher par UUID, statut, date ou message..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="search-input"
              />
              {searchTerm && (
                <span className="search-results-count">
                  {filteredVerifications.length} résultat{filteredVerifications.length > 1 ? 's' : ''}
                </span>
              )}
            </div>
            <div className="overflow-x-auto">
              <table>
                <thead>
                  <tr>
                    <th>UUID Signature</th>
                    <th>Statut</th>
                    <th>Date</th>
                    <th>Détails</th>
                  </tr>
                </thead>
                <tbody>
                  {filteredVerifications.length === 0 ? (
                    <tr>
                      <td colSpan="4" className="no-results">
                        <div className="text-center py-8 text-gray-500">
                          <p>Aucun résultat trouvé pour "{searchTerm}"</p>
                        </div>
                      </td>
                    </tr>
                  ) : (
                    filteredVerifications.map((verification) => {
                      const payload = parseExtractedPayload(verification.extracted_payload);
                      return (
                        <tr key={verification.id}>
                          <td>
                            {verification.signature_uuid ? (
                              <code>
                                {verification.signature_uuid}
                              </code>
                            ) : (
                              <span className="text-gray-400">N/A</span>
                            )}
                          </td>
                          <td>
                            <span className={`status-badge ${verification.verified ? 'verified' : 'failed'}`}>
                              {verification.verified ? '✓ Validée' : '✗ Échouée'}
                            </span>
                          </td>
                          <td>
                            {formatDate(verification.timestamp)}
                          </td>
                          <td>
                            {verification.verified && payload && payload.message ? (
                              <div className="message-details">
                                <p>Message extrait:</p>
                                <p>
                                  {payload.message}
                                </p>
                              </div>
                            ) : (
                              <span className="text-sm text-gray-500">
                                {verification.extracted_payload || 'Aucun détail'}
                              </span>
                            )}
                          </td>
                        </tr>
                      );
                    })
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

export default React.memo(MyVerifications);
