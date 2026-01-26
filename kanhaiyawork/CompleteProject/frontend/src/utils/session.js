export const setSession = (token) => {
  sessionStorage.setItem("auth_token", token);
};

export const clearSession = () => {
  sessionStorage.removeItem("auth_token");
};

export const isAuthenticated = () => {
  return !!sessionStorage.getItem("auth_token");
};
