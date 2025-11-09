import { atom } from 'jotai';

export const tokenTypeAtom = atom('bearer');
export const accessTokenAtom = atom(null);
export const userInfoAtom = atom(null);

export const isAuthenticatedAtom = atom(
  (get) => get(accessTokenAtom) !== null
);

export const authHeaderAtom = atom(
  (get) => {
    const token = get(accessTokenAtom);
    const tokenType = get(tokenTypeAtom);
    return token ? `${tokenType} ${token}` : null;
  }
);

export const loginAtom = atom(
  null,
  (_, set, { token, user }) => {
    set(accessTokenAtom, token);
    set(userInfoAtom, user);
  }
);

export const logoutAtom = atom(
  null,
  (_, set) => {
    set(accessTokenAtom, null);
    set(userInfoAtom, null);
  }
);