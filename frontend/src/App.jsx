import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Header from './components/Header'; // Путь к компоненту Header
import LoginPage from './pages/LoginPage';
import UserPage from './pages/UserPage';
import RegisterPage from './pages/RegisterPage';
import HomePage from './pages/HomePage';
import EditProfilePage from './pages/EditProfilePage';

const App = () => {
  return (
    <BrowserRouter>
      <Header />
      <main className="pt-20 px-4">
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
          <Route path="/user" element={<UserPage />} />
          <Route path="/edit-profile" element={<EditProfilePage />} />
        </Routes>
      </main>
    </BrowserRouter>
  );
};


export default App;