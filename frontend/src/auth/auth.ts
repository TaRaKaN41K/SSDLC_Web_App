export const saveToken = (token: string) => {
    localStorage.setItem('access_token', token);
  };
  
  export const getToken = (): string | null => {
    return localStorage.getItem('access_token');
  };
  
  export const removeToken = () => {
    localStorage.removeItem('access_token');
  };
  