import { axiosInstance } from './axiosInstance';

/**
 * Désactive le compte d'un utilisateur (admin seulement)
 * @param {number} userId - ID de l'utilisateur à désactiver
 * @returns {Promise} Réponse vide avec status 204
 */
export const deactivateUser = (userId) => {
  return axiosInstance.delete(`/users/${userId}/deactivate`);
};

